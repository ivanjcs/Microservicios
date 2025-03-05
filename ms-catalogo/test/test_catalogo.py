import pytest
from flask import json
from app import create_app 
from app.services import CommerceService, ProductoService
from unittest.mock import patch

@pytest.fixture
def client():
    app = create_app()
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client

@patch.object(ProductoService, 'find')
def test_get_producto_existente(mock_find, client):
    mock_find.return_value = {"id": 1, "nombre": "Producto X"}
    response = client.get("/catalogo/productos/1")
    
    assert response.status_code == 200
    assert response.json == {"id": 1, "nombre": "Producto X"}
    mock_find.assert_called_once_with(1)

@patch.object(ProductoService, 'find')
def test_get_producto_no_existente(mock_find, client):
    mock_find.return_value = None
    response = client.get("/catalogo/productos/999")
    
    assert response.status_code == 404
    assert response.json == {}  # Respuesta esperada si no se encuentra el producto
    mock_find.assert_called_once_with(999)
