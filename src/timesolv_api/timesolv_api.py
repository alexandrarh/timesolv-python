'''
TimeSolv API Client
A Python client for interacting with the TimeSolv API.
'''

import requests
import os
import sys
from datetime import datetime, timedelta
from typing import List, Dict, Set, Optional
from urllib.parse import urljoin

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

    def __init__(self, config_data: Dict, base_url: str='https://apps.timesolv.com/Services/rest/oAuth2V1/'):
        self.base_url = base_url
        self.access_token = self._get_access_token(config_data)
        self.headers = {
            "Authorization": f"Bearer {self.access_token}",
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
            token_data = self._request('POST', 'Token', payload=access_data)
            return token_data['access_token']
            
            # token_data = response.json()

            # if token_data.get("error"):
            #     raise TimeSolvAPIError(f"Error obtaining access token: {token_data['error_description']}")

        raise TimeSolvAPIError("Missing required authentication parameters.")
    
    # Helper
    def _request(self, method: str, endpoint: str, payload: Optional[Dict]=None, **kwargs) -> List[Dict]:
        '''Make a request to the TimeSolv API.'''
        full_url = urljoin(self.base_url, endpoint)

        try:
            response = requests.request(method, full_url, headers=self.headers, json=payload, **kwargs)       # Add timeout parameter if needed; also unsure of kwargs
            response.raise_for_status()
            return response.json()
        except requests.HTTPError as e:
            raise TimeSolvAPIError(f"HTTP error occurred: {e} - Response: {response.text}")
        except requests.RequestException as e:
            raise TimeSolvAPIError(f"Error making request to {full_url}: {e}")
        except ValueError as e:
            raise TimeSolvAPIError(f"Error parsing JSON response from {full_url}: {e}")
    
    # POST
    def get_firm_users(self) -> List[Dict]:
        '''Retrieve a list of firm users.'''
        pass
    
    # POST
    def get_timecards(self) -> List[Dict]:
        '''Retrieve a list of timecards.'''
        pass

