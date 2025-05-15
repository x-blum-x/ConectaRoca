from flask import jsonify
from models.models import User

def get_all_users(db):
    def route():
        users = User.query.all()
        user_list = []
        for user in users:
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
            user_list.append(user_data)
        return jsonify(user_list), 200
    return route