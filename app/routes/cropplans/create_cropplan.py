from flask import request, jsonify
from models.models import CropPlan
from datetime import datetime
from utils.token_validation import decode_token

def create_cropplan(db):
    def route():
        try:
            data = request.get_json()
            user_id = decode_token(request.headers.get('Authorization')).get('user_id')

            name = data.get('name')
            crop_type = data.get('crop_type')
            start_date = data.get('start_date')
            end_date = data.get('end_date')
            variety = data.get('variety')
            area = data.get('area')
            irrigated = data.get('irrigated', False)
            soil_type = data.get('soil_type')
            notes = data.get('notes')

            # Validação mínima
            if not name or not crop_type or area is None:
                return jsonify({'error': 'Campos "name", "crop_type" e "area" são obrigatórios.'}), 400

            cropplan = CropPlan(
                user_id=user_id,
                name=name,
                crop_type=crop_type,
                variety=variety,
                area=float(area),
                irrigated=bool(irrigated),
                soil_type=soil_type,
                notes=notes,
                start_date=datetime.strptime(start_date, '%Y-%m-%d') if start_date else None,
                end_date=datetime.strptime(end_date, '%Y-%m-%d') if end_date else None
            )

            db.session.add(cropplan)
            db.session.commit()

            return jsonify({
                'message': 'Plano de safra criado com sucesso.',
                'cropplan_id': cropplan.id
            }), 201

        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 500

    return route