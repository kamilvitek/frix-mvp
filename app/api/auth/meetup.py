from fastapi import APIRouter, HTTPException, Request, Query
from fastapi.responses import RedirectResponse
from datetime import datetime
from typing import Optional, List, Dict
from app.services.meetup import MeetupHandler
from app.services.token_storage import TokenStorage

router = APIRouter()
meetup = MeetupHandler()
token_storage = TokenStorage()

@router.get("/auth/meetup/login")
async def meetup_login():
    """
    Start the Meetup OAuth flow by redirecting to Meetup's authorization page
    """
    try:
        # Validate that we have all required credentials
        if not meetup.client_id or not meetup.client_secret:
            raise HTTPException(
                status_code=500,
                detail="Meetup API credentials are not configured"
            )
        
        if not meetup.redirect_uri:
            raise HTTPException(
                status_code=500,
                detail="Meetup redirect URI is not configured"
            )
            
        # Get the authorization URL
        auth_url = meetup.get_authorization_url()
        
        # Log the URL for debugging (you may want to remove this in production)
        print(f"Redirecting to Meetup auth URL: {auth_url}")
        
        return RedirectResponse(url=auth_url)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to start authentication: {str(e)}"
        )

@router.get("/oauth/callback")
async def meetup_callback(
    code: Optional[str] = None,
    error: Optional[str] = None,
    error_description: Optional[str] = None
):
    """
    Handle the OAuth callback from Meetup
    """
    # Handle error cases
    if error:
        error_msg = f"Authentication failed: {error}"
        if error_description:
            error_msg += f" - {error_description}"
        raise HTTPException(status_code=400, detail=error_msg)
    
    # Handle missing code
    if not code:
        return RedirectResponse(
            url="/auth/meetup/login",
            status_code=302
        )
    
    try:
        # Exchange the code for an access token
        token_data = meetup.get_access_token(code=code)
        
        # Store the token
        token_storage.save_token("meetup", token_data)
        
        # Redirect to a success page or return success response
        return {
            "status": "success",
            "message": "Successfully authenticated with Meetup!"
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to complete authentication: {str(e)}"
        )

@router.get("/auth/meetup/status")
async def auth_status():
    """
    Check if we have valid Meetup credentials
    """
    token = token_storage.get_token("meetup")
    if token:
        return {
            "authenticated": True,
            "expires_in": token.get("expires_in"),
            "token_type": token.get("token_type")
        }
    return {"authenticated": False}

@router.post("/auth/meetup/logout")
async def logout():
    """
    Remove stored Meetup credentials
    """
    if token_storage.delete_token("meetup"):
        return {"message": "Successfully logged out"}
    return {"message": "No active session found"}

@router.get("/meetup/events/search")
async def search_events(
    location: str,
    category: Optional[str] = None,
    radius: Optional[int] = Query(default=50, gt=0, le=100),
    start_date: Optional[str] = None
):
    """
    Search for Meetup events
    """
    # Check if we're authenticated
    if not token_storage.get_token("meetup"):
        raise HTTPException(
            status_code=401,
            detail="Not authenticated. Please authenticate with Meetup first."
        )
    
    try:
        # Convert start_date string to datetime if provided
        start_datetime = None
        if start_date:
            try:
                start_datetime = datetime.fromisoformat(start_date)
            except ValueError:
                raise HTTPException(
                    status_code=400,
                    detail="Invalid date format. Please use ISO format (YYYY-MM-DD or YYYY-MM-DDTHH:MM:SS)"
                )
        
        # Search for events
        events = meetup.search_events(
            location=location,
            category=category,
            start_date=start_datetime,
            radius=radius
        )
        
        return {
            "count": len(events),
            "events": events
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 