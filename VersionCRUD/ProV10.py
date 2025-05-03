import os
from datetime import datetime

import tkinter as tk
from tkinter import filedialog, messagebox, ttk


def crear_crud_sql():
    """
    Crea un formulario interactivo para definir la estructura de una tabla SQL
    y generar procedimientos almacenados para operaciones CRUD.
    """

    def guardar_archivos():
        """Valida entradas y guarda los archivos generados en la ubicación seleccionada."""
        try:
            # Capturar datos ingresados
            nombre_tabla = nombre_tabla_entry.get().strip()
            ubicacion = ubicacion_entry.get().strip()
            alias = alias_entry.get().strip()
            nombre_general = nombre_general_entry.get().strip()
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

            columnas = [(col.get(), tipo.get()) for col, tipo in zip(columnas_nombres, columnas_tipos) if col.get() and tipo.get()]
            if not columnas:
                raise ValueError("Debe haber al menos una columna definida.")

            fecha_actual = datetime.now().strftime("%Y-%m-%d")
            crear_procedimientos_almacenados(ubicacion, nombre_tabla, columnas, fecha_actual, alias=alias, nombre_general=nombre_general, **procedimientos)

            messagebox.showinfo("Éxito", f"Archivos creados correctamente en {ubicacion}.")
            ventana.destroy()

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

        eliminar_button = tk.Button(columnas_frame, text="Eliminar", command=lambda fila=fila: eliminar_columna(fila))
        eliminar_button.grid(row=fila, column=2, padx=5, pady=5)
        botones_eliminar.append(eliminar_button)

        actualizar_vista_tabla()

    def eliminar_columna(fila):
        """Elimina una fila de columna especificada."""
        columnas_nombres[fila].destroy()
        columnas_tipos[fila].set("")
        botones_eliminar[fila].destroy()

        columnas_nombres.pop(fila)
        columnas_tipos.pop(fila)
        botones_eliminar.pop(fila)
        actualizar_vista_tabla()

    def actualizar_vista_tabla():
        """Actualiza dinámicamente la vista previa de la tabla."""
        nombre_tabla = nombre_tabla_entry.get().strip()
        columnas = [f"{col.get()} {tipo.get()}" for col, tipo in zip(columnas_nombres, columnas_tipos) if col.get() and tipo.get()]
        contenido_tabla = f"CREATE TABLE {nombre_tabla} (\n    id INT PRIMARY KEY,\n    {',\n    '.join(columnas)}\n);"

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

    # --- Procedimientos almacenados ---
    procedimientos_labels = ["Add", "Edit", "Delete", "Get", "GetList", "GetListAll"]
    procedimientos_entries = {}
    for i, proc in enumerate(procedimientos_labels, start=4):
        tk.Label(ventana, text=f"Nombre {proc}:").grid(row=i, column=0, padx=5, pady=5)
        entry = tk.Entry(ventana)
        entry.grid(row=i, column=1, padx=5, pady=5)
        procedimientos_entries[proc] = entry

    nombre_add_entry = procedimientos_entries["Add"]
    nombre_edit_entry = procedimientos_entries["Edit"]
    nombre_delete_entry = procedimientos_entries["Delete"]
    nombre_get_entry = procedimientos_entries["Get"]
    nombre_getlist_entry = procedimientos_entries["GetList"]
    nombre_getlistall_entry = procedimientos_entries["GetListAll"]

    # --- Configuración de columnas ---
    tk.Label(ventana, text="Columnas:").grid(row=10, column=0, padx=5, pady=5)
    columnas_frame = tk.Frame(ventana)
    columnas_frame.grid(row=11, column=0, columnspan=3, padx=5, pady=5)

    columnas_nombres = []
    columnas_tipos = []
    botones_eliminar = []
    tipos_datos = ["INT", "VARCHAR(255)", "TEXT", "DATE", "FLOAT"]

    tk.Button(ventana, text="Agregar columna", command=agregar_columna).grid(row=12, column=1, padx=5, pady=5)

    # --- Vista previa de la tabla ---
    tk.Label(ventana, text="Vista previa de la tabla:").grid(row=13, column=0, padx=5, pady=5)
    tabla_text = tk.Text(ventana, height=10)
    tabla_text.grid(row=14, column=0, columnspan=3, padx=5, pady=5)

    # --- Botón guardar ---
    tk.Button(ventana, text="Guardar", command=guardar_archivos).grid(row=15, column=1, padx=5, pady=5)

    ventana.mainloop()


