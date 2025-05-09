from functools import wraps
from flask import request, jsonify
import jwt
import os

SECRET_KEY = os.getenv('JWT_SECRET_KEY')

def decode_token(auth_header):
    if not auth_header or not auth_header.startswith('Bearer '):
        return None
    token = auth_header.split(' ')[1]
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return payload
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return jsonify({'message': 'Token é necessário!'}), 401

        payload = decode_token(auth_header)
        if not payload:
            return jsonify({'message': 'Token inválido ou expirado!'}), 401

        return f(*args, **kwargs)
    return decorated
