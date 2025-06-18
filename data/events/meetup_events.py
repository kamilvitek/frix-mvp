import os
import sys
import time
import json
import requests
from datetime import datetime
from typing import Optional, Dict, Any

# Path to store tokens
CREDENTIALS_FILE = os.path.join(os.path.dirname(__file__), '..', 'tokens', 'meetup_token.json')
# Meetup OAuth2 endpoints and credentials
TOKEN_URL = 'https://secure.meetup.com/oauth2/access'
GRAPHQL_URL = 'https://api.meetup.com/gql'
CLIENT_ID = os.getenv('MEETUP_KEY')
CLIENT_SECRET = os.getenv('MEETUP_SECRET')


def load_tokens() -> Dict[str, Any]:
    """
    Load tokens from a JSON file. Extract from token_data structure.
    
    Returns:
        dict: A dictionary containing access_token, refresh_token, and expires_at
    
    Raises:
        SystemExit: If the credentials file is not found or token data is invalid
        json.JSONDecodeError: If the JSON file is malformed
    """
    try:
        with open(CREDENTIALS_FILE, 'r') as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                print(f"Error: Credentials file '{CREDENTIALS_FILE}' contains invalid JSON.", file=sys.stderr)
                sys.exit(1)
            
        # Extract the token data from the stored structure
        token_data = data.get('token_data', {})
        if not token_data:
            print("Error: No token_data found in credentials file.", file=sys.stderr)
            sys.exit(1)
            
        # Validate required fields
        required_fields = ['access_token', 'refresh_token', 'expires_in']
        missing_fields = [field for field in required_fields if field not in token_data]
        if missing_fields:
            print(f"Error: Missing required fields in token_data: {', '.join(missing_fields)}", file=sys.stderr)
            sys.exit(1)
            
        # Convert to the expected format
        return {
            'access_token': token_data['access_token'],
            'refresh_token': token_data['refresh_token'],
            'expires_at': time.time() + token_data['expires_in']  # Calculate expiration time
        }
    except FileNotFoundError:
        print(f"Error: Credentials file '{CREDENTIALS_FILE}' not found.", file=sys.stderr)
        sys.exit(1)


def save_tokens(tokens: Dict[str, Any]) -> None:
    """
    Save tokens back to the JSON file in the correct structure.
    
    Args:
        tokens (dict): Dictionary containing access_token, refresh_token, and expires_at
    """
    data = {
        'token_data': {
            'access_token': tokens['access_token'],
            'refresh_token': tokens['refresh_token'],
            'expires_in': int(tokens['expires_at'] - time.time()),
            'token_type': 'bearer'
        },
        'stored_at': time.strftime('%Y-%m-%dT%H:%M:%S.%f+00:00', time.gmtime())
    }
    with open(CREDENTIALS_FILE, 'w') as f:
        json.dump(data, f, indent=2)


def refresh_access_token(tokens: Dict[str, Any]) -> str:
    """
    Use the refresh token to obtain a new access token and update the tokens file.
    
    Args:
        tokens (dict): Current tokens dictionary containing refresh_token
        
    Returns:
        str: New access token
        
    Raises:
        requests.HTTPError: If the token refresh request fails
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
    
    Returns:
        str: Valid access token
    """
    tokens = load_tokens()
    expires_at = tokens.get('expires_at', 0)
    if time.time() >= expires_at - 60:
        return refresh_access_token(tokens)
    return tokens.get('access_token')


def fetch_event(event_id: str) -> Dict[str, Any]:
    """
    Fetches a Meetup event using GraphQL API.
    
    Args:
        event_id (str): The ID of the Meetup event to fetch
        
    Returns:
        dict: Event data including title, description, date/time, venue, etc.
        
    Raises:
        requests.HTTPError: If the API request fails
        Exception: If the GraphQL response contains errors or event is not found
    """
    # Validate event ID format
    if not event_id or not event_id.strip():
        raise ValueError("Event ID cannot be empty")
    
    access_token = get_valid_access_token()
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }
    
    query = """
    query($eventId: ID!) {
      event(id: $eventId) {
        id
        title
        description
        dateTime
        eventUrl
        venue {
          name
          city
          address
          country
        }
        group {
          name
          urlname
        }
      }
    }
    """
    
    variables = {
        "eventId": event_id
    }
    
    resp = requests.post(
        GRAPHQL_URL,
        headers=headers,
        json={
            "query": query,
            "variables": variables
        }
    )
    
    if resp.status_code != 200:
        print(f"Error response from Meetup API: {resp.text}", file=sys.stderr)
        resp.raise_for_status()
    
    try:
        data = resp.json()
    except json.JSONDecodeError:
        raise Exception("Invalid JSON response from Meetup API")

    if 'errors' in data:
        raise Exception(f"GraphQL Error: {data['errors']}")
    
    event_data = data.get('data', {}).get('event')
    if not event_data:
        raise Exception(f"Event not found with ID: {event_id}")
    
    return event_data


def print_event(event: Dict[str, Any]) -> None:
    """
    Prints selected event details to the terminal.
    
    Args:
        event (dict): Event data dictionary containing title, description, etc.
    """
    print(f"\nEvent Details:")
    print("=" * 50)
    print(f"Title: {event.get('title', '<no title>')}")
    
    # Format the datetime
    date_time = event.get('dateTime', '')
    if date_time:
        try:
            dt = datetime.fromisoformat(date_time.replace('Z', '+00:00'))
            print(f"Date & Time: {dt.strftime('%Y-%m-%d %H:%M')} UTC")
        except ValueError:
            print(f"Date & Time: {date_time}")
    
    # Print venue information
    venue = event.get('venue', {})
    if venue:
        venue_parts = []
        if venue.get('name'): venue_parts.append(venue['name'])
        if venue.get('city'): venue_parts.append(venue['city'])
        if venue.get('address'): venue_parts.append(venue['address'])
        print(f"Venue: {', '.join(venue_parts)}" if venue_parts else "Venue: TBD")
    else:
        print("Venue: TBD")
    
    # Print group information
    group = event.get('group', {})
    if group:
        print(f"Group: {group.get('name', 'N/A')}")
    
    print(f"Event URL: {event.get('eventUrl', 'N/A')}")
    
    '''Following code can prints description of the event'''
    # print("\nDescription:")
    # print("-" * 50)
    # print(event.get('description', '<no description>'))
    # print("=" * 50)


if __name__ == '__main__':
    # Validate OAuth2 credentials first
    if not CLIENT_ID or not CLIENT_SECRET:
        print("Error: Please set MEETUP_KEY and MEETUP_SECRET environment variables.", file=sys.stderr)
        sys.exit(1)

    # Collect user input - we only need the event ID with GraphQL
    print("\nMeetup Event Fetcher")
    print("-" * 20)
    event_id = input("Enter Meetup event ID: ").strip()

    try:
        event = fetch_event(event_id)
        print_event(event)
    except requests.HTTPError as e:
        print(f"HTTP error: {e}", file=sys.stderr)
        if hasattr(e, 'response'):
            print(f"Response: {e.response.text}", file=sys.stderr)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
