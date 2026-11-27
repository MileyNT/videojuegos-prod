import time

from sqlalchemy.exc import OperationalError

from app import app, db


for attempt in range(30):
    try:
        with app.app_context():
            with db.engine.connect():
                pass
        break
    except OperationalError:
        if attempt == 29:
            raise
        time.sleep(2)

with app.app_context():
    db.create_all()
