from typing import Iterable
import requests

from core.logging import LOG

async def async_iter(loop: Iterable):
    for i in loop:
        yield i
