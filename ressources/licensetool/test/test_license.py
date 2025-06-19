from unittest.mock import patch


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
def test_get_license_show_all(mock_graph_client, client):
    client.post('/api/v1/auth/test-login')  # Fake-Login
    mock_graph_client.return_value.get_license_status.return_value = {
        "value": [
            {
                "skuId": "sku-123",
                "skuPartNumber": "SKU_A",
                "consumedUnits": 5,
                "prepaidUnits": {"enabled": 10}
            }
        ]
    }

    response = client.get('/api/v1/licenses/status/show')
    assert response.status_code == 200
    assert b"sku-123" in response.data
