from apiflask import Schema
from flask import render_template
from app.extensions import db
from app.licenses import bp
from apiflask.fields import Integer as APIInteger, String as APIString
from apiflask.validators import Length
from app.models.license import LicenseModel, LicenseIn, LicenseOut, LicenseStatusOut, LicenseStatusAllOut
from app.modules.mggraph import GraphLicenseClient, SharePointClientTask
from pathlib import Path
from app.auth.utils import login_required
from app.modules.sku_mapping import SKU_DISPLAY_NAMES
import re
import json
import logging

# Logger definieren
logger = logging.getLogger(__name__)

# Templates-Route
@bp.get('/status/tenant')
@login_required
def show_tenant():
    logger.info("Tenant-Status-Seite angezeigt")
    return render_template("tenant.html")

@bp.get('/statusall')
@login_required
def show_status_all():
    logger.info("StatusAll-Seite angezeigt")
    return render_template("statusall.html")

#--------------------------------------------------------
# API-Routen für Lizenzen

@bp.get('/')
@bp.output(LicenseOut(many=True))
@login_required
def get_licenses():
    logger.info("Alle Lizenzen abgefragt")
    licenses = LicenseModel.query.all()
    return licenses

@bp.get('/<int:license_id>')
@bp.output(LicenseOut)
@login_required
def get_license(license_id):
    logger.info(f"Abfrage Lizenz mit ID: {license_id}")
    license = LicenseModel.query.get_or_404(license_id)
    return license

@bp.post('/')
@bp.input(LicenseIn, location='json')
@bp.output(LicenseOut, status_code=201)
@login_required
def create_license(json_data):
    logger.info(f"Neue Lizenz wird erstellt: {json_data}")
    license = LicenseModel(**json_data)
    db.session.add(license)
    db.session.commit()
    logger.info(f"Lizenz erfolgreich gespeichert: ID={license.id}")
    return license

@bp.get('/status/show')
@bp.output(LicenseStatusAllOut(many=True))
@login_required
def get_license_show_all():
    logger.info("Alle Lizenzstatus werden geladen (status/show)")
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

            tenant_display_name = config_data.get("tenant_name") or config_data.get("name") or tenant_id
            logger.info(f"Lade Lizenzstatus für Tenant: {tenant_display_name}")

            client = GraphLicenseClient(tenant_id)
            data = client.get_license_status()

            for item in data.get("value", []):
                consumed = item.get('consumedUnits', 0)
                available = item.get('prepaidUnits', {}).get('enabled', 0)
                free = int(available) - int(consumed)
                sku_display_name = SKU_DISPLAY_NAMES.get(item.get('skuPartNumber'), item.get('skuPartNumber'))

                license_info = {
                    'skuid': item.get('skuId', 'UNKNOWN'),
                    'skupartnumber': f"{sku_display_name}<br>({item.get('skuPartNumber', 'UNKNOWN')})",
                    'consumed_units': consumed,
                    'available_units': available,
                    'free_units': free,
                    'tenant': tenant_display_name
                }

                statusall.append(license_info)

        except Exception as e:
            logger.exception(f"Fehler bei Tenant {tenant_id}: {e}")
            continue

    logger.info(f"{len(statusall)} Lizenzeinträge geladen")
    return statusall

