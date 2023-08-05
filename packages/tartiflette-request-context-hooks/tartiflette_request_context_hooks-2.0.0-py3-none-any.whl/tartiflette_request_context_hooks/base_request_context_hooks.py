from abc import ABCMeta, abstractmethod
from .exceptions import RequestNotSetException, RequestDataNotStoredException


class BaseRequestContextHooks(metaclass=ABCMeta):
    _lib_label = 'ttfhooks'

    def __init__(self):
        """
        Performs actions to be done during setup of the application for later
        access by the the hooks. E.g. initialising factories.
        """
        self._request = None
        self._handler = None

    @property
    @abstractmethod
    def label(self, label):
        """
        Must not match anything that is an existing aiohttp request property
        """

    @property
    def _ns_label(self):
        return self._lib_label + '-' + self.label

    @property
    def request(self):
        return self._request

    @request.setter
    def request(self, value):
        self._request = value

    @property
    def handler(self):
        return self._handler

    @handler.setter
    def handler(self, value):
        self._handler = value

    @abstractmethod
    async def __aenter__(self):
        """
        Performs actions to be done on set up of the request.
        Must call self.store_request_data with the computed data
        """

    @abstractmethod
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """
        Performs actions to be done on tear down of the request.

        Retrieve relevant data with get_request_data and perform close actions
        on that.
        """

    async def __call__(self, *args, **kwargs):
        """
        Provides the value to be used in the resolver
        """
        return await self.get_request_data()

    async def store_request_data(self, data):
        self._request[self._ns_label] = data

    async def get_request_data(self):
        if not self._request:
            raise RequestNotSetException
        try:
            data = self._request[self._ns_label]
        except KeyError:
            raise RequestDataNotStoredException
        return data
