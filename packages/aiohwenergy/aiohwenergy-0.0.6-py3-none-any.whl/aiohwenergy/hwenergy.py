import logging

import aiohttp

from .device import Device
from .data import Data
from .errors import raise_error, RequestError, UnsupportedError

Logger = logging.getLogger(__name__)

SUPPORTED_API_VERSION = "v1"

SUPPORTED_DEVICES = [
    "HWE-P1",
    "SDM230-wifi",
    "SDM630-wifi",
]

class HomeWizardEnergy:
    """Communicate with a HomeWizard Energy device."""

    def __init__(self, host):
        Logger.debug("__init__ HomeWizardEnergy")
        self._host = host
        self._clientsession = self._get_clientsession()
        
        # Endpoints
        self.data = None
        self.device = None

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc, tb):
        await self.close()

    def _get_clientsession(self):
        """
        Get a clientsession that is tuned for communication with the Energy device
        """

        connector = aiohttp.TCPConnector(
            enable_cleanup_closed=True, # Home Assistant sets it so lets do it also
            limit_per_host=1, # Device can handle a limited amount of connections, only take what we need
        )

        return aiohttp.ClientSession(connector=connector)

    async def initialize(self):
        await self.update()

    async def update(self):
        Logger.debug("hwenergy update")
        status, response = await self.request('get', 'api')
        if status == 200 and response:
            if (response['api_version'] != SUPPORTED_API_VERSION):
                Logger.error("This library requires api to have version '%s'", SUPPORTED_API_VERSION)
                return
            self.device = Device(response, self.request)
            
            # if (self.device.product_type in SUPPORTED_DEVICES):
            status, data_response = await self.request('get', 'api/v1/data')
            if status == 200 and data_response:
                self.data = Data(data_response, self.request)
            else:
                Logger.error("Error getting data");
            # else:
            #     raise UnsupportedError(f"product_type {self.device.product_type} not supported")
        
    async def close(self):
        await self._clientsession.close()

    async def request(self, method, path, data=None):
        """Make a request to the API."""

        if self._clientsession.closed:
            # Avoid runtime errors when connection is closed.
            # This solves an issue when Updates were scheduled and HA was shutdown
            return None

        url = f'http://{self._host}/{path}'
        Logger.debug(f"URL: {url}")

        try:
            headers = {'Content-Type': 'application/json'}
            Logger.debug('%s, %s, %s' % (method, url, data))
            async with self._clientsession.request(method, url, json=data, headers=headers) as resp:
                Logger.debug('%s, %s' % (resp.status, await resp.text('utf-8')))

                data = None
                if resp.content_type == 'application/json':
                    data = await resp.json()
                                        
                return resp.status, data
        except aiohttp.client_exceptions.ClientError as err:
            raise RequestError(
                'Error requesting data from {}: {}'.format(self._host, err)
            ) from None


def _raise_on_error(data):
    """Check response for error message."""
    raise_error(data['error']['id'], data['error']["description"])
