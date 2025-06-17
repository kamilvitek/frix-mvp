import os
import sys
import time
import json
import requests
from tokens import meetup_token

# Path to store tokens
CREDENTIALS_FILE = 'credentials.json'
# Meetup OAuth2 endpoints and credentials
TOKEN_URL = 'https://secure.meetup.com/oauth2/access'
CLIENT_ID = os.getenv('MEETUP_KEY')
CLIENT_SECRET = os.getenv('MEETUP_SECRET')


def load_tokens() -> dict:
    """
    Load tokens from a JSON file. Expects keys: access_token, refresh_token, expires_at (epoch).
    """
    try:
        with open(CREDENTIALS_FILE, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Error: Credentials file '{CREDENTIALS_FILE}' not found.", file=sys.stderr)
        sys.exit(1)


def save_tokens(tokens: dict) -> None:
    """
    Save tokens back to the JSON file.
    """
    with open(CREDENTIALS_FILE, 'w') as f:
        json.dump(tokens, f, indent=2)


def refresh_access_token(tokens: dict) -> str:
    """
    Use the refresh token to obtain a new access token and update the tokens file.
    """
    data = {
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
        'grant_type': 'refresh_token',
        'refresh_token': tokens.get('refresh_token')
    }
    resp = requests.post(TOKEN_URL, data=data)
    resp.raise_for_status()
    new = resp.json()

    # Update tokens dict
    tokens['access_token'] = new['access_token']
    tokens['refresh_token'] = new.get('refresh_token', tokens.get('refresh_token'))
    tokens['expires_at'] = time.time() + new.get('expires_in', 0)
    save_tokens(tokens)
    return tokens['access_token']


def get_valid_access_token() -> str:
    """
    Ensure access token is valid; refresh if expired or about to expire (within 60s).
    """
    tokens = load_tokens()
    expires_at = tokens.get('expires_at', 0)
    if time.time() >= expires_at - 60:
        return refresh_access_token(tokens)
    return tokens.get('access_token')


def fetch_event(group_urlname: str, event_id: str) -> dict:
    """
    Fetches a Meetup event by group URL name and event ID using Meetup API v3 with OAuth2.
    """
    access_token = get_valid_access_token()
    headers = {'Authorization': f'Bearer {access_token}'}
    url = f"https://api.meetup.com/{group_urlname}/events/{event_id}"
    resp = requests.get(url, headers=headers)
    resp.raise_for_status()
    return resp.json()


def print_event(event: dict) -> None:
    """
    Prints selected event details to the terminal.
    """
    print(f"Event: {event.get('name', '<no title>')}")
    print(f"Date & Time: {event.get('local_date', '')} {event.get('local_time', '')}")

    venue = event.get('venue', {})
    if venue:
        print(f"Venue: {venue.get('name', '')} ({venue.get('city', '')}, {venue.get('address_1', '')})")
    else:
        print("Venue: TBD")

    print("\nDescription:\n")
    # Descriptions are HTML; consider stripping tags as needed
    print(event.get('description', '<no description>'))


if __name__ == '__main__':
    # Collect user input
    group = input("Enter Meetup group URL name (e.g., 'Py-Prague'): ").strip()
    event_id = input("Enter Meetup event ID: ").strip()

    # Validate OAuth2 credentials
    if not CLIENT_ID or not CLIENT_SECRET:
        print("Error: Please set MEETUP_CLIENT_ID and MEETUP_CLIENT_SECRET environment variables.", file=sys.stderr)
        sys.exit(1)

    try:
        event = fetch_event(group, event_id)
        print_event(event)
    except requests.HTTPError as e:
        print(f"HTTP error: {e}", file=sys.stderr)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
