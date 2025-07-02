import json
from pathlib import Path
import pytest
from unittest.mock import patch, mock_open


def test_get_licenses(client):
    client.post('/api/v1/auth/test-login')  # Fake-Login
    response = client.get('/api/v1/licenses/')
    assert response.status_code == 200
    assert b'Test License 1' in response.data
    assert b'Test License 2' in response.data


def test_get_license_by_id(client):
    client.post('/api/v1/auth/test-login')  # Fake-Login
    response = client.get('/api/v1/licenses/1')
    assert response.status_code == 200
    assert b'Test License 1' in response.data


def test_create_license(client):
    client.post('/api/v1/auth/test-login')  # Fake-Login
    payload = {"name": "New License", "count": 3}
    response = client.post('/api/v1/licenses/', json=payload)
    assert response.status_code == 201
    assert b'New License' in response.data


@patch("app.licenses.routes.GraphLicenseClient")
@patch("builtins.open", new_callable=mock_open, read_data='{"tenant_name": "Test Tenant"}')
def test_get_license_status_tenant_show(mock_open_file, mock_graph_client, client):
    client.post('/api/v1/auth/test-login')
    mock_graph_client.return_value.get_license_status.return_value = {
        "value": [
            {
                "skuId": "sku-abc",
                "skuPartNumber": "SKU_X",
                "consumedUnits": 2,
                "prepaidUnits": {"enabled": 5}
            }
        ]
    }

    response = client.get('/api/v1/licenses/status/show/test-tenant')
    assert response.status_code == 200
    assert b"sku-abc" in response.data
    assert b"SKU_X" in response.data


@patch("app.licenses.routes.GraphLicenseClient")
@patch("app.licenses.routes.SharePointClientTask")
@patch("builtins.open", new_callable=mock_open, read_data='{"tenant_name": "Test Tenant"}')
@patch("pathlib.Path.glob")
def test_get_license_all_showfetch(mock_glob, mock_open_file, mock_sharepoint, mock_graph_client, client):
    client.post('/api/v1/auth/test-login')

    mock_graph_client.return_value.get_license_status.return_value = {
        "value": [
            {
                "skuId": "sku-def",
                "skuPartNumber": "SKU_Y",
                "consumedUnits": 3,
                "prepaidUnits": {"enabled": 7}
            }
        ]
    }

    mock_glob.return_value = [Path("config-profiles/config-test-tenant-profile.json")]

    response = client.get('/api/v1/licenses/status/show-fetch')
    assert response.status_code == 200
    assert b"sku-def" in response.data
    assert mock_sharepoint.push_license_status_to_sharepoint.called


@patch("app.licenses.routes.GraphLicenseClient")
@patch("app.licenses.routes.SharePointClientTask")
@patch("builtins.open", new_callable=mock_open, read_data='{"tenant_name": "Test Tenant"}')
def test_get_license_status_tenant_showfetch(mock_open_file, mock_sharepoint, mock_graph_client, client):
    client.post('/api/v1/auth/test-login')

    mock_graph_client.return_value.get_license_status.return_value = {
        "value": [
            {
                "skuId": "sku-xyz",
                "skuPartNumber": "SKU_Z",
                "consumedUnits": 1,
                "prepaidUnits": {"enabled": 4}
            }
        ]
    }

    response = client.get('/api/v1/licenses/status/show-fetch/test-tenant')
    assert response.status_code == 200
    assert b"sku-xyz" in response.data
    assert b"SKU_Z" in response.data
    assert mock_sharepoint.push_license_status_to_sharepoint.called


@patch("builtins.open", side_effect=FileNotFoundError("Config not found"))
def test_get_license_status_tenant_show_error(mock_open_file, client):
    client.post('/api/v1/auth/test-login')
    response = client.get('/api/v1/licenses/status/show/missing-tenant')
    assert response.status_code == 200
    assert response.json == []


# 🆕 Erweiterte Tests zur Abdeckung

@patch("app.licenses.routes.GraphLicenseClient")
@patch("builtins.open", new_callable=mock_open, read_data='{"tenant_name": "Test Tenant"}')
@patch("pathlib.Path.glob")
def test_get_license_show_all(mock_glob, mock_open_file, mock_graph_client, client):
    client.post('/api/v1/auth/test-login')
    mock_graph_client.return_value.get_license_status.return_value = {
        "value": [
            {
                "skuId": "sku-show",
                "skuPartNumber": "SKU_SHOW",
                "consumedUnits": 2,
                "prepaidUnits": {"enabled": 5}
            }
        ]
    }
    mock_glob.return_value = [Path("config-profiles/config-test-tenant-profile.json")]

    response = client.get('/api/v1/licenses/status/show')
    assert response.status_code == 200
    assert b"sku-show" in response.data
    assert b"SKU_SHOW" in response.data


@patch("builtins.open", new_callable=mock_open, read_data='{"tenant_name": "Test Tenant"}')
@patch("app.licenses.routes.GraphLicenseClient")
@patch("app.licenses.routes.SharePointClientTask")
def test_get_license_status_tenant_showfetch_error(mock_sharepoint, mock_graph_client, mock_open_file, client):
    client.post('/api/v1/auth/test-login')
    mock_graph_client.return_value.get_license_status.side_effect = Exception("API Error")

    response = client.get('/api/v1/licenses/status/show-fetch/test-tenant')
    assert response.status_code == 200
    assert response.json == []


def test_get_status_pages(client):
    client.post('/api/v1/auth/test-login')

    response1 = client.get('/api/v1/licenses/status/tenant')
    response2 = client.get('/api/v1/licenses/statusall')

    assert response1.status_code == 200
    assert response2.status_code == 200
    assert b"<" in response1.data
    assert b"<" in response2.data


@patch("builtins.open", new_callable=mock_open, read_data="{ invalid json")
def test_get_license_status_tenant_invalid_json(mock_open_file, client):
    client.post('/api/v1/auth/test-login')
    response = client.get('/api/v1/licenses/status/show/test-tenant')
    assert response.status_code == 200
    assert response.json == []
