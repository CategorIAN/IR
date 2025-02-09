USE MyDatabase;
GO
CREATE TABLE Tables (
    Name NVARCHAR(255) PRIMARY KEY,
    DESCRIPTION NVARCHAR(255),
    Not_Applicable Bit,
    Empty Bit,
    Used Bit,
    Reviewed Date
)
