from aiohttp import ClientSession, ClientResponse, BasicAuth


class Auth:
    """Class to make authenticated requests."""

    def __init__(self, websession: ClientSession, host: str, user: str, password: str):
        """Initialize the auth."""
        self.websession = websession
        self.host = host
        self._auth = BasicAuth(user, password)

    async def request(self, path: str) -> ClientResponse:
        """Make a request."""

        return await self.websession.request(
            "GET",
            f"{self.host}/{path}",
            auth=self._auth,
        )
