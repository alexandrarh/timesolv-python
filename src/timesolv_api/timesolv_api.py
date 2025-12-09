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

            token_data = self._request('POST', 'Token', data=access_data)
            return token_data['access_token']

        raise TimeSolvAPIError("Missing required authentication parameters.")
    
    # Helper -> check if need List[Dict] at all
    def _request(self, method: str, endpoint: str, **kwargs) -> List[Dict]:
        '''Make a request to the TimeSolv API.'''
        full_url = urljoin(self.base_url, endpoint)

        headers = kwargs['headers'] if 'headers' in kwargs else None 
        data = kwargs['data'] if 'data' in kwargs else None
        json = kwargs['json'] if 'json' in kwargs else None
        
        try:
            response = requests.request(method, full_url, headers=headers, json=json, data=data)       # Add timeout parameter if needed; also unsure of kwargs
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
                "SortOrderAscending": false,
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

            response_data = self._request('POST', endpoint, headers=self.headers, json=payload)

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
                "SortOrderAscending": true,
                "PageSize": page_size,
                "PageNumber": page_number
            }

            response_data = self._request('POST', endpoint, headers=self.headers, json=payload)

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

    def get_taskcodes(self) -> List[Dict]:
        """
        Retrieve a list of task codes.

        Returns:
        - List[Dict]: A list of task codes.
        """
        task_codes = []
        endpoint = 'taskcodeSearch'
        page_size = 100
        page_number = 1

        while True:
            payload = {
                "OrderBy": "Id",
                "SortOrderAscending": false,
                "PageSize": page_size,
                "PageNumber": page_number,
                "Criteria": [
                    {
                    "FieldName": "isActive",
                    "Operator": "=",
                    "Value": 1
                    }
                ]
            }

            response_data = self._request('POST', endpoint, headers=self.headers, json=payload)

            taskcode = response_data.get("TaskCodes", [])
            if not taskcode:
                break

            # Append task codes to list
            task_codes.extend(taskcode)

            if len(taskcode) < page_size:
                break
            
            page_number += 1

        return task_codes

    def get_abbreviations(self) -> List[Dict]:
        """
        Retrieve a list of abbreviations.

        Returns:
        - List[Dict]: A list of abbreviations.
        """
        abbreviations = []
        endpoint = 'abbreviationSearch'
        page_size = 100
        page_number = 1

        while True:
            payload = {
                "OrderBy": "Id",
                "SortOrderAscending": False,
                "PageSize": page_size,
                "PageNumber": page_number,
                "Criteria": [
                    {
                        "FieldName": "IsActive",
                        "Operator": "=",
                        "Value": 1
                    }
                ]
            }

            response_data = self._request('POST', endpoint, headers=self.headers, json=payload)

            abbreviations_page = response_data.get("Abbreviations", [])
            if not abbreviations_page:
                break

            # Append abbreviations to list
            abbreviations.extend(abbreviations_page)

            if len(abbreviations_page) < page_size:
                break
            
            page_number += 1

        return abbreviations

    def get_clients(self) -> List[Dict]:
        """
        Retrieve a list of clients.

        Returns:
        - List[Dict]: A list of clients.
        """
        clients = []
        endpoint = 'clientSearch'
        page_size = 100
        page_number = 1

        while True:
            payload = {
                "OrderBy": "Id",
                "SortOrderAscending": False,
                "PageSize": page_size,
                "PageNumber": page_number,
                "Criteria": [
                    {
                        "FieldName": "ClientStatus",
                        "Operator": "=",
                        "Value": "Active"
                    }
                ]
            }

            response_data = self._request('POST', endpoint, headers=self.headers, json=payload)

            clients_page = response_data.get("Clients", [])
            if not clients_page:
                break

            # Append clients to list
            clients.extend(clients_page)

            if len(clients_page) < page_size:
                break
            
            page_number += 1

        return clients

    