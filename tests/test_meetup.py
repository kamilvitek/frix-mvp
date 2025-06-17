from app.services.meetup import MeetupHandler

def test_meetup():
    # Create instance of MeetupHandler
    handler = MeetupHandler()
    
    # Test get_authorization_url() - this will print the URL
    auth_url = handler.get_authorization_url()
    print(auth_url)
    
    stored_token = handler.token_storage.get_token("meetup")
    print("Token exists:", bool(stored_token))
if __name__ == "__main__":
    test_meetup()
    
