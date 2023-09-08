#This file connects points into a line
# It takes the first entered row as the start and proceeds from there
# To change order copy rows inorder necessary to create the correct line
# This line imports the arcpy module, which is the ArcPy library used for interacting with ArcGIS functionality in Python

import arcpy

# This line sets the workspace to the path of your geodatabase
arcpy.env.workspace = r"C:\Users\Nolan\Documents\ArcGIS\Test_Environment\Test_Environment.gdb"
# This line assigns the name of the feature class you want to process to the feature_class variable.
feature_class = "Edge_of_Pavement2"

# Create a list to store the points
# This line creates an empty list called point_list to store the point objects extracted from the feature class
point_list = []


# These lines read the feature class using a search cursor (arcpy.da.SearchCursor) and iterate through each row.
# The "SHAPE@XY" field token in the cursor indicates that we want to retrieve the x and y coordinates of each point.
# The x and y variables store the extracted coordinates, and a new arcpy.Point object is created with those coordinates. 
# The point object is then appended to the point_list.

# Read the feature class and iterate through the points
with arcpy.da.SearchCursor(feature_class, ["SHAPE@XY"]) as cursor:
    for row in cursor:
        # Extract the x and y coordinates
        x, y = row[0]
        
        # Create a point object and append it to the list      
        point = arcpy.Point(x, y)
        point_list.append(point)


#This line constructs a Polyline object (arcpy.Polyline) using the list of point objects stored in point_list.
# The arcpy.Array function is used to convert the list of points into an array that can be passed to the Polyline constructor.
# Create a Polyline object from the points
polyline = arcpy.Polyline(arcpy.Array(point_list))

# This line sets the path for the output feature class where the line feature will be saved. 
output_fc = r"C:\Users\Nolan\Documents\ArcGIS\Test_Environment\Test_Environment.gdb\Edge_Of_Pavement_Lines"


#These lines use an insert cursor (arcpy.da.InsertCursor) to insert the created polyline feature into the output feature class. 
# The "SHAPE@" field token indicates that the geometry will be inserted. The insertRow method is used to insert a new row into the feature class, 
# passing the polyline as the value for the geometry field.

# Create the feature class and insert the line feature
with arcpy.da.InsertCursor(output_fc, ["SHAPE@"]) as cursor:
    cursor.insertRow([polyline])

# Print the path to the output feature class
print("Line feature class created at:", output_fc)

# Make sure to modify the necessary parts of the code, such as the geodatabase path,
# feature class name, and output feature class path, to match your specific scenario.