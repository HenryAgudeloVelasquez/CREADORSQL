import os
from datetime import datetime

import tkinter as tk
from tkinter import filedialog, messagebox, ttk

from funciones_sql import crear_procedimientos_almacenados, guardar_archivo

# ¡Lista épica de tipos de datos de SQL Server!
TIPOS_DATOS_SQL_SERVER = [
    "BIGINT", "BINARY", "BIT", "CHAR", "DATE", "DATETIME", "DATETIME2",
    "DATETIMEOFFSET", "DECIMAL", "FLOAT", "GEOGRAPHY", "GEOMETRY",
    "HIERARCHYID", "IMAGE", "INT", "MONEY", "NCHAR", "NTEXT", "NUMERIC",
    "NVARCHAR", "REAL", "SMALLDATETIME", "SMALLINT", "SMALLMONEY",
    "SQL_VARIANT", "TEXT", "TIME", "TIMESTAMP", "TINYINT",
    "UNIQUEIDENTIFIER", "VARBINARY", "VARCHAR", "XML"
]

# ¡Diccionario mágico para mapear tipos de datos a dialectos SQL!
DIALECTOS_SQL = {
    "SQL Server": {
        "INT": "INT",
        "VARCHAR(255)": "VARCHAR(255)",
        "TEXT": "TEXT",
        "DATE": "DATE",
        "FLOAT": "FLOAT"
        # ... (¡Aventúrate a añadir más mapeos para SQL Server aquí!) ...
    },
    "MySQL": {
        "INT": "INT",
        "VARCHAR(255)": "VARCHAR(255)",
        "TEXT": "TEXT",
        "DATE": "DATE",
        "FLOAT": "FLOAT"
        # ... (¡Desafíate a ti mismo añadiendo más mapeos para MySQL!) ...
    },
    "PostgreSQL": {
        "INT": "INTEGER",
        "VARCHAR(255)": "VARCHAR(255)",
        "TEXT": "TEXT",
        "DATE": "DATE",
        "FLOAT": "REAL"
        # ... (¡Explora nuevos horizontes con PostgreSQL y sus mapeos!) ...
    }
    # ... (¡El universo de los dialectos SQL te espera!) ...
}


