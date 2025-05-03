
-- =============================================
-- Author:        Henry Agudelo
-- Create date: 2025-01-25
-- Description: Inserta un nuevo registro en la tabla 'gdfsgdfsg'
-- =============================================

CREATE PROCEDURE CT_SpaGeneral 
    @d INT, @df INT
AS
BEGIN
    INSERT INTO gdfsgdfsg (d, df) 
    VALUES (@d, @df)
END
    