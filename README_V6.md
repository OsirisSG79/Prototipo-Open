# Open Break — Cinematic Atelier V6

**Estado:** prototipo visual actualizado. **No es un SaaS listo para operar con clientes.**

## Inicio rápido

1. Para una vista rápida abre `index.html`, conservando intactas las carpetas `assets/` y `src/`.
2. Para mayor compatibilidad (sobre todo navegadores que restringen archivos locales): ejecuta `python -m http.server 8000` desde esta carpeta y abre `http://localhost:8000`.
3. Para reconstruir el sitio desde sus plantillas: `python build_site.py`.
4. Para pruebas reproducibles: `python tests/qa_static.py` y `node tests/test_schedule.js`.

## Qué cambió

- Hero reestructurado como una sola escena: titular centrado, **túnel de doce fotografías** con escala y profundidad, movimiento pausado, reacción al cursor, arrastre táctil/mouse y controles por teclado. El CTA lleva a la agenda de demostración.
- Se mantiene el carrusel original en una sección posterior, conservando arrastre, inercia, pausa y looping. No hay dos controladores para el mismo carrusel.
- Base de **Atelier V5 optimizada** con imágenes WebP externas y generador portable. El HTML principal ya no incrusta megabytes de fotografías.
- Se integró de la entrega más reciente la agenda y vista de teléfono como experiencia ilustrativa compartida. Reserva repetida no descuenta créditos; lista de espera no cobra; cancelación recupera saldo e inventario.
- Textos ajustados para no confundir demo local con backend real o app publicada.
- Fallback estático del túnel si JS no ejecuta y soporte para `prefers-reduced-motion`.

## Limitaciones / siguiente auditoría

- La composición del hero es una **interpretación propia** de la referencia, no una clonación exacta ni el motor WebGL de Melius.
- El Canvas de procesos y el Reformer 3D **no** alcanzan todavía la fidelidad isométrica / modelado GLB profesional pedidos.
- La agenda visual todavía no es una cuadrícula completa de siete columnas con horarios verticales como en la referencia.
- Las reservas y los créditos son un estado de ejemplo **en memoria del navegador**; no existen cuentas, pagos, persistencia real, concurrencia, notificaciones ni transacciones PostgreSQL verificadas.
- El pase de la app es una visualización, no un código QR auténtico.
- La solicitud de demo NO se transmite automáticamente a un servidor; no afirmar que fue recibida.
- No se midieron fotogramas reales en GPU ni Core Web Vitals de producción.

## Fuente de verdad

La versión activa se genera con **`build_site.py`**. Las antiguas pruebas de scripts generadores están archivadas en `legacy_builders/` y **no forman parte del build**. Los archivos de interacción activos del hero y calendario son `src/js/hero-tunnel.js` y `src/js/schedule-sync.js`.
