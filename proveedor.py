
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

class Herramienta_Proveedor:
    def __init__(self, page, volver):
        self.page = page
        self.volver = volver
        self.conn = conectar()
        self.cursor = self.conn.cursor() if self.conn else None
        self.armar_ui()
        self.mostrar_proveedores()

    def armar_ui(self):
        self.page.clean()
        self.txt_nombre = ft.TextField(label="Nombre", width=260)
        self.txt_cuit = ft.TextField(label="CUIT", width=260)
        self.txt_telefono = ft.TextField(label="Teléfono", width=260)
        self.txt_direccion = ft.TextField(label="Dirección", width=260)
        btn_alta = ft.ElevatedButton("Alta", on_click=self.alta)
        btn_baja = ft.ElevatedButton("Baja", on_click=self.baja)
        btn_consulta = ft.ElevatedButton("Consulta", on_click=self.consulta)
        btn_guardar = ft.ElevatedButton("Guardar", on_click=self.guardar)
        btn_volver = ft.ElevatedButton("Volver", on_click=self.volver_menu)
        self.tabla = ft.DataTable(
            columns=[
                ft.DataColumn(label=ft.Text("ID")),
                ft.DataColumn(label=ft.Text("Nombre")),
                ft.DataColumn(label=ft.Text("CUIT")),
                ft.DataColumn(label=ft.Text("Teléfono")),
                ft.DataColumn(label=ft.Text("Dirección")),
                ft.DataColumn(label=ft.Text("Acciones")),
            ],
            rows=[]
        )
        self.formulario = ft.Column([
            ft.Text("Proveedores", size=22, weight="bold"),
            self.txt_nombre,
            self.txt_cuit,
            self.txt_telefono,
            self.txt_direccion,
            ft.Row([btn_alta, btn_baja, btn_guardar, btn_consulta, btn_volver], spacing=10),
            ft.Divider(),
        ])
        self.contenedor = ft.Column([
            self.formulario,
            self.tabla
        ])
        self.page.add(self.contenedor)
        self.page.update()
    def guardar(self, e):
        nombre = self.txt_nombre.value.strip()
        cuit = self.txt_cuit.value.strip()
        telefono = self.txt_telefono.value.strip()
        direccion = self.txt_direccion.value.strip()
        if nombre and cuit and telefono and direccion:
            if hasattr(self, 'editando') and self.editando:
                self.cursor.execute("UPDATE proveedores SET nombre=%s, cuit=%s, telefono=%s, direccion=%s WHERE id=%s", (nombre, cuit, telefono, direccion, self.editando))
                self.conn.commit()
                self.editando = None
        self.limpiar()
        self.mostrar_proveedores()

    def mostrar_proveedores(self):
        self.tabla.rows.clear()
        if not self.cursor:
            self.page.update()
            return
        try:
            self.cursor.execute("SELECT id, nombre, cuit, telefono, direccion FROM proveedores")
            for fila in self.cursor.fetchall():
                idp = fila[0]
                self.tabla.rows.append(ft.DataRow(cells=[
                    ft.DataCell(ft.Text(str(idp))),
                    ft.DataCell(ft.Text(fila[1])),
                    ft.DataCell(ft.Text(fila[2])),
                    ft.DataCell(ft.Text(fila[3])),
                    ft.DataCell(ft.Text(fila[4])),
                        ft.DataCell(ft.Row([
                            ft.IconButton(content=ft.Image(src="iconos/modificar.png", width=24, height=24), tooltip="Editar", on_click=lambda e, id=idp: self.cargar_editar(id)),
                            ft.IconButton(content=ft.Image(src="iconos/borrar.png", width=24, height=24), tooltip="Borrar", on_click=lambda e, id=idp: self.borrar(id)),
                        ]))
                ]))
        except Exception:
            pass
        self.page.update()

    def alta(self, e):
        nombre = self.txt_nombre.value.strip()
        cuit = self.txt_cuit.value.strip()
        telefono = self.txt_telefono.value.strip()
        direccion = self.txt_direccion.value.strip()
        if nombre and cuit and telefono and direccion:
            self.cursor.execute("SELECT nombre FROM proveedores WHERE nombre=%s", (nombre,))
            if not self.cursor.fetchone():
                self.cursor.execute("INSERT INTO proveedores (nombre, cuit, telefono, direccion) VALUES (%s, %s, %s, %s)", (nombre, cuit, telefono, direccion))
                self.conn.commit()
        self.limpiar()
        self.mostrar_proveedores()

    def baja(self, e):
        nombre = self.txt_nombre.value.strip()
        if nombre:
            self.cursor.execute("DELETE FROM proveedores WHERE nombre=%s", (nombre,))
            self.conn.commit()
        self.limpiar()
        self.mostrar_proveedores()

    def consulta(self, e):
        nombre = self.txt_nombre.value.strip()
        if nombre:
            self.cursor.execute("SELECT cuit, telefono, direccion FROM proveedores WHERE nombre=%s", (nombre,))
            data = self.cursor.fetchone()
            if data:
                self.txt_cuit.value = data[0]
                self.txt_telefono.value = data[1]
                self.txt_direccion.value = data[2]
        self.page.update()
        self.mostrar_proveedores()

    def limpiar(self, e=None):
        self.txt_nombre.value = ""
        self.txt_cuit.value = ""
        self.txt_telefono.value = ""
        self.txt_direccion.value = ""
        self.editando = None
        self.page.update()
        self.mostrar_proveedores()

    def cargar_editar(self, idp):
        self.cursor.execute("SELECT id, nombre, cuit, telefono, direccion FROM proveedores WHERE id=%s", (idp,))
        data = self.cursor.fetchone()
        if data:
            self.txt_nombre.value = data[1]
            self.txt_cuit.value = data[2]
            self.txt_telefono.value = data[3]
            self.txt_direccion.value = data[4]
            self.editando = data[0]
        self.page.update()

    def borrar(self, idp):
        self.cursor.execute("DELETE FROM proveedores WHERE id=%s", (idp,))
        self.conn.commit()
        self.mostrar_proveedores()

    def volver_menu(self, e):
        self.page.clean()
        self.volver(self.page)
        self.page.update()
