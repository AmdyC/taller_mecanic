import flet as ft
import pymysql

from cliente import Herramienta_Cliente
from proveedor import Herramienta_Proveedor
from producto import Herramienta_Producto
from empleado import Herramienta_Empleado
from usuario import Herramienta_Usuario

# =========================
# CONFIGURACIÓN BASE DE DATOS
# =========================

DB_CONFIG = {
    "host": "localhost",
    "port": 3306,
    "user": "root",       # <-- ajustá usuario si hace falta
    "password": "1234",   # <-- ajustá contraseña si hace falta
    "database": "taller_mecanico",
    "charset": "utf8mb4",
    "autocommit": True,
}


def conectar():
    """Devuelve una conexión a MySQL o None si falla."""
    try:
        conn = pymysql.connect(**DB_CONFIG)
        print("Conexión exitosa a MySQL")
        return conn
    except Exception as ex:
        print(f"Error al conectar a MySQL: {ex}")
        return None


def obtener_resumen():
    """
    Devuelve (resumen, error_db)
    resumen: dict con conteos de tablas
    error_db: texto de error o None
    """
    resumen = {
        "clientes": 0,
        "proveedores": 0,
        "productos": 0,
        "empleados": 0,
        "usuarios": 0,
    }
    conn = conectar()
    if not conn:
        return resumen, "No se pudo conectar a la base de datos."

    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT COUNT(*) FROM clientes")
            resumen["clientes"] = cursor.fetchone()[0]

            cursor.execute("SELECT COUNT(*) FROM proveedores")
            resumen["proveedores"] = cursor.fetchone()[0]

            cursor.execute("SELECT COUNT(*) FROM productos")
            resumen["productos"] = cursor.fetchone()[0]

            cursor.execute("SELECT COUNT(*) FROM mecanicos")
            resumen["empleados"] = cursor.fetchone()[0]

            cursor.execute("SELECT COUNT(*) FROM usuarios")
            resumen["usuarios"] = cursor.fetchone()[0]

        return resumen, None
    except Exception as ex:
        return resumen, f"Error consultando la base de datos: {ex}"
    finally:
        conn.close()


# =========================
# FUNCIONES BD: VEHÍCULOS
# =========================

def obtener_vehiculos():
    """Devuelve (lista_vehiculos, error)"""
    conn = conectar()
    if not conn:
        return [], "No se pudo conectar a la base de datos."

    vehiculos = []
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT patente, marca, modelo, color FROM vehiculos ORDER BY patente")
            vehiculos = cursor.fetchall()
        return vehiculos, None
    except Exception as ex:
        return [], f"Error consultando vehiculos: {ex}"
    finally:
        conn.close()


def guardar_vehiculo_bd(patente, marca, modelo, color):
    """
    Inserta o actualiza un vehículo.
    Si la patente ya existe, actualiza datos.
    """
    conn = conectar()
    if not conn:
        return "No se pudo conectar a la base de datos."

    try:
        with conn.cursor() as cursor:
            sql = """
                INSERT INTO vehiculos (patente, marca, modelo, color)
                VALUES (%s, %s, %s, %s)
                ON DUPLICATE KEY UPDATE
                    marca = VALUES(marca),
                    modelo = VALUES(modelo),
                    color = VALUES(color)
            """
            cursor.execute(sql, (patente, marca, modelo, color))
        return None
    except Exception as ex:
        return f"Error guardando vehiculo: {ex}"
    finally:
        conn.close()


# =========================
# FUNCIONES BD: PRESUPUESTOS
# =========================

def obtener_presupuestos():
    """Devuelve (lista_presupuestos, error)"""
    conn = conectar()
    if not conn:
        return [], "No se pudo conectar a la base de datos."

    presupuestos = []
    try:
        with conn.cursor() as cursor:
            cursor.execute(
                "SELECT id_presupuesto, dni_cliente, monto, estado, detalle, fecha_creacion "
                "FROM presupuestos ORDER BY fecha_creacion DESC"
            )
            presupuestos = cursor.fetchall()
        return presupuestos, None
    except Exception as ex:
        return [], f"Error consultando presupuestos: {ex}"
    finally:
        conn.close()


def insertar_presupuesto_bd(dni_cliente, monto, estado, detalle):
    conn = conectar()
    if not conn:
        return "No se pudo conectar a la base de datos."
    try:
        with conn.cursor() as cursor:
            sql = """
                INSERT INTO presupuestos (dni_cliente, monto, estado, detalle)
                VALUES (%s, %s, %s, %s)
            """
            cursor.execute(sql, (dni_cliente, monto, estado, detalle))
        return None
    except Exception as ex:
        return f"Error insertando presupuesto: {ex}"
    finally:
        conn.close()


