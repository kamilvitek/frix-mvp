import os
from typing import Dict, List, Any, Optional
import requests
from datetime import datetime
from urllib.parse import urlencode, quote
from app.services.token_storage import TokenStorage
import json
from typing import Dict, List, Any


class MeetupHandler:
    """Handler for Meetup API integration"""
    
    def __init__(self):
        self.client_id = os.getenv('MEETUP_KEY').strip() if os.getenv('MEETUP_KEY') else None
        self.client_secret = os.getenv('MEETUP_SECRET').strip() if os.getenv('MEETUP_SECRET') else None
        # Redirect URI must be a public URL registered with Meetup, not localhost
        # For development, use a service like ngrok or a proper development domain
        self.redirect_uri = os.getenv('MEETUP_REDIRECT_URI')
        if not self.redirect_uri:
            raise ValueError("MEETUP_REDIRECT_URI must be set to a registered public URL")
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

    def manual_auth_flow(self) -> Dict[str, str]:
        """
        Run the OAuth flow manually by getting user input for the authorization code.
        Returns the token data if successful.
        """
        # Step 1: Get and display the authorization URL
        auth_url = self.get_authorization_url()
        print("\n1. Open this URL in your browser:")
        print(auth_url)
        
        # Step 2: Get the code from user input
        print("\n2. After authorizing, copy the 'code' parameter from the redirect URL")
        code = input("Enter the authorization code: ").strip()
        
        if not code:
            raise ValueError("Authorization code cannot be empty")
            
        # Step 3: Exchange the code for a token
        print("\n3. Exchanging code for token...")
        return self.get_access_token(code)

    def get_access_token(self, code: str) -> Dict[str, str]:
        """Exchange authorization code for access token"""
        # Do NOT URL encode the redirect URI for the token request (send as plain string)
        data = {
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'grant_type': 'authorization_code',
            'redirect_uri': self.redirect_uri,
            'code': code
        }
        
        headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        
        print("\n=== Token Exchange Debug Info ===")
        print(f"Token URL: {self.token_url}")
        print(f"Request Headers: {headers}")
        print(f"Request Data:")
        print(f"  - client_id: {self.client_id[:4]}...{self.client_id[-4:]}")
        print(f"  - client_secret: {self.client_secret[:4]}...{self.client_secret[-4:]}")
        print(f"  - grant_type: {data['grant_type']}")
        print(f"  - redirect_uri: {data['redirect_uri']}")
        print(f"  - code: {code[:10]}...")
        
        response = requests.post(
            self.token_url,
            data=data,
            headers=headers
        )
        
        print(f"\nResponse Status: {response.status_code}")
        print(f"Response Headers: {dict(response.headers)}")
        print(f"Response Body: {response.text}")
        
        if response.status_code != 200:
            error_detail = response.json() if response.text else str(response)
            print(f"\nToken request failed. Response: {error_detail}")
            raise Exception(f"Failed to get access token: {error_detail}")
        
        token_data = response.json()
        print("\nToken exchange successful!")
        self.token_storage.save_token("meetup", token_data)
        return token_data

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

if __name__ == "__main__":
    # Create an instance and run the auth flow
    handler = MeetupHandler()
    try:
        print("\nStarting Meetup OAuth Authentication Flow...")
        token_data = handler.manual_auth_flow()
        print("\nAuthentication successful!")
        print("Token has been saved automatically.")
        
        # Test the connection
        test_result = handler.test_connection()
        print(f"\nConnection test: {test_result['message']}")
    except Exception as e:
        print(f"\nError during authentication: {e}")


