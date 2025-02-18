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

CREATE TABLE Variables (
    Name NVARCHAR(255) PRIMARY KEY,
    Title NVARCHAR(255),
    TableName NVARCHAR(255) references Tables(Name),
    Description NVARCHAR(255),
    DataType NVARCHAR(20)
)


CREATE VIEW Review_Count AS
    SELECT Reviewed as Review_Date,
           Count(*) as Total_Reviewed
    FROM TABLES
    GROUP BY Reviewed

CREATE TABLE Person (
    Name NVARCHAR(50) PRIMARY KEY,
    Department NVARCHAR(50)
)

CREATE TABLE Request (
    ID Int primary key,
    Person nvarchar(50) references Person(Name),
    Description nvarchar(255),
    Start_Date Date,
    End_Date Date
)

CREATE TABLE Request_Variables (
    Request_ID int references Request(ID),
    VarName nvarchar(255) references Variables(Name),
    For_Select Bit,
    For_Join Bit,
    For_Where Bit,
    For_GroupBy Bit,
    For_OrderBy Bit
)

CREATE VIEW Request_Variable_Count AS
    SELECT VarName,
           Count(*) as Total_Uses
    FROM Request_Variables
    GROUP BY VarName



