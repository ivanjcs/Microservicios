import pytest
from flask import json
from app import create_app 
from app.services import CommerceService, ProductoService, CompraService
from unittest.mock import patch

@pytest.fixture
def client():
    app = create_app()
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client

@patch.object(CompraService, 'save')
def test_comprar_producto(mock_save, client):
    mock_save.return_value = {"id": 1, "producto": "Producto Y", "direccion_envio": "Calle 456"}
    compra_data = {"producto": "Producto Y", "direccion_envio": "Calle 456"}
    response = client.post("/compras", data=json.dumps(compra_data), content_type='application/json')
    
    assert response.status_code == 200
    assert response.json["id"] == 1
    mock_save.assert_called_once()

@patch.object(CompraService, 'delete')
def test_borrar_compra(mock_delete, client):
    mock_delete.return_value = {"id": 1, "deleted_at": "2025-03-05T12:00:00"}
    response = client.delete("/compras/1")
    
    assert response.status_code == 200
    assert "deleted_at" in response.json
    mock_delete.assert_called_once_with(1)

@patch.object(CompraService, 'delete')
def test_borrar_compra_fallida(mock_delete, client):
    mock_delete.return_value = {"id": 1, "deleted_at": None}
    response = client.delete("/compras/1")
    
    assert response.status_code == 500
    mock_delete.assert_called_once_with(1)
