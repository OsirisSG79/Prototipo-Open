# Dictamen estricto — Open Break Cinematic Atelier V6

**Hero: mejora visual importante, pero aún requiere comparación dinámica en navegadores reales.** **SaaS: no apto para producción.**

| Área | Estado | Evidencia / límite |
|---|---|---|
| Hero inicial | Mejorado | Túnel lateral con escala, centro comprimido y paneles grandes extremos |
| Movimiento del túnel | Implementado | Un controlador, pausa, pointer/drag, teclado y movimiento reducido |
| Carrusel original | Conservado | Se trasladó a una sección posterior con un único motor |
| Optimización WebP | Conservada | HTML principal de ~130 KB; fotos independientes |
| Agenda y teléfono | Integrados en una demo local | Reservas sin cobros dobles y espera sin débito |
| Canvas isométrico R1 | Pendiente | Falta escena multicapa con profundidad y rutas luminosas |
| Tarjetas R2 | Parcial | Sin materiales PBR ni acabado 3D avanzado |
| Agenda R3 | Parcial | Selector por día, no grid semanal completa |
| App R4 | Parcial | QR real, navegación y producción pendientes |
| Reformer GLB | Pendiente | Modelo procedimental, no es un GLB profesional |
| Scroll narrativo | Parcial | Sin transición de cámara continua entre escenas |
| Rendimiento GPU | No verificado | Sin mediciones FPS confiables con GPU real |

## Evidencia disponible
- `python build_site.py`: correcto.
- `python tests/qa_static.py`: correcto.
- `node tests/test_schedule.js`: correcto.
- Chromium produjo capturas del hero y agenda a 1440 px, y capturas de composición estática a 320/390/768 px; no se certificó el recorrido 3D.
- Prueba dinámica de demo: segunda reserva bloqueada, entrada a espera sin crédito y cancelación que devuelve plaza/crédito.

## Prioridad siguiente
1. Ajustar la coreografía de la portada comparando vídeo lado a lado con Melius.
2. Canvas isométrico multicapa responsive.
3. Agenda semanal de siete columnas y teléfono navegable.
4. Asset GLB realista del Reformer en Blender y pruebas de GPU.
5. Backend y simulación de operaciones por fases independientes.

El repositorio remoto de GitHub no se modificó en esta entrega.
