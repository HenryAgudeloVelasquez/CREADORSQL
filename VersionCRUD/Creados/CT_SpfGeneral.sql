
-- =============================================
-- Author:        Henry Agudelo
-- Create date: 2025-01-25
-- Description: Obtiene un registro de la tabla 'gdfsgdfsg' por su ID
-- =============================================

CREATE PROCEDURE CT_SpfGeneral 
    @id INT
AS
BEGIN
    SELECT * FROM gdfsgdfsg WHERE id = @id
END
    