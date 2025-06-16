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
    contenido_add = generar_sql_add(nombre_tabla, columnas, fecha_actual,nombre_proc_add)
    guardar_archivo(ubicacion, f"{nombre_proc_add}.sql", contenido_add)

    # --- EDIT ---
    nombre_proc_edit = f"{alias}{procedimientos.get('EDIT') or 'Actualizar'}{nombre_general}"
    contenido_edit = generar_sql_edit(nombre_tabla, columnas, fecha_actual,nombre_proc_edit)
    guardar_archivo(ubicacion, f"{nombre_proc_edit}.sql", contenido_edit)

    # --- DELETE ---
    nombre_proc_delete = f"{alias}{procedimientos.get('DELETE') or 'Eliminar'}{nombre_general}"
    contenido_delete = generar_sql_delete(nombre_tabla, fecha_actual,nombre_proc_delete)
    guardar_archivo(ubicacion, f"{nombre_proc_delete}.sql", contenido_delete)

    # --- GET ---
    nombre_proc_get = f"{alias}{procedimientos.get('GET') or 'ObtenerPorId'}{nombre_general}"
    contenido_get = generar_sql_get(nombre_tabla, fecha_actual,nombre_proc_get)
    guardar_archivo(ubicacion, f"{nombre_proc_get}.sql", contenido_get)

    # --- GETLIST ---
    nombre_proc_getlist = f"{alias}{procedimientos.get('GETLIST') or 'ObtenerLista'}{nombre_general}"
    contenido_getlist = generar_sql_getlist(nombre_tabla, fecha_actual,nombre_proc_getlist)
    guardar_archivo(ubicacion, f"{nombre_proc_getlist}.sql", contenido_getlist)

    # --- GETLISTALL ---
    nombre_proc_getlistall = f"{alias}{procedimientos.get('GETLISTALL') or 'ObtenerTodos'}{nombre_general}"
    contenido_getlistall = generar_sql_getlistall(nombre_tabla, fecha_actual,nombre_proc_getlistall)
    guardar_archivo(ubicacion, f"{nombre_proc_getlistall}.sql", contenido_getlistall)

def generar_sql_add(nombre_tabla, columnas, fecha_actual,procedimiento):
    """Genera el SQL para el procedimiento almacenado ADD."""
    return f"""
-- =============================================
-- Author:        Henry Agudelo
-- Create date: {fecha_actual}
-- Description: Inserta un nuevo registro en la tabla '{nombre_tabla}'
-- =============================================


CREATE PROCEDURE {procedimiento}
    {", ".join([f"@{col[0]} {col[1]}" for col in columnas])}
AS

BEGIN
    SET NOCOUNT ON;
    SET TRANSACTION ISOLATION LEVEL READ UNCOMMITTED;

BEGIN
    INSERT INTO {nombre_tabla} ({", ".join([col[0] for col in columnas])}) 
    VALUES ({", ".join([f"@{col[0]}" for col in columnas])})
END
END
    """

def generar_sql_edit(nombre_tabla, columnas, fecha_actual,procedimiento):
    """Genera el SQL para el procedimiento almacenado EDIT."""
    return f"""
-- =============================================
-- Author:        Henry Agudelo
-- Create date: {fecha_actual}
-- Description: Actualiza un registro de la tabla '{nombre_tabla}'
-- =============================================

CREATE PROCEDURE {procedimiento}
    @id INT,
    {", ".join([f"@{col[0]} {col[1]}" for col in columnas])}
AS

BEGIN
    SET NOCOUNT ON;
    SET TRANSACTION ISOLATION LEVEL READ UNCOMMITTED;

BEGIN
    UPDATE {nombre_tabla} 
    SET {", ".join([f"{col[0]} = @{col[0]}" for col in columnas])} 
    WHERE id = @id
END
END
    """

def generar_sql_delete(nombre_tabla, fecha_actual,procedimiento):
    """Genera el SQL para el procedimiento almacenado DELETE."""
    return f"""
-- =============================================
-- Author:        Henry Agudelo
-- Create date: {fecha_actual}
-- Description: Elimina un registro de la tabla '{nombre_tabla}' por su ID
-- =============================================

CREATE PROCEDURE {procedimiento}
    @id INT
AS

BEGIN
    SET NOCOUNT ON;
    SET TRANSACTION ISOLATION LEVEL READ UNCOMMITTED;

BEGIN
    UPDATE  {nombre_tabla} SET Estado = 0, FechaModifica = GETDATE() WHERE id = @id
END
END
    """

