from flask import Flask, request, redirect, url_for, render_template, jsonify
from datetime import datetime
import json
import os

app = Flask(__name__)

# ========================================
# SISTEMA DE VENTAS - Carloszerpav
# ========================================
# Este es mi sistema de gestión de ventas personal
# Lo hice para manejar mis ventas de manera fácil y rápida
# - Carloszerpav

# Lista global de ventas - aquí guardo todas mis ventas
ventas = []
contador_id = 1

# Mis rubros de trabajo - Carloszerpav
RUBROS = ['Maquillaje', 'Renacer', 'Tendencia', 'Accesorios', 'Zapatos']

def agregar_venta(cliente, valor_total, abono, rubros, fecha=None):
    """
    Función para agregar una nueva venta - Carloszerpav
    Esta función es la que uso para registrar cada venta que hago
    Me valida que todo esté bien antes de guardar
    """
    global contador_id
    
    try:
        # Validar y limpiar datos
        cliente = str(cliente).strip() if cliente else ""
        valor_total = float(valor_total) if valor_total else 0.0
        abono = float(abono) if abono else 0.0
        rubros = list(rubros) if rubros else []
        
        # Validación obligatoria de rubros - Carloszerpav
        # Me aseguro de que siempre seleccionen al menos un rubro
        if not rubros:
            raise ValueError("Debe seleccionar al menos un rubro")
        
        # Validar que los rubros seleccionados sean válidos
        # Esto evita que me metan rubros que no existen
        rubros_validos = [rubro for rubro in rubros if rubro in RUBROS]
        if not rubros_validos:
            raise ValueError("Los rubros seleccionados no son válidos")
        
        # Obtener fecha actual si no se proporciona
        if not fecha:
            fecha = datetime.now().strftime("%Y-%m-%d")
        
        # Calcular saldo pendiente
        saldo_pendiente = valor_total - abono
        
        # Crear historial de pagos inicial
        historial_pagos = []
        if abono > 0:
            historial_pagos.append({
                'id': 1,
                'monto': abono,
                'fecha': datetime.now().strftime("%Y-%m-%d %H:%M"),
                'tipo': 'Pago inicial'
            })
        
        # Crear la nueva venta con todos los datos - Carloszerpav
        nueva_venta = {
            'id': contador_id,
            'cliente': cliente,
            'valor_total': valor_total,
            'abono': abono,
            'saldo_pendiente': saldo_pendiente,
            'rubros': rubros_validos,  # Solo uso los rubros válidos
            'fecha': fecha,
            'fecha_registro': datetime.now().strftime("%Y-%m-%d %H:%M"),
            'estado': 'Activa' if saldo_pendiente > 0 else 'Cerrada',
            'historial_pagos': historial_pagos,
            'total_pagos': len(historial_pagos),
            'incluida_en_estadisticas': True,  # Nueva venta siempre incluida
            'mes_cierre': None  # Se establecerá cuando se cierre mensualmente
        }
        
        ventas.append(nueva_venta)
        contador_id += 1
        
        return nueva_venta
        
    except Exception as e:
        print(f"❌ Error en agregar_venta: {e}")
        raise e

def eliminar_venta(id):
    """
    Elimina una venta de la lista
    Args:
        id (int): El ID de la venta a eliminar
    Returns:
        bool: True si se encontró y eliminó la venta, False si no existe
    """
    global ventas
    ventas_original = len(ventas)
    ventas = [venta for venta in ventas if venta['id'] != id]
    return len(ventas) < ventas_original

def obtener_venta(id):
    """
    Obtiene una venta específica por ID
    Args:
        id (int): El ID de la venta
    Returns:
        dict: La venta encontrada o None si no existe
    """
    for venta in ventas:
        if venta['id'] == id:
            return venta
    return None

