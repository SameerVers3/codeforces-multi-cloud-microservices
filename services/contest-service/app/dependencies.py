from fastapi import Depends, HTTPException, status, Header
from sqlalchemy.orm import Session
import httpx
from uuid import UUID

from app.database import get_db
from app.config import settings

async def verify_token(authorization: str = Header(None)) -> dict:
    """Verify JWT token with auth service"""
    if not authorization:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authorization header missing"
        )
    
    try:
        token = authorization.replace("Bearer ", "")
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{settings.AUTH_SERVICE_URL}/api/v1/auth/me",
                headers={"Authorization": f"Bearer {token}"}
            )
            if response.status_code != 200:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid or expired token"
                )
            return response.json()
    except httpx.RequestError:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Auth service unavailable"
        )

async def get_current_user(auth_data: dict = Depends(verify_token)) -> dict:
    """Get current user from auth data"""
    return auth_data

async def require_staff(auth_data: dict = Depends(verify_token)) -> dict:
    """Require staff role"""
    if auth_data.get("role") != "staff":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Staff access required"
        )
    return auth_data

