def crear_procedimientos_almacenados(ubicacion,
                                    nombre_tabla,
                                    columnas,
                                    fecha_actual,
                                    nombre_add,
                                    nombre_edit,
                                    nombre_delete,
                                    nombre_get,
                                    nombre_getlist,
                                    nombre_getlistall,
                                    alias="",
                                    dialecto="SQL Server"):
    """¡Crea los archivos SQL para el CRUD con nombres personalizados 
    y soporte para diferentes dialectos SQL!"""

    mapeo_tipos = DIALECTOS_SQL.get(dialecto, DIALECTOS_SQL["SQL Server"])

    # --- ADD ---
    nombre_proc_add = f"{alias}{nombre_add or 'Insertar'}"
    contenido_add = f"""
-- =============================================
-- Author:		Henry Agudelo
-- Create date: {fecha_actual}
-- Description:	Inserta un nuevo registro en la tabla '{nombre_tabla}'
-- =============================================

CREATE PROCEDURE {nombre_proc_add} 
    {", ".join([f"@{col[0]} {mapeo_tipos.get(col[1], col[1])}" for col in columnas])}
AS
BEGIN
    INSERT INTO {nombre_tabla} ({", ".join([col[0] for col in columnas])}) 
    VALUES ({", ".join([f"@{col[0]}" for col in columnas])})
END
    """
    guardar_archivo(ubicacion, f"{nombre_proc_add}.sql", contenido_add)

    # --- EDIT ---
    nombre_proc_edit = f"{alias}{nombre_edit or 'Actualizar'}"
    contenido_edit = f"""
-- =============================================
-- Author:		Henry Agudelo
-- Create date: {fecha_actual}
-- Description:	Actualiza un registro de la tabla '{nombre_tabla}'
-- =============================================

CREATE PROCEDURE {nombre_proc_edit} 
    @id INT,
    {", ".join([f"@{col[0]} {mapeo_tipos.get(col[1], col[1])}" for col in columnas])}
AS
BEGIN
    UPDATE {nombre_tabla} 
    SET {", ".join([f"{col[0]} = @{col[0]}" for col in columnas])} 
    WHERE id = @id
END
    """
    guardar_archivo(ubicacion, f"{nombre_proc_edit}.sql", contenido_edit)

    # --- DELETE ---
    nombre_proc_delete = f"{alias}{nombre_delete or 'Eliminar'}"
    contenido_delete = f"""
-- =============================================
-- Author:		Henry Agudelo
-- Create date: {fecha_actual}
-- Description:	Elimina un registro de la tabla '{nombre_tabla}' por su ID
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
    nombre_proc_get = f"{alias}{nombre_get or 'ObtenerPorId'}"
    contenido_get = f"""
-- =============================================
-- Author:		Henry Agudelo
-- Create date: {fecha_actual}
-- Description:	Obtiene un registro de la tabla '{nombre_tabla}' por su ID
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
    nombre_proc_getlist = f"{alias}{nombre_getlist or 'ObtenerLista'}"
    contenido_getlist = f"""
-- =============================================
-- Author:		Henry Agudelo
-- Create date: {fecha_actual}
-- Description:	Obtiene una lista de registros de la tabla '{nombre_tabla}' 
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
    nombre_proc_getlistall = f"{alias}{nombre_getlistall or 'ObtenerTodos'}"
    contenido_getlistall = f"""
-- =============================================
-- Author:		Henry Agudelo
-- Create date: {fecha_actual}
-- Description:	Obtiene todos los registros de la tabla '{nombre_tabla}'
-- =============================================

CREATE PROCEDURE {nombre_proc_getlistall}
AS
BEGIN
    SELECT * FROM {nombre_tabla}
END
    """
    guardar_archivo(ubicacion, f"{nombre_proc_getlistall}.sql", contenido_getlistall)


def guardar_archivo(ubicacion, nombre_archivo, contenido):
    """Guarda el contenido en un archivo."""
    ruta_completa = os.path.join(ubicacion, nombre_archivo)
    try:
        with open(ruta_completa, "w") as archivo:
            archivo.write(contenido)
    except Exception as e:
        messagebox.showerror("Error", f"Error al crear el archivo: {e}")