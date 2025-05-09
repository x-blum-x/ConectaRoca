from flask import request, jsonify
from models.models import InventoryItem
from datetime import datetime

def add_inventory_item(db):
    def route():
        data = request.get_json()
        required = ['user_id', 'name', 'unit']
        if not all(field in data for field in required):
            return jsonify({'message': 'Campos obrigatórios: user_id, name, unit'}), 400

        try:
            item = InventoryItem(
                user_id=data['user_id'],
                name=data['name'],
                unit=data['unit'],
                category=data.get('category'),
                description=data.get('description'),
                created_at=datetime.utcnow()
            )
            db.session.add(item)
            db.session.commit()

            return jsonify({'message': 'Item cadastrado com sucesso'}), 201
        except Exception as e:
            db.session.rollback()
            return jsonify({'message': f'Erro ao cadastrar item: {str(e)}'}), 500
    return route