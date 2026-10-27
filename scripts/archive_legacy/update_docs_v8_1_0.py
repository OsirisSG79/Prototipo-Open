from pathlib import Path

docs_p = Path('/home/user/openbreak/docs.html')
content = docs_p.read_text(encoding='utf-8')

# Update docs.html to reflect UX-03 glTF PBR asset, UX-05 Sticky Scrubber, UX-12 Matrix and correct ZIP filename
content = content.replace("OpenBreak_Cinematic_V7_Proyecto_Completo.zip", "OpenBreak_Cinematic_V8_1_0_Proyecto_Completo.zip")
content = content.replace(
    '<td>Three.js Canvas con iluminación direccional dual, chasis de madera y carro deslizante.</td>',
    '<td>Three.js Canvas con micro-texturas procedurales (madera y aluminio) y asset binario glTF 2.0 (<code>reformer_studio.glb</code>).</td>'
)

if "UX-05" not in content:
    # Add UX-05 row into table
    row_ux05 = """        <tr>
          <td><strong>UX-05</strong></td>
          <td>Scrubber de scroll cinematográfico</td>
          <td>Pasarela sticky multi-pantalla (<code>240vh</code>) mapeando el avance del scroll a la rotación 3D y cables Bézier.</td>
          <td class="pass">PASS</td>
        </tr>"""
    target = '<tr>\n          <td><strong>UX-06</strong></td>'
    content = content.replace(target, row_ux05 + '\n' + target)

docs_p.write_text(content, encoding='utf-8')
print("Updated docs.html with V8.1.0 deliverables and accurate UX-03/UX-05 criteria.")
