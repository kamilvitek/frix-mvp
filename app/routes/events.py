from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List, Dict, Any
from ..services.meetup import MeetupHandler

router = APIRouter()
meetup_handler = MeetupHandler()

class CustomerEvent(BaseModel):
    """Model for customer event data"""
    country: str
    category: Optional[str] = None
    start: Optional[datetime] = None

@router.post("/events/related")
async def find_related_events(event: CustomerEvent) -> List[Dict[Any, Any]]:
    """
    Find events related to the provided customer event
    """
    try:
        events = meetup_handler.find_related_events(event)
        return events
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error finding related events: {str(e)}") 