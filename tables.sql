USE MyDatabase;
GO
CREATE TABLE Tables (
    Name NVARCHAR(255) PRIMARY KEY,
    DESCRIPTION NVARCHAR(255),
    Not_Applicable Bit,
    Empty Bit,
    Reviewed Date
)

ALTER TABLE Tables
add Is_View Bit

Alter Table Tables
add Not_In_Reference Bit
------------------------------------------------------------------------------------
CREATE TABLE Variables (
    Name NVARCHAR(255) PRIMARY KEY,
    TableName NVARCHAR(255) references Tables(Name),
    Description NVARCHAR(255),
    DataType NVARCHAR(20)
)

Alter table Variables
add Reviewed Date

Alter Table Variables
add Reference_To Nvarchar(255) references Variables(Name)

Alter Table Variables
add Primary_Key Bit

Alter Table Variables
add Not_In_Reference Bit
--------------------------------------------------------------------------------------------------
CREATE TABLE Person (
    Name NVARCHAR(50) PRIMARY KEY,
    Department NVARCHAR(50)
)
---------------------------------------------------------------------------------------------------
CREATE TABLE Request (
    ID Int primary key,
    Person nvarchar(50) references Person(Name),
    Description nvarchar(255),
    Start_Date Date,
    End_Date Date
)
---------------------------------------------------------------------------------------------------
CREATE TABLE Request_Variables (
    Request_ID int references Request(ID),
    VarName nvarchar(255) references Variables(Name),
)

--------------------------------------------------------------------------------------------------

CREATE TABLE IPEDS_Tables (
    Name NVARCHAR(255) PRIMARY KEY,
    DESCRIPTION NVARCHAR(255),
    Reviewed Date
)

Alter Table IPEDS_Tables
add SurveyNumber Int references IPEDS_Surveys(ID)

Alter Table IPEDS_Tables
add YearType nvarchar(50)

Alter Table IPEDS_Tables
add AY_Start nvarchar(50)

----------------------------------------------------------------------------------------

CREATE TABLE IPEDS_Surveys (
    ID Int primary key,
    Name nvarchar(50)
)

CREATE TABLE IPEDS_Variables (
    Name nvarchar(50) primary key,
    TableName nvarchar(255) references IPEDS_Tables(Name),
    DESCRIPTION nvarchar(255),
    DataType nvarchar(20),
    YearType nvarchar(50),
    FallsPrior int,
    Reviewed Date
)




