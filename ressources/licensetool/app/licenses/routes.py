from apiflask import Schema
from flask import render_template
from app.extensions import db
from app.licenses import bp
from apiflask.fields import Integer as APIInteger, String as APIString
from apiflask.validators import Length
from app.models.license import LicenseModel, LicenseIn, LicenseOut


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
<<<<<<< Updated upstream
=======


@bp.get('/frontend')
def show_frontend():
    return render_template("frontend.html")


@bp.get('/status/<tenant_name>')
@bp.output(LicenseStatusOut(many=True))
def get_license_status(tenant_name):

    client = GraphLicenseClient(tenant_name)
    #return client.get_license_status()

### Commented out, because for the first tests we need the whole informations, to build up the MSVC
### These below the commented is used to filter the informations. It is relatet to the commented out above @bp.output(LicenseStatusOut(many=True))
### The goal is that we can only show the skuid, skupartnumber, consumed units and available units. 

    data = client.get_license_status()
    
    licenses = []
    for item in data.get("value", []):
        consumed = item.get('consumedUnits', 0)
        available = item.get('prepaidUnits', {}).get('enabled', 0)
        free = int(available) - int(consumed)

        licenses.append({
            'skuid': item.get('skuId', 'UNKNOWN'),
            'skupartnumber': item.get('skuPartNumber', 'UNKNOWN'),
            'consumed_units': consumed,
            'available_units': available,
            'free_units': free
        })

    return licenses
>>>>>>> Stashed changes
