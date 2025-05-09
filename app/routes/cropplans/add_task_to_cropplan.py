from flask import request, jsonify
from models.models import Task, CropPlan
from datetime import datetime
import json

def add_task_to_cropplan(db):
    def route(id):
        try:
            data = request.get_json()

            # Confirma existência do plano
            cropplan = CropPlan.query.filter_by(id=id).first()
            if not cropplan:
                return jsonify({'error': 'Plano de safra não encontrado.'}), 404

            # Campos obrigatórios
            description = data.get('description')
            date = data.get('date')
            responsible = data.get('responsible')
            duration_hours = data.get('duration_hours')

            if not description or not date or not responsible or duration_hours is None:
                return jsonify({'error': 'Campos obrigatórios: description, date, responsible, duration_hours'}), 400

            # Campos opcionais
            notes = data.get('notes')
            status = data.get('status', 'pending')
            resources = data.get('resources')  # pode ser lista ou string JSON

            if isinstance(resources, list):
                resources = json.dumps(resources)

            task = Task(
                cropplan_id=id,
                description=description,
                status=status,
                date=datetime.strptime(date, '%Y-%m-%d'),
                responsible=responsible,
                duration_hours=float(duration_hours),
                notes=notes,
                resources=resources
            )

            db.session.add(task)
            db.session.commit()

            return jsonify({'message': 'Tarefa criada com sucesso.', 'task_id': task.id}), 201

        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 500

    return route