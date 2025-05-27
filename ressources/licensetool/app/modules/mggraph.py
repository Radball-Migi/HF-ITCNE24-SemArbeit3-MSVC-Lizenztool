# app/modules/mggraph.py

import json
import os
import requests
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
        #raise Exception(f"Access Token:\n{result['access_token']}")
        return result["access_token"]

    def get_license_status(self):
        headers = {"Authorization": f"Bearer {self.token}"}
        response = requests.get("https://graph.microsoft.com/v1.0/subscribedSkus", headers=headers)
        if response.status_code != 200:
            raise Exception(f"Graph API error: {response.status_code} - {response.text}")
        return response.json()
