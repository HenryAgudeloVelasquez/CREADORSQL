import os
from datetime import datetime

import tkinter as tk
from tkinter import filedialog, messagebox, ttk

def crear_crud_sql():
    """
    Crea un formulario para que el usuario defina la estructura de la tabla
    y genera archivos SQL para el CRUD (Crear, Leer, Actualizar, Eliminar),
    cada uno en un archivo separado.
    El agregado de columnas es vertical, permite personalizar el nombre de
    cada procedimiento, incluyendo un alias, muestra la creación de la tabla
    en un campo de texto grande que se actualiza dinámicamente,
    y permite eliminar columnas.
    """

    def guardar_archivos():
        try:
            nombre_tabla = nombre_tabla_entry.get()
            ubicacion = ubicacion_entry.get()
            alias = alias_entry.get()
            nombre_add = nombre_add_entry.get()
            nombre_edit = nombre_edit_entry.get()
            nombre_delete = nombre_delete_entry.get()
            nombre_get = nombre_get_entry.get()
            nombre_getlist = nombre_getlist_entry.get()
            nombre_getlistall = nombre_getlistall_entry.get()

            if not nombre_tabla:
                messagebox.showerror("Error", "Por favor ingresa un nombre de tabla.")
                return
            if not ubicacion:
                messagebox.showerror("Error", "Por favor selecciona una ubicación.")
                return

            columnas = []
            for i in range(len(columnas_nombres)):
                nombre = columnas_nombres[i].get()
                tipo = columnas_tipos[i].get()
                if nombre and tipo:
                    columnas.append((nombre, tipo))

            if not columnas:
                messagebox.showerror("Error", "Por favor define al menos una columna.")
                return

            fecha_actual = datetime.now().strftime("%Y-%m-%d")
            crear_procedimientos_almacenados(ubicacion, nombre_tabla, columnas, fecha_actual, nombre_add,
                                            nombre_edit, nombre_delete, nombre_get, nombre_getlist,
                                            nombre_getlistall, alias)
            messagebox.showinfo("Éxito", "Archivos creados correctamente en " + ubicacion)
            ventana.destroy()

        except Exception as e:
            messagebox.showerror("Error", f"Error al crear los archivos: {e}")

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
        tipo_combo = ttk.Combobox(columnas_frame, textvariable=tipo_var, values=tipos_datos)
        tipo_combo.grid(row=fila, column=3, padx=5, pady=5)
        columnas_tipos.append(tipo_var)

        eliminar_button = tk.Button(columnas_frame, text="Eliminar", command=lambda fila=fila: eliminar_columna(fila))
        eliminar_button.grid(row=fila, column=4, padx=5, pady=5)

        actualizar_vista_tabla()

    def eliminar_columna(fila):
        for widget in columnas_frame.grid_slaves(row=fila):
            widget.grid_forget()
        columnas_nombres.pop(fila)
        columnas_tipos.pop(fila)
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
            if nombre and tipo:
                columnas.append(f"{nombre} {tipo}")

        contenido_tabla = f"""CREATE TABLE {nombre_tabla} (
    id INT PRIMARY KEY,
    {",\n    ".join(columnas)}
);
"""
        tabla_text.delete("1.0", tk.END)
        tabla_text.insert(tk.END, contenido_tabla)

    ventana = tk.Tk()
    ventana.title("Crear CRUD SQL")

    # --- Nombre de la tabla ---
    nombre_tabla_label = tk.Label(ventana, text="Nombre de la tabla:")
    nombre_tabla_label.grid(row=0, column=0, padx=5, pady=5)
    nombre_tabla_entry = tk.Entry(ventana)
    nombre_tabla_entry.grid(row=0, column=1, padx=5, pady=5)
    nombre_tabla_entry.bind("<KeyRelease>", lambda event: actualizar_vista_tabla())

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

    # --- Nombres de procedimientos ---
    nombre_add_label = tk.Label(ventana, text="Nombre ADD:")
    nombre_add_label.grid(row=3, column=0, padx=5, pady=5)
    nombre_add_entry = tk.Entry(ventana)
    nombre_add_entry.grid(row=3, column=1, padx=5, pady=5)

    nombre_edit_label = tk.Label(ventana, text="Nombre EDIT:")
    nombre_edit_label.grid(row=4, column=0, padx=5, pady=5)
    nombre_edit_entry = tk.Entry(ventana)
    nombre_edit_entry.grid(row=4, column=1, padx=5, pady=5)

    nombre_delete_label = tk.Label(ventana, text="Nombre DELETE:")
    nombre_delete_label.grid(row=5, column=0, padx=5, pady=5)
    nombre_delete_entry = tk.Entry(ventana)
    nombre_delete_entry.grid(row=5, column=1, padx=5, pady=5)

    nombre_get_label = tk.Label(ventana, text="Nombre GET:")
    nombre_get_label.grid(row=6, column=0, padx=5, pady=5)
    nombre_get_entry = tk.Entry(ventana)
    nombre_get_entry.grid(row=6, column=1, padx=5, pady=5)

    nombre_getlist_label = tk.Label(ventana, text="Nombre GETLIST:")
    nombre_getlist_label.grid(row=7, column=0, padx=5, pady=5)
    nombre_getlist_entry = tk.Entry(ventana)
    nombre_getlist_entry.grid(row=7, column=1, padx=5, pady=5)

    nombre_getlistall_label = tk.Label(ventana, text="Nombre GETLISTALL:")
    nombre_getlistall_label.grid(row=8, column=0, padx=5, pady=5)
    nombre_getlistall_entry = tk.Entry(ventana)
    nombre_getlistall_entry.grid(row=8, column=1, padx=5, pady=5)

    # --- Columnas ---
    columnas_frame = tk.Frame(ventana)
    columnas_frame.grid(row=9, column=0, columnspan=3, padx=5, pady=5)

    columnas_nombres = []
    columnas_tipos = []
    tipos_datos = ["INT", "VARCHAR(255)", "TEXT", "DATE", "FLOAT"]

    agregar_columna_button = tk.Button(ventana, text="Agregar columna", command=agregar_columna)
    agregar_columna_button.grid(row=10, column=1, padx=5, pady=5)

    # --- Vista de la tabla ---
    tabla_label = tk.Label(ventana, text="Vista previa de la tabla:")
    tabla_label.grid(row=11, column=0, padx=5, pady=5)
    tabla_text = tk.Text(ventana, height=10)
    tabla_text.grid(row=12, column=0, columnspan=3, padx=5, pady=5)

    # --- Guardar ---
    guardar_button = tk.Button(ventana, text="Guardar", command=guardar_archivos)
    guardar_button.grid(row=13, column=1, padx=5, pady=5)

    ventana.mainloop()


def crear_procedimientos_almacenados(ubicacion, nombre_tabla, columnas, fecha_actual,
                                    nombre_add, nombre_edit, nombre_delete, nombre_get, nombre_getlist,
                                    nombre_getlistall, alias=""):
    """Crea los archivos SQL para el CRUD con nombres personalizados."""
    # ... (El código para crear los archivos SQL permanece igual) ...


def guardar_archivo(ubicacion, nombre_archivo, contenido):
    """Guarda el contenido en un archivo."""
    ruta_completa = os.path.join(ubicacion, nombre_archivo)
    try:
        with open(ruta_completa, "w") as archivo:
            archivo.write(contenido)
    except Exception as e:
        messagebox.showerror("Error", f"Error al crear el archivo: {e}")

crear_crud_sql()