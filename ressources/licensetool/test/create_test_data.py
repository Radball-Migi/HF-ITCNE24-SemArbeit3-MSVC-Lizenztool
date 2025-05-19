from app.extensions import db
from app.models.license import LicenseModel

def create_test_data():
    db.drop_all() # Drop all tables
    db.create_all() # Create all tables
    
    # Create test data
    license1 = LicenseModel(name='Test License 1', description='This is a test license 1')
    license2 = LicenseModel(name='Test License 2', description='This is a test license 2')
    
    # Add test data to the session    
    db.session.add(license1)
    db.session.add(license2)
    db.session.commit()
    
    
