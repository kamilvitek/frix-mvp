#Conflict score
# from app.services.eventbrite import EventbriteHandler
from app.models.event_storage import EventStorage
from datetime import datetime, timedelta, timezone
from typing import Optional, Dict, Any, List
import re

###Simulation of user's input
class Customer_event:
    def __init__(
        self,
        country: str,
        category: str,
        start: Optional[datetime] = None,
        end: Optional[datetime] = None,
        phq_label: Optional[str] = None
    ):
        self.country = self._format_location(country)
        self.category = self._format_category(category)
        self.start = self._format_date(start) if start else ""
        self.end = self._format_date(end) if end else ""
        self.phq_label = phq_label
        # Generate a unique ID for the event
        self.id = self._generate_id()
    
    def _format_date(self, date_obj: Optional[datetime]) -> str:
        """
        Format date to Eventbrite's expected format (UTC)
        Returns ISO 8601 formatted string with UTC timezone
        """
        if not date_obj:
            return ""
            
        # Ensure timezone is UTC
        if date_obj.tzinfo is None:
            date_obj = date_obj.replace(tzinfo=timezone.utc)
        else:
            date_obj = date_obj.astimezone(timezone.utc)
        return date_obj.strftime("%Y-%m-%dT%H:%M:%SZ")
    
    def _format_location(self, location: str) -> str:
        """
        Format location string for Eventbrite API
        Removes extra whitespace and normalizes format
        """
        if not location:
            return ""
        # Remove extra whitespace and normalize format
        location = re.sub(r'\s+', ' ', location.strip())
        # Ensure proper capitalization
        parts = [part.strip() for part in location.split(',')]
        parts = [part.title() for part in parts]
        return ', '.join(parts)
    
    def _format_category(self, category: str) -> str:
        """Format category string to match Eventbrite categories"""
        if not category:
            return ""
        return category.lower().strip()
    
    def _generate_id(self) -> str:
        """Generate a unique ID for the event"""
        # Create a clean, URL-friendly ID
        base = f"{self.country}_{self.category}"
        # Remove special characters and spaces
        clean_id = re.sub(r'[^a-zA-Z0-9]+', '_', base.lower())
        # Remove leading/trailing underscores
        return clean_id.strip('_')
    
    def __str__(self) -> str:
        return(
            f"Location: {self.country}\n"
            f"Category: {self.category}\n"
            f"Start: {self.start}\n"
            f"End: {self.end}\n"
            f"Label: {self.phq_label}\n"
        )

    def get_related_events(self) -> List[Dict[str, Any]]:
        """
        Fetch and store related events for this customer event
        Returns a list of related events with their details
        """
        # eventbrite = EventbriteHandler()
        storage = EventStorage()
        
        # First try to get events from storage
        events = storage.get_related_events(self.id)
        
        # If no events found in storage, fetch from Eventbrite and store them
        # if not events:
        #     events = eventbrite.search_related_events(self)
        #     if events:
        #         storage.store_related_events(self.id, events)
        
        return events

def format_event_output(event: Dict[str, Any]) -> str:
    """Format event details for display"""
    venue_name = event['venue']['name'] if event['venue'] else 'Online'
    category_name = event['category']['name'] if event['category'] else 'Uncategorized'
    
    return (
        f"Event: {event['name']}\n"
        f"Summary: {event['summary']}\n"
        f"Date: {event['start'].get('utc', '')} "
        f"({event['start'].get('timezone', 'UTC')})\n"
        f"Location: {venue_name}\n"
        f"Category: {category_name}\n"
        f"Status: {event['status']}\n"
        f"URL: {event['url']}\n"
        f"{'Online Event' if event['online_event'] else 'In-Person Event'}\n"
        f"Created: {event['created']}\n"
        f"Last Modified: {event['changed']}\n"
        f"-" * 50
    )

# Get current date and end date (90 days from now) with UTC timezone
current_date = datetime.now(timezone.utc)
end_date = current_date + timedelta(days=90)

input_event = Customer_event(
    country="Ostrava, Czech Republic",
    category="music",
    start=current_date,
    end=end_date,
    phq_label="music"
)

# Example usage:
related_events = input_event.get_related_events()
if related_events:
    print(f"Found {len(related_events)} related events:")
    for event in related_events:
        print(format_event_output(event))
else:
    print("No related events found")