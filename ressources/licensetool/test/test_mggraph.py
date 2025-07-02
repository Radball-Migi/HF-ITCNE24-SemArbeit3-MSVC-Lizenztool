import pytest
from unittest.mock import patch, mock_open, MagicMock
from app.modules.mggraph import SharePointClientTask, GraphLicenseClient


@pytest.fixture
def dummy_config():
    return {
        "tenant_id": "dummy-tenant",
        "client_id": "dummy-client",
        "thumbprint": "dummy-thumbprint",
        "cert_path": "dummy-cert.pem"
    }


@patch("builtins.open", new_callable=mock_open, read_data='{"tenant_id": "dummy-tenant", "client_id": "dummy-client", "thumbprint": "thumb", "cert_path": "dummy-cert.pem"}')
@patch("msal.ConfidentialClientApplication.acquire_token_for_client", return_value={"access_token": "dummy-token"})
@patch("msal.ConfidentialClientApplication.__init__", return_value=None)
@patch("requests.get")
def test_graph_license_client_success(mock_get, mock_init, mock_token, mock_open_file):
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"value": [{"skuId": "sku", "skuPartNumber": "part", "consumedUnits": 1, "prepaidUnits": {"enabled": 2}}]}
    mock_get.return_value = mock_response

    client = GraphLicenseClient("test-tenant")
    result = client.get_license_status()

    assert "value" in result
    assert mock_get.called
    assert client.token == "dummy-token"


@patch("builtins.open", new_callable=mock_open, read_data='{"tenant_id": "dummy-tenant", "client_id": "dummy-client", "thumbprint": "thumb", "cert_path": "dummy-cert.pem"}')
@patch("msal.ConfidentialClientApplication.acquire_token_for_client", return_value={"error_description": "invalid client"})
@patch("msal.ConfidentialClientApplication.__init__", return_value=None)
def test_authentication_failure(mock_init, mock_token, mock_open_file):
    with pytest.raises(Exception, match="Token acquisition failed"):
        GraphLicenseClient("test-tenant")


@patch("builtins.open", new_callable=mock_open, read_data='{"tenant_id": "dummy", "client_id": "dummy", "thumbprint": "dummy", "cert_path": "dummy.pem", "sharepoint_infos": {"site_id": "1", "license_list_id": "2", "tenant_list_id": "3", "field_mapping": {"Frei": "free", "Gebraucht": "used", "Verfügbar": "avail", "Infosup": "infosup", "Tenant": "Tenant", "Lizenzname": "Title"}, "tenant_field": "Tenant"}}')
@patch("msal.ConfidentialClientApplication.acquire_token_for_client", return_value={"access_token": "dummy-token"})
@patch("msal.ConfidentialClientApplication.__init__", return_value=None)
@patch("requests.get")
@patch("requests.patch")
@patch("requests.post")
def test_push_license_status_to_sharepoint(mock_post, mock_patch, mock_get, mock_init, mock_token, mock_open_file):
    mock_get.side_effect = [
        MagicMock(status_code=200, json=lambda: {"value": [{"fields": {"Title": "Tenant X", "enabled": True}}]}),
        MagicMock(status_code=200, json=lambda: {"value": []})
    ]
    mock_patch.return_value.status_code = 204
    mock_post.return_value.status_code = 201

    SharePointClientTask.push_license_status_to_sharepoint("Tenant X", [
        {"skupartnumber": "Test SKU", "consumed_units": 1, "available_units": 2, "free_units": 1}
    ])

    assert mock_get.call_count == 2
    assert mock_post.called or mock_patch.called


@patch("builtins.open", new_callable=mock_open, read_data='{"tenant_id": "dummy", "client_id": "dummy", "thumbprint": "dummy", "cert_path": "dummy.pem", "sharepoint_infos": {"site_id": "1", "license_list_id": "2", "tenant_list_id": "3", "field_mapping": {"Frei": "free", "Gebraucht": "used", "Verfügbar": "avail", "Infosup": "infosup", "Tenant": "Tenant", "Lizenzname": "Title"}, "tenant_field": "Tenant"}}')
@patch("msal.ConfidentialClientApplication.acquire_token_for_client", return_value={"access_token": "dummy-token"})
@patch("msal.ConfidentialClientApplication.__init__", return_value=None)
@patch("requests.get")
def test_push_license_status_inactive_tenant(mock_get, mock_init, mock_token, mock_open_file):
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = {"value": [{"fields": {"Title": "Tenant Y", "enabled": False}}]}

    SharePointClientTask.push_license_status_to_sharepoint("Tenant Y", [])
    mock_get.assert_called_once()


