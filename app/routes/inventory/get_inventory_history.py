from flask import request, jsonify
from models.models import InventoryMovement

def get_inventory_history(db):
    def route():
        item_id = request.args.get('item_id')
        if not item_id:
            return jsonify({'message': 'Informe o item_id'}), 400

        try:
            movements = InventoryMovement.query.filter_by(item_id=item_id).order_by(InventoryMovement.date.desc()).all()

            history = [
                {
                    'type': m.type,
                    'quantity': m.quantity,
                    'date': m.date.strftime('%Y-%m-%d') if m.date else None,
                    'unit_weight': m.unit_weight,
                    'total_weight': m.total_weight,
                    'unit_price': m.unit_price,
                    'total_value': m.total_value,
                    'responsible': m.responsible,
                    'location': m.location,
                    'note': m.note
                }
                for m in movements
            ]
            return jsonify(history)
        except Exception as e:
            return jsonify({'message': f'Erro ao buscar histórico: {str(e)}'}), 500
    return route