def registrar_pago(venta_id, monto_pago, tipo_pago="Abono"):
    """
    Registra un pago adicional para una venta
    Args:
        venta_id (int): ID de la venta
        monto_pago (float): Monto del pago
        tipo_pago (str): Tipo de pago (Abono, Cuota, etc.)
    Returns:
        dict: La venta actualizada o None si no se encuentra
    """
    venta = obtener_venta(venta_id)
    if not venta:
        return None
    
    if venta['estado'] == 'Cerrada':
        raise ValueError("No se pueden registrar pagos en ventas cerradas")
    
    if monto_pago <= 0:
        raise ValueError("El monto del pago debe ser mayor a 0")
    
    if monto_pago > venta['saldo_pendiente']:
        raise ValueError("El monto del pago no puede ser mayor al saldo pendiente")
    
    # Agregar pago al historial
    nuevo_pago = {
        'id': len(venta['historial_pagos']) + 1,
        'monto': monto_pago,
        'fecha': datetime.now().strftime("%Y-%m-%d %H:%M"),
        'tipo': tipo_pago
    }
    
    venta['historial_pagos'].append(nuevo_pago)
    
    # Actualizar totales
    venta['abono'] += monto_pago
    venta['saldo_pendiente'] -= monto_pago
    venta['total_pagos'] = len(venta['historial_pagos'])
    
    # Verificar si la venta se completa
    if venta['saldo_pendiente'] <= 0:
        venta['estado'] = 'Cerrada'
        venta['saldo_pendiente'] = 0
        # NO cambiar incluida_en_estadisticas aquí - se hará en el cierre mensual
    
    return venta

def obtener_estadisticas():
    """
    Función para obtener estadísticas - Carloszerpav
    Esta función me da todos los números importantes de mis ventas
    Me ayuda a ver cómo va mi negocio
    """
    # Ventas incluidas en estadísticas (activas + cerradas que aún no se han cerrado mensualmente)
    ventas_en_estadisticas = [venta for venta in ventas if venta.get('incluida_en_estadisticas', True)]
    ventas_activas = [venta for venta in ventas_en_estadisticas if venta['estado'] == 'Activa']
    ventas_cerradas = [venta for venta in ventas_en_estadisticas if venta['estado'] == 'Cerrada']
    ventas_excluidas = [venta for venta in ventas if not venta.get('incluida_en_estadisticas', True)]
    
    total_ventas_activas = len(ventas_activas)
    total_valor_activas = sum(venta['valor_total'] for venta in ventas_activas)
    total_abonado_activas = sum(venta['abono'] for venta in ventas_activas)
    total_pendiente_activas = sum(venta['saldo_pendiente'] for venta in ventas_activas)
    
    # Estadísticas por rubro (ventas incluidas en estadísticas)
    estadisticas_rubros = {}
    for rubro in RUBROS:
        ventas_rubro = [venta for venta in ventas_en_estadisticas if rubro in venta['rubros']]
        estadisticas_rubros[rubro] = {
            'cantidad': len(ventas_rubro),
            'valor_total': sum(venta['valor_total'] for venta in ventas_rubro),
            'abonado': sum(venta['abono'] for venta in ventas_rubro),
            'pendiente': sum(venta['saldo_pendiente'] for venta in ventas_rubro)
        }
    
    return {
        'total_ventas_activas': total_ventas_activas,
        'total_ventas_cerradas': len(ventas_cerradas),
        'total_ventas_excluidas': len(ventas_excluidas),
        'total_ventas': len(ventas),
        'total_valor': total_valor_activas,
        'total_abonado': total_abonado_activas,
        'total_pendiente': total_pendiente_activas,
        'por_rubro': estadisticas_rubros
    }

def formatear_fecha(fecha_str):
    """
    Formatea una fecha para mostrar
    Args:
        fecha_str (str): Fecha en formato YYYY-MM-DD
    Returns:
        str: Fecha formateada
    """
    try:
        fecha = datetime.strptime(fecha_str, "%Y-%m-%d")
        return fecha.strftime("%d/%m/%Y")
    except:
        return fecha_str

def formatear_moneda(valor):
    """
    Función para formatear moneda - Carloszerpav
    Me ayuda a mostrar los precios de manera bonita
    """
    return f"${valor:,.2f}"

