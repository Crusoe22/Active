# Facility ID find max
import arcpy
import pandas 

feature_class = r'C:\Users\Nolan\Documents\ArcGIS\ArcGIS Pro Projects\DateDelete\DateCleanUpDelete\GISDBSERVER22.sde\HUD_LGIM.DBO.WaterDistribution\HUD_LGIM.DBO.wServiceConnection'

# Get the current maximum value in the field
max_id = max([int(row[0]) for row in arcpy.da.SearchCursor(feature_class, "FACILITYID") if row[0] is not None and row[0].isdigit()])

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


# Set the path to the feature class that contains the field
fc_path = r'C:\Users\Nolan\Documents\ArcGIS\ArcGIS Pro Projects\DateDelete\DateCleanUpDelete\GISDBSERVER22.sde\HUD_LGIM.DBO.WaterDistribution\HUD_LGIM.DBO.wServiceConnection'

# Set the name of the field that contains the facility IDs
field_name = "FACILITYID"

# Create an update cursor to loop through the rows
with arcpy.da.UpdateCursor(fc_path, [field_name]) as cursor:
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