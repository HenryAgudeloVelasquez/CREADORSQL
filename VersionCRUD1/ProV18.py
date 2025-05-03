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
    filepath, _ = QFileDialog.getOpenFileName(
        None, "Seleccionar archivo de clientes", "",
        "CSV files (*.csv);;Excel files (*.xlsx);;All files (*)", options=options
    )
    if filepath:
        try:
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
    filepath, _ = QFileDialog.getOpenFileName(
        None, "Seleccionar archivo de productos", "",
        "CSV files (*.csv);;Excel files (*.xlsx);;All files (*)", options=options
    )
    if filepath:
        try:
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

        cliente = clientes[clientes['ID'] == cliente_id].iloc[0]
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

        tree.addTopLevelItem(QTreeWidgetItem([cliente['Nombre'], cliente['Dirección']]))
        for _, row in productos_cotizacion.iterrows():
            tree.addTopLevelItem(QTreeWidgetItem([row['Nombre'], str(row['Precio'])]))
        tree.addTopLevelItem(QTreeWidgetItem(["Subtotal", str(subtotal)]))
        tree.addTopLevelItem(QTreeWidgetItem(["Descuento", str(descuento)]))
        tree.addTopLevelItem(QTreeWidgetItem(["Total", str(total)]))

    except Exception as e:
        print(f"Error al generar la cotización: {e}")
        label_error.setText("Error al generar la cotización")


app = QApplication(sys.argv)
ventana = QWidget()
ventana.setWindowTitle("Sistema de Cotización")

# --- Widgets ---
label_archivo_clientes = QLabel("No se ha seleccionado ningún archivo")
label_archivo_productos = QLabel("No se ha seleccionado ningún archivo")
boton_cargar_clientes = QPushButton("Clientes")
boton_cargar_clientes.clicked.connect(cargar_archivo_clientes)
boton_cargar_productos = QPushButton("Productos")
boton_cargar_productos.clicked.connect(cargar_archivo_productos)
label_cliente = QLabel("ID del cliente:")
entry_cliente = QLineEdit()
label_productos = QLabel("IDs de productos (separados por comas):")
entry_productos = QLineEdit()
label_tipo = QLabel("Tipo de cotización:")
combobox_tipo = QComboBox()
combobox_tipo.addItems(["residencial", "comercial"])
boton_generar = QPushButton("Generar Cotización")
boton_generar.clicked.connect(generar_cotizacion)
label_error = QLabel("")
tree = QTreeWidget()

# --- Layout ---
grid = QGridLayout()
grid.addWidget(label_archivo_clientes, 0, 1)
grid.addWidget(boton_cargar_clientes, 0, 0)
grid.addWidget(label_archivo_productos, 1, 1)
grid.addWidget(boton_cargar_productos, 1, 0)
grid.addWidget(label_cliente, 2, 0)
grid.addWidget(entry_cliente, 2, 1)
grid.addWidget(label_productos, 3, 0)
grid.addWidget(entry_productos, 3, 1)
grid.addWidget(label_tipo, 4, 0)
grid.addWidget(combobox_tipo, 4, 1)
grid.addWidget(boton_generar, 5, 0, 1, 2)
grid.addWidget(label_error, 6, 0, 1, 2)
grid.addWidget(tree, 0, 2, 7, 1)  # La tabla ocupa varias filas

ventana.setLayout(grid)

ventana.show()
sys.exit(app.exec_())