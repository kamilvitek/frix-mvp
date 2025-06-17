import os
from dotenv import load_dotenv

def check_credentials():
    # Load environment variables
    load_dotenv()
    
    print("\nMeetup Credentials Check")
    print("=" * 30)
    
    # Get credentials
    client_id = os.getenv('MEETUP_KEY')
    client_secret = os.getenv('MEETUP_SECRET')
    redirect_uri = os.getenv('MEETUP_REDIRECT_URI')
    
    # Check Client ID
    if client_id:
        print(f"\nClient ID: {client_id[:4]}...{client_id[-4:]}")
        print(f"Length: {len(client_id)} characters")
    else:
        print("❌ MEETUP_KEY not found!")
        
    # Check Client Secret
    if client_secret:
        print(f"\nClient Secret: {client_secret[:4]}...{client_secret[-4:]}")
        print(f"Length: {len(client_secret)} characters")
    else:
        print("❌ MEETUP_SECRET not found!")
        
    # Check Redirect URI
    if redirect_uri:
        print(f"\nRedirect URI: {redirect_uri}")
        if not redirect_uri.startswith('http'):
            print("⚠️  Warning: Redirect URI should start with http:// or https://")
    else:
        print("❌ MEETUP_REDIRECT_URI not found!")

if __name__ == "__main__":
    check_credentials() 