import re
import requests

from bs4 import BeautifulSoup
from bs4.element import PageElement

from bot import exceptions as e


class CurrencyParser:

    def __init__(self, url: str) -> None:
        self.url = url

    async def _get_response(self) -> str:
        response = requests.get(self.url)
        if response.status_code == 200:
            return response.content
        raise e.CurrencyLoadError

    @staticmethod
    def _get_clean_value(currency: str) -> float:
        value = re.sub(r'[₽$€£]', '', currency).replace(
            ',', '.'
        )
        return float(value)

    @staticmethod
    def convert_to_dollars(amount: float, rate: float) -> float:
        if amount <= 0.001:
            return amount
        return amount / rate

    @staticmethod
    def convert_to_roubles(amount: float, rate: float) -> float:
        return round(amount * rate, 2)

    async def get_rate(self, name: str, class_: str) -> float:
        response: str = await self._get_response()
        soup = BeautifulSoup(response, 'html.parser')
        element: PageElement = soup.find(name, class_=class_)
        currency: str = element.get_text(strip=True)
        value: float = self._get_clean_value(currency)
        return value
