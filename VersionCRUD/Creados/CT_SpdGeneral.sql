
-- =============================================
-- Author:        Henry Agudelo
-- Create date: 2025-01-25
-- Description: Elimina un registro de la tabla 'gdfsgdfsg' por su ID
-- =============================================

CREATE PROCEDURE CT_SpdGeneral 
    @id INT
AS
BEGIN
    DELETE FROM gdfsgdfsg WHERE id = @id
END
    