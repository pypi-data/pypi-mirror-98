import csv
from datetime import datetime
from io import StringIO
from functools import wraps
import json
from typing import Dict, Union, List

import requests
import backoff

from .exceptions import CriteoAccountLostAccessException


class CriteoClient:
    """
    A Criteo client to help us request Criteo's REST API
    Usage:
    criteo_client = CriteoClient(criteo_client_secret_id, criteo_client_secret)
    advertisers = criteo_client.getAdvertisers()
    """

    def __init__(self, client_secret_id: str, client_secret: str):
        self._client_secret_id = client_secret_id
        self._client_secret = client_secret
        self.criteo_server_url = 'https://api.criteo.com/marketing'
        self.token = None

    @backoff.on_exception(backoff.expo, requests.exceptions.HTTPError, max_tries=5)
    def _make_request(self, endpoint: str, method: str, data: Union[Dict, str] = None, headers: Dict = None) -> requests.models.Response:
        """Send a request to criteo API"""
        response = requests.request(method=method, url=f"{self.criteo_server_url}{endpoint}", data=data, params=data, headers=headers)
        response.raise_for_status()
        return response

    def _authenticate(func):
        """Get the acccess token for Criteo API"""

        @wraps(func)
        def wrapper(self, *args, **kwargs):
            if self.token is None:
                reponse = self._make_request(
                    '/oauth2/token',
                    'POST',
                    {'client_id': self._client_secret_id, 'client_secret': self._client_secret, 'grant_type': 'client_credentials'},
                    {'content-type': "application/x-www-form-urlencoded"}
                    )
                self.token = reponse.json()['access_token']
            return func(self, *args, **kwargs)
        return wrapper

    @_authenticate
    def getAdvertisers(self) -> Dict:
        """Get advertisers data"""
        reponse = self._make_request(
            '/v1/portfolio',
            'GET',
            headers={'content-type': "application/json", 'Authorization': f"Bearer {self.token}"}
            )
        return reponse.json()

    @_authenticate
    def getCampaigns(self, advertiser_id: str) -> Dict:
        """Get specific campaigns data for an advertiser"""
        reponse = self._make_request(
            f'/v1/advertisers/{advertiser_id}/campaigns',
            'GET',
            headers={'content-type': "application/json", 'Authorization': f"Bearer {self.token}"}
            )
        return reponse.json()

    @_authenticate
    def download_report(self, advertiser_id: str, start_date: str, end_date: str,
                        report_type: str, dimensions: List[str], metrics: List[str], format: str = "Csv") -> bytes:
        """Download a statistics report"""
        stats_query = {
            "reportType": report_type,
            "advertiserIds": advertiser_id,
            "startDate": start_date,
            "endDate": end_date,
            "dimensions": dimensions,
            "metrics": metrics,
            "format": format
        }
        query_json = json.dumps(stats_query)
        reponse = self._make_request(
            '/v1/statistics',
            'POST',
            data=query_json,
            headers={'content-type': "application/json", 'Authorization': f"Bearer {self.token}"}
            )
        return reponse.content


def format_criteo_date_in_csv(criteo_report_string_with_headers: str,
                              column_to_change: str,
                              delimiter: str=';') -> str:
    """
    Transform criteo report csv to change date to adscale format.
    :returns: a csv with the valid date format.
    :raises: if column_to_change is not present in the header and the report is not empty
    """
    if not criteo_report_string_with_headers:
        return ''
    reader = csv.DictReader(StringIO(criteo_report_string_with_headers), delimiter=delimiter)
    if column_to_change not in reader.fieldnames:
        raise KeyError(f'column {column_to_change} that was supposedly in str is not present in csv. '
                       f'Are only valid {list(reader.fieldnames)}.')
    result_string_file = StringIO()
    writer = csv.DictWriter(result_string_file, reader.fieldnames, delimiter=delimiter)
    writer.writeheader()
    for row in reader:
        row.update({column_to_change: datetime.strptime(row[column_to_change], '%a %m/%d/%Y').strftime('%Y-%m-%d')})
        writer.writerow(row)
    return str(result_string_file.getvalue())


def check_access_account(client_secret_id: str, client_secret: str):
    "From client secret id and client secret, check if Arcane has access to it"
    criteo_client = CriteoClient(client_secret_id, client_secret)
    try:
        advertisers = criteo_client.getAdvertisers()
        if len(advertisers) == 0:
            raise CriteoAccountLostAccessException('There is no advertiser associated to the secret')
    except requests.exceptions.HTTPError as err:
        raise CriteoAccountLostAccessException( str(err) + '. You may not have sufficient authorization')
