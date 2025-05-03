
-- =============================================
-- Author:        Henry Agudelo
-- Create date: 2025-01-25
-- Description: Actualiza un registro de la tabla 'gdfsgdfsg'
-- =============================================

CREATE PROCEDURE CT_SpsGeneral 
    @id INT,
    @d INT, @df INT
AS
BEGIN
    UPDATE gdfsgdfsg 
    SET d = @d, df = @df 
    WHERE id = @id
END
    