def cerrar_mes_estadisticas(mes=None, año=None):
    """
    Cierra las estadísticas del mes especificado, excluyendo las ventas cerradas
    Args:
        mes (int): Mes a cerrar (1-12). Si es None, usa el mes actual
        año (int): Año a cerrar. Si es None, usa el año actual
    Returns:
        dict: Resumen del cierre mensual
    """
    if mes is None:
        mes = datetime.now().month
    if año is None:
        año = datetime.now().year
    
    # Obtener ventas cerradas que aún están en estadísticas
    ventas_a_excluir = [
        venta for venta in ventas 
        if venta['estado'] == 'Cerrada' and venta.get('incluida_en_estadisticas', True)
    ]
    
    # Marcar ventas como excluidas de estadísticas
    for venta in ventas_a_excluir:
        venta['incluida_en_estadisticas'] = False
        venta['mes_cierre'] = f"{año}-{mes:02d}"
    
    # Calcular resumen del cierre
    total_excluidas = len(ventas_a_excluir)
    valor_total_excluido = sum(venta['valor_total'] for venta in ventas_a_excluir)
    valor_abonado_excluido = sum(venta['abono'] for venta in ventas_a_excluir)
    
    resumen = {
        'mes': mes,
        'año': año,
        'ventas_excluidas': total_excluidas,
        'valor_total_excluido': valor_total_excluido,
        'valor_abonado_excluido': valor_abonado_excluido,
        'fecha_cierre': datetime.now().strftime("%Y-%m-%d %H:%M")
    }
    
    print(f"✅ Cierre mensual {mes}/{año}: {total_excluidas} ventas excluidas")
    return resumen

def obtener_ventas_cerradas_pendientes():
    """
    Obtiene las ventas cerradas que aún están incluidas en estadísticas
    Returns:
        list: Lista de ventas cerradas pendientes de cierre mensual
    """
    return [
        venta for venta in ventas 
        if venta['estado'] == 'Cerrada' and venta.get('incluida_en_estadisticas', True)
    ]

def obtener_estadisticas_por_periodo(fecha_inicio, fecha_fin):
    """
    Obtiene estadísticas de ventas en un período específico
    Args:
        fecha_inicio (str): Fecha de inicio en formato YYYY-MM-DD
        fecha_fin (str): Fecha de fin en formato YYYY-MM-DD
    Returns:
        dict: Estadísticas del período
    """
    try:
        # Convertir fechas a objetos datetime para comparación
        inicio = datetime.strptime(fecha_inicio, "%Y-%m-%d")
        fin = datetime.strptime(fecha_fin, "%Y-%m-%d")
        
        # Filtrar ventas en el período
        ventas_periodo = []
        for venta in ventas:
            fecha_venta = datetime.strptime(venta['fecha'], "%Y-%m-%d")
            if inicio <= fecha_venta <= fin:
                ventas_periodo.append(venta)
        
        # Calcular estadísticas
        total_ventas = len(ventas_periodo)
        total_valor = sum(venta['valor_total'] for venta in ventas_periodo)
        total_abonado = sum(venta['abono'] for venta in ventas_periodo)
        total_pendiente = sum(venta['saldo_pendiente'] for venta in ventas_periodo)
        
        # Ventas por estado
        ventas_activas = [v for v in ventas_periodo if v['estado'] == 'Activa']
        ventas_cerradas = [v for v in ventas_periodo if v['estado'] == 'Cerrada']
        
        # Estadísticas por rubro
        estadisticas_rubros = {}
        for rubro in RUBROS:
            ventas_rubro = [v for v in ventas_periodo if rubro in v['rubros']]
            estadisticas_rubros[rubro] = {
                'cantidad': len(ventas_rubro),
                'valor_total': sum(v['valor_total'] for v in ventas_rubro),
                'abonado': sum(v['abono'] for v in ventas_rubro),
                'pendiente': sum(v['saldo_pendiente'] for v in ventas_rubro)
            }
        
        # Ventas por día (para gráfica)
        ventas_por_dia = {}
        for venta in ventas_periodo:
            dia = venta['fecha']
            if dia not in ventas_por_dia:
                ventas_por_dia[dia] = {
                    'cantidad': 0,
                    'valor_total': 0,
                    'abonado': 0
                }
            ventas_por_dia[dia]['cantidad'] += 1
            ventas_por_dia[dia]['valor_total'] += venta['valor_total']
            ventas_por_dia[dia]['abonado'] += venta['abono']
        
        # Ordenar por fecha
        ventas_por_dia_ordenado = dict(sorted(ventas_por_dia.items()))
        
        return {
            'fecha_inicio': fecha_inicio,
            'fecha_fin': fecha_fin,
            'total_ventas': total_ventas,
            'total_valor': total_valor,
            'total_abonado': total_abonado,
            'total_pendiente': total_pendiente,
            'ventas_activas': len(ventas_activas),
            'ventas_cerradas': len(ventas_cerradas),
            'por_rubro': estadisticas_rubros,
            'por_dia': ventas_por_dia_ordenado,
            'ventas_detalle': ventas_periodo
        }
        
    except Exception as e:
        print(f"❌ Error en estadísticas por período: {e}")
        return None

