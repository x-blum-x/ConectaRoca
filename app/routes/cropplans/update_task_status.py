from flask import request, jsonify
from models.models import Task

def update_task_status(db):
    def route(id):
        try:
            data = request.get_json()
            new_status = data.get('status')

            if new_status not in ['pending', 'in_progress', 'done']:
                return jsonify({'error': 'Status inválido. Use: pending, in_progress ou done.'}), 400

            task = Task.query.filter_by(id=id).first()
            if not task:
                return jsonify({'error': 'Tarefa não encontrada.'}), 404

            task.status = new_status
            db.session.commit()

            return jsonify({'message': 'Status da tarefa atualizado com sucesso.'}), 200

        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 500

    return route