import os
from typing import Dict, List, Any, Optional
import requests
from datetime import datetime
from urllib.parse import urlencode, quote
from .token_storage import TokenStorage

class MeetupHandler:
    """Handler for Meetup API integration"""
    
    def __init__(self):
        self.client_id = os.getenv('MEETUP_KEY')
        self.client_secret = os.getenv('MEETUP_SECRET')
        self.redirect_uri = os.getenv('MEETUP_REDIRECT_URI', 'http://localhost:3000/oauth/callback')
        self.token_storage = TokenStorage()
        
        if not all([self.client_id, self.client_secret, self.redirect_uri]):
            raise ValueError("Missing required Meetup API configuration")
        
        # API endpoints from documentation
        self.auth_url = "https://secure.meetup.com/oauth2/authorize"
        self.token_url = "https://secure.meetup.com/oauth2/access"
        self.api_base_url = "https://api.meetup.com"

    def get_authorization_url(self) -> str:
        """Generate the authorization URL for OAuth2 flow"""
        # Ensure the redirect URI is properly URL encoded
        encoded_redirect = quote(self.redirect_uri, safe='')
        
        # Construct authorization URL with required parameters
        # Note: Meetup requires these exact parameters in this format
        auth_url = (
            f"{self.auth_url}"
            f"?client_id={quote(self.client_id)}"
            f"&response_type=code"
            f"&redirect_uri={encoded_redirect}"
        )
        
        print(f"Generated authorization URL: {auth_url}")
        return auth_url

    def get_access_token(self, code: str) -> Dict[str, str]:
        """Exchange authorization code for access token"""
        # URL encode the redirect URI for the token request
        encoded_redirect = quote(self.redirect_uri, safe='')
        
        data = {
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'grant_type': 'authorization_code',
            'redirect_uri': encoded_redirect,
            'code': code
        }
        
        headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        
        print(f"Requesting access token with data: {data}")
        
        response = requests.post(
            self.token_url,
            data=data,
            headers=headers
        )
        
        if response.status_code != 200:
            error_detail = response.json() if response.text else str(response)
            print(f"Token request failed. Response: {error_detail}")
            raise Exception(f"Failed to get access token: {error_detail}")
        
        token_data = response.json()
        self.token_storage.save_token("meetup", token_data)
        return token_data

    def find_related_events(self, customer_event) -> List[Dict[Any, Any]]:
        """
        Find events related to the customer event based on:
        - Location (same city/area)
        - Category/Topic
        - Date range (around the customer event date)
        """
        token_data = self.token_storage.get_token("meetup")
        if not token_data or 'access_token' not in token_data:
            raise ValueError("Please authenticate first")
            
        headers = {
            'Authorization': f"Bearer {token_data['access_token']}",
            'Accept': 'application/json'
        }
        
        # Extract location from customer event
        location = customer_event.country if hasattr(customer_event, 'country') else None
        if not location:
            raise ValueError("Customer event must have a location")
            
        # Build search parameters
        params = {
            'location': location,
            'radius': '50km',  # Default radius
            'page': 20
        }
        
        # Add category if available
        if hasattr(customer_event, 'category') and customer_event.category:
            params['topic_category'] = customer_event.category
            
        # Add date range if available
        if hasattr(customer_event, 'start') and customer_event.start:
            # Search for events around the customer event date
            params['start_date_range'] = customer_event.start
            
        try:
            response = requests.get(
                f"{self.api_base_url}/find/upcoming_events",
                headers=headers,
                params=params
            )
            
            if response.status_code == 200:
                events = response.json().get('events', [])
                return self._process_events(events)
            else:
                print(f"Error searching events: {response.text}")
                return []
                
        except Exception as e:
            print(f"Error finding related events: {str(e)}")
            return []
            
    def _process_events(self, events: List[Dict]) -> List[Dict]:
        """Process and format event data"""
        processed_events = []
        for event in events:
            processed_event = {
                'id': event.get('id'),
                'name': event.get('name'),
                'description': event.get('description'),
                'start_time': event.get('local_date', '') + ' ' + event.get('local_time', ''),
                'venue': event.get('venue', {}),
                'group': event.get('group', {}),
                'link': event.get('link'),
                'attendance_count': event.get('yes_rsvp_count', 0),
                'is_online': event.get('is_online_event', False),
                'category': event.get('group', {}).get('category', {}).get('name', '')
            }
            processed_events.append(processed_event)
        return processed_events

    def test_connection(self) -> Dict[str, Any]:
        """
        Test the API connection and authentication
        Returns the response data if successful, raises an exception if not
        """
        try:
            # First, let's check if we have valid credentials
            if not self.client_id or not self.client_secret:
                return {
                    "status": "error",
                    "message": "Missing API credentials. Please check MEETUP_KEY and MEETUP_SECRET environment variables."
                }

            # Try to make a simple API call to get some public data
            response = requests.get(
                f"{self.api_base_url}/status",
                headers={'Accept': 'application/json'}
            )

            if response.status_code == 200:
                return {
                    "status": "success",
                    "message": "Successfully connected to Meetup API",
                    "api_status": response.json()
                }
            else:
                return {
                    "status": "error",
                    "message": f"API request failed with status code: {response.status_code}",
                    "details": response.text
                }

        except Exception as e:
            return {
                "status": "error",
                "message": f"Connection test failed: {str(e)}"
            }
