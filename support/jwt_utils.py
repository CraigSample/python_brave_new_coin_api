'''
A collection of helper methods related to JWT token manipulation.
'''
import json
import logging
from typing import Optional

import jwt

LOGGER = logging.getLogger(__name__)


def get_decoded_access_token(access_token: str) -> Optional[dict]:
    '''
    Decode the given JWT access token as a dict object. If an error occurs, return None.

    Args:
        access_token (str): The JWT access token to decode.

    Returns:
        Optional[dict]: The decoded JWT access token.
    '''
    try:
        decoded_token = jwt.decode(access_token, options={"verify_signature": False})
        LOGGER.debug('decoded_token: %s', json.dumps(decoded_token, indent=2))
        return decoded_token
    except jwt.exceptions.InvalidTokenError as err:
        LOGGER.error('Error decoding access token: %s: ', err)
    return None
