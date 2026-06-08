"""
Auth Tests
"""

import pytest
from app import create_app


@pytest.fixture
def app():
    app = create_app()
    app.config['TESTING'] = True
    app.config['MONGO_URI'] = 'mongodb://localhost:27017/pos_ai_test'
    yield app


@pytest.fixture
def client(app):
    return app.test_client()


def test_health_check(client):
    response = client.get('/health')
    assert response.status_code == 200
    data = response.get_json()
    assert data['success'] is True
    assert data['data']['status'] == 'healthy'


def test_register(client):
    response = client.post('/api/v1/auth/register', json={
        'username': 'testuser',
        'email': 'test@example.com',
        'password': 'password123',
        'full_name': 'Test User'
    })
    assert response.status_code == 201


def test_login(client):
    # First register
    client.post('/api/v1/auth/register', json={
        'username': 'logintest',
        'email': 'login@example.com',
        'password': 'password123'
    })

    # Then login
    response = client.post('/api/v1/auth/login', json={
        'username': 'logintest',
        'password': 'password123'
    })
    assert response.status_code == 200
    data = response.get_json()
    assert 'access_token' in data['data']
