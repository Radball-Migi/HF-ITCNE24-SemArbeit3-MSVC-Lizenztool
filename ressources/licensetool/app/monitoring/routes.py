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


# Templates-Route
@bp.get('/')
@login_required
def show_monitoring():
    return render_template("monitoring.html")


@bp.get('/tenants')
@login_required
def api_get_monitoring_tenants():
    try:
        tenants = SharePointClientTask.get_tenants_from_sharepoint()
        return json.dumps(tenants), 200, {'Content-Type': 'application/json'}
    except Exception as e:
        return json.dumps({'error': str(e)}), 500, {'Content-Type': 'application/json'}
    
@bp.patch('/tenants/<int:item_id>')
@login_required
def update_tenant_monitoring(item_id):
    try:
        # Raw body einlesen und mit json parsen
        raw_data = request.data.decode('utf-8')
        body = json.loads(raw_data)

        enabled = body.get('enabled')
        monitoring = body.get('monitoring')

        if enabled is None and monitoring is None:
            return Response(
                json.dumps({'error': 'Kein Wert zum Aktualisieren angegeben.'}),
                status=400,
                content_type='application/json'
            )

        result = SharePointClientTask.update_tenant_fields(item_id, enabled=enabled, monitoring=monitoring)

        return Response(
            json.dumps({'success': True, 'updated': result}),
            status=200,
            content_type='application/json'
        )

    except Exception as e:
        return Response(
            json.dumps({'error': str(e)}),
            status=500,
            content_type='application/json'
        )