from flask import request, jsonify
from sqlalchemy import func, case
from models.models import InventoryItem, InventoryMovement
from utils.token_validation import decode_token

def get_inventory_balance(db):
    def route():
        user_id = decode_token(request.headers.get('Authorization')).get('user_id')
        if not user_id:
            return jsonify({'message': 'Informe o user_id'}), 400

        try:
            items = db.session.query(
                InventoryItem.id,
                InventoryItem.name,
                InventoryItem.unit,
                func.coalesce(func.sum(
                    case((InventoryMovement.type == 'entrada', InventoryMovement.quantity), else_=0)
                ), 0) -
                func.coalesce(func.sum(
                    case((InventoryMovement.type == 'saida', InventoryMovement.quantity), else_=0)
                ), 0),
                func.coalesce(func.sum(
                    case((InventoryMovement.type == 'entrada', InventoryMovement.total_value), else_=0)
                ), 0) -
                func.coalesce(func.sum(
                    case((InventoryMovement.type == 'saida', InventoryMovement.total_value), else_=0)
                ), 0)
            ).outerjoin(InventoryMovement, InventoryItem.id == InventoryMovement.item_id) \
             .filter(InventoryItem.user_id == user_id) \
             .group_by(InventoryItem.id).all()

            result = [
                {
                    'item_id': row[0],
                    'name': row[1],
                    'unit': row[2],
                    'balance': float(row[3]),
                    'total_value': float(row[4])
                }
                for row in items
            ]
            return jsonify(result)
        except Exception as e:
            return jsonify({'message': f'Erro ao obter saldo de estoque: {str(e)}'}), 500
    return route
