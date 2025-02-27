CREATE VIEW Request_Variable_Count AS
    SELECT VarName,
           Count(*) as Total_Uses
    FROM Request_Variables
    GROUP BY VarName


CREATE VIEW Review_Count AS
    SELECT Reviewed as Review_Date,
           Count(*) as Total_Reviewed
    FROM TABLES
    GROUP BY Reviewed


CREATE VIEW Table_Relevance AS
    SELECT Name,
             CASE
                 When Reviewed is NULL Then 'Not_Reviewed_Yet'
                 When Empty = 1 or Not_Applicable = 1 Then 'Not_Relevant'
                 Else 'Possibly_Relevant'
                 END AS Relevance_Status,
            CASE WHEN DESCRIPTION IS NULL THEN 0 ELSE 1 END AS Filled_Table_Description,
            CASE
                WHEN
                    EXISTS (
                        SELECT 1
                        FROM Variables
                        JOIN Tables as Inner_Tables on Variables.TableName = Inner_Tables.Name
                        Where Inner_Tables.Name = Outer_Tables.Name
                        and  Variables.Description is NULL
                    ) Then 0 Else 1 END As Filled_All_Variable_Descriptions,
            CASE
                WHEN
                    Exists (
                        Select 1
                        From Request_Variables
                        Join Variables On Request_Variables.VarName = Variables.Name
                        Join Tables as Inner_Tables On Variables.TableName = Inner_Tables.Name
                        Where Inner_Tables.Name = Outer_Tables.Name
                    ) Then 1 Else 0
            END AS Used
          FROM TABLES as Outer_Tables

CREATE VIEW Filled_Descriptions as
    SELECT Name,
           CASE WHEN DESCRIPTION IS NULL THEN 0 ELSE 1 END AS Filled_Table_Description,
           CASE
                WHEN
                    EXISTS (
                        SELECT 1
                        FROM Variables
                        JOIN Tables as Inner_Tables on Variables.TableName = Inner_Tables.Name
                        Where Inner_Tables.Name = Outer_Tables.Name
                        and  Variables.Description is NULL
                    ) Then 0 Else 1 END As Filled_All_Variable_Descriptions
    FROM Tables as Outer_Tables
    where Empty = 0 and Not_applicable = 0


CREATE VIEW Table_Relevance_Count AS
    SELECT Relevance,
           Count(*) AS Relevance_Count
    FROM (SELECT Name,
                 CASE
                     When Reviewed is NULL Then 'Not_Reviewed_Yet'
                     When Empty = 1 or Not_Applicable = 1 Then 'Not_Relevant'
                     Else 'Possibly_Relevant'
                     END AS Relevance
          FROM TABLES) as X
    GROUP BY Relevance
