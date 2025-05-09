from flask import request, jsonify
from utils.token_validation import decode_token
from models.models import User

def get_user_profile(db):
    def route():
        user_id = decode_token(request.headers.get('Authorization')).get('user_id')
        if not user_id:
            return jsonify({'message': 'Token inválido'}), 401

        user = User.query.filter_by(id=user_id).first()
        if not user:
            return jsonify({'message': 'Usuário não encontrado'}), 404

        user_data = {
            'id': user.id,
            'name': user.name,
            'email': user.email,
            'tel': user.tel,
            'cpf': user.cpf,
            'sexo': user.sexo,
            'idade': user.idade,
            'cidade': user.cidade,
            'estado': user.estado,
            'localidade': user.localidade,
            'last_modified': user.last_modified,
            'last_modifier': user.last_modifier,
            'created_at': user.created_at
        }
        return jsonify(user_data), 200
    return route
