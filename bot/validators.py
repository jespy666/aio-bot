from aiogram.types import Document

from PIL import Image

from bot import exceptions as e

from config import config


def validate_input_file(input_: Document) -> None:
    if not input_:
        raise e.IncorrectImageFormatError


def validate_size(size: str, model: str) -> None:
    if size not in config.IMAGE_SIZES[model]:
        raise e.IncorrectImageSizeError


def validate_image(path: str) -> None:
    with Image.open(path) as image:
        image_ext = image.format
        if not image_ext == 'PNG':
            raise e.IncorrectImageFormatError
        width = image.width
        height = image.height
        if not width == height:
            raise e.AspectRatioMismatchError


def validate_quality(quality: str) -> None:
    if quality not in ["standard", "hd"]:
        raise e.UnknownQualityError
