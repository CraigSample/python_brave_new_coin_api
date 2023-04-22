'''
A collection of helper methods related to test case validations.
'''
import json
import logging
import re
import time

from support import constants, datetime_utils, jwt_utils

LOGGER = logging.getLogger(__name__)


def is_uuid(candidate: str) -> bool:
    '''
    Check if the passed candidate is a valid UUID.

    Args:
        candidate (str): The string to validate.

    Returns:
        bool: Is the passed candidate a valid UUID?
    '''
    match = re.fullmatch(constants.UUID_REGEX,
                         candidate,
                         flags=re.IGNORECASE,
                         )
    return match is not None


def validate_access_token(access_token: str) -> bool:
    '''
    Validate that the given access_token.

    Args:
        access_token (str): The JWT access token to validate.

    Raises:
        ValueError: Invalid token type.

    Returns:
        bool: Is the given access_token a valid OAuth 2.0 token?
    '''
    try:
        decoded_token = jwt_utils.get_decoded_access_token(access_token)

        seconds_now = time.time()

        diff_seconds_to_iat = seconds_now - decoded_token['iat']
        diff_seconds_to_exp = decoded_token['exp'] - seconds_now
        LOGGER.debug('diff_seconds_to_iat: %s', diff_seconds_to_iat)
        LOGGER.debug('diff_seconds_to_exp: %s', diff_seconds_to_exp)
        iat_days, iat_hours, iat_minutes, iat_seconds = datetime_utils.convert_seconds_to_d_h_m_s(
            diff_seconds_to_iat)
        LOGGER.debug('iat_days %s, iat_hours %s, iat_minutes %s, iat_seconds %s',
                     iat_days, iat_hours, iat_minutes, iat_seconds)
        exp_days, exp_hours, exp_minutes, exp_seconds = datetime_utils.convert_seconds_to_d_h_m_s(
            diff_seconds_to_exp)
        LOGGER.debug('exp_days %s, exp_hours %s, exp_minutes %s, exp_seconds %s',
                     exp_days, exp_hours, exp_minutes, exp_seconds)
        assert iat_days < 1, 'The decoded token iat is expected to be less than one day. Found: ' \
            f"{decoded_token['iat']!a} seconds."
        assert exp_days < 1, 'The decoded token exp is expected to be less than one day. Found: ' \
            f"{decoded_token['ext']!a} seconds."
        assert decoded_token['azp'] == constants.BNC_CLIENT_ID, 'The decoded token azp is ' \
            f'expected to be the BNC client_id {constants.BNC_CLIENT_ID!a}. Found: ' \
            f"{decoded_token['azp']!a}."
        assert decoded_token['gty'] == 'client-credentials', 'The decoded token gty is ' \
            f"expected to be 'client-credentials'. Found: {decoded_token['gty']!a}."
        return True
    except ValueError as err:
        LOGGER.error('Error validating access token: %s: ', err)
    return False


def validate_get_asset(response_json: dict, num_expected_results: int = None) -> bool:
    '''
    Validate the results from the GET /asset endpoint.

    Args:
        response_json (dict): The json response from the endpoint.
        num_expected_results (int, optional): The number of expected results. Defaults to None,
            which will not check.

    Returns:
        bool: Are the results vaid?
    '''
    assert 'content' in response_json, "The response does not contain 'content' key."
    assert isinstance(response_json['content'],
                      list), "The 'content' key should have a list as value."
    if num_expected_results:
        assert len(response_json['content']) == num_expected_results, 'The number of entries ' + \
            f'in the content is expected to be {num_expected_results!a}. Found: ' \
            f"{len(response_json['content'])}."

    for entry in response_json['content']:
        assert 'id' in entry, "The entry does not contain 'id' key. Found: " + \
            f'{json.dumps(entry, indent=2)}.'
        assert is_uuid(entry['id']), f"The entry's id is not a valid UUID. Found: {entry['id']!a}"
        assert entry['status'] in ['ACTIVE', 'INACTIVE'], "The entry's status is expected to " + \
            f"be in 'ACTIVE', 'INACTIVE'. Found: {entry['status']}."
        assert entry['type'] in ['CRYPTO', 'FIAT'], "The entry's type is expected to be in " + \
            f"'CRYPTO', 'FIAT'. Found: {entry['type']}."
        assert isinstance(entry['name'], str), "The entry's name is expected to be a string. " + \
            f"Found: {entry['name']!a}  type: {type(entry['name'])}."
        assert isinstance(entry['symbol'], str), "The entry's symbol is expected to be a " + \
            f"string. Found: {entry['symbol']!a} type: {type(entry['symbol'])}."


def validate_get_market(response_json: dict, num_expected_results: int = None) -> bool:
    '''
    Validate the results from the GET /market endpoint.

    Args:
        response_json (dict): The json response from the endpoint.
        num_expected_results (int, optional): The number of expected results. Defaults to None,
            which will not check.

    Returns:
        bool: Are the results vaid?
    '''
    assert 'content' in response_json, "The response does not contain 'content' key."
    assert isinstance(response_json['content'],
                      list), "The 'content' key should have a list as value."
    if num_expected_results:
        assert len(response_json['content']) == num_expected_results, 'The number of entries ' + \
            f'in the content is expected to be {num_expected_results!a}. Found: ' \
            f"{len(response_json['content'])}"

    for entry in response_json['content']:
        assert 'id' in entry, "The entry does not contain 'id' key. Found: " + \
            f'{json.dumps(entry, indent=2)}.'
        assert is_uuid(entry['id']), f"The entry's id is not a valid UUID. Found: {entry['id']!a}."
        assert 'baseAssetId' in entry, "The entry does not contain 'baseAssetId' key. Found: " + \
            f'{json.dumps(entry, indent=2)}.'
        assert is_uuid(entry['baseAssetId']), "The entry's baseAssetId is not a valid UUID. " + \
            f"Found: {entry['baseAssetId']!a}."
        assert 'quoteAssetId' in entry, "The entry does not contain 'quoteAssetId' key. Found: " + \
            f'{json.dumps(entry, indent=2)}.'
        assert is_uuid(entry['quoteAssetId']), "The entry's quoteAssetId is not a valid UUID. " + \
            f"Found: {entry['quoteAssetId']!a}."
