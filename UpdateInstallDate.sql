-- Create file to update install date 

/* Write SQL code that updates a column called INSTALLDATE in the table called WSERVICECONNECTIONS. This code needs to pull the information from the table
CityworksDev.azteca.WORKORDER column ACTUALFINISHDATE. These tables are going to be joined on the columns ACCOUNTID. */

--Service Connection
[HUD_LGIM].[dbo].[WSERVICECONNECTION]
[HUD_Test].[dbo].[WSERVICECONNECTION]

--Water Main
[HUD_LGIM].[dbo].[WMAIN]
[HUD_Test].[dbo].[WMAIN]

--WORKORDER
[CityworksDev].[azteca].[WORKORDER]
[CityworksProd].[azteca].[WORKORDER]



--final code 

--Create temporary table 
CREATE TABLE #Temp_Table4 (
TEXT8 nvarchar(100),
ACTUALFINISHDATE datetime

)

Select *
FROM #Temp_Table4

-- Only grab the data for the New Meter Installs 
INSERT INTO #Temp_Table4 (TEXT8, ACTUALFINISHDATE)
SELECT LEFT(TEXT8, 8), ACTUALFINISHDATE
FROM [CityworksDev].[azteca].[WORKORDER]
WHERE DESCRIPTION = 'New meter installation' --'Install New Main' or 'New meter installation'



--Update the column INSTALLDATE in WSERVICECONNECTION
UPDATE [HUD_Test].[dbo].[WSERVICECONNECTION]
SET INSTALLDATE = temp.ACTUALFINISHDATE
FROM [HUD_Test].[dbo].[WSERVICECONNECTION] AS wsc
JOIN #temp_table4 AS temp ON wsc.ACCOUNTID = temp.TEXT8


--Select Data from WSERVICECONNECTIONS
Select *
FROM [HUD_Test].[dbo].[WSERVICECONNECTION]


-- Delete all data from temporary table 
DELETE FROM #Temp_Table4
