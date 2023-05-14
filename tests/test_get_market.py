'''
Basic tests for the GET /market endpoint.
'''
import json
import logging

from pytest import mark

from helpers import brave_new_coin_api
from support import constants, validations

LOGGER = logging.getLogger(__name__)


@mark.regression
@mark.market
def test_get_market_01(session):
    '''
    Test the GET /market endpoint with no parameters.

    Args:
        session (fixture): The requests session fixture.
    '''

    response = brave_new_coin_api.get_market(session, 200)
    response_json = response.json()
    LOGGER.debug('response_json: %s', json.dumps(response_json, indent=2)[:1500])

    validations.validate_get_market(response_json)


@mark.regression
@mark.market
def test_get_market_02(session):
    '''
    Test the GET /market endpoint with the baseAssetId parameter.

    Args:
        session (fixture): The requests session fixture.
    '''
    base_asset_id = constants.BTC_ASSET_ID

    response = brave_new_coin_api.get_market(session, 200, base_asset_id=base_asset_id)
    response_json = response.json()
    LOGGER.debug('response_json: %s', json.dumps(response_json, indent=2)[:1500])

    validations.validate_get_market(response_json)
    for entry in response_json['content']:
        assert entry['baseAssetId'] == base_asset_id, 'The returned entry expected to ' + \
            f"have baseAssetId {base_asset_id!a}. Found: {json.dumps(entry, indent=2)}"


@mark.regression
@mark.market
def test_get_market_03(session):
    '''
    Test the GET /market endpoint with the quoteAssetId parameter.

    Args:
        session (fixture): The requests session fixture.
    '''
    quote_asset_id = constants.USD_ASSET_ID

    response = brave_new_coin_api.get_market(session, 200, quote_asset_id=quote_asset_id)
    response_json = response.json()
    LOGGER.debug('response_json: %s', json.dumps(response_json, indent=2)[:1500])

    validations.validate_get_market(response_json)
    for entry in response_json['content']:
        assert entry['quoteAssetId'] == quote_asset_id, 'The returned entry expected to ' + \
            f"have quoteAssetId {quote_asset_id!a}. Found: {json.dumps(entry, indent=2)}"


@mark.regression
@mark.market
def test_get_market_04(session):
    '''
    Test the GET /market endpoint with the baseAssetId and quoteAssetId parameters.

    Args:
        session (fixture): The requests session fixture.
    '''
    base_asset_id = constants.BTC_ASSET_ID
    quote_asset_id = constants.USD_ASSET_ID

    response = brave_new_coin_api.get_market(session,
                                              200,
                                              base_asset_id=base_asset_id,
                                              quote_asset_id=quote_asset_id)
    response_json = response.json()
    LOGGER.debug('response_json: %s', json.dumps(response_json, indent=2)[:1500])

    validations.validate_get_market(response_json)
    for entry in response_json['content']:
        assert entry['baseAssetId'] == base_asset_id, 'The returned entry expected to ' + \
            f"have baseAssetId {base_asset_id!a}. Found: {json.dumps(entry, indent=2)}"
        assert entry['quoteAssetId'] == quote_asset_id, 'The returned entry expected to ' + \
            f"have quoteAssetId {quote_asset_id!a}. Found: {json.dumps(entry, indent=2)}"


@mark.regression
@mark.market
@mark.negative
def test_get_market_05(session):
    '''
    Test the GET /market endpoint with an invalid baseAssetId parameter.

    Args:
        session (fixture): The requests session fixture.
    '''
    base_asset_id = 'BOGUS'

    response = brave_new_coin_api.get_market(session, 400, base_asset_id=base_asset_id)
    response_json = response.json()
    LOGGER.debug('response_json: %s', json.dumps(response_json, indent=2)[:1500])

    assert response_json['status'] == 'BAD_REQUEST', 'The returned response was expected to ' + \
        f"have status 'BAD_REQUEST'. Found: {response_json['status']!a}."

@mark.regression
@mark.market
@mark.negative
def test_get_market_06(session):
    '''
    Test the GET /market endpoint with an unknown to the system baseAssetId parameter.

    Args:
        session (fixture): The requests session fixture.
    '''
    base_asset_id = constants.UNKNOWN_ASSET_ID

    response = brave_new_coin_api.get_market(session, 200, base_asset_id=base_asset_id)
    response_json = response.json()
    LOGGER.debug('response_json: %s', json.dumps(response_json, indent=2)[:1500])

    assert len(response_json) == 0, 'The number of returned results is expected to be 0. ' + \
        f'Found: {len(response_json)}.'

@mark.regression
@mark.market
@mark.negative
def test_get_market_07(session):
    '''
    Test the GET /market endpoint with an invalid quote_asset_id parameter.

    Args:
        session (fixture): The requests session fixture.
    '''
    quote_asset_id = 'BOGUS'

    response = brave_new_coin_api.get_market(session, 400, quote_asset_id=quote_asset_id)
    response_json = response.json()
    LOGGER.debug('response_json: %s', json.dumps(response_json, indent=2)[:1500])

    assert response_json['status'] == 'BAD_REQUEST', 'The returned response was expected to ' + \
        f"have status 'BAD_REQUEST'. Found: {response_json['status']!a}."

@mark.regression
@mark.market
@mark.negative
def test_get_market_08(session):
    '''
    Test the GET /market endpoint with an unknown to the system baseAssetId parameter.

    Args:
        session (fixture): The requests session fixture.
    '''
    base_asset_id = constants.UNKNOWN_ASSET_ID

    response = brave_new_coin_api.get_market(session, 200, base_asset_id=base_asset_id)
    response_json = response.json()
    LOGGER.debug('response_json: %s', json.dumps(response_json, indent=2)[:1500])

    assert len(response_json) == 0, 'The number of returned results is expected to be 0. ' + \
        f'Found: {len(response_json)}.'

@mark.regression
@mark.market
@mark.negative
def test_get_market_09(session):
    '''
    Test the GET /market endpoint with an unknown to the system quoteAssetId parameter.

    Args:
        session (fixture): The requests session fixture.
    '''
    quote_asset_id = constants.UNKNOWN_ASSET_ID

    response = brave_new_coin_api.get_market(session, 200, quote_asset_id=quote_asset_id)
    response_json = response.json()
    LOGGER.debug('response_json: %s', json.dumps(response_json, indent=2)[:1500])

    assert len(response_json) == 0, 'The number of returned results is expected to be 0. ' + \
        f'Found: {len(response_json)}.'