def crear_procedimientos_almacenados(ubicacion,
                                    nombre_tabla,
                                    columnas,
                                    fecha_actual,
                                    alias="",
                                    nombre_general="",
                                    **procedimientos):
    """Crea los archivos SQL para el CRUD con nombres personalizados."""

    # --- ADD ---
    nombre_proc_add = f"{nombre_general}{alias}{procedimientos.get('ADD') or 'Insertar'}"
    contenido_add = f"""
-- =============================================
-- Author:        Henry Agudelo
-- Create date: {fecha_actual}
-- Description: Inserta un nuevo registro en la tabla '{nombre_tabla}'
-- =============================================

CREATE PROCEDURE {nombre_proc_add} 
    {", ".join([f"@{col[0]} {col[1]}" for col in columnas])}
AS
BEGIN
    INSERT INTO {nombre_tabla} ({", ".join([col[0] for col in columnas])}) 
    VALUES ({", ".join([f"@{col[0]}" for col in columnas])})
END
    """
    guardar_archivo(ubicacion, f"{nombre_proc_add}.sql", contenido_add)

    # --- EDIT ---
    nombre_proc_edit = f"{nombre_general}{alias}{procedimientos.get('EDIT') or 'Actualizar'}"
    contenido_edit = f"""
-- =============================================
-- Author:        Henry Agudelo
-- Create date: {fecha_actual}
-- Description: Actualiza un registro de la tabla '{nombre_tabla}'
-- =============================================

CREATE PROCEDURE {nombre_proc_edit} 
    @id INT,
    {", ".join([f"@{col[0]} {col[1]}" for col in columnas])}
AS
BEGIN
    UPDATE {nombre_tabla} 
    SET {", ".join([f"{col[0]} = @{col[0]}" for col in columnas])} 
    WHERE id = @id
END
    """
    guardar_archivo(ubicacion, f"{nombre_proc_edit}.sql", contenido_edit)

    # --- DELETE ---
    nombre_proc_delete = f"{nombre_general}{alias}{procedimientos.get('DELETE') or 'Eliminar'}"
    contenido_delete = f"""
-- =============================================
-- Author:        Henry Agudelo
-- Create date: {fecha_actual}
-- Description: Elimina un registro de la tabla '{nombre_tabla}' por su ID
-- =============================================

CREATE PROCEDURE {nombre_proc_delete} 
    @id INT
AS
BEGIN
    DELETE FROM {nombre_tabla} WHERE id = @id
END
    """
    guardar_archivo(ubicacion, f"{nombre_proc_delete}.sql", contenido_delete)

    # --- GET ---
    nombre_proc_get = f"{nombre_general}{alias}{procedimientos.get('GET') or 'ObtenerPorId'}"
    contenido_get = f"""
-- =============================================
-- Author:        Henry Agudelo
-- Create date: {fecha_actual}
-- Description: Obtiene un registro de la tabla '{nombre_tabla}' por su ID
-- =============================================

CREATE PROCEDURE {nombre_proc_get} 
    @id INT
AS
BEGIN
    SELECT * FROM {nombre_tabla} WHERE id = @id
END
    """
    guardar_archivo(ubicacion, f"{nombre_proc_get}.sql", contenido_get)

    # --- GETLIST ---
    nombre_proc_getlist = f"{nombre_general}{alias}{procedimientos.get('GETLIST') or 'ObtenerLista'}"
    contenido_getlist = f"""
-- =============================================
-- Author:        Henry Agudelo
-- Create date: {fecha_actual}
-- Description: Obtiene una lista de registros de la tabla '{nombre_tabla}' 
--              (Agrega aquí la lógica para filtrar la lista)
-- =============================================

CREATE PROCEDURE {nombre_proc_getlist}
AS
BEGIN
    -- Implementa la lógica para obtener la lista con filtro
    SELECT * FROM {nombre_tabla} -- Reemplaza con tu consulta
END
    """
    guardar_archivo(ubicacion, f"{nombre_proc_getlist}.sql", contenido_getlist)

    # --- GETLISTALL ---
    nombre_proc_getlistall = f"{nombre_general}{alias}{procedimientos.get('GETLISTALL') or 'ObtenerTodos'}"
    contenido_getlistall = f"""
-- =============================================
-- Author:        Henry Agudelo
-- Create date: {fecha_actual}
-- Description: Obtiene todos los registros de la tabla '{nombre_tabla}'
-- =============================================

CREATE PROCEDURE {nombre_proc_getlistall}
AS
BEGIN
    SELECT * FROM {nombre_tabla}
END
    """
    guardar_archivo(ubicacion, f"{nombre_proc_getlistall}.sql", contenido_getlistall)


def guardar_archivo(ubicacion, nombre_archivo, contenido):
    """Guarda contenido en un archivo en la ubicación especificada."""
    ruta_completa = os.path.join(ubicacion, nombre_archivo)
    try:
        with open(ruta_completa, "w", encoding="utf-8") as archivo:  # Agregar encoding="utf-8"
            archivo.write(contenido)
    except Exception as e:
        messagebox.showerror("Error", f"Error al guardar el archivo {nombre_archivo}: {e}")


crear_crud_sql()