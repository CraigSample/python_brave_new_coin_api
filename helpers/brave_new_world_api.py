'''
Helper file for the BraveNewCoin API.
See: https://rapidapi.com/BraveNewCoin/api/bravenewcoin
'''
# pylint: disable=too-many-arguments
import json
import logging
from uuid import uuid4 as uuid

import requests

from support import constants

LOGGER = logging.getLogger(__name__)


def get_asset(session: requests.sessions.Session,
              expected_response: int,
              symbol: str = None,
              status: str = None,
              asset_type: str = None) -> requests.models.Response:
    '''
    Perform a GET on /asset. Return the response.

    Args:
      session (requests.sessions.Session): The requests session to use.
      expected_response (int): The expected response code.
      symbol (str, optional): Only return assets which have a particular ticker symbol e.g. BTC.
        Defaults to None.
      status (str, optional): ACTIVE or INACTIVE. Only return assets which have the particular
        status. Defaults to None, which defaults to the internal value of ACTIVE.
      type (str, optional): CRYPTO or FIAT. Only return assets of the particular type.
        Defaults to None.

    Returns:
      requests.models.Response: The response of the call.
    '''

    url = constants.BNC_URL.child('asset')

    if symbol:
        LOGGER.debug('AIEE!')
        url = url.set('symbol', symbol)
    if status:
        url = url.set('status', status)
    if asset_type:
        url = url.set('type', asset_type)

    LOGGER.info('Perform GET on %s...', url.to_text())
    response = session.get(url.to_text(),
                           timeout=constants.SESSION_TIMEOUT)
    assert response.status_code == expected_response, 'Error: Expected response code ' \
        f'{expected_response}. Received: {response.status_code} {response.reason!a}'
    return response


def get_asset_by_id(session: requests.sessions.Session,
                    expected_response: int,
                    asset_id: uuid) -> requests.models.Response:
    '''
    Perform a GET on /asset/{id}. Return the response.

    Args:
      session (requests.sessions.Session): The requests session to use.
      expected_response (int): The expected response code.
      asset_id (uuid): The unique resource identifier of an asset.

    Returns:
      requests.models.Response: The response of the call.
    '''

    url = constants.BNC_URL.child('asset', asset_id)

    LOGGER.info('Perform GET on %s...', url.to_text())

    response = session.get(url.to_text(),
                           timeout=constants.SESSION_TIMEOUT)
    assert response.status_code == expected_response, 'Error: Expected response code ' \
        f'{expected_response}. Received: {response.status_code} {response.reason!a}'
    return response


def get_asset_ticker(session: requests.sessions.Session,
                     expected_response: int,
                     asset_id: uuid,
                     percent_change: bool = False) -> requests.models.Response:
    '''
    Perform a GET on /market-cap. Return the response.

    Args:
      session (requests.sessions.Session): The requests session to use.
      expected_response (int): The expected response code.
      asset_id (uuid): The unique resource identifier of an asset.
      percent_change (bool, optional): When true the percentage changes in the price and 24 hour
        volume across 1, 7 and 30 days will be included in the response payload. Defaults to False.

    Returns:
      requests.models.Response: The response of the call.
    '''

    url = constants.BNC_URL.child('market-cap')

    url = url.set('assetId', asset_id)
    if percent_change:
        url = url.set('percentChange', percent_change)

    LOGGER.info('Perform GET on %s...', url.to_text())

    response = session.get(url.to_text(),
                           timeout=constants.SESSION_TIMEOUT)
    assert response.status_code == expected_response, 'Error: Expected response code ' \
        f'{expected_response}. Received: {response.status_code} {response.reason!a}'
    return response