# ========================================
# RUTAS DE LA APLICACIÓN
# ========================================

@app.route('/')
def index():
    """
    Página principal con formulario de registro y lista de ventas
    """
    estadisticas = obtener_estadisticas()
    # Solo mostrar ventas activas en la lista principal
    ventas_activas = [venta for venta in ventas if venta['estado'] == 'Activa']
    return render_template('index.html', 
                         ventas=ventas_activas, 
                         rubros=RUBROS,
                         estadisticas=estadisticas,
                         formatear_fecha=formatear_fecha,
                         formatear_moneda=formatear_moneda,
                         datetime=datetime)

@app.route('/agregar', methods=['POST'])
def agregar():
    """
    Ruta para agregar una nueva venta
    """
    try:
        cliente = request.form.get('cliente', '').strip()
        valor_total = request.form.get('valor_total', 0)
        abono = request.form.get('abono', 0)
        fecha = request.form.get('fecha', '').strip()
        rubros = request.form.getlist('rubros')
        
        # Validaciones
        if not cliente:
            print("❌ Error: Cliente vacío")
            return redirect('/')
        
        # Validación obligatoria de rubros
        if not rubros:
            print("❌ Error: Debe seleccionar al menos un rubro")
            return redirect('/')
        
        try:
            valor_total = float(valor_total) if valor_total else 0
            abono = float(abono) if abono else 0
        except ValueError as e:
            print(f"❌ Error al convertir valores numéricos: {e}")
            return redirect('/')
        
        if valor_total < 0 or abono < 0:
            print("❌ Error: Valores negativos no permitidos")
            return redirect('/')
        
        if not fecha:
            fecha = datetime.now().strftime("%Y-%m-%d")
        
        nueva_venta = agregar_venta(cliente, valor_total, abono, rubros, fecha)
        print(f"✅ Venta agregada: ID={nueva_venta['id']}, Cliente='{nueva_venta['cliente']}', Valor=${nueva_venta['valor_total']}, Rubros: {', '.join(rubros)}")
        
        return redirect('/')
        
    except Exception as e:
        print(f"❌ Error inesperado en agregar venta: {e}")
        return redirect('/')

@app.route('/eliminar/<int:id>')
def eliminar(id):
    """
    Ruta para eliminar una venta
    """
    if eliminar_venta(id):
        print(f"🗑️ Venta {id} eliminada")
    else:
        print(f"❌ Venta {id} no encontrada")
    
    return redirect('/')

@app.route('/api/estadisticas')
def api_estadisticas():
    """
    API para obtener estadísticas en formato JSON
    """
    return jsonify(obtener_estadisticas())

@app.route('/api/ventas')
def api_ventas():
    """
    API para obtener todas las ventas en formato JSON
    """
    return jsonify(ventas)

