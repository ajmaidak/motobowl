"""Minimal Yahoo Fantasy Sports API client.

Handles the OAuth2 dance (copy-paste redirect flow, suitable for a CLI script) and
caches tokens locally so you only authorize once. Read-only scope: fspt-r.
"""

import base64
import json
import os
import sys
import time
import webbrowser
from urllib.parse import parse_qs, quote, urlparse

import requests

AUTH_URL = "https://api.login.yahoo.com/oauth2/request_auth"
TOKEN_URL = "https://api.login.yahoo.com/oauth2/get_token"
API_BASE = "https://fantasysports.yahooapis.com/fantasy/v2"

# Yahoo no longer accepts "oob". Nothing listens on this URI: after approving,
# the browser fails to load it, and the code is copied from the address bar.
# Must match the redirect URI registered on the app (a Confidential Client).
REDIRECT_URI = "https://localhost:8080/callback"
SCOPE = "fspt-r"

HERE = os.path.dirname(os.path.abspath(__file__))
TOKEN_FILE = os.path.join(HERE, ".tokens.json")
CREDS_FILE = os.path.join(HERE, ".credentials.json")


class AuthError(Exception):
    pass


def _load_credentials():
    """Client id/secret from the environment, falling back to .credentials.json."""
    client_id = os.environ.get("YAHOO_CLIENT_ID")
    client_secret = os.environ.get("YAHOO_CLIENT_SECRET")
    if client_id and client_secret:
        return client_id, client_secret

    if os.path.exists(CREDS_FILE):
        with open(CREDS_FILE) as fh:
            creds = json.load(fh)
        if creds.get("yahoo_client_id") and creds.get("yahoo_client_secret"):
            return creds["yahoo_client_id"], creds["yahoo_client_secret"]

    raise AuthError(
        "No Yahoo API credentials found.\n"
        "Set YAHOO_CLIENT_ID and YAHOO_CLIENT_SECRET, or create "
        f"{CREDS_FILE} containing:\n"
        '  {"yahoo_client_id": "...", "yahoo_client_secret": "..."}'
    )


def _basic_auth_header(client_id, client_secret):
    raw = f"{client_id}:{client_secret}".encode()
    return "Basic " + base64.b64encode(raw).decode()


def _save_tokens(tokens):
    tokens["expires_at"] = time.time() + int(tokens.get("expires_in", 3600))
    with open(TOKEN_FILE, "w") as fh:
        json.dump(tokens, fh, indent=2)
    os.chmod(TOKEN_FILE, 0o600)
    return tokens


def _read_tokens():
    if not os.path.exists(TOKEN_FILE):
        return None
    with open(TOKEN_FILE) as fh:
        return json.load(fh)


def _extract_code(pasted):
    """Pull the auth code out of a pasted redirect URL, or accept a bare code."""
    pasted = pasted.strip()
    query = parse_qs(urlparse(pasted).query)
    if "error" in query:
        error = query["error"][0]
        hint = ""
        if error == "invalid_scope":
            hint = (
                "\nThe app lacks Fantasy Sports (fspt-r) permission -- Yahoo hasn't "
                "provisioned API access yet. Check API Permissions on the app page."
            )
        raise AuthError(
            f"Yahoo refused authorization: {error} "
            f"({query.get('error_description', [''])[0]}){hint}"
        )
    if "code=" in pasted:
        return parse_qs(urlparse(pasted).query).get("code", [""])[0]
    return pasted


