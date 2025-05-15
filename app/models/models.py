from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from utils.generate_unique_id import generate_unique_id
db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    
    def set_password(self, raw_password):
        self.password = generate_password_hash(raw_password)

    def check_password(self, raw_password):
        return check_password_hash(self.password, raw_password)

    id = db.Column(db.Integer, primary_key=True, default=lambda: generate_unique_id(User, db))
    email = db.Column(db.String(120), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(128), nullable=False)
    tel = db.Column(db.String(20))
    cpf = db.Column(db.String(20))
    sexo = db.Column(db.String(10))
    idade = db.Column(db.Integer)
    cidade = db.Column(db.String(100))
    estado = db.Column(db.String(50))
    localidade = db.Column(db.String(100))
    last_modified = db.Column(db.DateTime)
    last_modifier = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Transaction(db.Model):
    __tablename__ = 'transactions'

    id = db.Column(db.Integer, primary_key=True, default=lambda: generate_unique_id(Transaction, db))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    type = db.Column(db.String(10), nullable=False)  # 'income' or 'expense'
    amount = db.Column(db.Float, nullable=False)
    category = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    date = db.Column(db.Date, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class CropPlan(db.Model):
    __tablename__ = 'cropplans'

    id = db.Column(db.Integer, primary_key=True, default=lambda: generate_unique_id(CropPlan, db))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    crop_type = db.Column(db.String(100))
    variety = db.Column(db.String(100))
    area = db.Column(db.Float)
    irrigated = db.Column(db.Boolean, default=False)
    soil_type = db.Column(db.String(50))
    notes = db.Column(db.Text)
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class Task(db.Model):
    __tablename__ = 'tasks'

    id = db.Column(db.Integer, primary_key=True, default=lambda: generate_unique_id(Task, db))
    cropplan_id = db.Column(db.Integer, db.ForeignKey('cropplans.id'), nullable=False)
    description = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(20), default='pending')  # 'pending', 'in_progress', 'done'
    date = db.Column(db.Date)
    responsible = db.Column(db.String(100))
    duration_hours = db.Column(db.Float)
    resources = db.Column(db.Text) 
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class InventoryItem(db.Model):
    __tablename__ = 'inventory_items'

    id = db.Column(db.Integer, primary_key=True, default=lambda: generate_unique_id(InventoryItem, db))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    unit = db.Column(db.String(20), nullable=False)
    category = db.Column(db.String(100))
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class InventoryMovement(db.Model):
    __tablename__ = 'inventory_movements'

    id = db.Column(db.Integer, primary_key=True, default=lambda: generate_unique_id(InventoryMovement, db))
    item_id = db.Column(db.Integer, db.ForeignKey('inventory_items.id'), nullable=False)
    type = db.Column(db.String(10), nullable=False)  # 'entrada' or 'saida'
    quantity = db.Column(db.Float, nullable=False)
    date = db.Column(db.Date, nullable=False)
    unit_weight = db.Column(db.Float)
    total_weight = db.Column(db.Float)
    unit_price = db.Column(db.Float)
    total_value = db.Column(db.Float)
    responsible = db.Column(db.String(100))
    location = db.Column(db.String(100))
    note = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Message(db.Model):
    __tablename__ = 'messages'

    id = db.Column(db.Integer, primary_key=True, default=lambda: generate_unique_id(Message, db))
    sender_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    receiver_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    content = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    sender = db.relationship('User', foreign_keys=[sender_id], backref='sent_messages')
    receiver = db.relationship('User', foreign_keys=[receiver_id], backref='received_messages')