@app.route('/pago/<int:venta_id>', methods=['GET', 'POST'])
def gestionar_pago(venta_id):
    """
    Ruta para gestionar pagos de una venta específica
    """
    venta = obtener_venta(venta_id)
    if not venta:
        return redirect('/')
    
    if request.method == 'POST':
        try:
            monto_pago = float(request.form.get('monto_pago', 0))
            tipo_pago = request.form.get('tipo_pago', 'Abono')
            
            if monto_pago <= 0:
                print("❌ Error: Monto de pago inválido")
                return redirect(f'/pago/{venta_id}')
            
            venta_actualizada = registrar_pago(venta_id, monto_pago, tipo_pago)
            if venta_actualizada:
                print(f"✅ Pago registrado: Venta {venta_id}, Monto: ${monto_pago}")
                if venta_actualizada['estado'] == 'Cerrada':
                    print(f"🎉 Venta {venta_id} cerrada completamente")
            else:
                print(f"❌ Error al registrar pago en venta {venta_id}")
                
        except ValueError as e:
            print(f"❌ Error de validación: {e}")
        except Exception as e:
            print(f"❌ Error inesperado: {e}")
        
        return redirect('/')
    
    # GET: Mostrar formulario de pago
    return render_template('pago.html', venta=venta, formatear_moneda=formatear_moneda, formatear_fecha=formatear_fecha)

@app.route('/historial/<int:venta_id>')
def ver_historial(venta_id):
    """
    Ruta para ver el historial de pagos de una venta
    """
    venta = obtener_venta(venta_id)
    if not venta:
        return redirect('/')
    
    return render_template('historial.html', venta=venta, formatear_moneda=formatear_moneda, formatear_fecha=formatear_fecha)

@app.route('/buscar')
def buscar_ventas():
    """
    Ruta para buscar ventas por nombre de cliente
    """
    query = request.args.get('q', '').strip().lower()
    
    if not query:
        # Si no hay búsqueda, mostrar todas las ventas activas
        ventas_filtradas = [venta for venta in ventas if venta['estado'] == 'Activa']
    else:
        # Filtrar ventas activas que contengan el nombre del cliente
        ventas_filtradas = [
            venta for venta in ventas 
            if venta['estado'] == 'Activa' and query in venta['cliente'].lower()
        ]
    
    estadisticas = obtener_estadisticas()
    
    return render_template('index.html', 
                         ventas=ventas_filtradas, 
                         rubros=RUBROS,
                         estadisticas=estadisticas,
                         formatear_fecha=formatear_fecha,
                         formatear_moneda=formatear_moneda,
                         datetime=datetime,
                         busqueda=query)

@app.route('/cierre-mensual', methods=['GET', 'POST'])
def cierre_mensual():
    """
    Ruta para realizar el cierre mensual de estadísticas
    """
    if request.method == 'POST':
        try:
            mes = int(request.form.get('mes', datetime.now().month))
            año = int(request.form.get('año', datetime.now().year))
            
            resumen = cerrar_mes_estadisticas(mes, año)
            print(f"✅ Cierre mensual realizado: {resumen['ventas_excluidas']} ventas excluidas")
            
            return redirect('/')
            
        except Exception as e:
            print(f"❌ Error en cierre mensual: {e}")
            return redirect('/')
    
    # GET: Mostrar formulario de cierre mensual
    ventas_pendientes = obtener_ventas_cerradas_pendientes()
    estadisticas = obtener_estadisticas()
    
    return render_template('cierre_mensual.html', 
                         ventas_pendientes=ventas_pendientes,
                         estadisticas=estadisticas,
                         formatear_fecha=formatear_fecha,
                         formatear_moneda=formatear_moneda,
                         datetime=datetime)

@app.route('/ventas-excluidas')
def ventas_excluidas():
    """
    Ruta para ver las ventas excluidas de estadísticas
    """
    ventas_excluidas = [venta for venta in ventas if not venta.get('incluida_en_estadisticas', True)]
    estadisticas = obtener_estadisticas()
    
    return render_template('ventas_excluidas.html', 
                         ventas=ventas_excluidas,
                         estadisticas=estadisticas,
                         formatear_fecha=formatear_fecha,
                         formatear_moneda=formatear_moneda,
                         datetime=datetime)

