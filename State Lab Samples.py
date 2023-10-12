#State Lab Samples 

import arcpy

#Feature class location 
#import data from \\portalserver\Production Projects\GISDBSERVER22.sde\HUD_LGIM.DBO.State_Lab_Samples 
fc = r'\\portalserver\Production Projects\GISDBSERVER22.sde\HUD_LGIM.DBO.State_Lab_Samples' 


def cleardata(): #Clear data from State Lab Samples 
    # Create a list of field names to clear
    fields_to_clear = [ 'SAMPLE_NUMBER', 'SAMPLE_DATE',  'SAMPLE_TIME', 'SAMPLE_FIXTURE', 'EMPLOYEE', 'SAMPLE_TYPE',
                        'TESTED', 'LOCATION_COMMENTS','DATE_REC_LAB', 'TIME_REC_LAB', 'REC_LAB_BY', 'ANALYSIS_DATE',
                          'ANALYSIS_TIME', 'ANALYST', 'TOTAL_COLIFORM_RESULTS' ] 
      
    # Use an update cursor to clear data from the specified fields
    with arcpy.da.UpdateCursor(fc, fields_to_clear) as cursor:
        for row in cursor:
            for i in range(len(fields_to_clear)): #range increments by 1 and stops at specified number. len returns number of items in a list 
                row[i] = None  # Clear data in the field
            cursor.updateRow(row)


cleardata()
