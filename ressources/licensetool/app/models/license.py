from app.extensions import db
from apiflask import APIBlueprint, Schema
from apiflask.fields import Integer as APIInteger, String as APIString
from apiflask.validators import Length
from sqlalchemy.orm import relationship
from sqlalchemy import Table, Column, Integer as sa_Integer, String as sa_String, ForeignKey


class LicenseModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32))
    count = db.Column(db.Integer)

# Eingabe-Schema
class LicenseIn(Schema):
    name = APIString(required=True, validate=Length(min=1, max=32))
    count = APIInteger(required=True)

# Ausgabe-Schema
class LicenseOut(Schema):
    id = APIInteger()
    name = APIString()
    count = APIInteger()
    
class LicenseStatusOut(Schema):
    sku = APIString(required=True)
    consumed_units = APIInteger(required=True)
    available_units = APIInteger(required=True)