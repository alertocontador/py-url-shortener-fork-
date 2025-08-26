from fastapi import APIRouter, HTTPException
from fastapi.responses import RedirectResponse
from pydantic import BaseModel
from typing import Dict, Any
import string
import random
from db.mysql import get_mysql_connection

router = APIRouter()

class URLRequest(BaseModel):
    url: str

class CustomURLRequest(BaseModel):
    url: str
    custom_key: str

class URLResponse(BaseModel):
    short_key: str
    original_url: str

def generate_short_key(length: int = 6) -> str:
    """Generate a random short key"""
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))

def validate_url(url: str) -> bool:
    """Basic URL validation"""
    return url.startswith(('http://', 'https://')) and len(url) > 10



@router.post("/short-key", response_model=URLResponse)
async def post_short_key(request: URLRequest):
    """Generate a random short key for a given URL"""
    if not validate_url(request.url):
        raise HTTPException(status_code=400, detail="Invalid URL format")
    
    connection = get_mysql_connection()
    if not connection:
        raise HTTPException(status_code=500, detail="Database connection failed")
    
    try:
        cursor = connection.cursor()
        
        # Generate unique short key
        max_attempts = 10
        for _ in range(max_attempts):
            short_key = generate_short_key()
            
            # Check if short key already exists
            cursor.execute("SELECT id FROM urls WHERE short_key = %s", (short_key,))
            if not cursor.fetchone():
                break
        else:
            raise HTTPException(status_code=500, detail="Failed to generate unique short key")
        
        # Insert the URL mapping
        cursor.execute(
            "INSERT INTO urls (short_key, original_url) VALUES (%s, %s)",
            (short_key, request.url)
        )
        connection.commit()
        
        return URLResponse(short_key=short_key, original_url=request.url)
        
    except Exception as e:
        connection.rollback()
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    finally:
        connection.close()



@router.post("/short-key/custom", response_model=URLResponse)
async def post_short_key_custom(request: CustomURLRequest):
    """Create a custom short key for a given URL"""
    if not validate_url(request.url):
        raise HTTPException(status_code=400, detail="Invalid URL format")
    
    if not request.custom_key or len(request.custom_key) < 1:
        raise HTTPException(status_code=400, detail="Custom key cannot be empty")
    
    # Basic validation for custom key
    if not request.custom_key.replace('_', '').replace('-', '').isalnum():
        raise HTTPException(status_code=400, detail="Custom key can only contain letters, numbers, hyphens, and underscores")
    
    connection = get_mysql_connection()
    if not connection:
        raise HTTPException(status_code=500, detail="Database connection failed")
    
    try:
        cursor = connection.cursor()
        
        # Check if custom key already exists
        cursor.execute("SELECT id FROM urls WHERE short_key = %s", (request.custom_key,))
        if cursor.fetchone():
            raise HTTPException(status_code=409, detail="Custom key already exists")
        
        # Insert the URL mapping with custom key
        cursor.execute(
            "INSERT INTO urls (short_key, original_url) VALUES (%s, %s)",
            (request.custom_key, request.url)
        )
        connection.commit()
        
        return URLResponse(short_key=request.custom_key, original_url=request.url)
        
    except HTTPException:
        connection.rollback()
        raise
    except Exception as e:
        connection.rollback()
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    finally:
        connection.close()



@router.get("/short-key/{short_key}")
async def get_short_key(short_key: str):
    """Redirect or retrieve URL by short key"""
    connection = get_mysql_connection()
    if not connection:
        raise HTTPException(status_code=500, detail="Database connection failed")
    
    try:
        cursor = connection.cursor()
        
        # Find the original URL by short key
        cursor.execute("SELECT original_url FROM urls WHERE short_key = %s", (short_key,))
        result = cursor.fetchone()
        
        if not result:
            raise HTTPException(status_code=404, detail="Short key not found")
        
        original_url = result['original_url']
        return URLResponse(short_key=short_key, original_url=original_url)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    finally:
        connection.close()
