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
            # ... (código para capturar datos y validar entradas) ...

            fecha_actual = datetime.now().strftime("%Y-%m-%d")
            crear_procedimientos_almacenados(ubicacion, nombre_tabla, columnas, fecha_actual, alias=alias, nombre_general=nombre_general, **procedimientos)
            crear_archivo_cs(ubicacion, nombre_general, columnas)

            messagebox.showinfo("Éxito", f"Archivos creados correctamente en {ubicacion}.")

            # ... (código para limpiar campos) ...

        except ValueError as ve:
            messagebox.showerror("Error de validación", str(ve))
        except Exception as e:
            messagebox.showerror("Error", f"Error al crear los archivos: {e}")

    def buscar_ubicacion():
        """Abre un diálogo para seleccionar una carpeta y actualiza el campo de ubicación."""
        # ... (código para buscar ubicación) ...

    def agregar_columna():
        """Agrega una nueva fila para definir una columna."""
        # ... (código para agregar columna) ...

    def eliminar_columna(fila):
        """Elimina una fila de columna especificada."""
        # ... (código para eliminar columna) ...

    def actualizar_vista_tabla():
        """Actualiza dinámicamente la vista previa de la tabla."""
        # ... (código para actualizar vista de tabla) ...

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
    # ... (código para crear widgets) ...

    ventana.mainloop()


crear_crud_sql()