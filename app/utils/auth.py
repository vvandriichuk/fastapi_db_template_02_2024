import os
from fastapi import Security, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
import jwt


APP_SECRET_KEY = os.environ.get('APP_ACCESS_KEY')
JWT_ALGORITHM = os.environ.get('JWT_ALGORITHM', 'HS256')


security = HTTPBearer()


async def get_current_user(credentials: HTTPAuthorizationCredentials = Security(security)):
    token = credentials.credentials
    try:
        payload = jwt.decode(token, APP_SECRET_KEY, algorithms=[JWT_ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail="Invalid JWT token"
            )
        return username
    except jwt.PyJWTError:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Invalid JWT token"
        )
