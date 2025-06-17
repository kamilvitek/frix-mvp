import json
import os
from datetime import datetime, timezone
from typing import Dict, Optional

class TokenStorage:
    """Handles storage and retrieval of OAuth tokens"""
    
    def __init__(self, storage_dir: str = None):
        if storage_dir is None:
            # Get the project root directory
            project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
            storage_dir = os.path.join(project_root, "data", "tokens")
        
        self.storage_dir = storage_dir
        os.makedirs(storage_dir, exist_ok=True)
    
    def _get_token_file(self, service: str) -> str:
        """Get the path to the token file for a specific service"""
        return os.path.join(self.storage_dir, f"{service}_token.json")
    
    def save_token(self, service: str, token_data: Dict) -> None:
        """
        Save token data with timestamp
        """
        data = {
            "token_data": token_data,
            "stored_at": datetime.now(timezone.utc).isoformat()
        }
        
        with open(self._get_token_file(service), 'w') as f:
            json.dump(data, f, indent=2)
    
    def get_token(self, service: str) -> Optional[Dict]:
        """
        Retrieve token data if it exists
        """
        token_file = self._get_token_file(service)
        
        if not os.path.exists(token_file):
            return None
            
        try:
            with open(token_file, 'r') as f:
                data = json.load(f)
                return data.get("token_data")
        except (json.JSONDecodeError, KeyError):
            return None
    
    def delete_token(self, service: str) -> bool:
        """
        Delete token data for a service
        Returns True if token was deleted, False if it didn't exist
        """
        token_file = self._get_token_file(service)
        
        if os.path.exists(token_file):
            os.remove(token_file)
            return True
        return False

