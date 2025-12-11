# Taller Mecánico - Sistema de Gestión

Este proyecto es una aplicación de escritorio desarrollada con Flet y Python para la administración integral de un taller mecánico. Permite gestionar clientes, proveedores, repuestos, empleados y usuarios, todo con una interfaz moderna y personalizada.

## Características

- **Menú principal** con iconos personalizados y tooltips.
- **Gestión de Clientes:** Alta, edición, consulta y eliminación de clientes.
- **Gestión de Proveedores:** Registro y administración de proveedores.
- **Gestión de Repuestos:** Control de inventario de repuestos.
- **Gestión de Empleados:** Administración de personal del taller.
- **Gestión de Usuarios:** Control de acceso y roles.
- **Menú de administración:** Ficha técnica de vehículos y presupuestos.
- **Conexión a base de datos MySQL** para persistencia de datos.

## Requisitos

- Python 3.10+
- Flet
- mysql-connector-python
- MySQL Server con la base de datos `taller_mecanico` creada (ver archivo `taller_mecanico.sql`)

## Instalación

1. Clona el repositorio o descarga los archivos.
2. Crea y activa el entorno virtual (solo la primera vez):
   ```powershell
   python -m venv .venv
   .venv\Scripts\Activate
   ```
3. Instala las dependencias:
   ```powershell
   pip install -r requirements.txt
   ```
4. Configura la base de datos MySQL usando el script `taller_mecanico.sql`.
5. Ejecuta la aplicación principal:
   ```powershell
   python taller.py
   ```

## Estructura del Proyecto

- `FLET Visual/`
  - `taller.py` (main)
  - `cliente.py`, `proveedor.py`, `repuesto.py`, `empleado.py`, `usuario.py` (módulos)
  - `iconos/` (carpeta de imágenes)
  - `taller_mecanico.sql` (script de base de datos)

## Personalización

Todos los iconos utilizados en la interfaz están en la carpeta `iconos` y son exclusivos para este proyecto.
