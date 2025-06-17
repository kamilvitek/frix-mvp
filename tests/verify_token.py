from app.services.token_storage import TokenStorage
import json
from datetime import datetime

def verify_token():
    # Initialize token storage
    storage = TokenStorage()
    
    # Try to get the Meetup token
    token = storage.get_token("meetup")
    
    print("\nMeetup Token Verification")
    print("=" * 30)
    
    if token is None:
        print("❌ No token found! The OAuth flow might not have completed successfully.")
        return
    
    print("✅ Token found!")
    print("\nToken Details:")
    print("-" * 20)
    
    # Check token type
    token_type = token.get("token_type")
    print(f"Token Type: {token_type}")
    
    # Check if we have an access token
    access_token = token.get("access_token")
    if access_token:
        print(f"Access Token: {access_token[:10]}...{access_token[-10:]}")  # Show only start and end
    else:
        print("❌ No access token found!")
    
    # Check expiration if available
    expires_in = token.get("expires_in")
    if expires_in:
        print(f"Expires In: {expires_in} seconds")
    
    # Try to read the raw file to show storage timestamp
    token_file = storage._get_token_file("meetup")
    try:
        with open(token_file, 'r') as f:
            full_data = json.load(f)
            stored_at = full_data.get("stored_at")
            if stored_at:
                print(f"\nToken was stored at: {stored_at}")
    except Exception as e:
        print(f"\nCouldn't read storage timestamp: {str(e)}")

if __name__ == "__main__":
    verify_token() 