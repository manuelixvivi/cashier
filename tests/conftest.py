"""
Test Configuration
"""

import pytest


@pytest.fixture
def auth_headers(client):
    # Register and login to get token
    client.post('/api/v1/auth/register', json={
        'username': 'testadmin',
        'email': 'admin@example.com',
        'password': 'password123',
        'role': 'admin'
    })

    response = client.post('/api/v1/auth/login', json={
        'username': 'testadmin',
        'password': 'password123'
    })

    token = response.get_json()['data']['access_token']
    return {'Authorization': f'Bearer {token}'}
