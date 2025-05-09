from flask import request, jsonify
from models.models import Task, CropPlan
from datetime import datetime
import json
from utils.token_validation import decode_token

def get_task_timeline(db):
    def route():
        try:
            user_id = decode_token(request.headers.get('Authorization')).get('user_id')
            start_date_str = request.args.get('start_date')
            end_date_str = request.args.get('end_date')

            if not start_date_str or not end_date_str:
                return jsonify({'error': 'Parâmetros start_date e end_date são obrigatórios.'}), 400

            try:
                start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
                end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()
            except ValueError:
                return jsonify({'error': 'Formato de data inválido. Use YYYY-MM-DD.'}), 400

            # Identifica planos do usuário
            user_cropplans = CropPlan.query.with_entities(CropPlan.id).all()
            cropplan_ids = [cp.id for cp in user_cropplans]

            # Busca tarefas do range de datas
            tasks = Task.query.filter(
                Task.cropplan_id.in_(cropplan_ids),
                Task.date >= start_date,
                Task.date <= end_date
            ).order_by(Task.date.asc()).all()

            result = []
            for task in tasks:
                # converte de string para lista se possível
                try:
                    resources_data = json.loads(task.resources) if task.resources else []
                except (json.JSONDecodeError, TypeError):
                    resources_data = []

                result.append({
                    'id': task.id,
                    'description': task.description,
                    'status': task.status,
                    'date': task.date.isoformat() if task.date else None,
                    'responsible': task.responsible,
                    'duration_hours': task.duration_hours,
                    'resources': resources_data,
                    'notes': task.notes,
                    'cropplan_id': task.cropplan_id,
                    'created_at': task.created_at.isoformat() if task.created_at else None
                })

            return jsonify(result), 200

        except Exception as e:
            return jsonify({'error': str(e)}), 500

    return route