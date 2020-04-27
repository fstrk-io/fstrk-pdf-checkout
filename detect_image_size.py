import io
from dataclasses import dataclass

from PIL import Image

import requests


@dataclass
class ImageSize:
    width: int
    height: int


def detect(url: str) -> ImageSize:
    res = requests.get(url)
    with Image.open(io.BytesIO(res.content)) as img:
        width, height = img.size

    return ImageSize(width=width, height=height)