def actualizar_presupuesto_bd(id_presupuesto, dni_cliente, monto, estado, detalle):
    conn = conectar()
    if not conn:
        return "No se pudo conectar a la base de datos."
    try:
        with conn.cursor() as cursor:
            sql = """
                UPDATE presupuestos
                   SET dni_cliente = %s,
                       monto = %s,
                       estado = %s,
                       detalle = %s
                 WHERE id_presupuesto = %s
            """
            cursor.execute(sql, (dni_cliente, monto, estado, detalle, id_presupuesto))
        return None
    except Exception as ex:
        return f"Error actualizando presupuesto: {ex}"
    finally:
        conn.close()


# =========================
# COMPONENTES DE UI
# =========================

def crear_sidebar(page: ft.Page, navegar_dashboard, titulo_seccion: str):
    """
    Sidebar a la izquierda con navegación básica.
    No usa icons ni colors de Flet, solo imágenes y textos.
    """

    def boton_nav(texto, icon_src, on_click, activo=False):
        # Para "simular" activo, cambiamos el color del texto
        color_texto = "white" if not activo else "#38BDF8"
        return ft.Container(
            padding=10,
            content=ft.TextButton(
                content=ft.Row(
                    [
                        ft.Image(src=icon_src, width=20, height=20),
                        ft.Text(texto, color=color_texto, size=13),
                    ],
                    spacing=8,
                    alignment=ft.MainAxisAlignment.START,
                ),
                on_click=on_click,
            ),
        )

    return ft.Container(
        width=230,
        bgcolor="#111827",
        padding=20,
        content=ft.Column(
            [
                ft.Row(
                    [
                        ft.Image(src="./iconos/auto.png", width=30, height=30),
                        ft.Column(
                            [
                                ft.Text(
                                    "Taller Mecánico",
                                    size=18,
                                    weight="bold",
                                    color="white",
                                ),
                                ft.Text(
                                    "Panel alternativo",
                                    size=11,
                                    color="#9CA3AF",
                                ),
                            ],
                            spacing=0,
                        ),
                    ],
                    spacing=10,
                ),
                ft.Divider(color="#1F2937"),
                ft.Text("Navegación", size=11, color="#9CA3AF"),
                boton_nav(
                    "Inicio",
                    "./iconos/Ficha.png",
                    lambda e: navegar_dashboard(page),
                    activo=(titulo_seccion == "Inicio"),
                ),
                ft.Text("Gestión", size=11, color="#9CA3AF"),
                boton_nav(
                    "Clientes",
                    "./iconos/Cliente.png",
                    lambda e: Herramienta_Cliente(page, navegar_dashboard),
                    activo=(titulo_seccion == "Clientes"),
                ),
                boton_nav(
                    "Proveedores",
                    "./iconos/proveedor.png",
                    lambda e: Herramienta_Proveedor(page, navegar_dashboard),
                    activo=(titulo_seccion == "Proveedores"),
                ),
                boton_nav(
                    "Productos",
                    "./iconos/caja-de-cambios.png",
                    lambda e: Herramienta_Producto(page, navegar_dashboard),
                    activo=(titulo_seccion == "Productos"),
                ),
                boton_nav(
                    "Empleados",
                    "./iconos/Empleado.png",
                    lambda e: Herramienta_Empleado(page, navegar_dashboard),
                    activo=(titulo_seccion == "Empleados"),
                ),
                boton_nav(
                    "Usuarios",
                    "./iconos/usuarios.png",
                    lambda e: Herramienta_Usuario(page, navegar_dashboard),
                    activo=(titulo_seccion == "Usuarios"),
                ),
                ft.Text("Administración", size=11, color="#9CA3AF"),
                boton_nav(
                    "Ficha del vehículo",
                    "./iconos/auto.png",
                    lambda e: ficha_tecnica(page, navegar_dashboard),
                    activo=(titulo_seccion == "Ficha"),
                ),
                boton_nav(
                    "Presupuestos",
                    "./iconos/Presupuesto.png",
                    lambda e: presupuesto(page, navegar_dashboard),
                    activo=(titulo_seccion == "Presupuesto"),
                ),
                ft.Container(expand=True),
                ft.Divider(color="#1F2937"),
                ft.TextButton(
                    "Salir del sistema",
                    on_click=lambda e: page.window.close(),
                    style=ft.ButtonStyle(
                        color="red",
                    ),
                ),
            ],
            spacing=5,
            expand=True,
        ),
    )


