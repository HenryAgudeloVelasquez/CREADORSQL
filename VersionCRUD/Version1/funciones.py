import os
from datetime import datetime

import tkinter as tk
from tkinter import filedialog, messagebox, ttk

from funciones import crear_procedimientos_almacenados, guardar_archivo, convertir_tipo_dato
from tipos_datos import TIPOS_DATOS


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
            crear_archivo_cs(ubicacion, nombre_general, columnas)

            messagebox.showinfo("Éxito", f"Archivos creados correctamente en {ubicacion}.")

            # Limpiar campos después de guardar
            nombre_tabla_entry.delete(0, tk.END)
            ubicacion_entry.delete(0, tk.END)
            alias_entry.delete(0, tk.END)
            nombre_general_entry.delete(0, tk.END)
            for entry in procedimientos_entries.values():
                entry.delete(0, tk.END)
            for i in range(len(columnas_nombres)):
                eliminar_columna(0)

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
        tipo_combo = ttk.Combobox(columnas_frame, textvariable=tipo_var, values=TIPOS_DATOS)
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
        if columnas:
            contenido_tabla = f"CREATE TABLE {nombre_tabla} (\n    id INT PRIMARY KEY,\n    {',\n    '.join(columnas)}\n);"
        else:
            contenido_tabla = f"CREATE TABLE {nombre_tabla} (\n    id INT PRIMARY KEY\n);"
        tabla_text.delete("1.0", tk.END)
        tabla_text.insert(tk.END, contenido_tabla)

    def crear_archivo_cs(ubicacion, nombre_general, columnas):
        """Crea un archivo .cs con una clase DTO que representa la tabla."""
        contenido_cs = f"""using System.ComponentModel.DataAnnotations;

namespace TH.Models.DTO
{{
    public class {nombre_general}
    {{
{''.join([f"        public {convertir_tipo_dato(col[1])} {col[0]} {{ get; set; }}\n" for col in columnas])}
    }}
}}
    """
        guardar_archivo(ubicacion, f"{nombre_general}.cs", contenido_cs)

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
    procedimientos_vars = {}  # Diccionario para almacenar las variables StringVar

    for i, proc in enumerate(procedimientos_labels, start=4):
        tk.Label(ventana, text=f"Nombre {proc}:").grid(row=i, column=0, padx=5, pady=5)

        # Usar StringVar para cada campo de procedimiento
        var = tk.StringVar()
        procedimientos_vars[proc] = var  # Guardar la variable en el diccionario

        entry = tk.Entry(ventana, textvariable=var)  # Vincular la variable al Entry
        entry.grid(row=i, column=1, padx=5, pady=5)
        procedimientos_entries[proc] = entry

        # Función para actualizar el valor del campo cuando cambia nombre_general
        def actualizar_procedimiento(var=var, *args):  # Capturar var en cada iteración
            nombre_general = nombre_general_entry.get().strip()
            var.set(nombre_general)

        # Llamar a actualizar_procedimiento cuando cambia nombre_general
        nombre_general_entry.bind("<KeyRelease>", lambda _: actualizar_procedimiento(var))  # Pasar var como argumento

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

    tk.Button(ventana, text="Agregar columna", command=agregar_columna).grid(row=12, column=1, padx=5, pady=5)

    # --- Vista previa de la tabla ---
    tk.Label(ventana, text="Vista previa de la tabla:").grid(row=13, column=0, padx=5, pady=5)
    tabla_text = tk.Text(ventana, height=10)
    tabla_text.grid(row=14, column=0, columnspan=3, padx=5, pady=5)

    # --- Botón guardar ---
    tk.Button(ventana, text="Guardar", command=guardar_archivos).grid(row=15, column=1, padx=5, pady=5)

    ventana.mainloop()

crear_crud_sql()