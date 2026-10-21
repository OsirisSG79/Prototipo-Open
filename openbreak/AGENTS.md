# Normas para cualquier agente que modifique Open Break

Leer `README.md` y `AUDITORIA_V5.md` antes de tocar el código. Preservar las funcionalidades y evitar introducir dos controladores de la misma animación.

## Estilo editorial propio

La marca no necesita copiar otra página. Referencia conceptual: Melius (narrativa mediante demostraciones visuales); personalidad de Open Break: movimiento humano, un estudio real, materiales reales, ingeniería discreta.

Aplicar los criterios de la skill **frontend-design** de Anthropic (https://github.com/anthropics/skills/blob/main/skills/frontend-design/SKILL.md): construir desde la identidad del producto; evitar textos totalmente en mayúsculas, etiquetas decorativas repetidas, titulares con una única palabra coloreada, íconos genéricos y tarjetas duplicadas que no expresan información diferente.

Aplicar las **Web Interface Guidelines** de Vercel (https://github.com/vercel-labs/web-interface-guidelines): foco visible, controles semánticos, movimiento reducido, transformación/opacidad preferentes, pausa del movimiento continuo, soporte de teclado, y verificación responsive.

## Criterios de entrega

- **Nunca** afirmar 60 FPS sin medición real, ni garantía de cero sobrecupos sin backend y pruebas.
- No describir una demo local como un servicio conectado.
- No reutilizar fotos como si fueran clientes reales ni crear testimonios inventados.
- Si agregas Three.js, conserva fallback y mide el tamaño de descarga.
- No añadir `transition: all`; limitar efectos automáticos. Aceptar interacción accesible por clic y teclado.
- Una única inicialización para cada escena o loop. Limpiar observadores si el componente se desmonta.
- Probar al menos 320, 390, 768 y 1440 px y registrar limitaciones.
- No añadir dependencias o mover la arquitectura sin una justificación concreta.
