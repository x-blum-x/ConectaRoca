from flask import request, jsonify
from models.models import CropPlan
from utils.token_validation import decode_token

def list_cropplans(db):
    def route():
        try:
            user_id = decode_token(request.headers.get('Authorization')).get('user_id')

            cropplans = CropPlan.query.filter_by(user_id=user_id).order_by(CropPlan.start_date.desc()).all()

            result = []
            for plan in cropplans:
                result.append({
                    'id': plan.id,
                    'name': plan.name,
                    'crop_type': plan.crop_type,
                    'variety': plan.variety,
                    'area': plan.area,
                    'irrigated': plan.irrigated,
                    'soil_type': plan.soil_type,
                    'start_date': plan.start_date.isoformat() if plan.start_date else None,
                    'end_date': plan.end_date.isoformat() if plan.end_date else None,
                    'notes': plan.notes,
                    'created_at': plan.created_at.isoformat() if plan.created_at else None
                })

            return jsonify(result), 200

        except Exception as e:
            return jsonify({'error': str(e)}), 500

    return route
