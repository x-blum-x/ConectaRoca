from flask import request, jsonify
import jwt
import os
import datetime
from models.models import User

SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'supersecretkey')

def login_route(db):
    def route():
        data = request.get_json()
        identifier = data.get('email') or data.get('name')
        password = data.get('password')

        if not identifier or not password:
            return jsonify({'message': 'Informe nome/email e senha'}), 400

        user = User.query.filter((User.email == identifier) | (User.name == identifier)).first()

        if not user or not user.check_password(password):
            return jsonify({'message': 'Credenciais inválidas'}), 401

        token = jwt.encode({
            'user_id': user.id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24)
        }, SECRET_KEY, algorithm="HS256")

        return jsonify({'token': token})
    return route
