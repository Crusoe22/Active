import arcpy 
import pandas 

# Set the workspace environment
feature_class = r"C:\Users\Nolan\Documents\ArcGIS\ArcGIS Pro Projects\DateDelete\DateCleanUpDelete\GISDBSERVER22.sde\HUD_LGIM.DBO.GPSFeatures\HUD_LGIM.DBO.GPSMeters" 
field_to_update1 = 'ASSETID'
field_to_update2 = 'SIZE'
matching_field1 = 'GISACCOUNT'


def update_assetID():
    # Set the path to the Excel workbook
    excel_file_path = r'C:\Users\Nolan\Documents\ExcelSheets\GPSMetersExcel.xlsx'

    # Read Excel workbook into a Pandas DataFrame
    excel_data = pandas.read_excel(excel_file_path)

    # Iterate through each row in the DataFrame
    for row in excel_data.iterrows():
        # Get the GIS account number from the current row
        gis_account_number = row[matching_field1]

        # Use a cursor to update the feature class based on the GIS account number
        with arcpy.da.UpdateCursor(feature_class, [matching_field1, field_to_update1]) as cursor:
            for feature_row in cursor:
                # Check if the GIS account numbers match
                if feature_row[0] == gis_account_number:
                    # Update the assetid field with the corresponding value from the Excel workbook
                    feature_row[1] = row['ASSETID']

                    # Update the row in the feature class
                    cursor.updateRow(feature_row)

    # Print a message indicating the update is complete
    print("Update complete. AssetID")

def SizefromExcel():
    # Set the path to the Excel workbook
    excel_file_path1 = r'C:\Users\Nolan\Documents\ExcelSheets\GPSMetersExcel.xlsx'

    # Read Excel workbook into a Pandas DataFrame
    excel_data = pandas.read_excel(excel_file_path1)

    # Iterate through each row in the DataFrame
    for index, row in excel_data.iterrows():
        # Get the GIS account number from the current row
        gis_account_number = row[matching_field1]

        # Use a cursor to update the feature class based on the GIS account number
        with arcpy.da.UpdateCursor(feature_class, [matching_field1, field_to_update2]) as cursor:
            for feature_row in cursor:
                # Check if the GIS account numbers match
                if feature_row[0] == gis_account_number:
                    # Update the assetid field with the corresponding value from the Excel workbook
                    feature_row[1] = row['SIZE']

                    # Update the row in the feature class
                    cursor.updateRow(feature_row)

    # Print a message indicating the update is complete
    print("Update complete. Size")

def update_meterSize():
    
    with arcpy.da.UpdateCursor(feature_class, ["METER_SIZE", "SIZE"]) as cursor:
        for row in cursor:
            if row[1] == '0.625':
                row[0] = '5/8"'
            elif row[1] == '.625':
                row[0] = '5/8"'
            elif row[1] == '1':
                row[0] = "1"
            elif row[1] == '2':
                row[0] = "2"
            elif row[1] == '6':
                row[0] = "6"
            elif row[1] == '8':
                row[0] = "8"
            elif row[1] == 'L0.625':
                row[0] = 'L5/8'
            elif row[1] == 'L.625':
                row[0] = 'L5/8'
            elif row[1] == 'L1':
                row[0] = "L1"
            elif row[1] == 'L2':
                row[0] = "L2"
            elif row[1] == 'L6':
                row[0] = "L6"
            elif row[1] == 'L8':
                row[0] = "L8"
            cursor.updateRow(row)
    print('Update complete. Size to Meter Size')

def update_serviceType():
    # Update "Service Type" based on "meter size"
    with arcpy.da.UpdateCursor(feature_class, ["SERVICETYPE", "SIZE"]) as cursor:
        for row in cursor:
                if row[1] == '0.625' or 'L0.625':
                    row[0] = "Residential"
                elif row[1] == '1' or '2' or '6' or '8':
                    row[0] = "Commercial"
                elif row[1] is None:
                    row[0] = "Empty" #This might cause an error 
                cursor.updateRow(row)

def update_editor():
    # Update "Last Editor" and "Last Update Field"
    with arcpy.da.UpdateCursor(feature_class, ["LASTEDITOR", "LASTUPDATE"]) as cursor:
        for row in cursor:
            if row[0] is None:
                row[0] = "Nolan Moss"
            elif row[1] is None:
                row[1] = pandas.to_datetime('today').strftime('%m/%d/%Y')
            cursor.updateRow(row)
    print('Updated editor and date')