def crear_crud_sql():
    """
    ¡Crea un formulario supervitaminado para definir la estructura de la tabla 
    y generar archivos SQL para el CRUD!
    Permite agregar y eliminar columnas con estilo, personalizar los nombres 
    de los procedimientos, ¡y mucho más!
    """

    def guardar_archivos():
        try:
            nombre_tabla = nombre_tabla_entry.get()
            ubicacion = ubicacion_entry.get()
            alias = alias_entry.get()
            nombre_general = nombre_general_entry.get()
            nombre_add = nombre_add_entry.get()
            nombre_edit = nombre_edit_entry.get()
            nombre_delete = nombre_delete_entry.get()
            nombre_get = nombre_get_entry.get()
            nombre_getlist = nombre_getlist_entry.get()
            nombre_getlistall = nombre_getlistall_entry.get()
            dialecto = dialecto_var.get()

            # ¡Validaciones heroicas para salvar al usuario de errores!
            if not nombre_tabla:
                messagebox.showerror(
                    "Error", "¡Alto ahí! Debes ingresar un nombre de tabla.")
                return
            if not ubicacion:
                messagebox.showerror(
                    "Error", "¡No te escapes! Debes seleccionar una ubicación.")
                return
            if not nombre_tabla.isalnum():
                messagebox.showerror(
                    "Error",
                    "¡Nombre de tabla inválido! Solo se permiten caracteres alfanuméricos."
                )
                return

            columnas = []
            for i in range(len(columnas_nombres)):
                nombre = columnas_nombres[i].get()
                tipo = columnas_tipos[i].get()
                longitud = columnas_longitudes[i].get()
                if nombre and tipo:
                    if longitud:
                        tipo += f"({longitud})"
                    columnas.append((nombre, tipo))

            if not columnas:
                messagebox.showerror(
                    "Error",
                    "¡Sin columnas no hay paraíso! Define al menos una.")
                return

            fecha_actual = datetime.now().strftime("%Y-%m-%d")

            # ¡Se usa el nombre general si está presente!
            nombre_add = nombre_add if nombre_add else nombre_general
            nombre_edit = nombre_edit if nombre_edit else nombre_general
            nombre_delete = nombre_delete if nombre_delete else nombre_general
            nombre_get = nombre_get if nombre_get else nombre_general
            nombre_getlist = nombre_getlist if nombre_getlist else nombre_general
            nombre_getlistall = nombre_getlistall if nombre_getlistall else nombre_general

            crear_procedimientos_almacenados(ubicacion, nombre_tabla,
                                            columnas, fecha_actual,
                                            nombre_add, nombre_edit,
                                            nombre_delete, nombre_get,
                                            nombre_getlist,
                                            nombre_getlistall, alias, dialecto)
            messagebox.showinfo(
                "¡Victoria!",
                f"¡Los archivos se crearon con éxito en {ubicacion}!")
            ventana.destroy()

        except Exception as e:
            messagebox.showerror(
                "¡Oh no!",
                f"Algo salió mal al crear los archivos: {e}")

    def buscar_ubicacion():
        ubicacion = filedialog.askdirectory()
        if ubicacion:
            ubicacion_entry.delete(0, tk.END)
            ubicacion_entry.insert(0, ubicacion)

    def agregar_columna():
        fila = len(columnas_nombres)

        nombre_label = tk.Label(columnas_frame, text="Nombre:")
        nombre_label.grid(row=fila, column=0, padx=5, pady=5)
        nombre_entry = tk.Entry(columnas_frame)
        nombre_entry.grid(row=fila, column=1, padx=5, pady=5)
        columnas_nombres.append(nombre_entry)

        tipo_var = tk.StringVar(value="INT")
        tipo_label = tk.Label(columnas_frame, text="Tipo:")
        tipo_label.grid(row=fila, column=2, padx=5, pady=5)
        tipo_combo = ttk.Combobox(columnas_frame,
                                  textvariable=tipo_var,
                                  values=TIPOS_DATOS_SQL_SERVER)
        tipo_combo.grid(row=fila, column=3, padx=5, pady=5)
        columnas_tipos.append(tipo_var)

        longitud_label = tk.Label(columnas_frame, text="Longitud:")
        longitud_label.grid(row=fila, column=4, padx=5, pady=5)
        longitud_entry = tk.Entry(columnas_frame)
        longitud_entry.grid(row=fila, column=5, padx=5, pady=5)
        columnas_longitudes.append(longitud_entry)

        eliminar_button = tk.Button(
            columnas_frame,
            text="Eliminar",
            command=lambda fila=fila: eliminar_columna(fila))
        eliminar_button.grid(row=fila, column=6, padx=5, pady=5)

        actualizar_vista_tabla()

    def eliminar_columna(fila):
        for widget in columnas_frame.grid_slaves(row=fila):
            widget.grid_forget()
        columnas_nombres.pop(fila)
        columnas_tipos.pop(fila)
        columnas_longitudes.pop(fila)
        actualizar_vista_tabla()

        # Reorganizar las filas después de eliminar una columna
        for i in range(fila, len(columnas_nombres)):
            for widget in columnas_frame.grid_slaves(row=i + 1):
                widget.grid(row=i, column=widget.grid_info()["column"])

    def actualizar_vista_tabla():
        nombre_tabla = nombre_tabla_entry.get()
        columnas = []
        for i in range(len(columnas_nombres)):
            nombre = columnas_nombres[i].get()
            tipo = columnas_tipos[i].get()
            longitud = columnas_longitudes[i].get()
            if nombre and tipo:
                if longitud:
                    tipo += f"({longitud})"
                columnas.append(f"{nombre} {tipo}")

        contenido_tabla = f"""CREATE TABLE {nombre_tabla} (
    id INT PRIMARY KEY,
    {",\n    ".join(columnas)}
);
"""
        tabla_text.delete("1.0", tk.END)
        tabla_text.insert(tk.END, contenido_tabla)

    ventana = tk.Tk()
    ventana.title("¡Crea tu CRUD SQL como un campeón!")

    # --- Nombre de la tabla ---
    nombre_tabla_label = tk.Label(ventana, text="Nombre de la tabla:")
    nombre_tabla_label.grid(row=0, column=0, padx=5, pady=5)
    nombre_tabla_entry = tk.Entry(ventana)
    nombre_tabla_entry.grid(row=0, column=1, padx=5, pady=5)
    nombre_tabla_entry.bind("<KeyRelease>",
                            lambda event: actualizar_vista_tabla())

    # --- Ubicación ---
    ubicacion_label = tk.Label(ventana, text="Ubicación:")
    ubicacion_label.grid(row=1, column=0, padx=5, pady=5)
    ubicacion_entry = tk.Entry(ventana)
    ubicacion_entry.grid(row=1, column=1, padx=5, pady=5)
    buscar_button = tk.Button(ventana, text="Buscar", command=buscar_ubicacion)
    buscar_button.grid(row=1, column=2, padx=5, pady=5)

    # --- Alias ---
    alias_label = tk.Label(ventana, text="Alias:")
    alias_label.grid(row=2, column=0, padx=5, pady=5)
    alias_entry = tk.Entry(ventana)
    alias_entry.grid(row=2, column=1, padx=5, pady=5)

    # --- Dialecto SQL ---
    dialecto_label = tk.Label(ventana, text="Dialecto SQL:")
    dialecto_label.grid(row=3, column=0, padx=5, pady=5)
    dialecto_var = tk.StringVar(value="SQL Server")
    dialecto_combo = ttk.Combobox(ventana,
                                  textvariable=dialecto_var,
                                  values=list(DIALECTOS_SQL.keys()))
    dialecto_combo.grid(row=3, column=1, padx=5, pady=5)

    # --- Nombre general de procedimiento ---
    nombre_general_label = tk.Label(ventana, text="Nombre general:")
    nombre_general_label.grid(row=4, column=0, padx=5, pady=5)
    nombre_general_entry = tk.Entry(ventana)
    nombre_general_entry.grid(row=4, column=1, padx=5, pady=5)

    # --- Nombres de procedimientos ---
    nombre_add_label = tk.Label(ventana, text="Nombre ADD:")
    nombre_add_label.grid(row=5, column=0, padx=5, pady=5)
    nombre_add_entry = tk.Entry(ventana)
    nombre_add_entry.grid(row=5, column=1, padx=5, pady=5)

    nombre_edit_label = tk.Label(ventana, text="Nombre EDIT:")
    nombre_edit_label.grid(row=6, column=0, padx=5, pady=5)
    nombre_edit_entry = tk.Entry(ventana)
    nombre_edit_entry.grid(row=6, column=1, padx=5, pady=5)

    nombre_delete_label = tk.Label(ventana, text="Nombre DELETE:")
    nombre_delete_label.grid(row=7, column=0, padx=5, pady=5)
    nombre_delete_entry = tk.Entry(ventana)
    nombre_delete_entry.grid(row=7, column=1, padx=5, pady=5)

    nombre_get_label = tk.Label(ventana, text="Nombre GET:")
    nombre_get_label.grid(row=8, column=0, padx=5, pady=5)
    nombre_get_entry = tk.Entry(ventana)
    nombre_get_entry.grid(row=8, column=1, padx=5, pady=5)

    nombre_getlist_label = tk.Label(ventana, text="Nombre GETLIST:")
    nombre_getlist_label.grid(row=9, column=0, padx=5, pady=5)
    nombre_getlist_entry = tk.Entry(ventana)
    nombre_getlist_entry.grid(row=9, column=1, padx=5, pady=5)

    nombre_getlistall_label = tk.Label(ventana, text="Nombre GETLISTALL:")
    nombre_getlistall_label.grid(row=10, column=0, padx=5, pady=5)
    nombre_getlistall_entry = tk.Entry(ventana)
    nombre_getlistall_entry.grid(row=10, column=1, padx=5, pady=5)

    # --- Columnas ---
    columnas_frame = tk.Frame(ventana)
    columnas_frame.grid(row=11, column=0, columnspan=3, padx=5, pady=5)

    columnas_nombres = []
    columnas_tipos = []
    columnas_longitudes = []  # ¡Para almacenar las longitudes de las columnas!

    agregar_columna_button = tk.Button(ventana,
                                       text="Agregar columna",
                                       command=agregar_columna)
    agregar_columna_button.grid(row=12, column=1, padx=5, pady=5)

    # --- Vista de la tabla ---
    tabla_label = tk.Label(ventana, text="Vista previa de la tabla:")
    tabla_label.grid(row=13, column=0, padx=5, pady=5)
    tabla_text = tk.Text(ventana, height=10)
    tabla_text.grid(row=14, column=0, columnspan=3, padx=5, pady=5)

    # --- Guardar ---
    guardar_button = tk.Button(ventana, text="Guardar", command=guardar_archivos)
    guardar_button.grid(row=15, column=1, padx=5, pady=5)

    # --- Funcionalidad para el nombre general ---
    def actualizar_nombres_procedimientos(event=None):
        nombre = nombre_general_entry.get()
        nombre_add_entry.delete(0, tk.END)
        nombre_add_entry.insert(0, nombre)
        nombre_edit_entry.delete(0, tk.END)
        nombre_edit_entry.insert(0, nombre)
        nombre_delete_entry.delete(0, tk.END)
        nombre_delete_entry.insert(0, nombre)
        nombre_get_entry.delete(0, tk.END)
        nombre_get_entry.insert(0, nombre)
        nombre_getlist_entry.delete(0, tk.END)
        nombre_getlist_entry.insert(0, nombre)
        nombre_getlistall_entry.delete(0, tk.END)
        nombre_getlistall_entry.insert(0, nombre)

    nombre_general_entry.bind("<KeyRelease>", actualizar_nombres_procedimientos)

    ventana.mainloop()

