from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import RedirectResponse, JSONResponse
from ..services.meetup import MeetupHandler
import os

router = APIRouter()
meetup_handler = MeetupHandler()

@router.get("/oauth/meetup/test-config")
async def test_config():
    """
    Test endpoint to verify OAuth configuration
    """
    config = {
        "client_id": os.getenv('MEETUP_KEY', '').strip(),
        "client_id_length": len(os.getenv('MEETUP_KEY', '').strip()),
        "client_secret_set": bool(os.getenv('MEETUP_SECRET')),
        "redirect_uri": os.getenv('MEETUP_REDIRECT_URI', 'http://localhost:8000/oauth/callback')
    }
    return config

@router.get("/oauth/meetup")
async def meetup_auth(request: Request):
    """
    Start the OAuth flow by redirecting to Meetup's authorization page
    """
    try:
        auth_url = meetup_handler.get_authorization_url()
        print(f"Redirecting to Meetup authorization URL: {auth_url}")
        return RedirectResponse(url=auth_url)
    except Exception as e:
        print(f"Error generating authorization URL: {str(e)}")
        return JSONResponse(
            status_code=500,
            content={"error": f"Failed to generate authorization URL: {str(e)}"}
        )

@router.get("/oauth/callback")
async def oauth_callback(request: Request, code: str = None, error: str = None, error_description: str = None):
    """
    Handle the OAuth callback from Meetup
    """
    # Log all query parameters for debugging
    query_params = dict(request.query_params)
    print(f"\nReceived callback with params: {query_params}")
    print(f"Headers: {dict(request.headers)}")

    if error:
        error_msg = f"Authorization failed: {error}"
        if error_description:
            error_msg += f" - {error_description}"
        print(f"OAuth Error: {error_msg}")
        return JSONResponse(
            status_code=400,
            content={
                "error": error_msg,
                "received_params": query_params,
                "headers": dict(request.headers)
            }
        )
    
    if not code:
        print("No authorization code received in callback")
        return JSONResponse(
            status_code=400,
            content={
                "error": "No authorization code received",
                "received_params": query_params,
                "headers": dict(request.headers)
            }
        )
    
    try:
        # Exchange the code for an access token
        token_data = meetup_handler.get_access_token(code)
        print("Successfully obtained access token")
        return JSONResponse(content={
            "message": "Authentication successful",
            "token_type": token_data.get("token_type"),
            "received_params": query_params
        })
    except Exception as e:
        print(f"Error exchanging code for token: {str(e)}")
        return JSONResponse(
            status_code=400,
            content={
                "error": str(e),
                "received_params": query_params,
                "headers": dict(request.headers)
            }
        ) 