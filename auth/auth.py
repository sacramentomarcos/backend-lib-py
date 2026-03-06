import time
import jwt
from os import environ

JWT_SECRET = environ['secret']
JWT_ALGORITHM = environ['algorithm']

def token_response(token:str):
    return {
        'access_token': token
    }