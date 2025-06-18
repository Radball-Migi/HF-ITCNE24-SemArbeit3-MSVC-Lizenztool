# app/modules/mggraph.py

import json
import os
import requests
from urllib.parse import quote
from msal import ConfidentialClientApplication

class GraphLicenseClient:
    def __init__(self, tenant_name: str):
        self.tenant_name = tenant_name
        self.config = self._load_config()
        self.token = self._authenticate()

    def _load_config(self):
        config_file = f"config-profiles/config-{self.tenant_name}-profile.json"
        with open(config_file, "r") as f:
            return json.load(f)

    def _authenticate(self):
        authority = f"https://login.microsoftonline.com/{self.config['tenant_id']}"
        app = ConfidentialClientApplication(
            client_id=self.config['client_id'],
            authority=authority,
            client_credential={
                "private_key": open(self.config['cert_path'], "r").read(),
                "thumbprint": self.config['thumbprint']
            }
        )
        result = app.acquire_token_for_client(scopes=["https://graph.microsoft.com/.default"])
        if "access_token" not in result:
            raise Exception(f"Token acquisition failed: {result.get('error_description')}")
        return result["access_token"]

    def get_license_status(self):
        headers = {"Authorization": f"Bearer {self.token}"}
        response = requests.get("https://graph.microsoft.com/v1.0/subscribedSkus", headers=headers, timeout=10)
        if response.status_code != 200:
            raise Exception(f"Graph API error: {response.status_code} - {response.text}")
        return response.json()


class SharePointClient:
    def __init__(self):
        self.token = self._authenticate()

    def _authenticate(self):
        client_id = os.getenv("CLIENT_ID")
        tenant_id = os.getenv("TENANT_ID")
        thumbprint = os.getenv("THUMBPRINT")
        cert_path = os.getenv("CERT_PATH")

        authority = f"https://login.microsoftonline.com/{tenant_id}"
        app = ConfidentialClientApplication(
            client_id=client_id,
            authority=authority,
            client_credential={
                "private_key": open(cert_path, "r").read(),
                "thumbprint": thumbprint
            }
        )
        result = app.acquire_token_for_client(scopes=["https://graph.microsoft.com/.default"])
        if "access_token" not in result:
            raise Exception(f"SharePoint Token error: {result.get('error_description')}")
        return result["access_token"]


