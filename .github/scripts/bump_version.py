#!/usr/bin/env python3
import xml.etree.ElementTree as ET
import re

ADDON_XML = 'addon.xml'

def bump_version(version):
    parts = version.split('.')
    if len(parts) == 0:
        return '1.0.0.0'
    # Bump last part
    try:
        parts[-1] = str(int(parts[-1]) + 1)
    except Exception:
        parts[-1] = '1'
    return '.'.join(parts)

def main():
    tree = ET.parse(ADDON_XML)
    root = tree.getroot()
    old_version = root.attrib['version']
    new_version = bump_version(old_version)
    root.attrib['version'] = new_version
    tree.write(ADDON_XML, encoding='utf-8', xml_declaration=True)
    print(f"Bumped version: {old_version} -> {new_version}")

if __name__ == '__main__':
    main()
