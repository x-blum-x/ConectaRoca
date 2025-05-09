from flask import request, jsonify
from models.models import User, db

def register_route(db):
    def route():
        data = request.get_json()
        email = data.get('email')
        name = data.get('name')
        password = data.get('password')

        if not all([email, name, password]):
            return jsonify({'message': 'Campos obrigatórios: email, nome, senha'}), 400

        if User.query.filter_by(email=email).first():
            return jsonify({'message': 'Email já cadastrado'}), 409

        new_user = User(email=email, name=name)
        new_user.set_password(password)

        db.session.add(new_user)
        db.session.commit()

        return jsonify({'message': 'Usuário cadastrado com sucesso'}), 201
    return route
