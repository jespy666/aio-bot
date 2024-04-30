class IncorrectModelError(Exception):
    pass


class InsufficientFundsError(Exception):
    pass


class IncorrectImageSizeError(Exception):
    pass


class IncorrectImageFormatError(Exception):
    pass


class AspectRatioMismatchError(Exception):
    pass


class UnknownQualityError(Exception):
    pass


class CurrencyLoadError(Exception):
    pass
