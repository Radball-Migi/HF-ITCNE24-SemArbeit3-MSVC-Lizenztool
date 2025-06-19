from app.extensions import db
from app.models.license import LicenseModel

def create_test_data():
    db.drop_all()
    db.create_all()

    db.session.add_all([
        LicenseModel(name='Test License 1', count=10),
        LicenseModel(name='Test License 2', count=5),
    ])
    db.session.commit()