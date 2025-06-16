import tkinter as tk
from tkinter import filedialog, messagebox, ttk

import crud_generator  # Importa las funciones del otro archivo

def crear_crud_sql():
    """
    Crea un formulario interactivo para definir la estructura de una tabla SQL,
    generar procedimientos almacenados para operaciones CRUD y un archivo .cs
    con una clase DTO que representa la tabla.
    """

    def guardar_archivos():
        """Valida entradas y guarda los archivos generados en la ubicación seleccionada."""
        try:
            # Capturar datos ingresados
            conector = '_'
            nombre_tabla = nombre_tabla_entry.get().strip()
            ubicacion = ubicacion_entry.get().strip()
            alias = alias_entry.get().strip()
            nombre_general = nombre_general_entry.get().strip()
            nombre_ruta_DTO = nombre_ruta_DTO_entry.get().strip()  # Capturar el nombre de la ruta DTO
            api_texto = api_entry.get().strip()  # Capturar el texto del campo API
            procedimientos = {
                "ADD": nombre_add_entry.get().strip(),
                "EDIT": nombre_edit_entry.get().strip(),
                "DELETE": nombre_delete_entry.get().strip(),
                "GET": nombre_get_entry.get().strip(),
                "GETLIST": nombre_getlist_entry.get().strip(),
                "GETLISTALL": nombre_getlistall_entry.get().strip(),
            }

            if not nombre_tabla:
                raise ValueError("El nombre de la tabla no puede estar vacío.")
            if not ubicacion:
                raise ValueError("Selecciona una ubicación válida para guardar los archivos.")

            columnas = [(col.get(), tipo.get(), lon.get()) for col, tipo, lon in zip(columnas_nombres, columnas_tipos, columnas_longitudes) if col.get() and tipo.get()]
            if not columnas:
                raise ValueError("Debe haber al menos una columna definida.")

            # Validar nombres de columnas
            for nombre, _, _ in columnas:
                if not nombre.isalnum() or not nombre[0].isalpha():
                    raise ValueError(f"Nombre de columna inválido: {nombre}. Debe ser alfanumérico y comenzar con una letra.")

            crud_generator.crear_procedimientos_almacenados(ubicacion, nombre_tabla, columnas, alias=alias, nombre_general=nombre_general, **procedimientos)
            crud_generator.crear_archivo_dto(ubicacion, nombre_general, columnas, nombre_ruta_DTO)  # Pasar el nombre de la ruta DTO

            # Obtener los nombres de los procedimientos almacenados
            nombre_sp_add = f"{alias}{procedimientos.get('ADD') or 'Insertar'}{nombre_general}"
            nombre_sp_edit = f"{alias}{procedimientos.get('EDIT') or 'Actualizar'}{nombre_general}"
            nombre_sp_delete = f"{alias}{procedimientos.get('DELETE') or 'Eliminar'}{nombre_general}"
            nombre_sp_get = f"{alias}{procedimientos.get('GET') or 'ObtenerPorId'}{nombre_general}"
            nombre_sp_getlist = f"{alias}{procedimientos.get('GETLIST') or 'ObtenerLista'}{nombre_general}"
            nombre_sp_getlistall = f"{alias}{procedimientos.get('GETLISTALL') or 'ObtenerTodos'}{nombre_general}"

            # Llamar a la función crear_servicio_cs con los nombres de los procedimientos
            crud_generator.crear_servicio_cs(
                ubicacion, nombre_general, nombre_ruta_DTO, nombre_sp_get, nombre_sp_getlist, nombre_sp_getlistall,
                nombre_sp_add, nombre_sp_edit, nombre_sp_delete, nombre_general,alias
            )

            crud_generator.crear_servicio_Interfaces_cs(
                ubicacion, nombre_general, nombre_ruta_DTO, api_texto,alias
            )

            crud_generator.crear_servicio_Controller_cs(
                ubicacion, nombre_general, nombre_ruta_DTO, api_texto,alias
            )

            messagebox.showinfo("Éxito", f"Archivos creados correctamente en {ubicacion}.")

        except ValueError as ve:
            messagebox.showerror("Error de validación", str(ve))
        except Exception as e:
            messagebox.showerror("Error", f"Error al crear los archivos: {e}")

    def buscar_ubicacion():
        """Abre un diálogo para seleccionar una carpeta y actualiza el campo de ubicación."""
        ubicacion = filedialog.askdirectory()
        if ubicacion:
            ubicacion_entry.delete(0, tk.END)
            ubicacion_entry.insert(0, ubicacion)

    def agregar_columna():
        """Agrega una nueva fila para definir una columna."""
        fila = len(columnas_nombres)

        nombre_entry = tk.Entry(columnas_frame)
        nombre_entry.grid(row=fila, column=0, padx=5, pady=5)
        columnas_nombres.append(nombre_entry)

        tipo_var = tk.StringVar(value="INT")
        tipo_combo = ttk.Combobox(columnas_frame, textvariable=tipo_var, values=tipos_datos)
        tipo_combo.grid(row=fila, column=1, padx=5, pady=5)
        columnas_tipos.append(tipo_var)

        longitud_entry = tk.Entry(columnas_frame, width=5)  # Campo para la longitud
        longitud_entry.grid(row=fila, column=2, padx=5, pady=5)
        columnas_longitudes.append(longitud_entry)  # Almacenar la longitud

        eliminar_button = tk.Button(columnas_frame, text="Eliminar", command=lambda fila=fila: eliminar_columna(fila))
        eliminar_button.grid(row=fila, column=3, padx=5, pady=5)  # Mover el botón Eliminar
        botones_eliminar.append(eliminar_button)

        actualizar_vista_tabla()

    def eliminar_columna(fila):
        """Elimina una fila de columna especificada."""
        columnas_nombres[fila].destroy()
        columnas_tipos[fila].set("")
        columnas_longitudes[fila].destroy()  # Eliminar la longitud
        botones_eliminar[fila].destroy()

        columnas_nombres.pop(fila)
        columnas_tipos.pop(fila)
        columnas_longitudes.pop(fila)  # Eliminar la longitud
        botones_eliminar.pop(fila)
        actualizar_vista_tabla()

    def actualizar_vista_tabla():
        """Actualiza dinámicamente la vista previa de la tabla."""
        nombre_tabla = nombre_tabla_entry.get().strip()
        columnas = []
        for col, tipo, long in zip(columnas_nombres, columnas_tipos, columnas_longitudes):
            col_name = col.get().strip()
            col_type = tipo.get().strip()
            col_len = long.get().strip()
            if col_name and col_type:
                if col_type == "VARCHAR" and col_len:
                    columnas.append(f"{col_name} {col_type}({col_len})")
                else:
                    columnas.append(f"{col_name} {col_type}")

        contenido_tabla = f"CREATE TABLE {nombre_tabla} (\n    Id BIGINT PRIMARY KEY,\n  IdUsuario BIGINT,\n  IdUsuarioModifica BIGINT,\n  FechaModifica datetime,\n  FechaRegistro datetime,\n  Estado bit,\n  IdActividad BIGINT,\n  IdProyecto BIGINT,\n    {',\n    '.join(columnas)}\n);"
        tabla_text.delete("1.0", tk.END)
        tabla_text.insert(tk.END, contenido_tabla)

    # Configuración principal de la ventana
    ventana = tk.Tk()
    ventana.title("Generador de CRUD SQL")

    # --- Widgets principales ---
    tk.Label(ventana, text="Nombre de la tabla:").grid(row=0, column=0, padx=5, pady=5)
    nombre_tabla_entry = tk.Entry(ventana)
    nombre_tabla_entry.grid(row=0, column=1, padx=5, pady=5)
    nombre_tabla_entry.bind("<KeyRelease>", lambda _: actualizar_vista_tabla())

    tk.Label(ventana, text="Ubicación:").grid(row=1, column=0, padx=5, pady=5)
    ubicacion_entry = tk.Entry(ventana)
    ubicacion_entry.grid(row=1, column=1, padx=5, pady=5)
    tk.Button(ventana, text="Buscar", command=buscar_ubicacion).grid(row=1, column=2, padx=5, pady=5)

    tk.Label(ventana, text="Alias:").grid(row=2, column=0, padx=5, pady=5)
    alias_entry = tk.Entry(ventana)
    alias_entry.grid(row=2, column=1, padx=5, pady=5)

    # --- Nombre general de procedimientos ---
    tk.Label(ventana, text="Nombre general de procedimientos:").grid(row=3, column=0, padx=5, pady=5)
    nombre_general_entry = tk.Entry(ventana)
    nombre_general_entry.grid(row=3, column=1, padx=5, pady=5)

    # --- Nombre ruta DTO ---
    tk.Label(ventana, text="Nombre ruta DTO:").grid(row=4, column=0, padx=5, pady=5)
    nombre_ruta_DTO_entry = tk.Entry(ventana)
    nombre_ruta_DTO_entry.grid(row=4, column=1, padx=5, pady=5)

    # --- API ---
    tk.Label(ventana, text="API:").grid(row=5, column=0, padx=5, pady=5)  # Nueva fila para el campo API
    api_entry = tk.Entry(ventana)
    api_entry.grid(row=5, column=1, padx=5, pady=5)  # Nueva fila para el campo API

    # --- Procedimientos almacenados ---
    procedimientos_labels = ["_SpAdd", "_SpEdit", "_SpDelete", "_SpGet", "_SpGetList", "_SpGetListAll"]
    procedimientos_entries = {}

    for i, proc in enumerate(procedimientos_labels, start=6):  # Empezar en la fila 6
        tk.Label(ventana, text=f"Nombre {proc}:").grid(row=i, column=0, padx=5, pady=5)

        # Crear Entry con el valor por defecto
        entry = tk.Entry(ventana)
        entry.insert(0, proc)  # Insertar el valor por defecto
        entry.grid(row=i, column=1, padx=5, pady=5)
        procedimientos_entries[proc] = entry

    nombre_add_entry = procedimientos_entries["_SpAdd"]
    nombre_edit_entry = procedimientos_entries["_SpEdit"]
    nombre_delete_entry = procedimientos_entries["_SpDelete"]
    nombre_get_entry = procedimientos_entries["_SpGet"]
    nombre_getlist_entry = procedimientos_entries["_SpGetList"]
    nombre_getlistall_entry = procedimientos_entries["_SpGetListAll"]

    # --- Configuración de columnas ---
    tk.Label(ventana, text="Columnas:").grid(row=12, column=0, padx=5, pady=5)  # Cambiar la fila a 12
    columnas_frame = tk.Frame(ventana)
    columnas_frame.grid(row=13, column=0, columnspan=3, padx=5, pady=5)  # Cambiar la fila a 13

    columnas_nombres = []
    columnas_tipos = []
    columnas_longitudes = []  # Lista para almacenar las longitudes de las columnas
    botones_eliminar = []
    tipos_datos = [
        "INT",  # Números enteros
        "VARCHAR",  # Cadenas de caracteres de longitud variable
        "TEXT",  # Texto de longitud variable, más grande que VARCHAR
        "DATE",  # Fecha (año, mes, día)
        "FLOAT",  # Números de punto flotante con precisión simple
        "DECIMAL",  # Números decimales con precisión definida por el usuario
        "BOOL",  # Booleano (verdadero o falso)
        "DATETIME",  # Fecha y hora
        "TINYINT",  # Enteros pequeños (0 a 255)
        "SMALLINT",  # Enteros de tamaño mediano
        "BIGINT",  # Enteros grandes
        "NUMERIC",  # Similar a DECIMAL, pero con mayor precisión
        "MONEY",  # Valores monetarios
        "SMALLMONEY",  # Valores monetarios más pequeños
        "BIT",  # Un solo bit (0 o 1)
        "NVARCHAR",  # Cadenas de caracteres Unicode de longitud variable
        "NTEXT",  # Texto Unicode de longitud variable
        "BINARY",  # Datos binarios de longitud fija
        "VARBINARY",  # Datos binarios de longitud variable
        "IMAGE",  # Datos binarios grandes (imágenes, documentos, etc.)
        "TIMESTAMP",  # Marca de tiempo que se actualiza automáticamente
        "UNIQUEIDENTIFIER",  # Identificador único global (GUID)
        "XML",  # Datos XML
        "CURSOR",  # Referencia a un cursor
        "SQL_VARIANT",  # Puede almacenar diferentes tipos de datos
        "TABLE",  # Tipo especial para almacenar conjuntos de resultados
    ]  # Actualizar tipos de datos

    tk.Button(ventana, text="Agregar columna", command=agregar_columna).grid(row=14, column=1, padx=5, pady=5)  # Cambiar la fila a 14

    # --- Vista previa de la tabla ---
    tk.Label(ventana, text="Vista previa de la tabla:").grid(row=15, column=0, padx=5, pady=5)  # Cambiar la fila a 15
    tabla_text = tk.Text(ventana, height=10)
    tabla_text.grid(row=16, column=0, columnspan=3, padx=5, pady=5)  # Cambiar la fila a 16

    # --- Botón guardar ---
    tk.Button(ventana, text="Guardar", command=guardar_archivos).grid(row=17, column=1, padx=5, pady=5)  # Cambiar la fila a 17

    ventana.mainloop()

if __name__ == "__main__":
    crear_crud_sql()