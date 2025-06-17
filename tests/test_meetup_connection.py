from app.services.meetup import MeetupHandler
from dotenv import load_dotenv
import os

def main():
    # Load environment variables from .env file
    load_dotenv()
    
    print("\nMeetup API Configuration Test")
    print("=" * 30)
    
    # Check environment variables
    meetup_key = os.getenv('MEETUP_KEY')
    meetup_secret = os.getenv('MEETUP_SECRET')
    redirect_uri = os.getenv('MEETUP_REDIRECT_URI')
    
    print("\nChecking environment variables:")
    print(f"MEETUP_KEY: {'✓ Set' if meetup_key else '✗ Missing'}")
    print(f"MEETUP_SECRET: {'✓ Set' if meetup_secret else '✗ Missing'}")
    print(f"MEETUP_REDIRECT_URI: {'✓ Set' if redirect_uri else '✗ Missing'}")
    
    if redirect_uri:
        print(f"\nConfigured Redirect URI: {redirect_uri}")
        if redirect_uri.startswith('@'):
            print("⚠️  Warning: Redirect URI should not start with '@'")
        if 'example.com' in redirect_uri:
            print("⚠️  Warning: Using example.com is not allowed, please use your actual redirect URI")
    
    try:
        # Create MeetupHandler instance
        meetup = MeetupHandler()
        
        # Get authorization URL
        auth_url = meetup.get_authorization_url()
        print("\nAuthorization URL:")
        print(auth_url)
        
        # Test the connection
        result = meetup.test_connection()
        
        # Print the result
        print("\nAPI Connection Test:")
        print(f"Status: {result['status']}")
        print(f"Message: {result['message']}")
        if result['status'] == 'success':
            print("\nAPI Status Details:")
            print(result['api_status'])
        elif 'details' in result:
            print("\nError Details:")
            print(result['details'])
            
    except ValueError as e:
        print(f"\n❌ Configuration Error: {str(e)}")
    except Exception as e:
        print(f"\n❌ Unexpected Error: {str(e)}")

if __name__ == "__main__":
    main() 