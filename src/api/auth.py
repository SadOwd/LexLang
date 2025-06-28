"""
Authentication utilities for LexLang API.
This module provides a basic API key authentication mechanism.
"""

from fastapi import Security, HTTPException, status
from fastapi.security import APIKeyHeader
import os
import logging

logger = logging.getLogger(__name__)

# Define API key header
api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)

# In a real application, retrieve API keys from a secure database or environment
# For demonstration, we'll use an environment variable
API_KEYS = {
    "supersecretkey": "user_admin", # Example: "API_KEY_VALUE": "USER_ID"
    "anotherkey": "user_guest"
}

# Load API keys from environment variable if available
if os.getenv("LEXLANG_API_KEYS"):
    try:
        env_keys = json.loads(os.getenv("LEXLANG_API_KEYS"))
        API_KEYS.update(env_keys)
        logger.info("Loaded API keys from environment variable LEXLANG_API_KEYS.")
    except json.JSONDecodeError:
        logger.warning("LEXLANG_API_KEYS environment variable is not valid JSON. Using default keys.")
else:
    logger.warning("LEXLANG_API_KEYS environment variable not set. Using default hardcoded keys (for dev only!).")

async def get_api_key(api_key: str = Security(api_key_header)):
    """
    Validates the API key provided in the X-API-Key header.
    Returns the associated user ID if valid, raises HTTPException otherwise.
    """
    if api_key is None:
        logger.warning("API key missing in request.")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="API Key missing. Please provide X-API-Key header.",
            headers={"WWW-Authenticate": "X-API-Key"},
        )
    
    if api_key in API_KEYS:
        logger.info(f"API Key authenticated for user: {API_KEYS[api_key]}")
        return api_key
    else:
        logger.warning(f"Invalid API Key provided: {api_key}")
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid API Key. Access denied.",
            headers={"WWW-Authenticate": "X-API-Key"},
        )

async def get_current_user(api_key: str = Security(get_api_key)):
    """
    Returns the user ID associated with the validated API key.
    """
    return API_KEYS.get(api_key)

# You can add more complex roles/permissions here later if needed
def has_role(role: str):
    def role_checker(current_user: str = Depends(get_current_user)):
        # For simplicity, assuming user_admin has all roles
        if role == "admin" and current_user != "user_admin":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not enough permissions."
            )
        # Add other role checks here
        return current_user
    return role_checker