def generar_sql_get(nombre_tabla, fecha_actual,procedimiento):
    """Genera el SQL para el procedimiento almacenado GET."""
    return f"""
-- =============================================
-- Author:        Henry Agudelo
-- Create date: {fecha_actual}
-- Description: Obtiene un registro de la tabla '{nombre_tabla}' por su ID
-- =============================================

CREATE PROCEDURE {procedimiento}
    @id INT
AS

BEGIN
    SET NOCOUNT ON;
    SET TRANSACTION ISOLATION LEVEL READ UNCOMMITTED;

BEGIN
    SELECT * FROM {nombre_tabla} WHERE id = @id
END
END
    """

def generar_sql_getlist(nombre_tabla, fecha_actual,procedimiento):
    """Genera el SQL para el procedimiento almacenado GETLIST."""
    return f"""
-- =============================================
-- Author:        Henry Agudelo
-- Create date: {fecha_actual}
-- Description: Obtiene una lista de registros de la tabla '{nombre_tabla}' 
--              (Agrega aquí la lógica para filtrar la lista)
-- =============================================

CREATE PROCEDURE {procedimiento}
AS

BEGIN
    SET NOCOUNT ON;
    SET TRANSACTION ISOLATION LEVEL READ UNCOMMITTED;

BEGIN
    -- Implementa la lógica para obtener la lista con filtro
    SELECT * FROM {nombre_tabla} -- Reemplaza con tu consulta
END
END
    """

def generar_sql_getlistall(nombre_tabla, fecha_actual,procedimiento):
    """Genera el SQL para el procedimiento almacenado GETLISTALL."""
    return f"""
-- =============================================
-- Author:        Henry Agudelo
-- Create date: {fecha_actual}
-- Description: Obtiene todos los registros de la tabla '{nombre_tabla}'
-- =============================================

CREATE PROCEDURE {procedimiento}
AS

BEGIN
    SET NOCOUNT ON;
    SET TRANSACTION ISOLATION LEVEL READ UNCOMMITTED;

BEGIN
    SELECT * FROM {nombre_tabla}
END
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

def crear_archivo_dto(ubicacion, nombre_general, columnas, nombre_ruta_DTO):
    """Crea un archivo .cs con una clase DTO que representa la tabla."""
    contenido_cs = f"""using System.ComponentModel.DataAnnotations;

namespace {nombre_ruta_DTO}
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
    
    if tipo_sql in ("INT", "INTEGER", "TINYINT", "SMALLINT", "BIGINT"):
        return "int"
    elif tipo_sql in ("VARCHAR", "NVARCHAR", "TEXT", "NTEXT", "CHAR", "NCHAR"):
        return "string"
    elif tipo_sql in ("FLOAT", "REAL"):
        return "float"
    elif tipo_sql in ("DECIMAL", "NUMERIC", "MONEY", "SMALLMONEY"):
        return "decimal"
    elif tipo_sql in ("DATE"):
        return "DateTime"
    elif tipo_sql in ("DATETIME", "SMALLDATETIME"):
        return "DateTime"
    elif tipo_sql in ("BOOL", "BIT"):
        return "bool"
    elif tipo_sql in ("BINARY", "VARBINARY", "IMAGE"):
        return "byte[]"
    elif tipo_sql == "TIMESTAMP":
        return "byte[]"  # O "long" si se usa como número de secuencia
    elif tipo_sql == "UNIQUEIDENTIFIER":
        return "Guid"
    elif tipo_sql == "XML":
        return "XmlDocument"  # O "XDocument" según la librería que uses
    else:
        return "object"  # Tipo de dato genérico para casos no contemplados

