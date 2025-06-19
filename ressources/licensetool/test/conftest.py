import pytest
from app import create_app
from app.extensions import db as _db
from test.create_test_data import create_test_data
from config import TestingConfig

@pytest.fixture(scope='session')
def app():
    app = create_app(TestingConfig)
    return app

@pytest.fixture(scope='session')
def db(app):
    with app.app_context():
        _db.create_all()
        yield _db
        _db.drop_all()

@pytest.fixture(scope='function')
def client(app, db):
    with app.app_context():
        create_test_data()
        test_client = app.test_client()
        test_client.post('/api/v1/auth/test-login')
        yield test_client
        db.session.remove()
        db.get_engine().dispose()