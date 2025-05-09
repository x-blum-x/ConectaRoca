from flask import request, jsonify
from collections import defaultdict
from models.models import Transaction
from utils.token_validation import decode_token
from datetime import datetime

def get_cashflow(db):
    def route():
        user_id = decode_token(request.headers.get('Authorization')).get('user_id')
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')

        if not user_id or not start_date or not end_date:
            return jsonify({'message': 'Informe start_date e end_date corretamente'}), 400

        try:
            start = datetime.strptime(start_date, "%Y-%m-%d").date()
            end = datetime.strptime(end_date, "%Y-%m-%d").date()

            transactions = Transaction.query.filter(
                Transaction.user_id == user_id,
                Transaction.date >= start,
                Transaction.date <= end
            ).all()

            monthly = defaultdict(lambda: {'income': 0, 'expense': 0})

            for t in transactions:
                if t.type in ['income', 'expense']:
                    month = t.date.strftime('%Y-%m')
                    monthly[month][t.type] += t.amount

            return jsonify(monthly)

        except ValueError:
            return jsonify({'message': 'Formato de data inválido. Use YYYY-MM-DD.'}), 400
        except Exception as e:
            return jsonify({'message': f'Erro ao gerar fluxo de caixa: {str(e)}'}), 500
    return route
