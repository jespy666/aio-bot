from aiogram.types import Document

from bot import exceptions as e

from config import config


def validate_input_file(document: Document) -> None:
    if not document:
        raise e.EmptyDocumentError


def validate_size(size: str, model: str) -> None:
    if size not in config.IMAGE_SIZES[model]:
        raise e.IncorrectImageSizeError
