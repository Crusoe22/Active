DELETE FROM [HUD_LGIM].[GIS].[PAYMENTEXTENSIONSTABLE_XYTABLETOPOINT]

--Creat PaymentExtensions 
--This is for the dashboards 

--Give OBJECTID a value
DECLARE @max_objectid INT;
SET @max_objectid = (SELECT MAX(OBJECTID) FROM [HUD_LGIM].[GIS].[PAYMENTEXTENSIONSTABLE_XYTABLETOPOINT]);

IF @max_objectid IS NULL
BEGIN
  SET @max_objectid = 0;
END


--Insert data into dbo.PAYMENTEXECUTIONS
INSERT INTO [HUD_LGIM].[GIS].[PAYMENTEXTENSIONSTABLE_XYTABLETOPOINT] (OBJECTID, Cycle_Code, Account_No, Name, Home_Phone, Business_Phone, 
	Address, Start_Date, Latitude, Longitude, current_balance, payment_date, total_payment, tendered_amt, owing_amt, debtor_no, overdue_balance, 
	latecharge_balance, occupant_code, interest_balance, arrange_amt, active_yn, change_amt, trans_date, system_date, balance)
SELECT
@max_objectid + ROW_NUMBER() OVER (ORDER BY da.cycle_, pa.account_no),
da.cycle_,
pa.account_no,
da.name,
da.home_phone,
da.business_phone,
CONCAT(CAST(da.serv_street_no AS VARCHAR(25)), ' ', CAST(da.serv_street_mod AS VARCHAR(25)), ' ', CAST(da.serv_street AS VARCHAR(25)),
' ', CAST(da.serv_unit AS VARCHAR(11)), ' ', CAST(da.serv_city AS VARCHAR(25)), ' ', CAST(da.serv_province AS VARCHAR(25)), ' ', CAST(da.serv_postal_zip AS VARCHAR(11))) AS full_address,
ap.start_date,
CAST(ws.Latitude AS FLOAT),
CAST(ws.Longitude AS FLOAT),
ap.current_balance,
wp.payment_date,
wp.total_payment,
ca.tendered_amt,
ca.owing_amt,
ca.debtor_no,
ap.overdue_balance,
ap.latecharge_balance,
ap.occupant_code,
ap.interest_balance,
pa.arrange_amt,
pa.active_yn,
ca.change_amt,
ca.trans_date,
ca.system_date,
ba.balance


-- ap.utility_type(char(1)), ap.start_date(datetime), ap.overdue_balance(decimal(12, 2)), ap.latecharge_balance(decimal(12, 2)), ap.occupant_code(smallint), ap.current_balance(decimal(12, 2)), ap.intrest_balance(decimal(12, 2)) 
-- pa.arrange_amt(decimal(10, 2)), pa.active_yn(char(1)), pa.occupant_code(smallint) 
-- da.occupant_code(smallint)
-- wp.occupant_code(smallint), wp.total_payment(decimal(11, 2))
-- ca.tendered_amt(decimal(12, 2)), ca.owing_amt(decimal(12, 2)), ca.change_amt(decimal(12,2)), ca.trans_date(datetime), ca.system_date(datetime) 

--Grab data from correct tables 

--Live Environment
--
/** FROM [192.168.3.10].[northstar_live].[harris_live].[pu_account_pay] ap 
FULL OUTER JOIN [192.168.3.10].[northstar_live].[harris_live].[pu_pay_arrangh] pa ON ap.account_no = pa.account_no 
FULL OUTER JOIN [192.168.3.10].[northstar_live].[harris_live].[pu_account] da ON ap.account_no = da.account_no
FULL OUTER JOIN [192.168.3.10].[northstar_live].[harris_live].[puaccbal] ba	ON ap.account_no = ba.account_no
FULL OUTER JOIN [192.168.3.10].[northstar_live].[harris_live].wbmkpaym wp ON ap.account_no = wp.account_no
FULL OUTER JOIN [192.168.3.10].[northstar_live].[harris_live].icpcashm ca ON da.debtor_no = ca.debtor_no
FULL OUTER JOIN [HUD_LGIM].[dbo].[WSERVICECONNECTION] ws**/