def get_daily_ohlcv(session: requests.sessions.Session,
                    expected_response: int,
                    start_after: uuid = None,
                    size: int = None,
                    index_id: uuid = None,
                    timestamp: str = None,
                    index_type: str = None) -> requests.models.Response:
    '''
    Perform a GET on /ohlcv. Return the response.

    Args:
      session (requests.sessions.Session): The requests session to use.
      expected_response (int): The expected response code.
      start_after (uuid, optional):   Retrieve OHLCV for the indexId or indexType required,
        starting after this particular record id. Every record in the dataset has a universal
        identifier (UUID). This parameter provides for pagination through large selections
        since every response includes a nextId that can be used here. Defaults to None.
      size (int, optional): Integer 1 to 2000. The maximum size to return in the result set up to
        the overall limit of 2000. This parameter is ignored if no timestamp is provided. Otherwise,
        since records are in reverse data order, use in conjunction with timestamp to make
        selections back in time. Defaults to None, which defaults to the internal value of 10.
      index_id (uuid, optional): Retrieve all the OHLCV values for a particular asset or market by
        its id. The index id is a universal identifier (UUID) that will differ based on the index
        type. Defaults to None.
      timestamp (str, optional): Retrieve all daily OHLCV records up to the timestamp provided. All
        dates are stored in UTC. Timestamp strings should be in the form YYYY-MM-DDThh:mm:ssZ.
        Defaults to None.
      index_type (str, optional): Restrict the OHLCV results to the index type. Either MWA or GWA.
        Defaults to None.

    Returns:
      requests.models.Response: The response of the call.
    '''

    url = constants.BNC_URL.child('ohlcv')
    if start_after:
        url = url.set('startAfter', str(start_after))
    if size:
        url = url.set('size', str(size))
    if index_id:
        url = url.set('indexId', str(index_id))
    if timestamp:
        url = url.set('timestamp', timestamp)
    if index_type:
        url = url.set('indexType', index_type)

    LOGGER.info('Perform GET on %s...', url.to_text())

    response = session.get(url.to_text(),
                           timeout=constants.SESSION_TIMEOUT)
    assert response.status_code == expected_response, 'Error: Expected response code ' \
        f'{expected_response}. Received: {response.status_code} {response.reason!a}'
    return response


def get_market(session: requests.sessions.Session,
               expected_response: int,
               base_asset_id: uuid = None,
               quote_asset_id: uuid = None) -> requests.models.Response:
    '''
    Perform a GET on /market. Return the response.

    Args:
      session (requests.sessions.Session): The requests session to use.
      expected_response (int): The expected response code.
      base_asset_id (str, optional): Only return markets which contain the asset id on the base
        side of the market.
      quote_asset_id (str, optional):Only return markets which contain the asset id on the quote
        side of the market.

    Returns:
      requests.models.Response: The response of the call.
    '''

    url = constants.BNC_URL.child('market')

    if base_asset_id:
        url = url.set('baseAssetId', base_asset_id)

    if quote_asset_id:
        url = url.set('quoteAssetId', quote_asset_id)

    LOGGER.info('Perform GET on %s...', url.to_text())

    response = session.get(url.to_text(),
                           timeout=constants.SESSION_TIMEOUT)
    assert response.status_code == expected_response, 'Error: Expected response code ' \
        f'{expected_response}. Received: {response.status_code} {response.reason!a}'
    return response


def get_market_by_id(session: requests.sessions.Session,
                     expected_response: int,
                     market_id: uuid) -> requests.models.Response:
    '''
    Perform a GET on /market/{id}. Return the response.

    Args:
      session (requests.sessions.Session): The requests session to use.
      expected_response (int): The expected response code.
      market_id (uuid): The unique resource identifier of a market.

    Returns:
      requests.models.Response: The response of the call.
    '''

    url = constants.BNC_URL.child('market', market_id)

    LOGGER.info('Perform GET on %s...', url.to_text())

    response = session.get(url.to_text(),
                           timeout=constants.SESSION_TIMEOUT)
    assert response.status_code == expected_response, 'Error: Expected response code ' \
        f'{expected_response}. Received: {response.status_code} {response.reason!a}'
    return response


def post_get_token(expected_response: int, payload: dict) -> requests.models.Response:
    '''
    Perform a POST on /oauth/token. Return the response.

    Args:
      expected_response (int): The expected response code.
      payload (dict): The payload to pass for the endpoint.

    Returns:
        requests.models.Response: The response of the call.
    '''

    url = constants.BNC_URL.child('oauth', 'token')

    LOGGER.info('Perform POST on %s with payload %s...',
                url.to_text(), json.dumps(payload, indent=2))

    headers = {
        'content-type': 'application/json',
        'X-RapidAPI-Key': constants.BNC_KEY,
        'X-RapidAPI-Host': constants.BNC_HOST
    }

    response = requests.post(url.to_text(),
                             headers=headers,
                             json=payload,
                             # Kill the child if it runs for more than 2 minutes.
                             timeout=2 * 60,)
    assert response.status_code == expected_response, 'Error: Expected response code ' \
        f'{expected_response}. Received: {response.status_code} {response.reason!a}'
    return response
