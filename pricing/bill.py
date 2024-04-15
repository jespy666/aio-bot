import tiktoken

from utils import exceptions as e


class Bill:

    IMG_PRICES = {
        'standard': {
            '1024x1024': 0.050,
            '1024x1792': 0.090,
            '1792x1024': 0.090,
        },
        'hd': {
            '1024x1024': 0.090,
            '1024x1792': 0.150,
            '1792x1024': 0.150,
        }
    }

    TEXT_PRICES = {
        'input': 0.06,
        'output': 0.09,
    }

    def __init__(self, balance: float):
        self.balance = balance

    @staticmethod
    def calculate_tokens(text: str) -> int:
        encoding = tiktoken.get_encoding('cl100k_base')
        return len(encoding.encode(text))

    def get_net_balance(self, price: float) -> float:
        return self.balance - price


class ImageBill(Bill):

    def __init__(self, balance: float, size: str, quality: str):
        super().__init__(balance)
        self.size = size
        self.quality = quality

    def _get_image_bill(self) -> float:
        if self.IMG_PRICES.get(self.quality) is None:
            raise e.WrongSizeError
        if self.IMG_PRICES[self.quality].get(self.size) is None:
            raise e.WrongQualityError
        return self.IMG_PRICES[self.quality][self.size]

    def calculate(self) -> float:
        price: float = self._get_image_bill()
        net_balance = self.get_net_balance(price)
        return net_balance


class TextBill(Bill):

    def __init__(self, balance: float, input_: str, output_: str):
        super().__init__(balance)
        self.input = input_
        self.output = output_

    def _get_text_bill(self) -> float:
        input_tokens = self.calculate_tokens(self.input)
        output_tokens = self.calculate_tokens(self.output)
        input_price = (self.TEXT_PRICES['input'] * input_tokens) / 1000
        output_price = (self.TEXT_PRICES['output'] * output_tokens) / 1000
        return input_price + output_price

    def calculate(self) -> float:
        price: float = self._get_text_bill()
        net_balance = self.get_net_balance(price)
        return net_balance