def tarjeta_resumen(titulo: str, valor: int, icon_src: str):
    """
    Tarjeta simple sin BoxShadow ni cosas raras.
    """
    return ft.Container(
        bgcolor="white",
        padding=12,
        border_radius=8,
        border=ft.border.all(1, "#E5E7EB"),
        content=ft.Row(
            [
                ft.Image(src=icon_src, width=32, height=32),
                ft.Column(
                    [
                        ft.Text(titulo, size=11, color="#6B7280"),
                        ft.Text(str(valor), size=18, weight="bold", color="#111827"),
                    ],
                    spacing=2,
                ),
            ],
            spacing=10,
            alignment=ft.MainAxisAlignment.START,
        ),
    )


# =========================
# VISTAS
# =========================

def dashboard(page: ft.Page):
    """Vista principal con resumen de datos."""

    page.clean()

    resumen, error_db = obtener_resumen()

    sidebar = crear_sidebar(page, dashboard, "Inicio")

    contenido = ft.Column(
        [
            ft.Text("Panel general del taller", size=22, weight="bold", color="#111827"),
            ft.Text(
                "Esta es una versión alternativa del sistema, con otro diseño pero misma lógica.",
                size=12,
                color="#6B7280",
            ),
            ft.Divider(),
        ],
        spacing=5,
    )

    if error_db:
        contenido.controls.append(
            ft.Container(
                bgcolor="#FEE2E2",
                padding=10,
                border_radius=8,
                content=ft.Text(error_db, color="#B91C1C"),
            )
        )
    else:
        contenido.controls.append(
            ft.Row(
                [
                    tarjeta_resumen("Clientes", resumen["clientes"], "./iconos/Cliente.png"),
                    tarjeta_resumen("Proveedores", resumen["proveedores"], "./iconos/proveedor.png"),
                    tarjeta_resumen("Productos", resumen["productos"], "./iconos/caja-de-cambios.png"),
                    tarjeta_resumen("Empleados", resumen["empleados"], "./iconos/Empleado.png"),
                    tarjeta_resumen("Usuarios", resumen["usuarios"], "./iconos/usuarios.png"),
                ],
                spacing=12,
                wrap=True,
            )
        )

    contenido.controls.append(
        ft.Container(
            margin=ft.margin.only(top=20),
            content=ft.Text(
                "Desde este panel podés ir a cada módulo usando el menú de la izquierda.",
                size=12,
                color="#6B7280",
            ),
        )
    )

    layout = ft.Row(
        [
            sidebar,
            ft.Container(
                bgcolor="#F3F4F6",
                padding=20,
                expand=True,
                content=contenido,
            ),
        ],
        expand=True,
    )

    page.add(layout)
    page.update()


