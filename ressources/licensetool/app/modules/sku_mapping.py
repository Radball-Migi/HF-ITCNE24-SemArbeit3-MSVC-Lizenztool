import json
from pathlib import Path

def load_sku_mapping():
    mapping_path = Path("config/sku_mappings.json")
    if not mapping_path.exists():
        return {}
    with open(mapping_path, "r", encoding="utf-8") as f:
        return json.load(f)

SKU_DISPLAY_NAMES = load_sku_mapping()