class SharePointClientTask(SharePointClient):
    def push_license_status_to_sharepoint(tenant_name: str, licenses: list):
        config_file = "config-profiles/sharepoint/sp-config-iseschool2013-profile.json"
        with open(config_file, "r") as f:
            config = json.load(f)

        # Auth-Infos
        tenant_id = config["tenant_id"]
        client_id = config["client_id"]
        thumbprint = config["thumbprint"]
        cert_path = config["cert_path"]
        sp_config = config["sharepoint_infos"]

        site_id = sp_config["site_id"]
        license_list_id = sp_config["license_list_id"]
        tenant_list_id = sp_config["tenant_list_id"]
        field_mapping = sp_config["field_mapping"]
        tenant_field = sp_config["tenant_field"]

        # Authentifizierung
        authority = f"https://login.microsoftonline.com/{tenant_id}"
        app = ConfidentialClientApplication(
            client_id=client_id,
            authority=authority,
            client_credential={
                "private_key": open(cert_path, "r").read(),
                "thumbprint": thumbprint
            }
        )

        result = app.acquire_token_for_client(scopes=["https://graph.microsoft.com/.default"])
        if "access_token" not in result:
            raise Exception(f"Token acquisition failed: {result.get('error_description')}")
        token = result["access_token"] 
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }

        # Schritt 1: Prüfe ob Tenant vorhanden & aktiv
        tenant_list_url = f"https://graph.microsoft.com/v1.0/sites/{site_id}/lists/{tenant_list_id}/items?expand=fields"
        tenant_list_resp = requests.get(tenant_list_url, headers=headers)
        tenant_list_resp.raise_for_status()

        tenant_items = tenant_list_resp.json().get("value", [])
        matching_tenant = next((item for item in tenant_items if item["fields"].get("Title") == tenant_name), None)

        if not matching_tenant:
            print(f"❌ Tenant '{tenant_name}' NICHT in Tenantliste gefunden – Abbruch.")
            return

        if not matching_tenant["fields"].get("enabled", True):
            print(f"⚠️ Tenant '{tenant_name}' ist inaktiv (enabled=False) – Abbruch.")
            return

        # Schritt 2: Hole bestehende Lizenz-Einträge
        license_list_url = f"https://graph.microsoft.com/v1.0/sites/{site_id}/lists/{license_list_id}/items?expand=fields"
        license_list_resp = requests.get(license_list_url, headers=headers)
        license_list_resp.raise_for_status()

        existing_items = license_list_resp.json().get("value", [])

        # Schritt 3: Verarbeiten der Lizenzdaten
        for lic in licenses:
            sku = lic.get("skupartnumber", "UNKNOWN")
            free = lic.get("free_units", 0)
            used = lic.get("consumed_units", 0)
            avail = lic.get("available_units", 0)

            match = next(
                (item for item in existing_items if
                item["fields"].get("Title") == sku and
                item["fields"].get(tenant_field) == tenant_name),
                None
            )

            # Felder zusammenstellen (nur Zahlen bei Update)
            if match:
                item_id = match["id"]
                # Standard-Felder
                sp_fields = {
                    field_mapping["Frei"]: free,
                    field_mapping["Gebraucht"]: used,
                    field_mapping["Verfügbar"]: avail
                }

                # Zusätzliche Logik: Supporter informieren?
                if free == 0:
                    # Falls es ein bestehendes Item ist, prüfe ob technician_informed gesetzt ist
                    trigger_field = field_mapping.get("Infosup", "trigger_inform_supporter")
                    if match:
                        technician_informed = match["fields"].get("technician_informed", False)
                        if not technician_informed:
                            sp_fields[trigger_field] = True
                    else:
                        # Bei Neuanlage können wir davon ausgehen, dass niemand informiert ist
                        sp_fields[trigger_field] = True
                else:
                    # Wenn wieder Lizenzen verfügbar sind, kannst du optional zurücksetzen:
                    trigger_field = field_mapping.get("Infosup", "trigger_inform_supporter")
                    sp_fields[trigger_field] = False
                    
                url_update = f"https://graph.microsoft.com/v1.0/sites/{site_id}/lists/{license_list_id}/items/{item_id}/fields"
                response = requests.patch(url_update, headers=headers, json=sp_fields)
                print(f"🔁 Lizenz '{sku}' für Tenant '{tenant_name}' wurde aktualisiert.")
            else:
                # Neuanlage – vollständige Felder setzen
                sp_fields = {
                    field_mapping["Tenant"]: tenant_name,
                    field_mapping["Lizenzname"]: sku,
                    field_mapping["Frei"]: free,
                    field_mapping["Gebraucht"]: used,
                    field_mapping["Verfügbar"]: avail
                }
                url_create = f"https://graph.microsoft.com/v1.0/sites/{site_id}/lists/{license_list_id}/items"
                response = requests.post(url_create, headers=headers, json={"fields": sp_fields})
                print(f"🆕 Neue Lizenz '{sku}' für Tenant '{tenant_name}' erstellt.")

            response.raise_for_status()
            
            
    def get_tenants_from_sharepoint():
        config_file = "config-profiles/sharepoint/sp-config-iseschool2013-profile.json"
        with open(config_file, "r") as f:
            config = json.load(f)

        sp_config = config["sharepoint_infos"]
        site_id = sp_config["site_id"]
        tenant_list_id = sp_config["tenant_list_id"]

        authority = f"https://login.microsoftonline.com/{config['tenant_id']}"
        app = ConfidentialClientApplication(
            client_id=config["client_id"],
            authority=authority,
            client_credential={
                "private_key": open(config["cert_path"], "r").read(),
                "thumbprint": config["thumbprint"]
            }
        )

        result = app.acquire_token_for_client(scopes=["https://graph.microsoft.com/.default"])
        if "access_token" not in result:
            raise Exception(f"Token acquisition failed: {result.get('error_description')}")

        token = result["access_token"]
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }

        url = f"https://graph.microsoft.com/v1.0/sites/{site_id}/lists/{tenant_list_id}/items?expand=fields"
        response = requests.get(url, headers=headers)
        response.raise_for_status()

        tenant_items = response.json().get("value", [])
        tenant_list = []
        for item in tenant_items:
            fields = item["fields"]
            tenant_list.append({
                "id": item.get("id"),
                "title": fields.get("Title"),
                "enabled": fields.get("enabled", True),
                "monitoring": fields.get("monitoring", False)  # falls vorhanden
            })

        return tenant_list
    
    @staticmethod
    def update_tenant_fields(item_id: int, enabled=None, monitoring=None):
        config_file = "config-profiles/sharepoint/sp-config-iseschool2013-profile.json"
        with open(config_file, "r") as f:
            config = json.load(f)

        sp_config = config["sharepoint_infos"]
        site_id = sp_config["site_id"]
        tenant_list_id = sp_config["tenant_list_id"]

        authority = f"https://login.microsoftonline.com/{config['tenant_id']}"
        app = ConfidentialClientApplication(
            client_id=config["client_id"],
            authority=authority,
            client_credential={
                "private_key": open(config["cert_path"], "r").read(),
                "thumbprint": config["thumbprint"]
            }
        )

        result = app.acquire_token_for_client(scopes=["https://graph.microsoft.com/.default"])
        if "access_token" not in result:
            raise Exception(f"Token acquisition failed: {result.get('error_description')}")

        token = result["access_token"]
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }

        # Nur Felder befüllen, die angegeben sind
        fields = {}
        if enabled is not None:
            fields["enabled"] = enabled
        if monitoring is not None:
            fields["monitoring"] = monitoring

        if not fields:
            raise Exception("Keine Felder zum Aktualisieren übergeben.")

        url = f"https://graph.microsoft.com/v1.0/sites/{site_id}/lists/{tenant_list_id}/items/{item_id}/fields"
        response = requests.patch(url, headers=headers, json=fields)
        response.raise_for_status()

        return {"id": item_id, "updated": fields}



