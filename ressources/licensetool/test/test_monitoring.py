from test import client
from unittest.mock import patch
import json


@patch("app.monitoring.routes.render_template")
def test_show_monitoring(mock_render, client):
    client.post('/api/v1/auth/test-login')  # Fake-Login
    mock_render.return_value = "Monitoring Seite"
    response = client.get("/api/v1/monitoring/")
    assert response.status_code == 200
    assert b"Monitoring Seite" in response.data


@patch("app.monitoring.routes.SharePointClientTask.get_tenants_from_sharepoint")
def test_api_get_monitoring_tenants(mock_get, client):
    client.post('/api/v1/auth/test-login')  # Fake-Login
    mock_get.return_value = [{"name": "Tenant A"}, {"name": "Tenant B"}]
    response = client.get("/api/v1/monitoring/tenants")
    assert response.status_code == 200
    data = json.loads(response.data)
    assert len(data) == 2


@patch("app.monitoring.routes.SharePointClientTask.update_tenant_fields")
def test_update_tenant_monitoring_success(mock_update, client):
    client.post('/api/v1/auth/test-login')  # Fake-Login
    mock_update.return_value = {"enabled": True}
    payload = json.dumps({"enabled": True})
    response = client.patch("/api/v1/monitoring/tenants/1", data=payload, content_type="application/json")
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data["success"] is True


def test_update_tenant_monitoring_invalid_payload(client):
    client.post('/api/v1/auth/test-login')  # Fake-Login
    response = client.patch("/api/v1/monitoring/tenants/1", data=json.dumps({}), content_type="application/json")
    assert response.status_code == 400
    assert b"Kein Wert zum Aktualisieren" in response.data
