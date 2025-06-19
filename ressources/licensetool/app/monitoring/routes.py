from apiflask import Schema
from flask import render_template, request, Response
from app.extensions import db
from app.monitoring import bp
from apiflask.fields import Integer as APIInteger, String as APIString
from apiflask.validators import Length
from app.modules.mggraph import GraphLicenseClient, SharePointClientTask
from pathlib import Path
from app.auth.utils import login_required
import re
import json
import logging

logger = logging.getLogger(__name__)

# Templates-Route
@bp.get('/')
@login_required
def show_monitoring():
    logger.info("Monitoring-Übersichtsseite aufgerufen")
    return render_template("monitoring.html")


@bp.get('/tenants')
@login_required
def api_get_monitoring_tenants():
    logger.info("Abfrage aller Tenants über SharePoint gestartet")
    try:
        tenants = SharePointClientTask.get_tenants_from_sharepoint()
        logger.info(f"{len(tenants)} Tenants empfangen")
        return json.dumps(tenants), 200, {'Content-Type': 'application/json'}
    except Exception as e:
        logger.exception("Fehler beim Abrufen der Tenants aus SharePoint")
        return json.dumps({'error': str(e)}), 500, {'Content-Type': 'application/json'}


@bp.patch('/tenants/<int:item_id>')
@login_required
def update_tenant_monitoring(item_id):
    logger.info(f"Tenant-Update für ID {item_id} gestartet")
    try:
        raw_data = request.data.decode('utf-8')
        body = json.loads(raw_data)
        logger.debug(f"Rohdaten: {body}")

        enabled = body.get('enabled')
        monitoring = body.get('monitoring')

        if enabled is None and monitoring is None:
            logger.warning("Kein Wert zum Aktualisieren angegeben")
            return Response(
                json.dumps({'error': 'Kein Wert zum Aktualisieren angegeben.'}),
                status=400,
                content_type='application/json'
            )

        result = SharePointClientTask.update_tenant_fields(item_id, enabled=enabled, monitoring=monitoring)
        logger.info(f"Tenant {item_id} erfolgreich aktualisiert: {result}")

        return Response(
            json.dumps({'success': True, 'updated': result}),
            status=200,
            content_type='application/json'
        )

    except Exception as e:
        logger.exception(f"Fehler beim Aktualisieren von Tenant {item_id}")
        return Response(
            json.dumps({'error': str(e)}),
            status=500,
            content_type='application/json'
        )