@bp.get('/status/show/<tenant_name>')
@bp.output(LicenseStatusOut(many=True))
@login_required
def get_license_status_tenant_show(tenant_name):
    try:
        config_file = f"config-profiles/config-{tenant_name}-profile.json"
        logger.info(f"Lade Lizenzstatus für Tenant '{tenant_name}'")

        with open(config_file, "r") as f:
            config_data = json.load(f)

        client = GraphLicenseClient(tenant_name)
        data = client.get_license_status()
        tenant_display_name = config_data.get("tenant_name")

        licenses = []
        for item in data.get("value", []):
            consumed = item.get('consumedUnits', 0)
            available = item.get('prepaidUnits', {}).get('enabled', 0)
            free = int(available) - int(consumed)
            sku_display_name = SKU_DISPLAY_NAMES.get(item.get('skuPartNumber'), item.get('skuPartNumber'))

            licenses.append({
                'skuid': item.get('skuId', 'UNKNOWN'),
                'skupartnumber': f"{sku_display_name}<br>({item.get('skuPartNumber', 'UNKNOWN')})",
                'consumed_units': consumed,
                'available_units': available,
                'free_units': free
            })

        logger.info(f"{len(licenses)} Einträge für Tenant '{tenant_name}' geladen")
        return licenses

    except Exception as e:
        logger.exception(f"Fehler beim Abrufen von Lizenzdaten für {tenant_name}")
        return []

@bp.get('/status/show-fetch')
@bp.output(LicenseStatusAllOut(many=True))
@login_required
def get_license_all_showfetch():
    logger.info("Starte Fetch und Push für alle Tenants (status/show-fetch)")
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

            tenant_display_name = config_data.get("tenant_name") or config_data.get("name") or tenant_id
            logger.info(f"Verarbeite Tenant: {tenant_display_name}")

            client = GraphLicenseClient(tenant_id)
            data = client.get_license_status()

            licenses = []
            for item in data.get("value", []):
                consumed = item.get('consumedUnits', 0)
                available = item.get('prepaidUnits', {}).get('enabled', 0)
                free = int(available) - int(consumed)
                sku_display_name = SKU_DISPLAY_NAMES.get(item.get('skuPartNumber'), item.get('skuPartNumber'))

                license_info = {
                    'skuid': item.get('skuId', 'UNKNOWN'),
                    'skupartnumber': f"{sku_display_name} ({item.get('skuPartNumber', 'UNKNOWN')})",
                    'consumed_units': consumed,
                    'available_units': available,
                    'free_units': free,
                    'tenant': tenant_display_name
                }

                licenses.append(license_info)
                statusall.append(license_info)

            SharePointClientTask.push_license_status_to_sharepoint(tenant_display_name, licenses)
            logger.info(f"Push an SharePoint abgeschlossen für Tenant: {tenant_display_name}")

        except Exception as e:
            logger.exception(f"Fehler bei Tenant {tenant_id}")
            continue

    logger.info(f"Fetch & Push für {len(statusall)} Einträge abgeschlossen")
    return statusall

@bp.get('/status/show-fetch/<tenant_name>')
@bp.output(LicenseStatusOut(many=True))
@login_required
def get_license_status_tenant_showfetch(tenant_name):
    try:
        config_file = f"config-profiles/config-{tenant_name}-profile.json"
        logger.info(f"Lade Konfiguration für Tenant: {tenant_name}")

        with open(config_file, "r") as f:
            config_data = json.load(f)

        tenant_display_name = config_data.get("tenant_name")
        logger.info(f"Tenant-Displayname: {tenant_display_name}")

        client = GraphLicenseClient(tenant_name)
        data = client.get_license_status()

        licenses = []
        for item in data.get("value", []):
            consumed = item.get('consumedUnits', 0)
            available = item.get('prepaidUnits', {}).get('enabled', 0)
            free = int(available) - int(consumed)
            sku_display_name = SKU_DISPLAY_NAMES.get(item.get('skuPartNumber'), item.get('skuPartNumber'))

            licenses.append({
                'skuid': item.get('skuId', 'UNKNOWN'),
                'skupartnumber': f"{sku_display_name} ({item.get('skuPartNumber', 'UNKNOWN')})",
                'consumed_units': consumed,
                'available_units': available,
                'free_units': free
            })

        SharePointClientTask.push_license_status_to_sharepoint(tenant_display_name, licenses)
        logger.info(f"{len(licenses)} Lizenzen für {tenant_name} verarbeitet und übertragen")

        return licenses

    except Exception as e:
        logger.exception(f"Fehler beim Abrufen von Lizenzdaten für '{tenant_name}'")
        return []