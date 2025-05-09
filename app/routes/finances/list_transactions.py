from flask import request, jsonify
from models.models import Transaction
from utils.token_validation import decode_token

def list_transactions(db):
    def route():
        user_id = decode_token(request.headers.get('Authorization')).get('user_id')
        if not id:
            return jsonify({'message': 'Usuário não encontrado'}), 400

        try:
            transactions = Transaction.query.filter_by(user_id=user_id).order_by(Transaction.date.desc()).all()
            result = [
                {
                    'id': t.id,
                    'type': t.type,
                    'amount': t.amount,
                    'category': t.category,
                    'description': t.description,
                    'date': t.date.strftime('%Y-%m-%d'),
                    'created_at': t.created_at.strftime('%Y-%m-%d %H:%M:%S') if t.created_at else None
                }
                for t in transactions
            ]
            return jsonify(result)
        except Exception as e:
            return jsonify({'message': f'Erro ao listar transações: {str(e)}'}), 500
    return route
