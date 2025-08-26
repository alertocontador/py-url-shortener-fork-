from fastapi import APIRouter, HTTPException
from typing import Dict, Any

router = APIRouter()



@router.post("/short-key")

async def post_short_key():
    """
    TODO: Implement POST /short-key
    """
    raise HTTPException(status_code=501, detail={
        "error": "Not implemented",
        "endpoint": "POST /short-key"
    })



@router.post("/short-key/custom")

async def post_short_key_custom():
    """
    TODO: Implement POST /short-key/custom
    """
    raise HTTPException(status_code=501, detail={
        "error": "Not implemented",
        "endpoint": "POST /short-key/custom"
    })



@router.get("/short-key/{short-key}")

async def get_short_key_short_key():
    """
    TODO: Implement GET /short-key/{short-key}
    """
    raise HTTPException(status_code=501, detail={
        "error": "Not implemented",
        "endpoint": "GET /short-key/{short-key}"
    })

