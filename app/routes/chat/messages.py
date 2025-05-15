from flask import request, jsonify
from models.models import db, Message, User
from utils.token_validation import decode_token
from datetime import datetime

def chat_route(db):
    def route():
        auth_header = request.headers.get('Authorization')
        token_data = decode_token(auth_header)
        sender_id = token_data.get('user_id')
        if not sender_id:
            return jsonify({'message': 'Token inválido'}), 401

        if request.method == 'POST':
            data = request.json
            receiver_id = data.get('receiver_id')
            content = data.get('content')

            if not receiver_id or not content:
                return jsonify({'message': 'Campos obrigatórios faltando'}), 400

            message = Message(sender_id=sender_id, receiver_id=receiver_id, content=content, timestamp=datetime.utcnow())
            db.session.add(message)
            db.session.commit()
            return jsonify({'message': 'Mensagem enviada com sucesso'}), 201

        elif request.method == 'GET':
            receiver_id = request.args.get('user_id', type=int)
            if not receiver_id:
                return jsonify({'message': 'ID do usuário destinatário não fornecido'}), 400

            messages = Message.query.filter(
                ((Message.sender_id == sender_id) & (Message.receiver_id == receiver_id)) |
                ((Message.sender_id == receiver_id) & (Message.receiver_id == sender_id))
            ).order_by(Message.timestamp.asc()).all()

            return jsonify([
                {
                    'id': msg.id,
                    'sender_id': msg.sender_id,
                    'receiver_id': msg.receiver_id,
                    'content': msg.content,
                    'timestamp': msg.timestamp.isoformat()
                } for msg in messages
            ]), 200

    return route