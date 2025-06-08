import os
from datetime import datetime
import requests
from typing import List, Dict, Any

class EventbriteHandler:
    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.getenv('EVENTBRITE_API_KEY')
        if not self.api_key:
            raise ValueError("Eventbrite API key is required")
        
        self.base_url = "https://www.eventbriteapi.com/v3"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
    
    def search_related_events(self, customer_event) -> List[Dict[Any, Any]]:
        """
        Search for events related to the customer event based on location and category
        Returns a list of relevant events
        """
        endpoint = f"{self.base_url}/events/search"
        
        # Convert category to Eventbrite format if needed
        # You might want to create a mapping dictionary for categories
        
        params = {
            "q": customer_event.q,
            "location.address": customer_event.country,
            # Add date parameters if provided
            "expand": "venue,category",
        }
        
        if customer_event.start:
            params["start_date.range_start"] = customer_event.start
        if customer_event.end:
            params["start_date.range_end"] = customer_event.end
            
        try:
            response = requests.get(endpoint, headers=self.headers, params=params)
            response.raise_for_status()
            events = response.json().get("events", [])
            
            # Transform events to a more usable format
            processed_events = []
            for event in events:
                processed_event = {
                    "name": event.get("name", {}).get("text", ""),
                    "description": event.get("description", {}).get("text", ""),
                    "start": event.get("start", {}).get("utc", ""),
                    "end": event.get("end", {}).get("utc", ""),
                    "venue": event.get("venue", {}).get("name", ""),
                    "category": event.get("category", {}).get("name", ""),
                    "url": event.get("url", ""),
                }
                processed_events.append(processed_event)
                
            return processed_events
            
        except requests.exceptions.RequestException as e:
            print(f"Error fetching events from Eventbrite: {e}")
            return [] 