# Sistema de Registro de Ventas

Una aplicación web moderna y intuitiva para el registro y gestión de ventas, desarrollada con Python Flask.

## 🚀 Características

### Funcionalidades Principales
- ✅ **Registro de ventas** con cliente/producto, valor total y abono
- ✅ **Cálculo automático** del saldo pendiente
- ✅ **Selección múltiple de rubros** (Maquillaje, Renacer, Tendencia, Accesorios, Zapatos)
- ✅ **Fecha automática** con opción de modificación manual
- ✅ **Estadísticas en tiempo real** por rubro y generales
- ✅ **Modo oscuro** predeterminado con opción de cambio
- ✅ **Interfaz responsive** y moderna

### Características Técnicas
- 🎨 **Diseño moderno** con Material Design
- 📱 **Responsive** para dispositivos móviles y escritorio
- ⚡ **Validación en tiempo real** de formularios
- 🔄 **Cálculos automáticos** de saldos pendientes
- 📊 **Estadísticas visuales** con gráficos por rubro
- 🎯 **UX optimizada** con animaciones suaves
- 🔒 **Validaciones robustas** de datos

## 📋 Requisitos

- Python 3.7 o superior
- pip (gestor de paquetes de Python)

## 🛠️ Instalación

1. **Clonar o descargar el proyecto**
   ```bash
   cd Desktop/Ventas
   ```

2. **Instalar dependencias**
   ```bash
   pip install -r requirements.txt
   ```

3. **Ejecutar la aplicación**
   ```bash
   python app.py
   ```

4. **Abrir en el navegador**
   ```
   http://localhost:5000
   ```

## 📖 Uso

### Registro de Ventas
1. **Cliente/Producto**: Ingresa el nombre del cliente o producto
2. **Fecha**: Se autocompleta con la fecha actual (modificable)
3. **Valor Total**: Ingresa el valor total de la venta
4. **Abono**: Ingresa el monto abonado
5. **Rubros**: Selecciona uno o varios rubros usando los checkboxes
6. **Saldo Pendiente**: Se calcula automáticamente
7. **Registrar**: Haz clic en "Registrar Venta"

### Gestión de Ventas
- **Ver todas las ventas** en la tabla principal
- **Eliminar ventas** con el botón de papelera
- **Ver estadísticas** en tiempo real
- **Filtrar por rubros** en las estadísticas

### Modo Oscuro/Claro
- Haz clic en el botón de luna/sol en la esquina superior derecha
- La preferencia se guarda automáticamente

## 🏗️ Estructura del Proyecto

```
Ventas/
├── app.py                 # Aplicación principal Flask
├── requirements.txt       # Dependencias de Python
├── README.md             # Este archivo
├── templates/
│   └── index.html        # Plantilla HTML principal
└── static/
    ├── css/
    │   └── style.css     # Estilos CSS
    └── js/
        └── script.js     # JavaScript interactivo
```

## 🎨 Rubros Disponibles

- **Maquillaje**: Productos de belleza y cosméticos
- **Renacer**: Productos de cuidado personal
- **Tendencia**: Productos de moda actual
- **Accesorios**: Complementos y accesorios
- **Zapatos**: Calzado y zapatillas

## 📊 Estadísticas

La aplicación muestra estadísticas en tiempo real:

- **Total de ventas** registradas
- **Valor total** de todas las ventas
- **Total abonado** en todas las ventas
- **Saldo pendiente** total
- **Estadísticas por rubro** con desglose detallado

## 🔧 Personalización

### Agregar Nuevos Rubros
Edita el archivo `app.py` y modifica la lista `RUBROS`:

```python
RUBROS = ['Maquillaje', 'Renacer', 'Tendencia', 'Accesorios', 'Zapatos', 'Nuevo Rubro']
```

### Cambiar Moneda
En `app.py`, modifica la función `formatear_moneda`:

```python
def formatear_moneda(valor):
    return f"€{valor:,.2f}"  # Para euros
```

## 🚀 Despliegue

### Desarrollo Local
```bash
python app.py
```

### Producción Local (Recomendado)
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

### Despliegue en Render (Cloud)

1. **Crear cuenta en Render**:
   - Ve a [render.com](https://render.com)
   - Regístrate con tu cuenta de GitHub

2. **Conectar repositorio**:
   - Haz clic en "New +" → "Web Service"
   - Conecta tu repositorio de GitHub
   - Selecciona `Carloszerpav/registro-ventas`

3. **Configurar el servicio**:
   - **Name**: `registro-ventas`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app`
   - **Plan**: Free (para empezar)

4. **Desplegar**:
   - Haz clic en "Create Web Service"
   - Render construirá y desplegará tu aplicación automáticamente

5. **Acceder a tu aplicación**:
   - Tu app estará disponible en: `https://tu-app-name.onrender.com`
   - Los cambios se despliegan automáticamente al hacer push a GitHub

**Archivos de configuración incluidos**:
- `render.yaml` - Configuración para Render
- `Procfile` - Comando de inicio
- `runtime.txt` - Versión de Python
- `requirements.txt` - Dependencias actualizadas

## 🐛 Solución de Problemas

### Error: "No module named 'flask'"
```bash
pip install -r requirements.txt
```

### Error: "Address already in use"
Cambia el puerto en `app.py`:
```python
app.run(debug=True, port=5001)
```

### Error: "Permission denied"
Ejecuta con permisos de administrador o cambia el puerto.

## 📝 Licencia

Este proyecto es de uso libre para fines educativos y comerciales.

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Por favor:

1. Fork el proyecto
2. Crea una rama para tu feature
3. Commit tus cambios
4. Push a la rama
5. Abre un Pull Request

## 📞 Soporte

Para soporte técnico o preguntas:
- Revisa la documentación
- Verifica los logs de la aplicación
- Consulta los requisitos del sistema

---

**Desarrollado con ❤️ usando Python Flask**
