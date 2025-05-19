#!/bin/bash

set -e  # Exit script on error

# === INTERACTIVE INPUT ===
read -p "Domain (e.g., mycompany.ch): " DOMAIN
read -s -p "Password for .pfx file: " CERT_PASSWORD
echo

# === DERIVE TENANT ===
TENANT="${DOMAIN%.ch}"

# === CONSTANTS ===
DAYS_VALID=365
EXPIRY_DATE=$(date -d "+$DAYS_VALID days" +%Y-%m-%d)
OUTPUT_CERT_DIR="./certs/$TENANT"
OUTPUT_INFO_DIR="./certs/infos"

# === CREATE DIRECTORY ===
mkdir -p "$OUTPUT_CERT_DIR"

# === DEFINE FILE PATHS ===
KEY_FILE="${OUTPUT_CERT_DIR}/mycert_${TENANT}.key"
CRT_FILE="${OUTPUT_CERT_DIR}/mycert_${TENANT}.crt"
PEM_FILE="${OUTPUT_CERT_DIR}/mycert_${TENANT}.pem"
PFX_FILE="${OUTPUT_CERT_DIR}/mycert_${TENANT}.pfx"
JSON_FILE="${OUTPUT_INFO_DIR}/cert-${TENANT}-info.json"

# === GENERATE PRIVATE KEY ===
openssl genrsa -out "$KEY_FILE" 2048

# === SELF-SIGNED CERTIFICATE ===
openssl req -new -x509 -key "$KEY_FILE" -out "$CRT_FILE" -days $DAYS_VALID -subj "//CN=$DOMAIN"

# === EXPORT TO .pfx ===
openssl pkcs12 -export -out "$PFX_FILE" -inkey "$KEY_FILE" -in "$CRT_FILE" -password pass:"$CERT_PASSWORD"

# === GENERATE PEM (combine key + certificate) ===
cat "$KEY_FILE" "$CRT_FILE" > "$PEM_FILE"

# === WRITE JSON FILE ===
cat <<EOF > "$JSON_FILE"
{
  "tenant": "$TENANT",
  "domain": "$DOMAIN",
  "key_path": "$(realpath "$KEY_FILE")",
  "cert_pem_path": "$(realpath "$PEM_FILE")",
  "pfx_path": "$(realpath "$PFX_FILE")",
  "password": "$CERT_PASSWORD",
  "expires": "$EXPIRY_DATE"
}
EOF

# === DONE ===
echo "All files have been successfully created in the directory '$OUTPUT_DIR':"
echo "Private Key: $(basename "$KEY_FILE")"
echo "PEM Certificate: $(basename "$PEM_FILE")"
echo "PFX File: $(basename "$PFX_FILE")"
echo "JSON Info: $(basename "$JSON_FILE")"