@app.route('/estadisticas-periodo', methods=['GET', 'POST'])
def estadisticas_periodo():
    """
    Ruta para ver estadísticas por período de tiempo
    """
    if request.method == 'POST':
        fecha_inicio = request.form.get('fecha_inicio', '')
        fecha_fin = request.form.get('fecha_fin', '')
        
        if fecha_inicio and fecha_fin:
            estadisticas_periodo = obtener_estadisticas_por_periodo(fecha_inicio, fecha_fin)
            if estadisticas_periodo:
                return render_template('estadisticas_periodo.html',
                                     estadisticas=estadisticas_periodo,
                                     formatear_fecha=formatear_fecha,
                                     formatear_moneda=formatear_moneda,
                                     datetime=datetime,
                                     rubros=RUBROS)
            else:
                print("❌ Error al obtener estadísticas del período")
                return redirect('/estadisticas-periodo')
    
    # GET: Mostrar formulario de selección de período
    # Establecer fechas por defecto (último mes)
    fecha_fin = datetime.now().strftime("%Y-%m-%d")
    fecha_inicio = (datetime.now().replace(day=1)).strftime("%Y-%m-%d")
    
    return render_template('estadisticas_periodo.html',
                         fecha_inicio=fecha_inicio,
                         fecha_fin=fecha_fin,
                         formatear_fecha=formatear_fecha,
                         formatear_moneda=formatear_moneda,
                         datetime=datetime)

@app.route('/api/estadisticas-periodo')
def api_estadisticas_periodo():
    """
    API para obtener estadísticas por período en formato JSON
    """
    fecha_inicio = request.args.get('fecha_inicio', '')
    fecha_fin = request.args.get('fecha_fin', '')
    
    if fecha_inicio and fecha_fin:
        estadisticas = obtener_estadisticas_por_periodo(fecha_inicio, fecha_fin)
        if estadisticas:
            return jsonify(estadisticas)
    
    return jsonify({'error': 'Fechas requeridas'}), 400

# ========================================
# EJECUCIÓN PRINCIPAL
# ========================================

if __name__ == '__main__':
    import socket
    
    # Obtener la IP local de la máquina
    def get_local_ip():
        try:
            # Conectar a un servidor externo para obtener la IP local
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            ip = s.getsockname()[0]
            s.close()
            return ip
        except:
            return "127.0.0.1"
    
    local_ip = get_local_ip()
    port = 5000
    
    print("🚀 Iniciando mi Sistema de Ventas - Carloszerpav...")
    print(f"📱 Acceso local: http://localhost:{port}")
    print(f"🌐 Acceso en red: http://{local_ip}:{port}")
    print("📱 Para acceder desde móvil/otra PC en la misma red:")
    print(f"   - Abre el navegador y ve a: http://{local_ip}:{port}")
    print("   - Asegúrate de que el firewall permita conexiones en el puerto 5000")
    print("\n✨ Características de mi sistema - Carloszerpav:")
    print("   - Registro de ventas con cliente y valor")
    print("   - Cálculo automático de saldo pendiente")
    print("   - Selección múltiple de rubros")
    print("   - Fecha automática con opción de modificación")
    print("   - Modo oscuro predeterminado")
    print("   - Interfaz moderna y responsive")
    print("   - Estadísticas por rubro")
    print("   - Formato de moneda")
    print("   - Validación de formularios")
    print("   - Sistema de pagos en cuotas")
    print("   - Historial de pagos por venta")
    print("   - Buscador por nombre de cliente")
    print("   - Cierre mensual de estadísticas")
    print("   - Gestión de ventas excluidas")
    print("📋 Mis rubros de trabajo - Carloszerpav:")
    for rubro in RUBROS:
        print(f"   - {rubro}")
    print("📁 Estructura de archivos:")
    print("   - app.py (aplicación Flask)")
    print("   - templates/index.html (plantilla)")
    print("   - static/css/style.css (estilos)")
    print("   - static/js/script.js (JavaScript)")
    print("\n💡 Para mantener la aplicación funcionando:")
    print("   - No cierres esta ventana")
    print("   - Usa el archivo 'iniciar_app.bat' para ejecutar más fácilmente")
    print("   - O ejecuta: python app.py")
    print("\n🔒 Configuración de red:")
    print(f"   - Host: 0.0.0.0 (accesible desde cualquier IP)")
    print(f"   - Puerto: {port}")
    print(f"   - IP local: {local_ip}")
    
    app.run(debug=True, host='0.0.0.0', port=port)
