'''
Basic tests for the GET /asset endpoint.
'''
import json
import logging

from pytest import mark

from helpers import brave_new_coin_api
from support import validations

LOGGER = logging.getLogger(__name__)


@mark.regression
@mark.asset
def test_get_asset_01(session):
    '''
    Test the GET /asset endpoint with no parameters.

    Args:
        session (fixture): The requests session fixture.
    '''

    response = brave_new_coin_api.get_asset(session, 200)
    response_json = response.json()
    LOGGER.debug('response_json: %s', json.dumps(response_json, indent=2)[:1500])

    validations.validate_get_asset(response_json)


@mark.regression
@mark.asset
def test_get_asset_02(session):
    '''
    Test the GET /asset endpoint with the symbol parameter.

    Args:
        session (fixture): The requests session fixture.
    '''
    symbol = 'DOT'

    response = brave_new_coin_api.get_asset(session, 200, symbol=symbol)
    response_json = response.json()
    LOGGER.debug('response_json: %s', json.dumps(response_json, indent=2)[:1500])

    validations.validate_get_asset(response_json, num_expected_results=1)
    assert response_json['content'][0]['symbol'] == symbol, 'The returned entry expected to ' + \
        f"have symbol {symbol!a}. Found: {response_json['content'][0]['symbol']!a}."


@mark.regression
@mark.asset
def test_get_asset_03(session):
    '''
    Test the GET /asset endpoint with the status parameter.

    Args:
        session (fixture): The requests session fixture.
    '''
    status = 'INACTIVE'

    response = brave_new_coin_api.get_asset(session, 200, status=status)
    response_json = response.json()
    LOGGER.debug('response_json: %s', json.dumps(response_json, indent=2)[:1500])

    validations.validate_get_asset(response_json)
    for entry in response_json['content']:
        assert entry['status'] == status, 'The returned entry expected ' + \
            f"to have status {status!a}. Found: {entry['status']!a}."


@mark.regression
@mark.asset
def test_get_asset_04(session):
    '''
    Test the GET /asset endpoint with the type parameter.

    Args:
        session (fixture): The requests session fixture.
    '''
    asset_type = 'FIAT'

    response = brave_new_coin_api.get_asset(session, 200, asset_type=asset_type)
    response_json = response.json()
    LOGGER.debug('response_json: %s', json.dumps(response_json, indent=2)[:1500])

    validations.validate_get_asset(response_json)
    for entry in response_json['content']:
        assert entry['type'] == asset_type, 'The returned entry expected ' + \
            f"to have type {asset_type!a}. Found: {entry['type']!a}."


@mark.regression
@mark.asset
@mark.negative
def test_get_asset_05(session):
    '''
    Test the GET /asset endpoint with an invalid symbol parameter: unknown.

    Args:
        session (fixture): The requests session fixture.
    '''
    symbol = 'BOGUS'

    response = brave_new_coin_api.get_asset(session, 200, symbol=symbol)
    response_json = response.json()
    LOGGER.debug('response_json: %s', json.dumps(response_json, indent=2)[:1500])

    assert len(response_json) == 0, 'The number of returned results is expected to be 0. ' + \
        f'Found: {len(response_json)}.'


@mark.regression
@mark.asset
@mark.negative
def test_get_asset_06(session):
    '''
    Test the GET /asset endpoint with an invalid status parameter: unknown.

    Args:
        session (fixture): The requests session fixture.
    '''
    status = 'BOGUS'

    response = brave_new_coin_api.get_asset(session, 400, status=status)
    response_json = response.json()
    LOGGER.debug('response_json: %s', json.dumps(response_json, indent=2)[:1500])

    assert response_json['status'] == 'BAD_REQUEST', 'The returned response was expected to ' + \
        f"have status 'BAD_REQUEST'. Found: {response_json['status']!a}."


@mark.regression
@mark.asset
@mark.negative
def test_get_asset_07(session):
    '''
    Test the GET /asset endpoint with the type parameter: unknown.

    Args:
        session (fixture): The requests session fixture.
    '''
    asset_type = 'BOGUS'

    response = brave_new_coin_api.get_asset(session, 400, asset_type=asset_type)
    response_json = response.json()
    LOGGER.debug('response_json: %s', json.dumps(response_json, indent=2)[:1500])

    assert response_json['status'] == 'BAD_REQUEST', 'The returned response was expected to ' + \
        f"have status 'BAD_REQUEST'. Found: {response_json['status']!a}."

@mark.regression
@mark.asset
def test_get_asset_08(session):
    '''
    Test the GET /asset endpoint with an invalid symbol parameter: lower case.

    Args:
        session (fixture): The requests session fixture.
    '''
    symbol = 'btc'

    response = brave_new_coin_api.get_asset(session, 200, symbol=symbol)
    response_json = response.json()
    LOGGER.debug('response_json: %s', json.dumps(response_json, indent=2)[:1500])

    assert len(response_json) == 0, 'The number of returned results is expected to be 0. ' + \
        f'Found: {len(response_json)}.'


@mark.regression
@mark.asset
@mark.negative
def test_get_asset_09(session):
    '''
    Test the GET /asset endpoint with an invalid status parameter: lower case.

    Args:
        session (fixture): The requests session fixture.
    '''
    status = 'active'

    response = brave_new_coin_api.get_asset(session, 400, status=status)
    response_json = response.json()
    LOGGER.debug('response_json: %s', json.dumps(response_json, indent=2)[:1500])

    assert response_json['status'] == 'BAD_REQUEST', 'The returned response was expected to ' + \
        f"have status 'BAD_REQUEST'. Found: {response_json['status']!a}."


@mark.regression
@mark.asset
@mark.negative
def test_get_asset_10(session):
    '''
    Test the GET /asset endpoint with the type parameter: lower case.

    Args:
        session (fixture): The requests session fixture.
    '''
    asset_type = 'crypto'

    response = brave_new_coin_api.get_asset(session, 400, asset_type=asset_type)
    response_json = response.json()
    LOGGER.debug('response_json: %s', json.dumps(response_json, indent=2)[:1500])

    assert response_json['status'] == 'BAD_REQUEST', 'The returned response was expected to ' + \
        f"have status 'BAD_REQUEST'. Found: {response_json['status']!a}."
