from fastapi.testclient import TestClient
from ..root_app.root_app import app

client = TestClient(app)

def test_homepage():
        response = client.get('/')
        assert response.status_code == 200
        assert response.template.name == 'index.html'
        assert "request" in response.context