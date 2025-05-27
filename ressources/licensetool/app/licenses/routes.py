import os
from apiflask import Schema
from app.extensions import db
from app.licenses import bp
from apiflask.fields import Integer as APIInteger, String as APIString
from apiflask.validators import Length
from app.models.license import LicenseModel, LicenseIn, LicenseOut, LicenseStatusOut
from app.modules.mggraph import GraphLicenseClient


@bp.get('/')
@bp.output(LicenseOut(many=True))
def get_licenses():
    licenses = LicenseModel.query.all()
    return licenses


@bp.get('/<int:license_id>')
@bp.output(LicenseOut)
def get_license(license_id):
    license = LicenseModel.query.get_or_404(license_id)
    return license


@bp.post('/')
@bp.input(LicenseIn, location='json')
@bp.output(LicenseOut, status_code=201)
def create_license(json_data):
    license = LicenseModel(**json_data)
    db.session.add(license)
    db.session.commit()
    return license


@bp.get('/status/<tenant_name>')
#@bp.output(LicenseStatusOut(many=True))
def get_license_status(tenant_name):

    client = GraphLicenseClient(tenant_name)
    return client.get_license_status()

### Commented out, because for the first tests we need the whole informations, to build up the MSVC
### These below the commented is used to filter the informations. It is relatet to the commented out above @bp.output(LicenseStatusOut(many=True))

#    data = client.get_license_status()
#    
#    licenses = []
#    for item in data.get('value', []):
#        licenses.append({
#            'sku': item.get('skuPartNumber', UNKNOWN),
#           'consumed_units': item.get('consumedUnits', 0),
#            'available_units': item.get('prepaidUnits', {}).get('enabled', 0)
#        })
#    return licenses