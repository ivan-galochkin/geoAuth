import os
import time
from schemas import UserSchema
from db_session import create_session
import jwt

JWT_SECRET = os.environ["JWT_SECRET"]


def create_access_jwt(user_id: int):
    payload = {
        "user_id": user_id,
        "exp": time.time() + 1200
    }
    access_token = jwt.encode(payload, JWT_SECRET, algorithm="HS256")

    return access_token


def create_refresh_jwt(user_id: int):
    payload = {
        "user_id": user_id,
        "time": time.time()
    }
    refresh_token = jwt.encode(payload, JWT_SECRET, algorithm="HS256")

    return refresh_token


def create_response(user):
    return {"tokens": {"access_token": create_access_jwt(user.uid), "refresh_token": create_refresh_jwt(user.uid)}}


def decode_jwt(token):
    try:
        return jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
    except jwt.ExpiredSignatureError:
        return "expired"
    except jwt.exceptions.DecodeError:
        return "wrong token"
