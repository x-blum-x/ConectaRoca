import logging
from flask import Flask
from utils.token_validation import token_required
import os
from models.models import db
from dotenv import load_dotenv

# Importações de rotas organizadas por módulo
from routes.auth.login_user import login_route
from routes.auth.register_user import register_route
from routes.users.get_user import get_user_profile
from routes.users.up_user import update_user_profile
# CONTROLE FINANCEIRO
from routes.finances.create_transaction import create_transaction
from routes.finances.list_transactions import list_transactions
from routes.finances.get_finance_summary import get_finance_summary
from routes.finances.get_cashflow import get_cashflow
from routes.finances.get_categories import get_categories
# GESTÃO DE ESTOQUE
from routes.inventory.create_item import add_inventory_item
from routes.inventory.create_moviment import register_movement
from routes.inventory.get_inventory_balance import get_inventory_balance
from routes.inventory.get_inventory_history import get_inventory_history
# PLANEJAMENTO DE SAFRA E ATIVIDADES
from routes.cropplans.create_cropplan import create_cropplan
from routes.cropplans.list_cropplans import list_cropplans
from routes.cropplans.add_task_to_cropplan import add_task_to_cropplan
from routes.cropplans.update_task_status import update_task_status
from routes.cropplans.get_task_timeline import get_task_timeline

# from routes.reports import (
#     get_dashboard, get_finance_report,
#     get_productivity_report, get_tasks_report
# )
# from routes.productivity import (
#     register_productivity, get_by_area,
#     get_by_crop, get_summary
# )

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
with app.app_context():
    db.create_all()

# AUTENTICAÇÃO E USUÁRIOS
app.add_url_rule('/auth/login', 'login', login_route(db), methods=['POST'])
app.add_url_rule('/auth/register', 'register', register_route(db), methods=['POST'])
app.add_url_rule('/users/me', 'get_user_profile', token_required(get_user_profile(db)), methods=['GET'])
app.add_url_rule('/users/<string:id>', 'update_user_profile', token_required(update_user_profile(db)), methods=['PUT'])

# CONTROLE FINANCEIRO
app.add_url_rule('/finance/transactions', 'create_transaction', token_required(create_transaction(db)), methods=['POST'])
app.add_url_rule('/finance/transactions', 'list_transactions', token_required(list_transactions(db)), methods=['GET'])
app.add_url_rule('/finance/summary', 'get_finance_summary', token_required(get_finance_summary(db)), methods=['GET'])
app.add_url_rule('/finance/cashflow', 'get_cashflow', token_required(get_cashflow(db)), methods=['GET'])
app.add_url_rule('/finance/categories', 'get_categories', token_required(get_categories(db)), methods=['GET'])

# PLANEJAMENTO DE SAFRA E ATIVIDADES
app.add_url_rule('/cropplans', 'create_cropplan', token_required(create_cropplan(db)), methods=['POST'])
app.add_url_rule('/cropplans', 'list_cropplans', token_required(list_cropplans(db)), methods=['GET'])
app.add_url_rule('/cropplans/<string:id>/tasks', 'add_task_to_cropplan', token_required(add_task_to_cropplan(db)), methods=['POST'])
app.add_url_rule('/tasks/<string:id>/status', 'update_task_status', token_required(update_task_status(db)), methods=['PUT'])
app.add_url_rule('/tasks/timeline', 'get_task_timeline', token_required(get_task_timeline(db)), methods=['GET'])

# GESTÃO DE ESTOQUE
app.add_url_rule('/inventory/items', 'add_inventory_item', token_required(add_inventory_item(db)), methods=['POST'])
app.add_url_rule('/inventory/movements', 'register_movement', token_required(register_movement(db)), methods=['POST'])
app.add_url_rule('/inventory/balance', 'get_inventory_balance', token_required(get_inventory_balance(db)), methods=['GET'])
app.add_url_rule('/inventory/history', 'get_inventory_history', token_required(get_inventory_history(db)), methods=['GET'])

# RELATÓRIOS
# app.add_url_rule('/reports/dashboard', 'get_dashboard', token_required(get_dashboard(db)), methods=['GET'])
# app.add_url_rule('/reports/finance', 'get_finance_report', token_required(get_finance_report(db)), methods=['GET'])
# app.add_url_rule('/reports/productivity', 'get_productivity_report', token_required(get_productivity_report(db)), methods=['GET'])
# app.add_url_rule('/reports/tasks', 'get_tasks_report', token_required(get_tasks_report(db)), methods=['GET'])

# PRODUTIVIDADE
# app.add_url_rule('/productivity/records', 'register_productivity', token_required(register_productivity), methods=['POST'])
# app.add_url_rule('/productivity/by-area', 'get_by_area', token_required(get_by_area(db)), methods=['GET'])
# app.add_url_rule('/productivity/by-crop', 'get_by_crop', token_required(get_by_crop(db)), methods=['GET'])
# app.add_url_rule('/productivity/summary', 'get_summary', token_required(get_summary(db)), methods=['GET'])

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
