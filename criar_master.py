from app import create_app
from app.bootstrap import bootstrap


app = create_app()

with app.app_context():
    bootstrap()