def ficha_tecnica(page: ft.Page, navegar_dashboard):
    page.clean()

    sidebar = crear_sidebar(page, navegar_dashboard, "Ficha")

    txt_patente = ft.TextField(label="Patente", width=150)
    txt_marca = ft.TextField(label="Marca", width=150)
    txt_modelo = ft.TextField(label="Modelo", width=150)
    txt_color = ft.TextField(label="Color", width=150)

    lbl_error = ft.Text("", color="#B91C1C", size=11)
    lbl_ok = ft.Text("", color="#15803D", size=11)

    tabla_vehiculos = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("Patente")),
            ft.DataColumn(ft.Text("Marca")),
            ft.DataColumn(ft.Text("Modelo")),
            ft.DataColumn(ft.Text("Color")),
        ],
        rows=[],
    )

    def cargar_tabla():
        vehiculos, error = obtener_vehiculos()
        tabla_vehiculos.rows.clear()
        lbl_error.value = ""
        lbl_ok.value = ""
        if error:
            lbl_error.value = error
        else:
            for v in vehiculos:
                patente, marca, modelo, color = v

                def on_select(e, p=patente, m=marca, mo=modelo, c=color):
                    txt_patente.value = p
                    txt_marca.value = m
                    txt_modelo.value = mo
                    txt_color.value = c
                    lbl_error.value = ""
                    lbl_ok.value = ""
                    page.update()

                tabla_vehiculos.rows.append(
                    ft.DataRow(
                        cells=[
                            ft.DataCell(ft.Text(patente)),
                            ft.DataCell(ft.Text(marca)),
                            ft.DataCell(ft.Text(modelo)),
                            ft.DataCell(ft.Text(color)),
                        ],
                        on_select_changed=on_select,
                    )
                )
        page.update()

    def limpiar_campos(e=None):
        txt_patente.value = ""
        txt_marca.value = ""
        txt_modelo.value = ""
        txt_color.value = ""
        lbl_error.value = ""
        lbl_ok.value = ""
        page.update()

    def guardar_click(e):
        lbl_error.value = ""
        lbl_ok.value = ""
        patente = (txt_patente.value or "").strip()
        marca = (txt_marca.value or "").strip()
        modelo = (txt_modelo.value or "").strip()
        color = (txt_color.value or "").strip()

        if not patente or not marca or not modelo or not color:
            lbl_error.value = "Todos los campos son obligatorios."
            page.update()
            return

        err = guardar_vehiculo_bd(patente, marca, modelo, color)
        if err:
            lbl_error.value = err
        else:
            lbl_ok.value = "Vehículo guardado correctamente."
            cargar_tabla()

        page.update()

    btn_guardar = ft.ElevatedButton("Guardar / Actualizar", on_click=guardar_click)
    btn_limpiar = ft.ElevatedButton("Limpiar", on_click=limpiar_campos)
    btn_volver = ft.ElevatedButton("Volver al panel", on_click=lambda e: navegar_dashboard(page))

    contenido = ft.Column(
        [
            ft.Text("Ficha técnica del vehículo", size=22, weight="bold", color="#111827"),
            ft.Text(
                "Formulario para registrar y consultar vehículos por patente.",
                size=12,
                color="#6B7280",
            ),
            ft.Divider(),
            ft.Row([txt_patente, txt_marca, txt_modelo, txt_color], spacing=10),
            ft.Row([btn_guardar, btn_limpiar, btn_volver], spacing=10),
            lbl_error,
            lbl_ok,
            ft.Text("Vehículos registrados", size=14, weight="bold"),
            ft.Container(
                bgcolor="white",
                border_radius=8,
                border=ft.border.all(1, "#E5E7EB"),
                padding=10,
                content=tabla_vehiculos,
            ),
        ],
        spacing=8,
    )

    layout = ft.Row(
        [
            sidebar,
            ft.Container(
                bgcolor="#F3F4F6",
                padding=20,
                expand=True,
                content=contenido,
            ),
        ],
        expand=True,
    )

    page.add(layout)
    cargar_tabla()
    page.update()