def crear_servicio_cs(ubicacion, nombre_clase, namespace, nombre_sp_get, nombre_sp_get_list, nombre_sp_get_all, nombre_sp_add, nombre_sp_edit, nombre_sp_delete, nombre_modelo,alias):
    """Crea un archivo .cs con la estructura de servicio proporcionada."""
    contenido = f"""
using Dapper;
using {alias}.Data;
using {alias}.Interfaces;
using {alias}.Models;
using System.Data;
using API.Library;
using System.Reflection;

namespace {alias}.Services
{{
    public class Service{nombre_clase}(DataConnectionContext context, IResponseService responseService) : IService{nombre_clase}<{nombre_clase}>
    {{
        private readonly DataConnectionContext context = context;
        private readonly IResponseService _responseService = responseService;



        #region SERVICIOS GET
        public async Task<IResponseService> Get(dynamic id)
        {{
            try
            {{
                using var connection = context.CreateConnection();
                var param = new DynamicParameters();
                param.Add("@Id", id, DbType.Int32, ParameterDirection.Input, 10);

                dynamic resultado = await connection.QueryFirstOrDefaultAsync("dbo.{nombre_sp_get}", param, commandType: CommandType.StoredProcedure);

                _responseService.EstablecerRespuesta(true, resultado);
            }}
            catch (Exception ex)
            {{
                _responseService.Error = ex.Message;
                _responseService.Estado = false;
            }}
            return _responseService;
        }}
        #endregion

        #region SERVICIOS GETLIST
        public async Task<IResponseService> GetList(dynamic id)
        {{
            try
            {{
                using var connection = context.CreateConnection();
                var param = new DynamicParameters();
                param.Add("@Id", idUsuario, DbType.Int64, ParameterDirection.Input, 50);
                var resultado = await connection.QueryAsync("dbo.{nombre_sp_get_list}", param, commandType: CommandType.StoredProcedure);

                _responseService.EstablecerRespuestaLista(true, resultado);
            }}
            catch (Exception ex)
            {{
                _responseService.Error = ex.Message;
                _responseService.Estado = false;
            }}
            return _responseService;
        }}
        #endregion

        #region SERVICIOS GETLISTALL
        public async Task<IResponseService> GetListAll()
        {{
            try
            {{
                using var connection = context.CreateConnection();
                var resultado = await connection.QueryAsync("dbo.{nombre_sp_get_all}", null, commandType: CommandType.StoredProcedure);
                _responseService.EstablecerRespuestaLista(true, resultado);
            }}
            catch (Exception ex)
            {{
                _responseService.Error = ex.Message;
                _responseService.Estado = false;
            }}
            return _responseService;
        }}
        #endregion

        #region SERVICIOS ADD
        public async Task<IResponseService> Add({nombre_clase} model)
        {{
            try
            {{
                 using var connection = context.CreateConnection();
                 var parameters = new DynamicParameters();

                // Ejemplo: parameters.Add("@", model.Nombre, DbType.String, ParameterDirection.Input);
                
              


                dynamic resultado = await connection.ExecuteScalarAsync("dbo.{nombre_sp_add}", parameters, commandType: CommandType.StoredProcedure);
                _responseService.EstablecerRespuesta(true, model);
            }}
            catch (Exception ex)
            {{
                _responseService.Error = ex.Message;
                _responseService.Estado = false;
            }}
            return _responseService;
        }}
        #endregion

        #region SERVICIOS EDIT
        public async Task<IResponseService> Edit(dynamic id,{nombre_clase} model)
        {{
            try
            {{
                using var connection = context.CreateConnection();
                var parameters = new DynamicParameters();

                // Ejemplo: param.Add("@Nombre", model.Nombre, DbType.String, ParameterDirection.Input);

                dynamic resultado = await connection.ExecuteScalarAsync("dbo.{nombre_sp_edit}", parameters, commandType: CommandType.StoredProcedure);

                _responseService.EstablecerRespuesta(true, resultado);
            }}
            catch (Exception ex)
            {{
                _responseService.Error = ex.Message;
                _responseService.Estado = false;
            }}
            return _responseService;
        }}
        #endregion

        #region SERVICIOS DELETE
        public async Task<IResponseService> Delete(dynamic id)
        {{
            try
            {{
                using var connection = context.CreateConnection();
                var param = new DynamicParameters();
                param.Add("@Id", id, DbType.Int32, ParameterDirection.Input, 10);
                dynamic resultado = await connection.ExecuteScalarAsync("dbo.{nombre_sp_delete}", param, commandType: CommandType.StoredProcedure);

                _responseService.EstablecerRespuestaLista(true, resultado);
            }}
            catch (Exception ex)
            {{
                _responseService.Error = ex.Message;
                _responseService.Estado = false;
            }}
            return _responseService;
        }}
        #endregion

    }}
}}
"""
    guardar_archivo(ubicacion, f"Service{nombre_clase}.cs", contenido)

