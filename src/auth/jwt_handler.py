"""JWT token handling and authentication."""
from datetime import datetime, timedelta
from typing import Optional, Dict
from jose import JWTError, jwt
from fastapi import HTTPException, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from ..config.settings import Settings

security = HTTPBearer()
settings = Settings()

class JWTHandler:
    """Handles JWT token operations."""
    
    @staticmethod
    def create_access_token(data: Dict, expires_delta: Optional[timedelta] = None) -> str:
        """Create a new JWT access token."""
        to_encode = data.copy()
        expire = datetime.utcnow() + (expires_delta or timedelta(minutes=30))
        to_encode.update({"exp": expire})
        return jwt.encode(to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
    
    @staticmethod
    def verify_token(credentials: HTTPAuthorizationCredentials = Security(security)) -> Dict:
        """Verify and decode JWT token."""
        try:
            token = credentials.credentials
            payload = jwt.decode(
                token,
                settings.JWT_SECRET_KEY,
                algorithms=[settings.JWT_ALGORITHM]
            )
            if payload.get("exp") < datetime.utcnow().timestamp():
                raise HTTPException(
                    status_code=401,
                    detail="Token has expired"
                )
            return payload
        except JWTError:
            raise HTTPException(
                status_code=401,
                detail="Invalid authentication credentials"
            )