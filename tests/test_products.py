"""
Product Tests
"""

import pytest


def test_create_product(client, auth_headers):
    response = client.post('/api/v1/products', 
                          json={
                              'name': 'Test Product',
                              'sku': 'TEST001',
                              'category': 'Test',
                              'base_unit': 'pcs',
                              'cost_price': 10000,
                              'stock': 100
                          },
                          headers=auth_headers)
    assert response.status_code == 201


def test_list_products(client, auth_headers):
    response = client.get('/api/v1/products', headers=auth_headers)
    assert response.status_code == 200
