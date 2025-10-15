from app import create_app

def test_logs_endpoint_smoke():
    app = create_app()
    client = app.test_client()
    resp = client.get('/logs/')
    assert resp.status_code == 200