@patch("builtins.open", side_effect=FileNotFoundError)
def test_config_file_not_found(mock_open_file):
    with pytest.raises(FileNotFoundError):
        GraphLicenseClient("missing-tenant")


# -------- Erweiterte Tests --------

@patch("builtins.open", new_callable=mock_open, read_data='{"tenant_id": "t", "client_id": "c", "thumbprint": "tp", "cert_path": "cert.pem", "sharepoint_infos": {"site_id": "1", "tenant_list_id": "2"}}')
@patch("msal.ConfidentialClientApplication.acquire_token_for_client", return_value={"access_token": "token"})
@patch("msal.ConfidentialClientApplication.__init__", return_value=None)
@patch("requests.get")
def test_get_tenants_from_sharepoint(mock_get, mock_init, mock_token, mock_open_file):
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = {
        "value": [
            {"id": "1", "fields": {"Title": "Tenant1", "enabled": True, "monitoring": False}},
            {"id": "2", "fields": {"Title": "Tenant2", "enabled": False, "monitoring": True}}
        ]
    }
    tenants = SharePointClientTask.get_tenants_from_sharepoint()
    assert len(tenants) == 2
    assert tenants[0]["title"] == "Tenant1"


@patch("builtins.open", new_callable=mock_open, read_data='{"tenant_id": "t", "client_id": "c", "thumbprint": "tp", "cert_path": "cert.pem", "sharepoint_infos": {"site_id": "1", "tenant_list_id": "2"}}')
@patch("msal.ConfidentialClientApplication.acquire_token_for_client", return_value={"access_token": "token"})
@patch("msal.ConfidentialClientApplication.__init__", return_value=None)
@patch("requests.patch")
def test_update_tenant_fields(mock_patch, mock_init, mock_token, mock_open_file):
    mock_patch.return_value.status_code = 204
    result = SharePointClientTask.update_tenant_fields(item_id=1, enabled=True, monitoring=False)
    assert result["updated"]["enabled"] is True
    assert result["updated"]["monitoring"] is False


@patch("builtins.open", new_callable=mock_open, read_data='{"tenant_id": "t", "client_id": "c", "thumbprint": "tp", "cert_path": "cert.pem", "sharepoint_infos": {"site_id": "1", "tenant_list_id": "2"}}')
@patch("msal.ConfidentialClientApplication.acquire_token_for_client", return_value={"access_token": "token"})
@patch("msal.ConfidentialClientApplication.__init__", return_value=None)
def test_update_tenant_fields_no_fields(mock_init, mock_token, mock_open_file):
    with pytest.raises(Exception, match="Keine Felder zum Aktualisieren"):
        SharePointClientTask.update_tenant_fields(item_id=1)



@patch("builtins.open", new_callable=mock_open, read_data='{"tenant_id": "t", "client_id": "c", "thumbprint": "tp", "cert_path": "cert.pem"}')
@patch("msal.ConfidentialClientApplication.__init__", return_value=None)
@patch("msal.ConfidentialClientApplication.acquire_token_for_client", return_value={"error_description": "fail"})
def test_sharepoint_authentication_error(mock_token, mock_init, mock_open_file):
    with pytest.raises(Exception, match="SharePoint Token error"):
        SharePointClientTask()


@patch("builtins.open", side_effect=FileNotFoundError)
def test_load_config_file_not_found(mock_open_file):
    with pytest.raises(FileNotFoundError):
        GraphLicenseClient("missing")


@patch("builtins.open", new_callable=mock_open, read_data="{invalid-json")
def test_load_config_json_error(mock_open_file):
    with pytest.raises(Exception):
        GraphLicenseClient("invalid")
