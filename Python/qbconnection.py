import requests
import json
import base64
import hmac
import hashlib
import time
import os

class QuickbaseAPI:
    def __init__(self, realm, user_token, app_token=None):
        self.realm = realm
        self.user_token = user_token
        self.app_token = app_token
        self.base_url = f"https://api.quickbase.com/v1"
        
    def _get_auth_header(self):
        """Generate the authentication header for Quickbase API"""
        timestamp = str(int(time.time()))
        nonce = base64.b64encode(os.urandom(16)).decode('utf-8')
        
        # Create the signature string
        signature_string = f"{self.user_token}&{timestamp}&{nonce}"
        
        # Generate HMAC signature
        signature = hmac.new(
            self.app_token.encode('utf-8'),
            signature_string.encode('utf-8'),
            hashlib.sha256
        ).hexdigest()
        
        return {
            'QB-Realm-Hostname': self.realm,
            'Authorization': f'QB-USER-TOKEN {self.user_token}',
            'QB-Timestamp': timestamp,
            'QB-Nonce': nonce,
            'QB-Signature': signature
        }

    def make_request(self,endpoint,payload):
        headers = self._get_auth_header()
        headers['Content-Type'] = 'application/json'
        
        response = requests.post(
            endpoint,
            headers=headers,
            json=payload
        )
        
        return response.json()