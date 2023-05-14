'''
Constant variables common to test suite.
'''
import hyperlink

# Ideally the BNC_ values would be stored in a keyvault.
BNC_URL = hyperlink.parse('https://bravenewcoin.p.rapidapi.com')
BNC_AUDIENCE = 'https://api.bravenewcoin.com'
BNC_CLIENT_ID = 'oCdQoZoI96ERE9HY3sQ7JmbACfBf55RY'
BNC_HOST = 'bravenewcoin.p.rapidapi.com'
# See https://rapidapi.com/BraveNewCoin/api/bravenewcoin/pricing for a valid API key.
BNC_KEY = '18e0320fb8msh591358e90b4ed56p1a8e84jsn774229aa559f'

BTC_ASSET_ID = 'f1ff77b6-3ab4-4719-9ded-2fc7e71cff1f'
UNKNOWN_ASSET_ID = '4c486ca3-1ee3-4f9c-83a2-748c5852065a'
USD_ASSET_ID = 'e77b9824-126a-418e-a69c-a2e682578e94'

SESSION_TIMEOUT = 120
UUID_REGEX = '[0-9a-f]{8}-[0-9a-f]{4}-[0-5][0-9a-f]{3}-[089ab][0-9a-f]{3}-[0-9a-f]{12}'
