# Optimización para Móviles - Header Colapsable

## 🎯 Problema Solucionado
El header superior ocupaba demasiado espacio en pantallas móviles iOS, dificultando el uso del sistema.

## ✅ Solución Implementada
**Header colapsable que se reduce al hacer scroll hacia abajo**

### Características:
- **Se reduce automáticamente** al hacer scroll hacia abajo
- **Se expande** al hacer scroll hacia arriba o volver al top
- **Optimizado para iOS** con detección de gestos táctiles
- **Transiciones suaves** para mejor experiencia de usuario
- **Responsive** - funciona mejor en pantallas pequeñas

### Comportamiento:
1. **Estado normal**: Header completo con título, descripción y botones
2. **Al hacer scroll hacia abajo**: Header se reduce, ocupa menos espacio
3. **Al hacer scroll hacia arriba**: Header vuelve a su tamaño normal
4. **En móviles**: Umbral de scroll más bajo (50px vs 100px)

### Archivos modificados:
- `static/css/style.css` - Estilos para header colapsable y optimizaciones de teclado
- `static/js/script.js` - Lógica de detección de scroll y manejo de teclado móvil
- `MOVIL_OPTIMIZACION.md` - Esta documentación

### Nuevas optimizaciones agregadas:
- **Pantalla estable**: Evita que la pantalla se mueva cuando aparece el teclado
- **Scroll inteligente**: Hace scroll automático al input activo
- **Prevención de zoom**: Evita el zoom automático en inputs en iOS
- **Detección de teclado**: Detecta cuando aparece/desaparece el teclado
- **Restauración de posición**: Restaura la posición del scroll cuando se oculta el teclado

## 🚀 Beneficios:
- ✅ **Más espacio útil** para el contenido principal
- ✅ **Mejor experiencia** en móviles iOS
- ✅ **Navegación más fluida** con gestos táctiles
- ✅ **Mantiene funcionalidad** completa del header
- ✅ **Transiciones suaves** y profesionales
- ✅ **Pantalla estable** al escribir (no se mueve con el teclado)
- ✅ **Scroll inteligente** al input activo
- ✅ **Prevención de zoom** automático en inputs

## 📱 Compatibilidad:
- ✅ iOS Safari
- ✅ Chrome móvil
- ✅ Firefox móvil
- ✅ Android Chrome
- ✅ Desktop (funciona pero menos crítico)

**Carloszerpav** - Optimización específica para mejorar la experiencia en móviles iOS 🎉