def crear_servicio_Interfaces_csv2(ubicacion, nombre_clase,  nombre_modelo, nombre_api):
    """Crea un archivo .cs con la estructura de servicio proporcionada."""
    contenido = f"""
using {nombre_api}.Models;
using API.Library;

namespace {nombre_api}.Interfaces
{{
        public interface IService{nombre_clase}: IServiceBase<{nombre_clase}>
        {{
            
        }}
}}
"""
    guardar_archivo(ubicacion, f"IService{nombre_clase}.cs", contenido)

def crear_servicio_Interfaces_cs(ubicacion, nombre_clase,  nombre_modelo, nombre_api,alias):

    nombre_clase = "IService" + nombre_clase
    """Crea un archivo .cs con la estructura de servicio proporcionada."""
    contenido = f"""
using {alias}.Models;
using API.Library;

namespace {alias}.Interfaces
{{
     public interface {nombre_clase}<T> : IServiceBase<T>
    {{
            
    }}
}}
"""
    guardar_archivo(ubicacion, f"{nombre_clase}.cs", contenido)

def crear_servicio_Controller_cs(ubicacion, nombre_clase,  nombre_modelo, nombre_api,alias):

    nombre_controller =  nombre_clase + "Controller" 
    nombre_servicio = "IService" + nombre_clase
    
    """Crea un archivo .cs con la estructura de servicio proporcionada."""
    contenido = f"""

using {nombre_api}.Interfaces;
using {alias}.Models;
using Microsoft.AspNetCore.Authentication.JwtBearer;
using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;
using API.Library;
using {alias}.Services;    

namespace API.{alias}.Controllers
{{
    [Route("api/[controller]/[action]")]
    [ApiController]

    
    public class {nombre_controller}({nombre_servicio}<{nombre_clase}> service{nombre_clase}, IResponseService responseService) : Controller
{{
    private readonly IService{nombre_clase}<{nombre_clase}> _service = service{nombre_clase};
    private readonly IResponseService _responseService = responseService;

    #region SERVICIOS GET
    [HttpGet("{{id}}")]
    public async Task<ActionResult> Get(string id)
    {{
        var response = await _service.Get(id);
        if (response.Estado)
            return Ok(response.Resultado);

        return BadRequest(new {{ message = response.Error }});
    }}

    [HttpGet("{{id}}")]
    public async Task<ActionResult> GetList(string id)
    {{
        var response = await _service.GetList(idDiagnostico);
        if (response.Estado)
            return Ok(new {{ data = response.Resultado, totalItems = response.TotalItems }});

        return BadRequest(new {{ message = response.Error }});
    }}

    
    
    [HttpGet]
    public async Task<ActionResult> GetListAll()
    {{
        var response = await _service.GetListAll();
        if (response.Estado)
            return Ok(new {{ data = response.Resultado, totalItems = response.TotalItems }});

        return BadRequest(response.Error);
    }}

    #endregion

    #region SERVICIOS POST - PUT

    [HttpPost]
    public async Task<ActionResult> Add({nombre_clase} model)
    {{
        if (!ModelState.IsValid)
            return BadRequest(ModelState);

        
        var response = await _service.Add(model);
        if (response.Estado)
            return Ok(response.Resultado);

        return BadRequest(new {{ message = response.Error }});
    }}

    [HttpPut]
    public async Task<ActionResult> Edit({nombre_clase} model)
    {{
        var response = await _service.Edit(model.Id, model);
        if (response.Estado)
            return Ok(response.Resultado);

        return BadRequest(new {{ message = response.Error }});

    }}

    [HttpDelete]
    public async Task<ActionResult> Delete(long id)
    {{
        var response = await _service.Delete(id);
        if (response.Estado)
            return Ok(response.Resultado);

        return BadRequest(new {{ message = response.Error }});
    }}

    #endregion

}}
  
}}
"""
    guardar_archivo(ubicacion, f"{nombre_controller}.cs", contenido)