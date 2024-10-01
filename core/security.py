from fastapi import Header, HTTPException
import os

API_KEY = os.getenv("API_KEY")

async def api_key_required(api_key: str = Header(...)):
    if api_key != API_KEY:
        raise HTTPException(status_code=403, detail="Could not validate credentials")
