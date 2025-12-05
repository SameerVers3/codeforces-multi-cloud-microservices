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

async def verify_contest_access(
    contest_id: UUID,
    current_user: dict = Depends(verify_token),
    db: Session = Depends(get_db)
) -> bool:
    """Verify user has access to contest (registered or staff)"""
    import httpx
    
    # Staff can access any contest
    if current_user.get("role") == "staff":
        return True
    
    # Check if user is registered
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{settings.CONTEST_SERVICE_URL}/api/v1/registrations/contest/{contest_id}/is-registered",
            headers={"Authorization": f"Bearer {current_user.get('token', '')}"}
        )
        if response.status_code == 200:
            data = response.json()
            return data.get("is_registered", False)
    
    return False

