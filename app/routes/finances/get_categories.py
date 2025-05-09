from flask import request, jsonify

def get_categories(db):
    def route():
        return jsonify([
            'Alimentação',
            'Insumos',
            'Venda',
            'Compra',
            'Equipamentos',
            'Manutenção',
            'Energia',
            'Água',
            'Combustível',
            'Outros'
        ])
    return route