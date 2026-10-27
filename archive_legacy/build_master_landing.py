import re
import json

print("Iniciando actualización integral de landing_melius_style.html hacia el Master Prompt...")

with open('/home/user/openbreak/landing_melius_style.html', 'r', encoding='utf-8') as f:
    source_html = f.read()

# Extraer el bloque Three.js y data_uris si existen
three_script_match = re.search(r'(function init3DReformer\(\).*?function toggleReformerSprings\(\)\s*\{.*?\})', source_html, re.DOTALL)
print("Three script extracted:", bool(three_script_match))

