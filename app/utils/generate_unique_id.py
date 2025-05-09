import random

def generate_unique_id(model, db):
    while True:
        new_id = random.randint(100, 999999999)
        if not db.session.query(model).filter_by(id=new_id).first():
            return new_id