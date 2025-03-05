import pytest
from flask import json
from app import create_app 
from app.services import PagoService
from unittest.mock import patch

@pytest.fixture
def client():
    app = create_app()
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client

@patch.object(PagoService, 'registrar_pago')
def test_registrar_pago(mock_registrar, client):
    mock_registrar.return_value = {"id": 1, "producto": "Producto X", "precio": 100.0, "medio_pago": "tarjeta"}
    pago_data = {"producto": "Producto X", "precio": 100.0, "medio_pago": "tarjeta"}
    response = client.post("/pagos/registrar", data=json.dumps(pago_data), content_type='application/json')
    
    assert response.status_code == 200
    assert response.json["id"] == 1
    mock_registrar.assert_called_once()

@patch.object(PagoService, 'find_by_id')
@patch.object(PagoService, 'cancelar_pago')
def test_cancelar_pago(mock_cancelar, mock_find, client):
    mock_find.return_value = {"id": 1, "producto": "Producto X", "precio": 100.0, "medio_pago": "tarjeta"}
    mock_cancelar.return_value = {"id": 1, "producto": "Producto X", "precio": 100.0, "medio_pago": "tarjeta", "estado": "cancelado"}
    
    response = client.put("/pagos/cancelar/1")
    
    assert response.status_code == 200
    assert response.json["estado"] == "cancelado"
    mock_find.assert_called_once_with(1)
    mock_cancelar.assert_called_once()

@patch.object(PagoService, 'find_by_id')
def test_cancelar_pago_no_existente(mock_find, client):
    mock_find.return_value = None
    response = client.put("/pagos/cancelar/999")
    
    assert response.status_code == 400
    assert response.json == {}
    mock_find.assert_called_once_with(999)
