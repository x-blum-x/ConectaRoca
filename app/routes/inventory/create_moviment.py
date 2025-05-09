from flask import request, jsonify
from models.models import InventoryMovement
from datetime import datetime

def register_movement(db):
    def route():
        data = request.get_json()
        required = ['item_id', 'type', 'quantity', 'date']
        if not all(field in data for field in required):
            return jsonify({'message': 'Campos obrigatórios: item_id, type, quantity, date'}), 400

        if data['type'] not in ['entrada', 'saida']:
            return jsonify({'message': 'Tipo deve ser "entrada" ou "saida"'}), 400

        try:
            quantity = float(data['quantity'])
            unit_weight = float(data.get('unit_weight', 0))
            unit_price = float(data.get('unit_price', 0))
            total_weight = unit_weight * quantity if unit_weight else None
            total_value = unit_price * quantity if unit_price else None
            date_obj = datetime.strptime(data['date'], '%Y-%m-%d').date()

            movement = InventoryMovement(
                item_id=data['item_id'],
                type=data['type'],
                quantity=quantity,
                date=date_obj,
                unit_weight=unit_weight if unit_weight else None,
                total_weight=total_weight,
                unit_price=unit_price if unit_price else None,
                total_value=total_value,
                responsible=data.get('responsible'),
                location=data.get('location'),
                note=data.get('note'),
                created_at=datetime.utcnow()
            )

            db.session.add(movement)
            db.session.commit()

            return jsonify({'message': 'Movimentação registrada com sucesso'}), 201
        except ValueError:
            return jsonify({'message': 'Erro no formato de data ou campos numéricos inválidos'}), 400
        except Exception as e:
            db.session.rollback()
            return jsonify({'message': f'Erro ao registrar movimentação: {str(e)}'}), 500
    return route