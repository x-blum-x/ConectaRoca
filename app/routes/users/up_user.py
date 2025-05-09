from flask import request, jsonify
from datetime import datetime
from utils.token_validation import decode_token
from models.models import User

def update_user_profile(db):
    def route(id):
        auth_header = request.headers.get('Authorization')
        modifier_id = decode_token(auth_header).get('user_id') if auth_header else None
        if not modifier_id:
            return jsonify({'message': 'Token inválido'}), 401

        user = User.query.filter_by(id=id).first()
        if not user:
            return jsonify({'message': 'Usuário não encontrado'}), 404

        data = request.get_json()
        allowed_fields = ['name', 'email', 'tel', 'cpf', 'sexo', 'idade', 'cidade', 'estado', 'localidade']
        updates = {k: data[k] for k in allowed_fields if k in data and data[k] is not None}

        if not updates:
            return jsonify({'message': 'Informe ao menos um campo para atualizar'}), 400

        for field, value in updates.items():
            setattr(user, field, value)

        user.last_modified = datetime.utcnow()
        user.last_modifier = modifier_id

        db.session.commit()

        return jsonify({'message': 'Perfil atualizado com sucesso'}), 200
    return route
