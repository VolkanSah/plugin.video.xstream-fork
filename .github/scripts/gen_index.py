#!/usr/bin/env python3
import os

ZIPS_DIR = 'zips'
INDEX_HTML = os.path.join(ZIPS_DIR, 'index.html')

zip_files = [f for f in os.listdir(ZIPS_DIR) if f.endswith('.zip')]
zip_files.sort(reverse=True)

html = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>xStream Addon Zips</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 2em; }
        table { border-collapse: collapse; width: 60%; }
        th, td { border: 1px solid #ccc; padding: 0.5em 1em; text-align: left; }
        th { background: #f0f0f0; }
        tr:nth-child(even) { background: #fafafa; }
    </style>
</head>
<body>
    <h1>xStream Addon Downloads</h1>
    <table>
        <tr><th>Filename</th><th>Download</th></tr>
'''
for zipf in zip_files:
    html += f'        <tr><td>{zipf}</td><td><a href="{zipf}">Download</a></td></tr>\n'
html += '''    </table>
</body>
</html>
'''

with open(INDEX_HTML, 'w', encoding='utf-8') as f:
    f.write(html)

print(f"index.html generated with {len(zip_files)} zip files.")
