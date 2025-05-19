from test import client

def test_get_license(client):
    """Test the get license endpoint."""
    response = client.get('/license')
    assert response.status_code == 200
    assert b'License' in response.data
    
def test_get_license_by_id(client):
    """Test the get license by id endpoint."""
    response = client.get('/license/1')
    assert response.status_code == 200
    assert b'License' in response.data
    
def test_get_license_by_id_not_found(client):
    """Test the get license by id endpoint with a non-existing id."""
    response = client.get('/license/99999999')
    assert response.status_code == 404
    assert b'License not found' in response.data