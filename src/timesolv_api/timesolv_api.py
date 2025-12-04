'''
TimeSolv API Client
A Python client for interacting with the TimeSolv API.
'''

import requests
import os
import sys
from datetime import datetime, timedelta
from typing import List, Dict, Set, Optional

class TimeSolvAPIError(Exception):
    '''Custom exception for TimeSolv API errors.'''
    pass

class TimeSolvAuth:
    '''Handles authentication for TimeSolv API.'''

    def __init__(self, api_key: str):
        pass
    
    # POST
    def get_access_token(self):
        '''Authenticate and return an access token.'''
        pass

class TimeSolvAPI:
    '''Client for TimeSolv API.'''

    def __init__(self, config_data: Dict):
        access_token = self._get_access_token(config_data)
        
        self.headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }

    # Helper
    def _get_access_token(self, config_data: Dict) -> str:
        '''Retrieve access token for initialization.'''
        # Normalize keys to lowercase
        config_data_lower = {k.lower(): v for k, v in config_data.items()}

        if config_data_lower.get('client_id') and config_data_lower.get('client_secret') and config_data_lower.get('code') and config_data_lower.get('redirect_uri'):
            access_data = {
                'client_id': config_data_lower['client_id'],
                'client_secret': config_data_lower['client_secret'],
                'grant_type': 'authorization_code',
                'code': config_data_lower['code'],
                'redirect_uri': config_data_lower['redirect_uri']
            }

            # TODO: Call _request helper instead
            response = requests.post('https://apps.timesolv.com/Services/rest/oAuth2V1/Token', data=access_data)
            token_data = response.json()

            if token_data.get("error"):
                raise TimeSolvAPIError(f"Error obtaining access token: {token_data['error_description']}")

            return token_data['access_token']

        raise TimeSolvAPIError("Missing required authentication parameters.")
    
    # Helper
    def _request(self, method: str):
        '''Make a request to the TimeSolv API.'''
        pass
    
    # POST
    def get_firm_users(self) -> List[Dict]:
        '''Retrieve a list of firm users.'''
        pass
    
    # POST
    def get_timecards(self) -> List[Dict]:
        '''Retrieve a list of timecards.'''
        pass

