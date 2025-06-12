#!/usr/bin/env python3
import os
import zipfile
import xml.etree.ElementTree as ET

# Paths
BASE_DIR = ''
ADDON_XML = os.path.join(BASE_DIR, 'addon.xml')
ZIPS_DIR = os.path.join(BASE_DIR, 'zips')

# Parse addon.xml for id and version
tree = ET.parse(ADDON_XML)
root = tree.getroot()
addon_id = root.attrib.get('id', 'addon')
addon_version = root.attrib.get('version', '0.0.1')

zip_name = f"{addon_id}-{addon_version}.zip"
zip_path = os.path.join(ZIPS_DIR, zip_name)

# Exclude folders
EXCLUDE_DIRS = {'.git', '.github', 'zips'}

def should_exclude(path):
    for ex in EXCLUDE_DIRS:
        if os.path.commonpath([os.path.abspath(path), os.path.join(BASE_DIR, ex)]) == os.path.join(BASE_DIR, ex):
            return True
    return False

def zipdir(path, ziph):
    for root_dir, dirs, files in os.walk(path):
        # Exclude unwanted directories
        dirs[:] = [d for d in dirs if not should_exclude(os.path.join(root_dir, d))]
        for file in files:
            file_path = os.path.join(root_dir, file)
            if should_exclude(file_path):
                continue
            arcname = os.path.relpath(file_path, BASE_DIR)
            ziph.write(file_path, arcname)

if not os.path.exists(ZIPS_DIR):
    os.makedirs(ZIPS_DIR)

with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
    zipdir(BASE_DIR, zipf)

print(f"Created zip: {zip_path}")
