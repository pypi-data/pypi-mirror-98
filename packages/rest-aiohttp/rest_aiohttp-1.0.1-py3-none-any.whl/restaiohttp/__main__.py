import aiohttp

from restaiohttp.serializers import Serializer


class API:
    """
    Generic API class for sending async HTTP requests
    """

    def __init__(self, url, format=None, session=None, serializer=None, session_kwargs=None):
        """
        API class initializer
        :param url: Request url
        :param format: serializer format
        :param session: AIOHttp Client Session
        :param serializer: Serializer class
        :param session_kwargs: AIOHttp Client Session kwargs
        """

        self.url = url
        self.format = format if format is not None else 'json'

        if serializer is None:
            self.serializer = Serializer(default=format)

        if not session_kwargs:
            session_kwargs = {}

        if session is None:
            self.session = aiohttp.ClientSession(**session_kwargs)

    async def _request(self, method, data=None, headers=None):
        """
        Generic method for sending async request
        :param method: HTTP request name
        :param data: Payload for sending
        :param headers: HTTP request headers
        :return: serialized response content
        """

        _headers = {'accept': self.serializer.get_content_type()}

        data = {} if data is None else self.serializer.dumps(data)

        if headers:
            _headers.update(headers)

        response = await self.session.request(method, self.url, data=data, headers=_headers, ssl=False)

        content = await response.read()
        content = self.serializer.loads(content)
        return content

    async def get(self, headers=None, **kwargs):
        """
        ASYNC HTTP GET request
        :param headers: Request headers
        :param kwargs: Additional params
        :return: Serialized response content
        """
        return await self._request('GET', headers=headers)

    async def post(self, data=None, headers=None, **kwargs):
        """
        ASYNC HTTP POST request
        :param data: Provided payload
        :param headers: Request headers
        :param kwargs: Additional params
        :return: Serialized response content
        """
        return await self._request('POST', data=data, headers=headers)

    async def patch(self, data=None, headers=None, **kwargs):
        """
        ASYNC HTTP PATCH request
        :param data: Provided payload
        :param headers: Request headers
        :param kwargs: Additional params
        :return: Serialized response content
        """
        return await self._request('PATCH', data=data, headers=headers)

    async def put(self, data=None, headers=None, **kwargs):
        """
        ASYNC HTTP PUT request
        :param data: Provided payload
        :param headers: Request headers
        :param kwargs: Additional params
        :return: Serialized response content
        """
        return await self._request('PUT', data=data, headers=headers)

    async def delete(self, headers=None, **kwargs):
        """
        ASYNC HTTP DELETE request
        :param headers: Request headers
        :param kwargs: Additional params
        :return: Serialized response content
        """
        return await self._request('DELETE', headers=headers)

    async def __aenter__(self):
        """
        Asyncio with enter
        """
        return self

    async def __aexit__(self, exc_type, exc, tb):
        """
        Asyncio with exit
        """
        await self.close()

    async def close(self):
        """
        Close underlying session
        """
        await self.session.close()
