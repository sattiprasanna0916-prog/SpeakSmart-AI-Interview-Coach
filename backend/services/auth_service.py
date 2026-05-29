import os
from datetime import datetime, timedelta

from jose import jwt, JWTError
from fastapi import (
    HTTPException,
    Depends
)
from fastapi.security import (
    HTTPBearer,
    HTTPAuthorizationCredentials
)


# --------------------------------
# CONFIG
# --------------------------------
SECRET_KEY = os.getenv(
    "JWT_SECRET",
    "dev_secret_key"
)

ALGORITHM = "HS256"

ACCESS_TOKEN_EXPIRE_MINUTES = 60


security = HTTPBearer()


# --------------------------------
# CREATE ACCESS TOKEN
# --------------------------------
def create_access_token(data: dict):

    payload = data.copy()

    expire = datetime.utcnow() + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )

    payload.update({
        "exp": expire,
        "type": "access"
    })

    token = jwt.encode(
        payload,
        SECRET_KEY,
        algorithm=ALGORITHM
    )

    return token


# --------------------------------
# VERIFY TOKEN
# --------------------------------
def verify_token(
    credentials: HTTPAuthorizationCredentials = Depends(security)
):

    try:
        token = credentials.credentials

        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        user_id = payload.get("sub")

        if not user_id:
            raise HTTPException(
                status_code=401,
                detail="Invalid token"
            )

        return payload

    except JWTError:
        raise HTTPException(
            status_code=401,
            detail="Token expired or invalid"
        )