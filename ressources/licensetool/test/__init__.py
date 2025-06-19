import pytest
from app import create_app
from test.create_test_data import create_test_data

@pytest.fixture
def client():

    app = create_app()
    app.config.update({
        "TESTING": True,
    })
    client = app.test_client()

    with app.app_context():
        create_test_data()

    return client
