import flet as ft
import pymysql

def conectar():
    try:
        conn = pymysql.connect(
            host='localhost',
            port=3306,
            user='root',
            password='1234',
            database='taller_mecanico',
            charset='utf8mb4',
            autocommit=True
        )
        return conn
    except Exception:
        return None

class Herramienta_Cliente:
    def __init__(self, page, volver):
        self.page = page
        self.volver = volver
        self.conn = conectar()
        self.cursor = self.conn.cursor() if self.conn else None
        self.armar_ui()
        self.mostrar_clientes()

    def armar_ui(self):
        self.page.clean()
        self.txt_dni = ft.TextField(label="DNI", width=260)
        self.txt_nombre = ft.TextField(label="Nombre", width=260)
        self.txt_apellido = ft.TextField(label="Apellido", width=260)
        self.txt_direccion = ft.TextField(label="Dirección", width=260)
        self.txt_telefono = ft.TextField(label="Teléfono", width=260)
        btn_guardar = ft.ElevatedButton("Guardar", on_click=self.guardar)
        btn_limpiar = ft.ElevatedButton("Limpiar", on_click=self.limpiar)
        btn_alta = ft.ElevatedButton("Alta", on_click=self.alta)
        btn_baja = ft.ElevatedButton("Baja", on_click=self.baja)
        btn_consulta = ft.ElevatedButton("Consulta", on_click=self.consulta)
        btn_volver = ft.ElevatedButton("Volver", on_click=self.volver_menu)
        self.tabla = ft.DataTable(
            columns=[
                ft.DataColumn(label=ft.Text("DNI")),
                ft.DataColumn(label=ft.Text("Nombre")),
                ft.DataColumn(label=ft.Text("Apellido")),
                ft.DataColumn(label=ft.Text("Dirección")),
                ft.DataColumn(label=ft.Text("Teléfono")),
                ft.DataColumn(label=ft.Text("Acciones")),
            ],
            rows=[]
        )
        self.formulario = ft.Column([
            ft.Text("Clientes", size=22, weight="bold"),
            self.txt_dni,
            self.txt_nombre,
            self.txt_apellido,
            self.txt_direccion,
            self.txt_telefono,
            ft.Row([btn_alta, btn_baja, btn_guardar, btn_limpiar, btn_volver], spacing=10),
            ft.Divider(),
        ])
        self.contenedor = ft.Column([
            self.formulario,
            self.tabla
        ])
        self.page.add(self.contenedor)
        self.page.update()

    def mostrar_clientes(self):
        self.tabla.rows.clear()
        if not self.cursor:
            self.tabla.rows.append(ft.DataRow(cells=[
                ft.DataCell(ft.Text("")),
                ft.DataCell(ft.Text("")),
                ft.DataCell(ft.Text("")),
                ft.DataCell(ft.Text("")),
                ft.DataCell(ft.Text("")),
                ft.DataCell(ft.Text("Error de conexión a la base de datos", style=ft.TextStyle(color="red"))),
            ]))
            self.page.update()
            return
        try:
            self.cursor.execute("SELECT dni, nombre, apellido, direccion, telefono FROM clientes")
            filas = self.cursor.fetchall()
            if not filas:
                self.tabla.rows.append(ft.DataRow(cells=[
                    ft.DataCell(ft.Text("")),
                    ft.DataCell(ft.Text("")),
                    ft.DataCell(ft.Text("")),
                    ft.DataCell(ft.Text("")),
                    ft.DataCell(ft.Text("")),
                    ft.DataCell(ft.Text("No hay clientes cargados", style=ft.TextStyle(color="#888"))),
                ]))
            else:
                for fila in filas:
                    dni = fila[0]
                    self.tabla.rows.append(ft.DataRow(cells=[
                        ft.DataCell(ft.Text(str(dni))),
                        ft.DataCell(ft.Text(fila[1])),
                        ft.DataCell(ft.Text(fila[2])),
                        ft.DataCell(ft.Text(fila[3])),
                        ft.DataCell(ft.Text(fila[4])),
                        ft.DataCell(ft.Row([
                            ft.IconButton(content=ft.Image(src="iconos/modificar.png", width=24, height=24), tooltip="Editar", on_click=lambda e, id=dni: self.cargar_editar(id)),
                            ft.IconButton(content=ft.Image(src="iconos/borrar.png", width=24, height=24), tooltip="Borrar", on_click=lambda e, id=dni: self.borrar(id)),
                        ]))
                    ]))
        except Exception as ex:
            self.tabla.rows.append(ft.DataRow(cells=[
                ft.DataCell(ft.Text("")),
                ft.DataCell(ft.Text("")),
                ft.DataCell(ft.Text("")),
                ft.DataCell(ft.Text("")),
                ft.DataCell(ft.Text("")),
                ft.DataCell(ft.Text(f"Error: {ex}", style=ft.TextStyle(color="red"))),
            ]))
        self.page.update()

    def guardar(self, e):
        dni = self.txt_dni.value.strip()
        nombre = self.txt_nombre.value.strip()
        apellido = self.txt_apellido.value.strip()
        direccion = self.txt_direccion.value.strip()
        telefono = self.txt_telefono.value.strip()
        if dni and nombre and apellido and direccion and telefono:
            if hasattr(self, 'editando') and self.editando:
                # Si está editando, actualiza el cliente con el DNI original
                self.cursor.execute("UPDATE clientes SET dni=%s, nombre=%s, apellido=%s, direccion=%s, telefono=%s WHERE dni=%s", (dni, nombre, apellido, direccion, telefono, self.editando))
                self.conn.commit()
                self.editando = None
            else:
                self.cursor.execute("INSERT INTO clientes (dni, nombre, apellido, direccion, telefono) VALUES (%s, %s, %s, %s, %s)", (dni, nombre, apellido, direccion, telefono))
                self.conn.commit()
        self.limpiar()
        self.mostrar_clientes()
    def alta(self, e):
        dni = self.txt_dni.value.strip()
        nombre = self.txt_nombre.value.strip()
        apellido = self.txt_apellido.value.strip()
        direccion = self.txt_direccion.value.strip()
        telefono = self.txt_telefono.value.strip()
        if dni and nombre and apellido and direccion and telefono:
            self.cursor.execute("SELECT dni FROM clientes WHERE dni=%s", (dni,))
            if not self.cursor.fetchone():
                self.cursor.execute("INSERT INTO clientes (dni, nombre, apellido, direccion, telefono) VALUES (%s, %s, %s, %s, %s)", (dni, nombre, apellido, direccion, telefono))
                self.conn.commit()
        self.limpiar()
        self.mostrar_clientes()

    def baja(self, e):
        dni = self.txt_dni.value.strip()
        if dni:
            self.cursor.execute("DELETE FROM clientes WHERE dni=%s", (dni,))
            self.conn.commit()
        self.limpiar()
        self.mostrar_clientes()

    def consulta(self, e):
        dni = self.txt_dni.value.strip()
        if dni:
            self.cursor.execute("SELECT nombre, apellido, direccion, telefono FROM clientes WHERE dni=%s", (dni,))
            data = self.cursor.fetchone()
            if data:
                self.txt_nombre.value = data[0]
                self.txt_apellido.value = data[1]
                self.txt_direccion.value = data[2]
                self.txt_telefono.value = data[3]
        self.page.update()
        self.mostrar_clientes()

    def limpiar(self, e=None):
        self.txt_dni.value = ""
        self.txt_nombre.value = ""
        self.txt_apellido.value = ""
        self.txt_direccion.value = ""
        self.txt_telefono.value = ""
        self.editando = None
        self.page.update()
        self.mostrar_clientes()

    def cargar_editar(self, dni):
        self.cursor.execute("SELECT dni, nombre, apellido, direccion, telefono FROM clientes WHERE dni=%s", (dni,))
        data = self.cursor.fetchone()
        if data:
            self.txt_dni.value = data[0]
            self.txt_nombre.value = data[1]
            self.txt_apellido.value = data[2]
            self.txt_direccion.value = data[3]
            self.txt_telefono.value = data[4]
            self.editando = data[0]
            self.page.update()

    def borrar(self, dni):
        self.cursor.execute("DELETE FROM clientes WHERE dni=%s", (dni,))
        self.conn.commit()
        self.mostrar_clientes()

    def volver_menu(self, e):
        self.page.clean()
        self.volver(self.page)
        self.page.update()