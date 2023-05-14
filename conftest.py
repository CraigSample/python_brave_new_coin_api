'''
Pytest fixtures for the test suite.
'''
import json
import logging

import pytest
import requests

from . import brave_new_coin_api
from support import constants

LOGGER = logging.getLogger(__name__)


@pytest.fixture(name='access_token_dict', scope='session')
def fixture_get_access_token() -> dict:
    '''
    Get an initial BraveNewCoin OAuth 2.0 Access Token from /oauth/token.

    Returns:
        dict: A dictionary returned by the oauth/token endpoint.
    '''
    payload_dict = {
        'audience': constants.BNC_AUDIENCE,
        'client_id': constants.BNC_CLIENT_ID,
        'grant_type': "client_credentials"
    }

    response = brave_new_coin_api.post_get_token(200, payload_dict)

    response_json = response.json()
    LOGGER.debug('response_json: %s', json.dumps(response_json, indent=2))
    yield response_json


@pytest.fixture(name='session')
def fixture_session(access_token_dict):
    '''
    This fixture will provide the default requests session used by *most* of the endpoints.

    Args:
        access_token_dict (fixture): The session scoped access_token fixture.

    Yields:
        requests.sessions.Session: The requests session.
    '''
    request = requests.Session()

    request.headers.update({
        'Authorization': 'Bearer ' + access_token_dict['access_token'],
        'X-RapidAPI-Key': constants.BNC_KEY,
        'X-RapidAPI-Host': constants.BNC_HOST
    })
    yield request
    request.close()
