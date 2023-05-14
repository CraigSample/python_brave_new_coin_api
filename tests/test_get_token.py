'''
Basic tests for the GET /oauth/token endpoint.
'''
import logging

from pytest import mark

from helpers import brave_new_coin_api
from support import constants, validations

LOGGER = logging.getLogger(__name__)

@mark.regression
@mark.token
@mark.token_1
def test_get_token_01():
    '''
    Test the POST GetToken endpoint with a proper payload.
    '''
    payload_dict = {
        'audience': constants.BNC_AUDIENCE,
        'client_id': constants.BNC_CLIENT_ID,
        'grant_type': "client_credentials"
    }

    response = brave_new_coin_api.post_get_token(200, payload_dict)
    response_json = response.json()

    access_token = response_json["access_token"]
    assert access_token is not None, 'The access_token is not populated.'
    assert validations.validate_access_token(access_token), 'The access_token is not a valid ' \
        'OAuth 2.0 token.'
    assert response_json['token_type'] == 'Bearer', 'The token_type is expected to be ' \
        f"'Bearer'. Found: {response_json['token_type']!a}."
    assert isinstance(response_json['expires_in'], int), 'The expires_in is expected to be' \
         f"type 'int'. Found: {type(response_json['expires_in'])!a}."
    assert response_json['expires_in'] < 86400

@mark.regression
@mark.token
@mark.negative
@mark.token_2
def test_get_token_02():
    '''
    Test the POST GetToken endpoint with an incorrect payload: missing key.
    '''
    payload_dict = {
        'audience': constants.BNC_AUDIENCE,
        'client_id': constants.BNC_CLIENT_ID
    }

    response = brave_new_coin_api.post_get_token(400, payload_dict)
    assert response.reason == 'Bad Request', 'The response.reason is expected to be ' \
        f"'Bad Request'. Found: {response.reason!a}."


@mark.regression
@mark.token
@mark.negative
@mark.token_3
def test_get_token_03():
    '''
    Test the POST GetToken endpoint with an incorrect payload: incorrect key value.
    '''
    payload_dict = {
        'audience': constants.BNC_AUDIENCE,
        'client_id': constants.BNC_CLIENT_ID,
        'grant_type': "client_credentials2"
    }

    response = brave_new_coin_api.post_get_token(403, payload_dict)

    assert response.reason == 'Forbidden', 'The response.reason is expected to be ' \
        f"'Forbidden'. Found: {response.reason!a}."
