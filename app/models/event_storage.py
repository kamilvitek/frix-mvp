from typing import List, Dict, Any
from datetime import datetime
import json
import os

class EventStorage:
    def __init__(self, storage_dir: str = None):
        """
        Initialize event storage with a directory to store event data
        """
        if storage_dir is None:
            # Get the project root directory (parent of app directory)
            project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
            storage_dir = os.path.join(project_root, "data", "events")
        
        self.storage_dir = storage_dir
        os.makedirs(storage_dir, exist_ok=True)
        print(f"Events will be stored in: {self.storage_dir}")
    
    def store_related_events(self, customer_event_id: str, related_events: List[Dict[Any, Any]]) -> str:
        """
        Store related events for a specific customer event
        Returns the path where events were stored
        """
        # Create a filename based on customer event details
        filename = f"{customer_event_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        filepath = os.path.join(self.storage_dir, filename)
        
        # Prepare data for storage
        data = {
            "customer_event_id": customer_event_id,
            "timestamp": datetime.now().isoformat(),
            "related_events": related_events
        }
        
        # Save to file
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
            
        return filepath
    
    def get_related_events(self, customer_event_id: str) -> List[Dict[Any, Any]]:
        """
        Retrieve the most recent related events for a customer event
        """
        # Find the most recent file for this customer event
        files = [f for f in os.listdir(self.storage_dir) 
                if f.startswith(customer_event_id) and f.endswith('.json')]
        
        if not files:
            return []
            
        # Get the most recent file
        latest_file = max(files)
        filepath = os.path.join(self.storage_dir, latest_file)
        
        # Read and return the events
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return data.get('related_events', []) 