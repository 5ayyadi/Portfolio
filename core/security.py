from fastapi import Header
from errors.error_schema import UnauthorizedAccess
import os

API_KEY = os.getenv("API_KEY")

async def api_key_required(api_key: str = Header(...)):
    if api_key != API_KEY:
        raise UnauthorizedAccess
