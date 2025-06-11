from apiflask import Schema
from flask import render_template
from app.extensions import db
from app.licenses import bp
from apiflask.fields import Integer as APIInteger, String as APIString
from apiflask.validators import Length
from app.models.license import LicenseModel, LicenseIn, LicenseOut, LicenseStatusOut, LicenseStatusAllOut
from app.modules.mggraph import GraphLicenseClient, push_license_status_to_sharepoint
from pathlib import Path
import re
import json

# Templates-Route
@bp.get('/status/tenant')
def show_frontend():
    return render_template("tenant.html")

@bp.get('/statusall')
def show_status_all():
    return render_template("statusall.html")

#--------------------------------------------------------
# API-Routen für Lizenzen

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


@bp.get('/status/show')
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

            licenses = []

            for item in data.get("value", []):
                consumed = item.get('consumedUnits', 0)
                available = item.get('prepaidUnits', {}).get('enabled', 0)
                free = int(available) - int(consumed)

                license_info = {
                    'skuid': item.get('skuId', 'UNKNOWN'),
                    'skupartnumber': item.get('skuPartNumber', 'UNKNOWN'),
                    'consumed_units': consumed,
                    'available_units': available,
                    'free_units': free,
                    'tenant': display_name
                }

                licenses.append(license_info)
                statusall.append(license_info)

        except Exception as e:
            print(f"Fehler bei Tenant {tenant_id}: {e}")
            continue

    return statusall
   
@bp.get('/status/show/<tenant_name>')
@bp.output(LicenseStatusOut(many=True))
def get_license_status_tenant_show(tenant_name):
    try:
        config_file = f"config-profiles/config-{tenant_name}-profile.json"
        with open(config_file, "r") as f:
            config_data = json.load(f)

        client = GraphLicenseClient(tenant_name)
        data = client.get_license_status()
        display_name = config_data.get("tenant_name")

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

        print(display_name)

        return licenses

    except Exception as e:
        print(f"Fehler beim Abrufen von Lizenzdaten für {tenant_name}: {e}")
        return []
    

@bp.get('/status/show-fetch')
@bp.output(LicenseStatusAllOut(many=True))
def get_license_all_showfetch():
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

            licenses = []

            for item in data.get("value", []):
                consumed = item.get('consumedUnits', 0)
                available = item.get('prepaidUnits', {}).get('enabled', 0)
                free = int(available) - int(consumed)

                license_info = {
                    'skuid': item.get('skuId', 'UNKNOWN'),
                    'skupartnumber': item.get('skuPartNumber', 'UNKNOWN'),
                    'consumed_units': consumed,
                    'available_units': available,
                    'free_units': free,
                    'tenant': display_name
                }

                licenses.append(license_info)
                statusall.append(license_info)

            # Push Lizenzdaten für diesen Tenant ins SharePoint
            push_license_status_to_sharepoint(display_name, licenses)

        except Exception as e:
            print(f"Fehler bei Tenant {tenant_id}: {e}")
            continue

    return statusall

@bp.get('/status/show-fetch/<tenant_name>')
@bp.output(LicenseStatusOut(many=True))
def get_license_status_tenant_showfetch(tenant_name):
    try:
        config_file = f"config-profiles/config-{tenant_name}-profile.json"
        print(f"[DEBUG] Lade Konfigurationsdatei: {config_file}")

        with open(config_file, "r") as f:
            config_data = json.load(f)

        display_name = config_data.get("tenant_name")
        print(f"[DEBUG] Display-Name aus Konfig: {display_name}")

        client = GraphLicenseClient(tenant_name)
        data = client.get_license_status()

        print(f"[DEBUG] Daten vom Graph-Client für {tenant_name}:")
        import json as jsonlib
        print(jsonlib.dumps(data, indent=2))

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

        # Optional: Push in SharePoint
        push_license_status_to_sharepoint(display_name, licenses)

        print(f"[DEBUG] Lizenzliste ({len(licenses)} Einträge) erfolgreich erstellt.")
        return licenses

    except Exception as e:
        print(f"[ERROR] Fehler beim Abrufen von Lizenzdaten für '{tenant_name}': {e}")
        import traceback
        traceback.print_exc()
        return []
