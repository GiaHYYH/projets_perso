from fastapi import status, HTTPException
import os
import jwt

from dotenv import load_dotenv

load_dotenv()

jwt_secret = os.getenv("JWT_SECRET")
jwt_algorithm = os.getenv("JWT_ALGORITHM")

def create_jwt(usr_mail: str):
    payload = {"sub": usr_mail}
    token = jwt.encode(payload, jwt_secret, algorithm=jwt_algorithm)
    return token

def verify_jwt(token: str) -> str:
    try:
        payload = jwt.decode(token, jwt_secret, algorithms=[jwt_algorithm])
        usr_mail = payload["sub"]
        if usr_mail is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token invalide.")
        return usr_mail
    
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token invalide.")
