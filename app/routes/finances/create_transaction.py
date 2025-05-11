from flask import request, jsonify
from models.models import Transaction
from datetime import datetime
from utils.token_validation import decode_token

def create_transaction(db):
    def route():
        data = request.get_json()
        required = ['type', 'amount', 'category', 'date']
        if not all(field in data for field in required):
            return jsonify({'message': 'Campos obrigatórios: user_id, type, amount, category, date'}), 400

        if data['type'] not in ['income', 'expense']:
            return jsonify({'message': 'Tipo deve ser "income" ou "expense"'}), 400

        try:
            # Preparar os dados recebidos
            date_obj = datetime.strptime(data['date'], '%Y-%m-%d').date()
            user_id = decode_token(request.headers.get('Authorization')).get('user_id')
            trans_type = data['type']
            description = data.get('description', '').lower()
            amount = data['amount']

            # Termos-chave para detecção
            key_words = ['soja', 'milho', 'trigo', 'cana', 'feijão', 'arroz']
            action_words = ['compra', 'venda', 'comercialização', 'negócio']

            # Busca por transações do mesmo dia, tipo e usuário
            existing_transactions = Transaction.query.filter(
                Transaction.user_id == user_id,
                Transaction.type == trans_type,
                Transaction.date == date_obj
            ).all()

            for t in existing_transactions:
                existing_desc = t.description.lower()
                # Verifica se há uma palavra-chave em comum
                if any(kw in existing_desc and kw in description for kw in key_words):
                    if any(act in existing_desc and act in description for act in action_words):
                        if t.amount == amount:
                            return jsonify({
                                'message': 'Transação semelhante já registrada neste dia para este usuário'
                            }), 409

            # Se não encontrou conflito, cria a transação
            transaction = Transaction(
                user_id=user_id,
                type=trans_type,
                amount=amount,
                category=data['category'],
                description=description,
                date=date_obj
            )

            db.session.add(transaction)
            db.session.commit()

            return jsonify({'message': 'Transação registrada com sucesso'}), 201
        except Exception as e:
            db.session.rollback()
            return jsonify({'message': f'Erro ao registrar transação: {str(e)}'}), 500
    return route