def presupuesto(page: ft.Page, navegar_dashboard):
    page.clean()

    sidebar = crear_sidebar(page, navegar_dashboard, "Presupuesto")

    txt_dni = ft.TextField(label="DNI Cliente", width=150)
    txt_monto = ft.TextField(label="Monto", width=100)
    dd_estado = ft.Dropdown(
        label="Estado",
        width=140,
        options=[
            ft.dropdown.Option("Pendiente"),
            ft.dropdown.Option("Aprobado"),
            ft.dropdown.Option("Rechazado"),
        ],
        value="Pendiente",
    )
    txt_detalle = ft.TextField(label="Detalle", multiline=True, min_lines=2, max_lines=4, width=350)

    lbl_error = ft.Text("", color="#B91C1C", size=11)
    lbl_ok = ft.Text("", color="#15803D", size=11)

    presupuesto_seleccionado_id = {"id": None}

    tabla_presupuestos = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("ID")),
            ft.DataColumn(ft.Text("DNI")),
            ft.DataColumn(ft.Text("Monto")),
            ft.DataColumn(ft.Text("Estado")),
            ft.DataColumn(ft.Text("Fecha")),
        ],
        rows=[],
    )

    def cargar_tabla():
        presupuestos, error = obtener_presupuestos()
        tabla_presupuestos.rows.clear()
        lbl_error.value = ""
        lbl_ok.value = ""
        presupuesto_seleccionado_id["id"] = None
        if error:
            lbl_error.value = error
        else:
            for p in presupuestos:
                pid, dni, monto, estado, detalle, fecha = p

                def on_select(e, _id=pid, _dni=dni, _monto=monto, _estado=estado, _detalle=detalle):
                    presupuesto_seleccionado_id["id"] = _id
                    txt_dni.value = _dni
                    txt_monto.value = str(_monto)
                    dd_estado.value = _estado
                    txt_detalle.value = _detalle or ""
                    lbl_error.value = ""
                    lbl_ok.value = ""
                    page.update()

                tabla_presupuestos.rows.append(
                    ft.DataRow(
                        cells=[
                            ft.DataCell(ft.Text(str(pid))),
                            ft.DataCell(ft.Text(dni)),
                            ft.DataCell(ft.Text(str(monto))),
                            ft.DataCell(ft.Text(estado)),
                            ft.DataCell(ft.Text(str(fecha))),
                        ],
                        on_select_changed=on_select,
                    )
                )
        page.update()

    def limpiar_campos(e=None):
        txt_dni.value = ""
        txt_monto.value = ""
        dd_estado.value = "Pendiente"
        txt_detalle.value = ""
        lbl_error.value = ""
        lbl_ok.value = ""
        presupuesto_seleccionado_id["id"] = None
        page.update()

    def guardar_nuevo(e):
        lbl_error.value = ""
        lbl_ok.value = ""
        dni = (txt_dni.value or "").strip()
        monto_txt = (txt_monto.value or "").strip()
        estado = dd_estado.value
        detalle = (txt_detalle.value or "").strip()

        if not dni or not monto_txt or not estado:
            lbl_error.value = "DNI, Monto y Estado son obligatorios."
            page.update()
            return

        try:
            monto = float(monto_txt)
        except ValueError:
            lbl_error.value = "El monto debe ser numérico."
            page.update()
            return

        err = insertar_presupuesto_bd(dni, monto, estado, detalle)
        if err:
            lbl_error.value = err
        else:
            lbl_ok.value = "Presupuesto cargado correctamente."
            limpiar_campos()
            cargar_tabla()

        page.update()

    def actualizar_existente(e):
        lbl_error.value = ""
        lbl_ok.value = ""
        if presupuesto_seleccionado_id["id"] is None:
            lbl_error.value = "Primero seleccioná un presupuesto de la lista."
            page.update()
            return

        dni = (txt_dni.value or "").strip()
        monto_txt = (txt_monto.value or "").strip()
        estado = dd_estado.value
        detalle = (txt_detalle.value or "").strip()

        if not dni or not monto_txt or not estado:
            lbl_error.value = "DNI, Monto y Estado son obligatorios."
            page.update()
            return

        try:
            monto = float(monto_txt)
        except ValueError:
            lbl_error.value = "El monto debe ser numérico."
            page.update()
            return

        err = actualizar_presupuesto_bd(
            presupuesto_seleccionado_id["id"],
            dni,
            monto,
            estado,
            detalle,
        )
        if err:
            lbl_error.value = err
        else:
            lbl_ok.value = "Presupuesto actualizado correctamente."
            limpiar_campos()
            cargar_tabla()

        page.update()

    btn_nuevo = ft.ElevatedButton("Guardar nuevo", on_click=guardar_nuevo)
    btn_actualizar = ft.ElevatedButton("Actualizar seleccionado", on_click=actualizar_existente)
    btn_limpiar = ft.ElevatedButton("Limpiar", on_click=limpiar_campos)
    btn_volver = ft.ElevatedButton("Volver al panel", on_click=lambda e: navegar_dashboard(page))

    contenido = ft.Column(
        [
            ft.Text("Presupuesto", size=22, weight="bold", color="#111827"),
            ft.Text(
                "Registro y actualización de presupuestos del taller.",
                size=12,
                color="#6B7280",
            ),
            ft.Divider(),
            ft.Row([txt_dni, txt_monto, dd_estado], spacing=10),
            txt_detalle,
            ft.Row([btn_nuevo, btn_actualizar, btn_limpiar, btn_volver], spacing=10),
            lbl_error,
            lbl_ok,
            ft.Text("Presupuestos registrados", size=14, weight="bold"),
            ft.Container(
                bgcolor="white",
                border_radius=8,
                border=ft.border.all(1, "#E5E7EB"),
                padding=10,
                content=tabla_presupuestos,
            ),
        ],
        spacing=8,
    )

    layout = ft.Row(
        [
            sidebar,
            ft.Container(
                bgcolor="#F3F4F6",
                padding=20,
                expand=True,
                content=contenido,
            ),
        ],
        expand=True,
    )

    page.add(layout)
    cargar_tabla()
    page.update()


# =========================
# PUNTO DE ENTRADA FLET
# =========================

def main(page: ft.Page):
    page.title = "Taller Mecánico - Variante"
    page.window.maximized = True
    page.horizontal_alignment = ft.CrossAxisAlignment.STRETCH
    page.vertical_alignment = ft.MainAxisAlignment.START
    dashboard(page)


if __name__ == "__main__":
    ft.app(target=main)
