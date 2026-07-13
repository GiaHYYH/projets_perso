from fastapi import Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from auth import verify_jwt


security = HTTPBearer()


def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials

    usr_mail = verify_jwt(token)

    return usr_mail