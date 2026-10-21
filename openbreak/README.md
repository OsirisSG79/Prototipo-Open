# Open Break — Atelier V5

**Estado: prototipo visual interactivo. No está listo para comercialización ni procesa reservas, pagos o solicitudes de demo reales.**

## Abrir y revisar

1. Abre `index.html` o `landing_melius_style.html` en un navegador moderno. Mantén juntas las carpetas `assets/` y `src/css/`.
2. Si el navegador restringe contenido local, ejecuta desde esta carpeta `python -m http.server 8000` y abre `http://localhost:8000/`.
3. La tipografía se solicita a Google Fonts. Sin conexión, el navegador utilizará las alternativas definidas en CSS.
4. Si no hay WebGL, el visor Reformer muestra una fotografía en lugar de un espacio tridimensional. Es un comportamiento previsto, no una prueba del render 3D.

## Contenido principal

- `index.html`: landing compilada y editable a través de las plantillas.
- `landing_melius_style.html`: alias compatible con la versión original.
- `prototype.html`: simulación antigua preservada, **no integrada al backend real**.
- `src/css/editorial.css`: dirección artística específica del producto.
- `src/js/*.js`: controladores para cursor, carrusel, Canvas y Reformer.
- `src/modules/workflow_section.html`: escena de producto interactiva.
- `assets/optimized/*.webp`: fotografías separadas del HTML.
- `assets/three.min.js`: motor gráfico local preexistente.
- `templates/*`: secciones heredadas usadas en compilación.
- `build_site.py`: ensamblador reproducible, sin rutas absolutas.
- `tests/qa_visual.py`: pruebas visuales automatizadas.
- `schema.py`: borrador de arquitectura PostgreSQL; no aplicar en producción sin auditoría de seguridad, concurrencia y datos.

## Modificar y reconstruir

Edita las fuentes. En esta carpeta ejecuta:

```bash
python build_site.py
```

Si deseas regenerar las imágenes desde el JSON de origen, instala Pillow con `python -m pip install Pillow`. Si no tienes Pillow, el ensamblador reutiliza las WebP ya incluidas.

No edites `index.html` si quieres conservar los cambios en el siguiente ensamblado.

## Pruebas

Instala Playwright y su navegador compatible (`pip install playwright`, `python -m playwright install chromium`). Ejecuta:

```bash
python tests/qa_visual.py
```

La prueba carga todo dentro de un documento aislado, sin depender de un servidor. Valida cuatro tamaños de pantalla, menú, Canvas, pausa y formulario. **La prueba deshabilita WebGL; no valida el modelo 3D ni el rendimiento real en GPU.**

## Límites relevantes

- No hay endpoint de solicitudes: preparar una demo no contacta al negocio. No se almacenan teléfonos ni nombres en `localStorage`.
- Simulaciones de créditos, concurrencia y waitlists representan un comportamiento esperado; no están conectadas a una base de datos.
- La escena Reformer está modelada por geometrías procedurales de Three.js: incluye más detalles, pero requiere una malla profesional GLB/Blender y pruebas reales de GPU para alcanzar acabado fotorrealista.
- Tarifas, pagos por Stripe/SPEI y soporte por WhatsApp son hipótesis y capacidades sujetas a integración y validación comercial.
- Las fotografías existentes son recursos de referencia, no casos de clientes comprobados.

Consulta `AUDITORIA_V5.md` para las fuentes de diseño, riesgos y próximas fases.
