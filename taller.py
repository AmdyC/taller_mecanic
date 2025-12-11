import flet as ft
import pymysql
from cliente import Herramienta_Cliente
from proveedor import Herramienta_Proveedor
from producto import Herramienta_Producto
from empleado import Herramienta_Empleado
from usuario import Herramienta_Usuario

def conectar():
    import time
    try:
        start = time.time()
        conn = pymysql.connect(
            host='localhost',
            port=3306,
            user='root',
            password='1234',
            database='taller_mecanico',
            connect_timeout=5,
            charset='utf8mb4',
            autocommit=True
        )
        print(f"Conexión exitosa")
        return conn
    except Exception as ex:
        print(f"Error al conectar a MySQL: {ex}")
        return ex

def menu_principal(page: ft.Page):
    page.window.maximized = True
    page.title = "Taller Mecánico"
    iconos = {
        "cliente": ft.Image(src="./iconos/Cliente.png", width=32, height=32),
        "proveedor": ft.Image(src="./iconos/proveedor.png", width=32, height=32),
        "producto": ft.Image(src="./iconos/caja-de-cambios.png", width=32, height=32),
        "empleado": ft.Image(src="./iconos/Empleado.png", width=32, height=32),
        "usuario": ft.Image(src="./iconos/usuarios.png", width=32, height=32),
        "ficha": ft.Image(src="./iconos/auto.png", width=32, height=32),
        "presupuesto": ft.Image(src="./iconos/Presupuesto.png", width=32, height=32)
    }
    conn = conectar()
    resumen = {}
    error_db = None
    if conn and not isinstance(conn, Exception):
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM clientes")
            resumen['clientes'] = cursor.fetchone()[0]
            cursor.execute("SELECT COUNT(*) FROM proveedores")
            resumen['proveedores'] = cursor.fetchone()[0]
            cursor.execute("SELECT COUNT(*) FROM productos")
            resumen['productos'] = cursor.fetchone()[0]
            cursor.execute("SELECT COUNT(*) FROM mecanicos")
            resumen['empleados'] = cursor.fetchone()[0]
            cursor.execute("SELECT COUNT(*) FROM usuarios")
            resumen['usuarios'] = cursor.fetchone()[0]
        except Exception as ex:
            error_db = f"Error consultando la base de datos: {ex}"
        finally:
            cursor.close()
            conn.close()
    elif isinstance(conn, Exception):
        error_db = f"No se pudo conectar a la base de datos. Error: {conn}"
    else:
        error_db = "No se pudo conectar a la base de datos. Verifique configuración y servidor MySQL."
    archivo_menu = ft.PopupMenuButton(
        items=[
            ft.PopupMenuItem(text="Copiar", icon=ft.Image(src="./iconos/bandeja-de-entrada.png", width=24, height=24)),
            ft.PopupMenuItem(text="Pegar", icon=ft.Image(src="./iconos/papel.png", width=24, height=24)),
            ft.PopupMenuItem(text="Salir", icon=ft.Image(src="./iconos/nota-adhesiva.png", width=24, height=24), on_click=lambda e: page.window.close()),
        ],
        content=ft.Row([ft.Image(src="./iconos/carpeta.png", width=24, height=24), ft.Text("Archivo")]), tooltip="Archivo"
    )
    herramientas_menu = ft.PopupMenuButton(
        items=[
            ft.PopupMenuItem(content=ft.Row([iconos["cliente"], ft.Text("Cliente")]), on_click=lambda e: Herramienta_Cliente(page, menu_principal), tooltip="Gestión de clientes"),
            ft.PopupMenuItem(content=ft.Row([iconos["proveedor"], ft.Text("Proveedor")]), on_click=lambda e: Herramienta_Proveedor(page, menu_principal), tooltip="Gestión de proveedores"),
            ft.PopupMenuItem(content=ft.Row([iconos["producto"], ft.Text("Producto")]), on_click=lambda e: Herramienta_Producto(page, menu_principal), tooltip="Gestión de productos"),
            ft.PopupMenuItem(content=ft.Row([iconos["empleado"], ft.Text("Empleado")]), on_click=lambda e: Herramienta_Empleado(page, menu_principal), tooltip="Gestión de empleados"),
            ft.PopupMenuItem(content=ft.Row([iconos["usuario"], ft.Text("Usuario")]), on_click=lambda e: Herramienta_Usuario(page, menu_principal), tooltip="Gestión de usuarios"),
        ],
        content=ft.Row([ft.Image(src="./iconos/gestion-de-proyectos.png", width=24, height=24), ft.Text("Herramientas")]), tooltip="Herramientas"
    )
    administracion_menu = ft.PopupMenuButton(
        items=[
            ft.PopupMenuItem(content=ft.Row([iconos["ficha"], ft.Text("Ficha del Vehículo")]), on_click=lambda e: ficha_tecnica(page), tooltip="Ficha técnica"),
            ft.PopupMenuItem(content=ft.Row([iconos["presupuesto"], ft.Text("Presupuesto")]), on_click=lambda e: presupuesto(page), tooltip="Presupuestos"),
        ],
        content=ft.Row([ft.Image(src="./iconos/Ficha.png", width=24, height=24), ft.Text("Administración")]), tooltip="Administración"
    )
    barra_menu = ft.Row([
        archivo_menu,
        herramientas_menu,
        administracion_menu
    ], alignment=ft.MainAxisAlignment.START, spacing=20)
    acceso_rapido = ft.Row([
        ft.IconButton(content=iconos["cliente"], tooltip="Clientes", on_click=lambda e: Herramienta_Cliente(page, menu_principal)),
        ft.IconButton(content=iconos["proveedor"], tooltip="Proveedores", on_click=lambda e: Herramienta_Proveedor(page, menu_principal)),
        ft.IconButton(content=iconos["producto"], tooltip="Productos", on_click=lambda e: Herramienta_Producto(page, menu_principal)),
        ft.IconButton(content=iconos["empleado"], tooltip="Empleados", on_click=lambda e: Herramienta_Empleado(page, menu_principal)),
        ft.IconButton(content=iconos["usuario"], tooltip="Usuarios", on_click=lambda e: Herramienta_Usuario(page, menu_principal)),
    ], alignment=ft.MainAxisAlignment.START, spacing=16)
    resumen_items = []
    if error_db:
        resumen_items.append(ft.Text(error_db, color="#FF0000", size=16))
    else:
        resumen_items.append(ft.Text("Resumen de datos", size=20, weight="bold"))
        resumen_items.append(ft.Row([
            ft.Image(src="./iconos/Cliente.png", width=24, height=24), ft.Text(f"Clientes: {resumen.get('clientes', 0)}"),
            ft.Image(src="./iconos/proveedor.png", width=24, height=24), ft.Text(f"Proveedores: {resumen.get('proveedores', 0)}"),
            ft.Image(src="./iconos/caja-de-cambios.png", width=24, height=24), ft.Text(f"Productos: {resumen.get('productos', 0)}"),
            ft.Image(src="./iconos/Empleado.png", width=24, height=24), ft.Text(f"Empleados: {resumen.get('empleados', 0)}"),
            ft.Image(src="./iconos/usuarios.png", width=24, height=24), ft.Text(f"Usuarios: {resumen.get('usuarios', 0)}"),
        ], spacing=16))
    page.clean()
    page.add(
        ft.Container(
            content=ft.Column([
                barra_menu,
                ft.Divider(),
                acceso_rapido,
                ft.Divider(),
                *resumen_items
            ], alignment=ft.MainAxisAlignment.START),
            padding=20
        )
    )
    page.update()

def ficha_tecnica(page: ft.Page):
    page.clean()
    txt_patente = ft.TextField(label="Patente", width=260)
    txt_marca = ft.TextField(label="Marca", width=260)
    txt_modelo = ft.TextField(label="Modelo", width=260)
    txt_color = ft.TextField(label="Color", width=260)
    btn_volver = ft.ElevatedButton("Volver", on_click=lambda e: menu_principal(page))
    page.add(
        ft.Text("Ficha Técnica del Vehículo", size=22, weight="bold"),
        txt_patente,
        txt_marca,
        txt_modelo,
        txt_color,
        btn_volver
    )
    page.update()

def presupuesto(page: ft.Page):
    page.clean()
    txt_dni = ft.TextField(label="DNI Cliente", width=260)
    txt_monto = ft.TextField(label="Monto", width=260)
    txt_estado = ft.TextField(label="Estado", width=260)
    btn_volver = ft.ElevatedButton("Volver", on_click=lambda e: menu_principal(page))
    page.add(
        ft.Text("Presupuesto", size=22, weight="bold"),
        txt_dni,
        txt_monto,
        txt_estado,
        btn_volver
    )
    page.update()

def main(page: ft.Page):
    menu_principal(page)

ft.app(target=main)
