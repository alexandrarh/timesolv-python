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
        config_data_lower = {k.lower(): v for k, v in config_data.items()}          # Normalize keys to lowercase

        if config_data_lower.get('client_id') and config_data_lower.get('client_secret') and config_data_lower.get('auth_code') and config_data_lower.get('redirect_uri'):
            access_data = {
                'client_id': config_data_lower['client_id'],
                'client_secret': config_data_lower['client_secret'],
                'grant_type': 'authorization_code',
                'code': config_data_lower['auth_code'],
                'redirect_uri': config_data_lower['redirect_uri']
            }

            token_data = self._request('POST', 'Token', payload=access_data)
            return token_data['access_token']

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
    
    def get_firm_users(self) -> List[Dict]:
        """
        Retrieve a list of firm users.

        Returns:
        - List[Dict]: A list of firm users.
        """
        firm_users = []
        endpoint = 'firmUserSearch'
        page_size = 100
        page_number = 1

        while True:
            payload = {
                "OrderBy": "Id",
                "SortOrderAscending": 0,
                "PageSize": page_size,
                "PageNumber": page_number,
                "Criteria": [
                    {
                        "FieldName": "UserStatus",
                        "Operator": "=",
                        "Value": "Active"
                    }
                ]
            }

            response_data = self._request('POST', endpoint, payload=payload)

            # Extract user information
            users = response_data.get("FirmUsers", [])
            if not users:
                break

            # Append users to firm list
            firm_list.extend(users)

            if len(users) < page_size:
                break
            
            page_number += 1

        return firm_users
    
    def get_timecards(self, firm_user_id: int, start_date: str, end_date: str) -> List[Dict]:
        """
        Search for timecards within the specified date range.

        Args:
        - firm_user_id (int): The ID of the firm user whose timecards are to be searched.
        - start_date (str): The start date for the search (YYYY-MM-DD).
        - end_date (str): The end date for the search (YYYY-MM-DD).

        Returns:
        - A list of dictionaries containing timecard details.
        """

        user_timecards = []
        endpoint = 'timecardSearch'
        page_size = 100
        page_number = 1

        while True:
            payload = {
                "Criteria": [
                    {
                        "FieldName": "FirmUserId",
                        "Operator": "=",
                        "Value": firm_user_id
                    },
                    {
                        "FieldName": "Date",
                        "Operator": ">=",
                        "Value": start_date
                    },
                    {
                        "FieldName": "Date",
                        "Operator": "<=",
                        "Value": end_date
                    }
                ],
                "OrderBy": "Date",
                "SortOrderAscending": 1,
                "PageSize": page_size,
                "PageNumber": page_number
            }

            response_data = self._request('POST', endpoint, payload=payload)

            # Extract timecard information
            timecards = response_data.get("TimeCards", [])
            if not timecards:
                break

            # Append timecards to list
            user_timecards.extend(timecards)

            if len(timecards) < page_size:
                break
            
            page_number += 1

        return user_timecards