def update_fixed():
    # Fixed
    with arcpy.da.UpdateCursor(feature_class, ["ACCURACY"]) as cursor:
        for row in cursor:
            if row[0] is None:
                row[0] = "Fixed"
            cursor.updateRow(row)
    print('Update Accuracy')

def update_accountNum():
    # ACCOUNTID GISACCOUNT
    with arcpy.da.UpdateCursor(feature_class, ['GISACCOUNT', 'ACCOUNTID']) as cursor:
        for row in cursor:
            row[1] = row[0]
            cursor.updateRow(row)
    print('Update Account Number')

def update_location():
    
    # Calculate geometry attributes Lat and Long
    arcpy.management.CalculateGeometryAttributes(feature_class, [["Latitude", "POINT_Y"], ["Longitude", "POINT_X"]], "", "", "", "DD")

    # Calculate geometry attributes Northing and Easting
    arcpy.management.CalculateGeometryAttributes(feature_class, [["NORTHING", "POINT_Y"], ["EASTING", "POINT_X"]], "", "", "", "SAME_AS_INPUT")

    #Calculate Z-value
    arcpy.management.CalculateGeometryAttributes(feature_class, [["ELEVATION", "POINT_Z"]], "", "", "", "")

    #convert meters to feet
    with arcpy.da.UpdateCursor(feature_class, ["ELEVATION"]) as cursor:
        for row in cursor:    
            elevation_in_meters = row[0] # Extract the elevation value from the tuple
            elevation_in_feet = elevation_in_meters * 3.280839895 # Convert elevation to feet
            row[0] = elevation_in_feet # Update the feature with the new elevation value
            cursor.updateRow(row) # Update the row in the feature class


    print("Update completed successfully!")

def update_empty():
    # ACCOUNTID Notes
    with arcpy.da.UpdateCursor(feature_class, ['ACCOUNTID', 'Notes']) as cursor:
        for row in cursor:
            if row[1] == 'Empty':
                row[0] = 'Empty'
            elif row[1] == 'empty':
                row[0] = 'Empty'
            cursor.updateRow(row)
    print('Update Empty')

def update_facilityID():
    feature_class_maxID = r'C:\Users\Nolan\Documents\ArcGIS\ArcGIS Pro Projects\DateDelete\DateCleanUpDelete\GISDBSERVER22.sde\HUD_LGIM.DBO.WaterDistribution\HUD_LGIM.DBO.wServiceConnection'

    # Get the current maximum value in the field
    max_id = max([int(row[0]) for row in arcpy.da.SearchCursor(feature_class_maxID, "FACILITYID") if row[0] is not None and row[0].isdigit()])

    print('Current Max ID')
    print(max_id)

    # Add 1 to the maximum value if there are any empty or non-numeric values in the field
    with arcpy.da.UpdateCursor(feature_class, "FACILITYID") as cursor:
        for i, row in enumerate(cursor):
            if row[0] is None or not row[0].isdigit():
                row[0] = str(max_id + 1)
                cursor.updateRow(row)
                max_id += 1
            elif row[0] == '0':
                row[0] = str(max_id + 1)
                cursor.updateRow(row)
                max_id += 1
            else:
                pass  # do nothing

    print("Field 'FACILITYID' has been updated.")
    print(max_id)

    # Create an update cursor to loop through the rows
    with arcpy.da.UpdateCursor(feature_class, ["FACILITYID"]) as cursor:
        for row in cursor:
            # Check if the value is None or an empty string
            if row[0] is None or row[0] == "":
                continue
            
            # Convert the value to an integer
            try:
                value = int(row[0])
            except ValueError:
                # Skip over rows where the value is not an integer
                continue
            
            # Check if the value is greater than 89990012
            if value > 999999:
                # Set the value to 0
                value = '0'
            
            # Convert the value back to text
            row[0] = str(value)
            cursor.updateRow(row)


update_assetID()
SizefromExcel()
update_meterSize()
update_serviceType()
update_editor()
update_fixed()
update_accountNum()
update_location()
update_empty()
update_facilityID()