def _authorize(client_id, client_secret):
    """First-run browser authorization; returns a fresh token set."""
    url = (
        f"{AUTH_URL}?client_id={client_id}&redirect_uri={quote(REDIRECT_URI, safe='')}"
        f"&response_type=code&scope={SCOPE}&language=en-us"
    )
    print("Authorize Motobowl to read your Yahoo fantasy data:\n")
    print(f"  {url}\n")
    try:
        webbrowser.open(url)
    except Exception:
        pass

    print("After approving, the browser will fail to load a localhost page.")
    print("That's expected -- copy the URL from its address bar.\n")
    code = _extract_code(input("Paste that URL (or just the code= value): "))
    if not code:
        raise AuthError("No code entered.")

    resp = requests.post(
        TOKEN_URL,
        headers={"Authorization": _basic_auth_header(client_id, client_secret)},
        data={
            "grant_type": "authorization_code",
            "redirect_uri": REDIRECT_URI,
            "code": code,
        },
        timeout=30,
    )
    if resp.status_code != 200:
        raise AuthError(f"Token exchange failed ({resp.status_code}): {resp.text}")
    return _save_tokens(resp.json())


def _refresh(tokens, client_id, client_secret):
    resp = requests.post(
        TOKEN_URL,
        headers={"Authorization": _basic_auth_header(client_id, client_secret)},
        data={
            "grant_type": "refresh_token",
            "redirect_uri": REDIRECT_URI,
            "refresh_token": tokens["refresh_token"],
        },
        timeout=30,
    )
    if resp.status_code != 200:
        raise AuthError(
            f"Token refresh failed ({resp.status_code}): {resp.text}\n"
            f"Delete {TOKEN_FILE} and re-run to authorize again."
        )
    return _save_tokens(resp.json())


def get_access_token():
    client_id, client_secret = _load_credentials()
    tokens = _read_tokens()
    if tokens is None:
        tokens = _authorize(client_id, client_secret)
    elif tokens.get("expires_at", 0) < time.time() + 60:
        tokens = _refresh(tokens, client_id, client_secret)
    return tokens["access_token"]


def get(path, params=None):
    """GET a Fantasy API resource and return the parsed JSON body."""
    params = dict(params or {})
    params["format"] = "json"
    token = get_access_token()
    url = f"{API_BASE}/{path.lstrip('/')}"

    resp = requests.get(
        url, headers={"Authorization": f"Bearer {token}"}, params=params, timeout=30
    )

    if resp.status_code == 401:
        # Token went stale early; force one refresh and retry.
        client_id, client_secret = _load_credentials()
        tokens = _refresh(_read_tokens(), client_id, client_secret)
        resp = requests.get(
            url,
            headers={"Authorization": f"Bearer {tokens['access_token']}"},
            params=params,
            timeout=30,
        )

    if resp.status_code != 200:
        raise RuntimeError(f"Yahoo API error ({resp.status_code}) for {url}:\n{resp.text}")
    return resp.json()


def flatten(node):
    """Merge Yahoo's nested list-of-dicts blobs into one flat dict.

    Yahoo returns objects as arrays of single-key dicts mixed with nested
    arrays, e.g. [[{"player_key": ...}, {"name": {...}}], {"selected_position": [...]}].
    """
    out = {}
    if isinstance(node, dict):
        for key, value in node.items():
            if isinstance(value, (list, dict)) and key not in ("name", "bye_weeks"):
                nested = flatten(value)
                out[key] = nested if nested else value
            else:
                out[key] = value
    elif isinstance(node, list):
        for item in node:
            if isinstance(item, (dict, list)):
                out.update(flatten(item))
    return out


def find_key(node, target):
    """Depth-first search for the first value stored under `target`."""
    if isinstance(node, dict):
        if target in node:
            return node[target]
        for value in node.values():
            found = find_key(value, target)
            if found is not None:
                return found
    elif isinstance(node, list):
        for item in node:
            found = find_key(item, target)
            if found is not None:
                return found
    return None


def numbered_items(collection, wrapper):
    """Yahoo collections are dicts keyed '0','1',... plus 'count'. Yield each item."""
    if not isinstance(collection, dict):
        return
    for key in sorted((k for k in collection if k.isdigit()), key=int):
        entry = collection[key]
        if isinstance(entry, dict) and wrapper in entry:
            yield entry[wrapper]


def die(message):
    print(f"error: {message}", file=sys.stderr)
    sys.exit(1)
