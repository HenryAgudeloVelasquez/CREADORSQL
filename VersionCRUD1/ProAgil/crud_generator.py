import os
from datetime import datetime

from tkinter import messagebox


def crear_procedimientos_almacenados(ubicacion,
                                    nombre_tabla,
                                    columnas,
                                    fecha_actual=None,
                                    alias="",
                                    nombre_general="",
                                    **procedimientos):
    """Crea los archivos SQL para el CRUD con nombres personalizados."""
    if fecha_actual is None:
        fecha_actual = datetime.now().strftime("%Y-%m-%d")

    # --- ADD ---
    nombre_proc_add = f"{alias}{procedimientos.get('ADD') or 'Insertar'}{nombre_general}"
    contenido_add = generar_sql_add(nombre_tabla, columnas, fecha_actual)
    guardar_archivo(ubicacion, f"{nombre_proc_add}.sql", contenido_add)

    # --- EDIT ---
    nombre_proc_edit = f"{alias}{procedimientos.get('EDIT') or 'Actualizar'}{nombre_general}"
    contenido_edit = generar_sql_edit(nombre_tabla, columnas, fecha_actual)
    guardar_archivo(ubicacion, f"{nombre_proc_edit}.sql", contenido_edit)

    # --- DELETE ---
    nombre_proc_delete = f"{alias}{procedimientos.get('DELETE') or 'Eliminar'}{nombre_general}"
    contenido_delete = generar_sql_delete(nombre_tabla, fecha_actual)
    guardar_archivo(ubicacion, f"{nombre_proc_delete}.sql", contenido_delete)

    # --- GET ---
    nombre_proc_get = f"{alias}{procedimientos.get('GET') or 'ObtenerPorId'}{nombre_general}"
    contenido_get = generar_sql_get(nombre_tabla, fecha_actual)
    guardar_archivo(ubicacion, f"{nombre_proc_get}.sql", contenido_get)

    # --- GETLIST ---
    nombre_proc_getlist = f"{alias}{procedimientos.get('GETLIST') or 'ObtenerLista'}{nombre_general}"
    contenido_getlist = generar_sql_getlist(nombre_tabla, fecha_actual)
    guardar_archivo(ubicacion, f"{nombre_proc_getlist}.sql", contenido_getlist)

    # --- GETLISTALL ---
    nombre_proc_getlistall = f"{alias}{procedimientos.get('GETLISTALL') or 'ObtenerTodos'}{nombre_general}"
    contenido_getlistall = generar_sql_getlistall(nombre_tabla, fecha_actual)
    guardar_archivo(ubicacion, f"{nombre_proc_getlistall}.sql", contenido_getlistall)


def generar_sql_add(nombre_tabla, columnas, fecha_actual):
    """Genera el SQL para el procedimiento almacenado ADD."""
    columnas_str = ", ".join([f"@{col[0]} {col[1]}{f'({col[2]})' if col[1] == 'VARCHAR' and col[2] else ''}" for col in columnas])
    valores_str = ", ".join([f"@{col[0]}" for col in columnas])
    return f"""
-- =============================================
-- Author:        Henry Agudelo
-- Create date: {fecha_actual}
-- Description: Inserta un nuevo registro en la tabla '{nombre_tabla}'
-- =============================================

CREATE PROCEDURE {nombre_tabla}_Add 
    {columnas_str}
AS
BEGIN
    INSERT INTO {nombre_tabla} ({", ".join([col[0] for col in columnas])}) 
    VALUES ({valores_str})
END
    """


def generar_sql_edit(nombre_tabla, columnas, fecha_actual):
    """Genera el SQL para el procedimiento almacenado EDIT."""
    columnas_str = ", ".join([f"@{col[0]} {col[1]}{f'({col[2]})' if col[1] == 'VARCHAR' and col[2] else ''}" for col in columnas])
    set_str = ", ".join([f"{col[0]} = @{col[0]}" for col in columnas])
    return f"""
-- =============================================
-- Author:        Henry Agudelo
-- Create date: {fecha_actual}
-- Description: Actualiza un registro de la tabla '{nombre_tabla}'
-- =============================================

CREATE PROCEDURE {nombre_tabla}_Edit 
    @id INT,
    {columnas_str}
AS
BEGIN
    UPDATE {nombre_tabla} 
    SET {set_str}
    WHERE id = @id
END
    """


def generar_sql_delete(nombre_tabla, fecha_actual):
    """Genera el SQL para el procedimiento almacenado DELETE."""
    return f"""
-- =============================================
-- Author:        Henry Agudelo
-- Create date: {fecha_actual}
-- Description: Elimina un registro de la tabla '{nombre_tabla}' por su ID
-- =============================================

CREATE PROCEDURE {nombre_tabla}_Delete
    @id INT
AS
BEGIN
    DELETE FROM {nombre_tabla} WHERE id = @id
END
    """


def generar_sql_get(nombre_tabla, fecha_actual):
    """Genera el SQL para el procedimiento almacenado GET."""
    return f"""
-- =============================================
-- Author:        Henry Agudelo
-- Create date: {fecha_actual}
-- Description: Obtiene un registro de la tabla '{nombre_tabla}' por su ID
-- =============================================

CREATE PROCEDURE {nombre_tabla}_Get 
    @id INT
AS
BEGIN
    SELECT * FROM {nombre_tabla} WHERE id = @id
END
    """


def generar_sql_getlist(nombre_tabla, fecha_actual):
    """Genera el SQL para el procedimiento almacenado GETLIST."""
    return f"""
-- =============================================
-- Author:        Henry Agudelo
-- Create date: {fecha_actual}
-- Description: Obtiene una lista de registros de la tabla '{nombre_tabla}' 
--              (Agrega aquí la lógica para filtrar la lista)
-- =============================================

CREATE PROCEDURE {nombre_tabla}_GetList
AS
BEGIN
    -- Implementa la lógica para obtener la lista con filtro
    SELECT * FROM {nombre_tabla} -- Reemplaza con tu consulta
END
    """


def generar_sql_getlistall(nombre_tabla, fecha_actual):
    """Genera el SQL para el procedimiento almacenado GETLISTALL."""
    return f"""
-- =============================================
-- Author:        Henry Agudelo
-- Create date: {fecha_actual}
-- Description: Obtiene todos los registros de la tabla '{nombre_tabla}'
-- =============================================

CREATE PROCEDURE {nombre_tabla}_GetListAll
AS
BEGIN
    SELECT * FROM {nombre_tabla}
END
    """


def guardar_archivo(ubicacion, nombre_archivo, contenido):
    """Guarda contenido en un archivo en la ubicación especificada."""
    ruta_completa = os.path.join(ubicacion, nombre_archivo)
    try:
        with open(ruta_completa, "w", encoding="utf-8") as archivo:
            archivo.write(contenido)
    except Exception as e:
        messagebox.showerror("Error", f"Error al guardar el archivo {nombre_archivo}: {e}")


def crear_archivo_dto(ubicacion, nombre_general, columnas):
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


def convertir_tipo_dato(tipo_sql):
    """Convierte un tipo de dato SQL a un tipo de dato C#."""
    tipo_sql = tipo_sql.upper()
    if tipo_sql in ("INT", "INTEGER"):
        return "int"