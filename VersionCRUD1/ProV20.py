import tkinter as tk
from tkinter import filedialog, ttk, messagebox
import pandas as pd
from docx import Document

# Variables globales
clientes_df = None
productos_df = None

# Función para cargar archivos
def cargar_archivo(tipo):
    global clientes_df, productos_df
    ruta_archivo = filedialog.askopenfilename(
        defaultextension=".xlsx", filetypes=[("Archivos Excel", "*.xlsx")]
    )
    if not ruta_archivo:
        return
    try:
        if tipo == "clientes":
            clientes_df = pd.read_excel(ruta_archivo)
            # Validar columnas
            columnas_esperadas = ["Nombre/Razón Social", "ID/NIT", "Teléfono", "Email", "Dirección"]
            if not all(col in clientes_df.columns for col in columnas_esperadas):
                raise ValueError("El archivo de clientes no tiene las columnas esperadas.")
            messagebox.showinfo("Éxito", "Archivo de clientes cargado correctamente.")
            # Actualizar opciones del menú desplegable de búsqueda de clientes
            combo_busqueda_clientes['values'] = clientes_df.columns.tolist()
        elif tipo == "productos":
            productos_df = pd.read_excel(ruta_archivo)
            # Validar columnas
            columnas_esperadas = ["ID/Código", "Nombre", "Descripción", "Precio unitario"]
            if not all(col in productos_df.columns for col in columnas_esperadas):
                raise ValueError("El archivo de productos no tiene las columnas esperadas.")
            messagebox.showinfo("Éxito", "Archivo de productos cargado correctamente.")
            # Actualizar opciones del menú desplegable de búsqueda de productos
            combo_busqueda_productos['values'] = productos_df.columns.tolist()
    except Exception as e:
        messagebox.showerror("Error", f"Error al cargar el archivo: {e}")

# Función para buscar clientes
def buscar_clientes():
    global clientes_df
    if clientes_df is None:
        messagebox.showerror("Error", "Primero debes cargar el archivo de clientes.")
        return

    # Obtener el valor de búsqueda y la columna seleccionada
    valor_busqueda = campo_busqueda_clientes.get()
    columna_busqueda = combo_busqueda_clientes.get()

    if not valor_busqueda or not columna_busqueda:
        messagebox.showerror("Error", "Debes ingresar un valor de búsqueda y seleccionar una columna.")
        return

    try:
        # Filtrar los clientes
        resultados = clientes_df[
            clientes_df[columna_busqueda].str.contains(valor_busqueda, case=False)
        ]

        # Mostrar los resultados en la tabla
        tabla_clientes.delete(*tabla_clientes.get_children())
        for index, row in resultados.iterrows():
            tabla_clientes.insert("", tk.END, values=list(row))

    except Exception as e:
        messagebox.showerror("Error", f"Error al buscar clientes: {e}")

# Función para buscar productos
def buscar_productos():
    global productos_df
    if productos_df is None:
        messagebox.showerror("Error", "Primero debes cargar el archivo de productos.")
        return

    # Obtener el valor de búsqueda y la columna seleccionada
    valor_busqueda = campo_busqueda_productos.get()
    columna_busqueda = combo_busqueda_productos.get()

    if not valor_busqueda or not columna_busqueda:
        messagebox.showerror("Error", "Debes ingresar un valor de búsqueda y seleccionar una columna.")
        return

    try:
        # Filtrar los productos
        resultados = productos_df[
            productos_df[columna_busqueda].str.contains(valor_busqueda, case=False)
        ]

        # Mostrar los resultados en la tabla
        tabla_productos.delete(*tabla_productos.get_children())
        for index, row in resultados.iterrows():
            tabla_productos.insert("", tk.END, values=list(row))

    except Exception as e:
        messagebox.showerror("Error", f"Error al buscar productos: {e}")

# Función para generar cotización
def generar_cotizacion():
    global clientes_df, productos_df
    if clientes_df is None or productos_df is None:
        messagebox.showerror("Error", "Debes cargar ambos archivos antes de generar una cotización.")
        return

    try:
        # Obtener los productos seleccionados
        productos_seleccionados = []
        for item in tabla_productos.get_children():
            if tabla_productos.item(item)['values']:
                productos_seleccionados.append(tabla_productos.item(item)['values'])

        if not productos_seleccionados:
            messagebox.showerror("Error", "Debes seleccionar al menos un producto.")
            return

        # Crear un nuevo DataFrame con la información de la cotización
        cotizacion_df = pd.DataFrame(productos_seleccionados, columns=productos_df.columns)

        # Calcular el valor total de cada producto
        cotizacion_df['Valor total'] = cotizacion_df['Cantidad'] * cotizacion_df['Precio unitario']

        # Mostrar la cotización en una nueva ventana
        ventana_cotizacion = tk.Toplevel(ventana)
        ventana_cotizacion.title("Cotización")

        # Crear la tabla de la cotización
        tabla_cotizacion = ttk.Treeview(ventana_cotizacion, columns=cotizacion_df.columns, show="headings")
        for col in cotizacion_df.columns:
            tabla_cotizacion.heading(col, text=col)
        for index, row in cotizacion_df.iterrows():
            tabla_cotizacion.insert("", tk.END, values=list(row))
        tabla_cotizacion.