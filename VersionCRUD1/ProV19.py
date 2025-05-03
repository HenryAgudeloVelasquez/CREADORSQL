import sys
import datetime
from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, QPushButton, 
                             QLineEdit, QComboBox, QFileDialog, QGridLayout,
                             QHeaderView, QTreeWidget, QTreeWidgetItem)
import pandas as pd

def registrar_archivo(ruta_archivo):
    """Registra la fecha, hora y ruta del archivo en el archivo de registro."""
    with open("registro_archivos.txt", "a") as f:
        ahora = datetime.datetime.now()
        f.write(f"{ahora} - {ruta_archivo}\n")

def cargar_archivo_clientes():
    """Carga el archivo CSV o XLSX de clientes y registra la carga."""
    global clientes
    options = QFileDialog.Options()
    options |= QFileDialog.DontUseNativeDialog
    filepaths, _ = QFileDialog.getOpenFileNames(
        None, "Seleccionar archivo de clientes", "",
        "CSV files (*.csv);;Excel files (*.xlsx);;All files (*)", options=options
    )
    if filepaths:
        try:
            filepath = filepaths[0]
            print(f"Ruta del archivo seleccionado: {filepath}")
            if filepath.endswith('.csv'):
                clientes = pd.read_csv(filepath)
            elif filepath.endswith('.xlsx'):
                clientes = pd.read_excel(filepath)
            label_archivo_clientes.setText(filepath)
            registrar_archivo(filepath)
        except Exception as e:
            label_archivo_clientes.setText("Error al cargar el archivo")

def cargar_archivo_productos():
    """Carga el archivo CSV o XLSX de productos y registra la carga."""
    global productos
    options = QFileDialog.Options()
    options |= QFileDialog.DontUseNativeDialog
    filepaths, _ = QFileDialog.getOpenFileNames(
        None, "Seleccionar archivo de productos", "",
        "CSV files (*.csv);;Excel files (*.xlsx);;All files (*)", options=options
    )
    if filepaths:
        try:
            filepath = filepaths[0]
            print(f"Ruta del archivo seleccionado: {filepath}")
            if filepath.endswith('.csv'):
                productos = pd.read_csv(filepath)
            elif filepath.endswith('.xlsx'):
                productos = pd.read_excel(filepath)
            label_archivo_productos.setText(filepath)
            registrar_archivo(filepath)
        except Exception as e:
            label_archivo_productos.setText("Error al cargar el archivo")

def generar_cotizacion():
    """Genera la cotización y la muestra en una tabla."""
    try:
        cliente_id = int(entry_cliente.text())
        productos_ids = [int(x) for x in entry_productos.text().split(",")]
        tipo_cotizacion = combobox_tipo.currentText()

        cliente = clientes[clientes['ID'] == cliente_id].iloc[0]  # Acceder a la fila del cliente
        productos_cotizacion = productos[productos['ID'].isin(productos_ids)]

        subtotal = productos_cotizacion['Precio'].sum()

        if tipo_cotizacion == "residencial":
            descuento = 0.05
        elif tipo_cotizacion == "comercial":
            descuento = 0.10
        else:
            descuento = 0

        total = subtotal * (1 - descuento)

        tree.clear()
        tree.setHeaderLabels(["Descripción", "Valor"])
        tree.header().setSectionResizeMode(QHeaderView.Stretch)

        # Mostrar la información del cliente
        tree.addTopLevelItem(QTreeWidgetItem(["Cliente:", cliente['Nombre']]))
        tree.addTopLevelItem(QTreeWidgetItem(["Dirección:", cliente['Dirección']]))

        # Mostrar los productos
        for _, row in productos_cotizacion.iterrows():
            tree.addTopLevelItem(QTreeWidgetItem([row['Nombre'], str(row['Precio'])]))

        # Mostrar el resumen
        tree.addTopLevelItem(QTreeWidgetItem(["Subtotal:", str(subtotal)]))
        tree.addTopLevelItem(QTreeWidgetItem(["Descuento:", str(descuento)]))
        tree.addTopLevelItem(QTreeWidgetItem(["Total:", str(total)]))

    except Exception as e:
        print(f"Error al generar la cotización: {e}")
        label_error.setText("Error al generar la cotización")

# ... (El resto del código para la interfaz gráfica se mantiene igual) ...