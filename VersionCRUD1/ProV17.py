
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import pandas as pd
import datetime

def registrar_archivo(ruta_archivo):
    """Registra la fecha, hora y ruta del archivo en el archivo de registro."""
    with open("registro_archivos.txt", "a") as f:
        ahora = datetime.datetime.now()
        f.write(f"{ahora} - {ruta_archivo}\n")

def cargar_archivo_clientes():
    """Carga el archivo CSV o XLSX de clientes y registra la carga."""
    global clientes
    filepath = filedialog.askopenfilename(
        initialdir="/",
        title="Seleccionar archivo de clientes",
        filetypes=(("CSV files", "*.csv"), ("Excel files", "*.xlsx"), ("all files", "*.*"))
    )
    if filepath:
        try:
            if filepath.endswith('.csv'):
                clientes = pd.read_csv(filepath)
            elif filepath.endswith('.xlsx'):
                clientes = pd.read_excel(filepath)
            label_archivo_clientes.config(text=filepath)
            registrar_archivo(filepath)  # Registrar el archivo cargado
        except Exception as e:
            label_archivo_clientes.config(text="Error al cargar el archivo")


def cargar_archivo_productos():
    """Carga el archivo CSV o XLSX de productos y registra la carga."""
    global productos
    filepath = filedialog.askopenfilename(
        initialdir="/",
        title="Seleccionar archivo de productos",
        filetypes=(("CSV files", "*.csv"), ("Excel files", "*.xlsx"), ("all files", "*.*"))
    )
    if filepath:
        try:
            if filepath.endswith('.csv'):
                productos = pd.read_csv(filepath)
            elif filepath.endswith('.xlsx'):
                productos = pd.read_excel(filepath)
            label_archivo_productos.config(text=filepath)
            registrar_archivo(filepath)  # Registrar el archivo cargado
        except Exception as e:
            label_archivo_productos.config(text="Error al cargar el archivo")


def generar_cotizacion():
    """Genera la cotización y la muestra en una tabla."""
    try:
        cliente_id = int(entry_cliente.get())
        productos_ids = [int(x) for x in entry_productos.get().split(",")]
        tipo_cotizacion = combobox_tipo.get()

        # Obtener datos del cliente y productos (usando los dataframes globales)
        cliente = clientes[clientes['ID'] == cliente_id].iloc[0]
        productos_cotizacion = productos[productos['ID'].isin(productos_ids)]

        # Calcular subtotal
        subtotal = productos_cotizacion['Precio'].sum()

        # Aplicar descuentos según el tipo de cotización
        if tipo_cotizacion == "residencial":
            descuento = 0.05  # 5% de descuento para residenciales
        elif tipo_cotizacion == "comercial":
            descuento = 0.10  # 10% de descuento para comerciales
        else:
            descuento = 0

        # Calcular total
        total = subtotal * (1 - descuento)

        # Mostrar la cotización en la tabla
        for i in tree.get_children():
            tree.delete(i)  # Limpiar la tabla

        tree.insert("", tk.END, values=(cliente['Nombre'], cliente['Dirección']))
        for _, row in productos_cotizacion.iterrows():
            tree.insert("", tk.END, values=(row['Nombre'], row['Precio']))
        tree.insert("", tk.END, values=("Subtotal", subtotal))
        tree.insert("", tk.END, values=("Descuento", descuento))
        tree.insert("", tk.END, values=("Total", total))

    except Exception as e:
        print(f"Error al generar la cotización: {e}")
        label_error.config(text="Error al generar la cotización")


# Crear la ventana principal
ventana = tk.Tk()
ventana.title("Sistema de Cotización")

# --- Frame para cargar archivos ---
frame_archivo = tk.LabelFrame(ventana, text="Cargar archivos CSV")
frame_archivo.grid(row=0, column=0, padx=10, pady=10)

boton_cargar_clientes = tk.Button(frame_archivo, text="Clientes", command=cargar_archivo_clientes)
boton_cargar_clientes.grid(row=0, column=0, padx=5, pady=5)

label_archivo_clientes = tk.Label(frame_archivo, text="No se ha seleccionado ningún archivo")
label_archivo_clientes.grid(row=0, column=1, padx=5, pady=5)

boton_cargar_productos = tk.Button(frame_archivo, text="Productos", command=cargar_archivo_productos)
boton_cargar_productos.grid(row=1, column=0, padx=5, pady=5)

label_archivo_productos = tk.Label(frame_archivo, text="No se ha seleccionado ningún archivo")
label_archivo_productos.grid(row=1, column=1, padx=5, pady=5)

# --- Frame para ingresar datos de la cotización ---
frame_cotizacion = tk.LabelFrame(ventana, text="Generar Cotización")
frame_cotizacion.grid(row=1, column=0, padx=10, pady=10)

label_cliente = tk.Label(frame_cotizacion, text="ID del cliente:")
label_cliente.grid(row=0, column=0, padx=5, pady=5)
entry_cliente = tk.Entry(frame_cotizacion)
entry_cliente.grid(row=0, column=1, padx=5, pady=5)

label_productos = tk.Label(frame_cotizacion, text="IDs de productos (separados por comas):")
label_productos.grid(row=1, column=0, padx=5, pady=5)
entry_productos = tk.Entry(frame_cotizacion)
entry_productos.grid(row=1, column=1, padx=5, pady=5)

label_tipo = tk.Label(frame_cotizacion, text="Tipo de cotización:")
label_tipo.grid(row=2, column=0, padx=5, pady=5)
combobox_tipo = ttk.Combobox(frame_cotizacion, values=["residencial", "comercial"], state="readonly")
combobox_tipo.grid(row=2, column=1, padx=5, pady=5)
combobox_tipo.current(0)  # Seleccionar "residencial" por defecto

boton_generar = tk.Button(frame_cotizacion, text="Generar Cotización", command=generar_cotizacion)
boton_generar.grid(row=3, column=0, columnspan=2, padx=5, pady=5)

label_error = tk.Label(frame_cotizacion, text="", fg="red")
label_error.grid(row=4, column=0, columnspan=2, padx=5, pady=5)

# --- Frame para mostrar la cotización ---
frame_tabla = tk.LabelFrame(ventana, text="Cotización")
frame_tabla.grid(row=0, column=1, rowspan=2, padx=10, pady=10)

tree = ttk.Treeview(frame_tabla, columns=("Descripción", "Valor"), show="headings")
tree.heading("Descripción", text="Descripción")
tree.heading("Valor", text="Valor")
tree.pack(expand=True, fill="both")

ventana.mainloop()
