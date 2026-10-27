# OPEN BREAK · Auditoría estricta · Atelier V5

**Fecha:** 21 de octubre de 2026  
**Origen:** `openbreak_project_complete (2).zip` del usuario.  
**Objeto de auditoría:** landing y experiencia visual, no producto operativo completo.

## Dictamen

Se mejoró la dirección de arte, la carga, la reproducibilidad y el comportamiento responsive del prototipo. **Esta V5 no alcanza todavía la sofisticación visual de Melius y no es un SaaS listo para comercializar.** No se debe confundir mejora de interfaz con capacidad real del motor de negocio.

## Skills y fuentes aplicadas

1. [Anthropic — frontend-design](https://github.com/anthropics/skills/blob/main/skills/frontend-design/SKILL.md): dirección artística específica, contraste tipográfico, moderación de titulares con énfasis, evitar etiquetas/insignias repetidas y motion decorativo sin propósito. **Aplicado** en hero, copia, jerarquías, geometría de tarjetas y ritmo de secciones.
2. [Vercel — Web Interface Guidelines](https://github.com/vercel-labs/web-interface-guidelines): foco visible, etiquetas y controles, evitar `transition: all`, animación interrumpible, control de movimiento automático, imágenes optimizadas y pruebas multi-viewport. **Aplicado** en navegación, tarjetas, galería, formulario, salida de imágenes y tests.
3. [View Source — Melius](https://view-source.com/work/melius): la diferencia no se reduce a cursors/hover, sino a escenas WebGL y flujos que se ensamblan nodo por nodo. **Aplicado como criterio de dirección**, no como una copia de su código o de sus recursos.
4. [GSAP ScrollTrigger docs](https://gsap.com/docs/v3/Plugins/ScrollTrigger/): candidato para futuras secuencias cinematográficas sincronizadas, **no instalado** aún para evitar peso y complejidad innecesarios sin storyboard aprobado.

## Hallazgos y cambios

| Prioridad | Hallazgo de la versión recibida | Acción V5 | Estado |
|---|---|---|---|
| P0 | Carrusel/cursor/3D inicializados dos veces: módulos nuevos + scripts heredados | Eliminar controladores duplicados y mantener uno por elemento | Corregido |
| P0 | Lead almacenado solo en `localStorage` pero mostrado como recibido | Ya no se almacena; se etiqueta como solicitud local, copiable | Contenido honesto; integración pendiente |
| P1 | HTML de aprox. 7.4 MB con fotografías Base64 y Three.js incrustado | HTML compilado de ~113 KB + 11 WebP independientes + Three.js externo local | Corregido |
| P1 | Script `build_master_v4.py` usa rutas absolutas `/home/user/…` | `build_site.py` usa rutas relativas a proyecto | Corregido |
| P1 | Carrusel sin duplicación real de secuencia; cálculo de geometría en cada frame | Duplicación semánticamente oculta + dimensiones en caché + control de pausa | Mejorado y probado |
| P1 | Workflow con cuatro tarjetas absolutas de 1200 px y arrastre sin límites | Canvas con selección real de etapa, nodos responsivos y conexiones dinámicas | Mejorado y probado |
| P1 | Reformer era un bloque principal con pocos detalles de producto | Chasis abierto, rieles, ruedas, muelles helicoidales, poleas, cuerdas, barra y reposacabezas mediante geometría | Parcial; GPU no verificada |
| P1 | Promesas sobre infraestructura, tiempos y pagos sin código de respaldo | Copia condicionada y demos rotuladas explícitamente | Mejorado; validación legal/comercial pendiente |
| P2 | Demasiadas etiquetas en mayúsculas, cápsulas y títulos artificialmente enfáticos | Composición editorial asimétrica y tipografía Newsreader + IBM Plex Sans | Mejorado |
| P2 | Sin protocolo accesible de Canvas, ni manejo claro de pausa | Controles de navegación, aria-pressed y teclado, política de movimiento reducido | Mejorado y probado |

## Qué se comprobó

Ejecutado con Chromium headless y Playwright mediante contenido de prueba autocontenido (la navegación a localhost o a `file://` está bloqueada en este entorno):

- Anchos 320, 390, 768 y 1440: sin scroll horizontal.
- 24 tarjetas del carrusel (12 escenas + 12 copias ocultas de accesibilidad).
- IDs HTML únicos en los cuatro tamaños.
- Interacción con Canvas, avance y retroceso.
- Menú móvil abre y cierra; `aria-expanded` se actualiza.
- Botón de pausa del carrusel responde a clic.
- Formulario abre, rellena campos y muestra que **no se envió**.
- Modal cierra con Escape.
- JavaScript sin errores de página en esos escenarios.
- Fallback del Reformer aparece al desactivar WebGL.

**No verificado:** funcionamiento real del motor de Three.js sobre GPU, WebGL hardware, movimiento con 60 FPS, Core Web Vitals reales, VoiceOver en Safari, lector de pantalla completo, producción de backend, pagos o concurrencia.

## Pendientes — no aprobados

**P0 antes de operar como negocio**

- Backend seguro con autenticación, validación de cupos y pruebas transaccionales de PostgreSQL.
- Endpoint real para la captura de solicitudes, consentimiento y aviso de privacidad.
- Verificación de Stripe/SPEI y WhatsApp Cloud API por país y tipo de comercio.
- Política de paquetes, cancelaciones, créditos y lista de espera definitiva.

**P1 para acercarse a Melius**

- Modelado de producto con Blender/CAD y assets GLB optimizados; materiales PBR con mapas, rig de resortes y vista funcional en GPU.
- Storyboard de cámara, transiciones espaciales y secuencias guiadas por scroll.
- Flujos de reserva y espera no solo textuales, sino demostraciones que conecten visualmente pantallas de producto reales.
- Biblioteca propia de fotografías/art direction; las imágenes actuales son referenciales.
- Validación manual con pantalla táctil, Safari/iOS y hardware de gama media.

**P2 antes de publicación pública**

- Revisión editorial y jurídica de precios y afirmaciones competitivas.
- Analítica respetuosa, SEO/OG, Lighthouse real y estrategia de carga de fuentes.
- Auditoría de accesibilidad completa con lector de pantalla y pruebas de formularios.

## Recomendación de siguiente fase

No añadir más efectos globales todavía. Crear un único **showroom 3D profesional de Pilates Reformer**: diseño industrial correcto en Blender, texturas PBR, animación de carriage, luces y cámaras, GLB con LOD/fallback y una transición guiada por scroll de la portada a la selección de clases. Medir rendimiento de forma honesta. Después escalar este lenguaje a las simulaciones.

## Archivos importantes

`index.html`, `landing_melius_style.html`, `src/css/editorial.css`, `src/js/*.js`, `src/modules/workflow_section.html`, `build_site.py`, `assets/optimized/*.webp`, `tests/qa_visual.py`.