--Test Environment 
/**FROM [192.168.3.10].northstar_test.harris_test.pu_account_pay ap
FULL OUTER JOIN [192.168.3.10].northstar_test.harris_test.pu_pay_arrangh pa ON ap.account_no = pa.account_no
FULL OUTER JOIN [192.168.3.10].northstar_test.harris_test.pu_account da ON ap.account_no = da.account_no
FULL OUTER JOIN [192.168.3.10].northstar_test.harris_test.puaccbal ba ON ap.account_no = ba.account_no
FULL OUTER JOIN [192.168.3.10].northstar_test.harris_test.wbmkpaym wp ON ap.account_no = wp.account_no
FULL OUTER JOIN [192.168.3.10].northstar_test.harris_test.icpcashm ca ON da.debtor_no = ca.debtor_no
[HUD_Test].[dbo].[WSERVICECONNECTION] ws**/


FROM [192.168.3.10].northstar_test.harris_test.pu_account_pay ap
FULL OUTER JOIN [192.168.3.10].northstar_test.harris_test.pu_pay_arrangh pa ON ap.account_no = pa.account_no
FULL OUTER JOIN [192.168.3.10].northstar_test.harris_test.pu_account da ON ap.account_no = da.account_no
FULL OUTER JOIN [192.168.3.10].northstar_test.harris_test.puaccbal ba ON ap.account_no = ba.account_no
FULL OUTER JOIN [192.168.3.10].northstar_test.harris_test.wbmkpaym wp ON ap.account_no = wp.account_no
FULL OUTER JOIN [192.168.3.10].northstar_test.harris_test.icpcashm ca ON da.debtor_no = ca.debtor_no
FULL OUTER JOIN [HUD_Test].[dbo].[WSERVICECONNECTION] ws ON CAST(ap.account_no AS NVARCHAR(50)) = ws.ACCOUNTID --ACCOUNTID is stored as text so account_no had to be changed so the two values could be compaired 

WHERE pa.utility_type = 'W'
	AND pa.last_pay IS NULL
	--AND wp.payment_date = '2023-04-04 00:00:00' -- CAST(getdate() as DATE) OR CAST(payment_date as DATE) = CAST(getdate()-1 as DATE)  OR CAST(payment_date as DATE) = CAST(getdate()-2 as DATE) OR CAST(payment_date as DATE) = CAST(getdate()-3 as DATE) OR CAST(payment_date as DATE) = CAST(getdate()-4 as DATE);


-- OBJECTID, Cycle_Code, Account_No, Name, Home_Phone, Business_Phone, Address, Start_Date, Latitude, Longitude, current_balance, payment_date, total_payment, tendered_amt, owing_amt, debtor_no
-- Account_No, Address, Name, Home_Phone, Business_Phone, Cycle_Code
-- Delete all data that do not meet qulificaitons 
-- this deletes all duplicates from the field by only keeping the first one that was created (this is done by selecting the Mininum object ID) 
DELETE FROM [HUD_LGIM].[GIS].[PAYMENTEXTENSIONSTABLE_XYTABLETOPOINT]
WHERE OBJECTID not in(
		SELECT MIN(OBJECTID)
		FROM [HUD_LGIM].[GIS].[PAYMENT_EXTENSIONS_TABLE]
		GROUP BY Account_No, Address, Name, Home_Phone, Business_Phone, Cycle_Code)

DELETE FROM [HUD_LGIM].[GIS].[PAYMENTEXTENSIONSTABLE_XYTABLETOPOINT]
WHERE (account_no)AND (occupant_code) 
	NOT IN (
	SELECT account_no, MAX(occupant_code)
	FROM [HUD_LGIM].[GIS].[PAYMENTEXTENSIONSTABLE_XYTABLETOPOINT]
	GROUP BY account_no
);

DELETE FROM [HUD_LGIM].[GIS].[PAYMENTEXTENSIONSTABLE_XYTABLETOPOINT]
WHERE occupant_code not in(
		SELECT MIN(occupant_code)
		FROM [HUD_LGIM].[GIS].[PAYMENT_EXTENSIONS_TABLE]
		GROUP BY Account_No, Address, Name, Home_Phone, Business_Phone, Cycle_Code)