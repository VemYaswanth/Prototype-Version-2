from app import create_app
from app.utils.db_init import init_db

app = create_app()

with app.app_context():
    init_db()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
