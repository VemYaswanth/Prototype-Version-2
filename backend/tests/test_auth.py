from app import create_app, db

def test_app_starts():
    app = create_app()
    with app.app_context():
        assert app is not None
