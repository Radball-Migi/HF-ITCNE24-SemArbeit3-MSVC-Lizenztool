from test import client

def test_get_licenses(client):
    """Test the get license endpoint."""
    response = client.get('/api/v1/licenses/')
    assert response.status_code == 200
    assert b'Test License 1' in response.data
    
def test_get_license_by_id(client):
    """Test the get license by id endpoint."""
    response = client.get('/api/v1/licenses/1')
    assert response.status_code == 200
    assert b'Test License 1' in response.data
    
def test_get_license_by_id_not_found(client):
    """Test the get license by id endpoint with a non-existing id."""
    response = client.get('/api/v1/licenses/99999999')
    assert response.status_code == 404