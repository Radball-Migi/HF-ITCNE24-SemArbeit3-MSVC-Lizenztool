from apiflask import Schema
from flask import render_template
from app.extensions import db
from app.licenses import bp
from apiflask.fields import Integer as APIInteger, String as APIString
from apiflask.validators import Length
from app.models.license import LicenseModel, LicenseIn, LicenseOut, LicenseStatusOut, LicenseStatusAllOut
from app.modules.mggraph import GraphLicenseClient
from pathlib import Path
import re
import json

# Templates-Route
@bp.get('/frontend')
def show_frontend():
    return render_template("frontend.html")

@bp.get('/statusall')
def show_status_all():
    return render_template("statusall.html")


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


@bp.get('/status')
@bp.output(LicenseStatusAllOut(many=True))
def get_license_all():
    config_path = Path("config-profiles")
    statusall = []

    for config_file in config_path.glob("config-*-profile.json"):
        match = re.match(r"config-(.*?)-profile\.json", config_file.name)
        if not match:
            continue

        tenant_id = match.group(1)

        try:
            with open(config_file, "r") as f:
                config_data = json.load(f)

            display_name = config_data.get("tenant_name") or config_data.get("name") or tenant_id

            client = GraphLicenseClient(tenant_id)
            data = client.get_license_status()

            for item in data.get("value", []):
                consumed = item.get('consumedUnits', 0)
                available = item.get('prepaidUnits', {}).get('enabled', 0)
                free = int(available) - int(consumed)

                statusall.append({
                    'skuid': item.get('skuId', 'UNKNOWN'),
                    'skupartnumber': item.get('skuPartNumber', 'UNKNOWN'),
                    'consumed_units': consumed,
                    'available_units': available,
                    'free_units': free,
                    'tenant': display_name
                })

        except Exception as e:
            print(f"Fehler bei Tenant {tenant_id}: {e}")
            continue

    return statusall

@bp.get('/status/<tenant_name>')
@bp.output(LicenseStatusOut(many=True))
def get_license_status(tenant_name):
    client = GraphLicenseClient(tenant_name)
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