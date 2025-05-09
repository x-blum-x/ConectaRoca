from flask import request, jsonify
from utils.token_validation import decode_token
from models.models import Transaction

def get_finance_summary(db):
    def route():
        user_id = decode_token(request.headers.get('Authorization')).get('user_id')
        if not user_id:
            return jsonify({'message': 'Usuário não encontrado'}), 400

        try:
            transactions = Transaction.query.filter_by(user_id=user_id).all()

            income = sum(t.amount for t in transactions if t.type == 'income')
            expense = sum(t.amount for t in transactions if t.type == 'expense')
            balance = income - expense

            return jsonify({
                'total_income': income,
                'total_expense': expense,
                'balance': balance
            })
        except Exception as e:
            return jsonify({'message': f'Erro ao obter resumo financeiro: {str(e)}'}), 500
    return route