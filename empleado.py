     
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

class Herramienta_Empleado:
    def __init__(self, page, volver):
        self.page = page
        self.volver = volver
        self.conn = conectar()
        self.cursor = self.conn.cursor() if self.conn else None
        self.armar_ui()
        self.mostrar_empleados()

    def armar_ui(self):
        self.page.clean()
        self.txt_nombre = ft.TextField(label="Nombre", width=260)
        self.txt_apellido = ft.TextField(label="Apellido", width=260)
        self.txt_legajo = ft.TextField(label="Legajo", width=260)
        self.txt_rol = ft.TextField(label="Rol", width=260)
        self.txt_estado = ft.TextField(label="Estado", width=260)
        btn_alta = ft.ElevatedButton("Alta", on_click=self.alta)
        btn_baja = ft.ElevatedButton("Baja", on_click=self.baja)
        btn_consulta = ft.ElevatedButton("Consulta", on_click=self.consulta)
        btn_guardar = ft.ElevatedButton("Guardar", on_click=self.guardar)
        btn_volver = ft.ElevatedButton("Volver", on_click=self.volver_menu)
        self.tabla = ft.DataTable(
            columns=[
                ft.DataColumn(label=ft.Text("Legajo")),
                ft.DataColumn(label=ft.Text("Nombre")),
                ft.DataColumn(label=ft.Text("Apellido")),
                ft.DataColumn(label=ft.Text("Rol")),
                ft.DataColumn(label=ft.Text("Estado")),
                ft.DataColumn(label=ft.Text("Acciones")),
            ],
            rows=[]
        )
        self.formulario = ft.Column([
            ft.Text("Empleados", size=22, weight="bold"),
            self.txt_legajo,
            self.txt_nombre,
            self.txt_apellido,
            self.txt_rol,
            self.txt_estado,
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
        legajo = self.txt_legajo.value.strip()
        nombre = self.txt_nombre.value.strip()
        apellido = self.txt_apellido.value.strip()
        rol = self.txt_rol.value.strip()
        estado = self.txt_estado.value.strip()
        if legajo and nombre and apellido and rol and estado:
            if hasattr(self, 'editando') and self.editando:
                self.cursor.execute("UPDATE mecanicos SET legajo=%s, nombre=%s, apellido=%s, rol=%s, estado=%s WHERE legajo=%s", (legajo, nombre, apellido, rol, estado, self.editando))
                self.conn.commit()
                self.editando = None
        self.limpiar()
        self.mostrar_empleados()

    def mostrar_empleados(self):
        self.tabla.rows.clear()
        if not self.cursor:
            self.page.update()
            return
        try:
            self.cursor.execute("SELECT legajo, nombre, apellido, rol, estado FROM mecanicos")
            for fila in self.cursor.fetchall():
                legajo = fila[0]
                self.tabla.rows.append(ft.DataRow(cells=[
                    ft.DataCell(ft.Text(str(legajo))),
                    ft.DataCell(ft.Text(fila[1])),
                    ft.DataCell(ft.Text(fila[2])),
                    ft.DataCell(ft.Text(fila[3])),
                    ft.DataCell(ft.Text(fila[4])),
                        ft.DataCell(ft.Row([
                            ft.IconButton(content=ft.Image(src="iconos/modificar.png", width=24, height=24), tooltip="Editar", on_click=lambda e, id=legajo: self.cargar_editar(id)),
                            ft.IconButton(content=ft.Image(src="iconos/borrar.png", width=24, height=24), tooltip="Borrar", on_click=lambda e, id=legajo: self.borrar(id)),
                        ]))
                ]))
        except Exception:
            pass
        self.page.update()

    def alta(self, e):
        legajo = self.txt_legajo.value.strip()
        nombre = self.txt_nombre.value.strip()
        apellido = self.txt_apellido.value.strip()
        rol = self.txt_rol.value.strip()
        estado = self.txt_estado.value.strip()
        if legajo and nombre and apellido and rol and estado:
            self.cursor.execute("SELECT legajo FROM mecanicos WHERE legajo=%s", (legajo,))
            if not self.cursor.fetchone():
                self.cursor.execute("INSERT INTO mecanicos (legajo, nombre, apellido, rol, estado) VALUES (%s, %s, %s, %s, %s)", (legajo, nombre, apellido, rol, estado))
                self.conn.commit()
        self.limpiar()
        self.mostrar_empleados()

    def baja(self, e):
        legajo = self.txt_legajo.value.strip()
        if legajo:
            self.cursor.execute("DELETE FROM mecanicos WHERE legajo=%s", (legajo,))
            self.conn.commit()
        self.limpiar()
        self.mostrar_empleados()

    def consulta(self, e):
        legajo = self.txt_legajo.value.strip()
        if legajo:
            self.cursor.execute("SELECT nombre, apellido, rol, estado FROM mecanicos WHERE legajo=%s", (legajo,))
            data = self.cursor.fetchone()
            if data:
                self.txt_nombre.value = data[0]
                self.txt_apellido.value = data[1]
                self.txt_rol.value = data[2]
                self.txt_estado.value = data[3]
        self.page.update()
        self.mostrar_empleados()

    def limpiar(self, e=None):
        self.txt_legajo.value = ""
        self.txt_nombre.value = ""
        self.txt_apellido.value = ""
        self.txt_rol.value = ""
        self.txt_estado.value = ""
        self.editando = None
        self.page.update()
        self.mostrar_empleados()

    def cargar_editar(self, legajo):
        self.cursor.execute("SELECT legajo, nombre, apellido, rol, estado FROM mecanicos WHERE legajo=%s", (legajo,))
        data = self.cursor.fetchone()
        if data:
            self.txt_legajo.value = data[0]
            self.txt_nombre.value = data[1]
            self.txt_apellido.value = data[2]
            self.txt_rol.value = data[3]
            self.txt_estado.value = data[4]
            self.editando = data[0]
        self.page.update()

    def borrar(self, legajo):
        self.cursor.execute("DELETE FROM mecanicos WHERE legajo=%s", (legajo,))
        self.conn.commit()
        self.mostrar_empleados()

    def volver_menu(self, e):
        self.page.clean()
        self.volver(self.page)
