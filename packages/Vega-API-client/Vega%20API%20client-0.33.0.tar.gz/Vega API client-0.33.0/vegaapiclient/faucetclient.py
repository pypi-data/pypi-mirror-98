import requests


class FaucetClient(object):
    def __init__(self, url: str) -> None:
        self.url = url

        self._httpsession = requests.Session()

    def mint(self, amount: int, asset: str, party: str) -> requests.Response:
        """
        Mint tokens and allocate them to a party (pubkey).
        """
        req = {"amount": amount, "asset": asset, "party": party}
        url = f"{self.url}/api/v1/mint"
        return self._httpsession.post(url, json=req)
