import arcpy
import time
import os
import shutil
import datetime

#Shapefile destination 
destination_path = r"\\arcgisserver\Backups"

# Get current timestamp
timestamp = time.strftime("%Y%m%d_%H%M%S")

# Initialize the delete_list
delete_list = []


def grab_files():
    #set workspace environment
    arcpy.env.workspace = r"\\portalserver\Production Projects\GISDBSERVER22.sde" 

    feature_ServiceConnections = r"\\portalserver\Production Projects\GISDBSERVER22.sde\HUD_LGIM.DBO.WaterDistribution\HUD_LGIM.DBO.wServiceConnection", 
    feature_Hydrant = r"\\portalserver\Production Projects\GISDBSERVER22.sde\HUD_LGIM.DBO.WaterDistribution\HUD_LGIM.DBO.wHydrant", 
    feature_SystemValve = r"\\portalserver\Production Projects\GISDBSERVER22.sde\HUD_LGIM.DBO.WaterDistribution\HUD_LGIM.DBO.wSystemValve", 
    feature_ControlValve = r"\\portalserver\Production Projects\GISDBSERVER22.sde\HUD_LGIM.DBO.WaterDistribution\HUD_LGIM.DBO.wControlValve",
    feature_Main = r"\\portalserver\Production Projects\GISDBSERVER22.sde\HUD_LGIM.DBO.WaterDistribution\HUD_LGIM.DBO.wMain"

    output_folder = os.path.join(destination_path, f"WaterDistribution_{timestamp}")
    os.mkdir(output_folder)

    # Convert feature class to shapefile with updated timestamp
    arcpy.conversion.FeatureClassToShapefile([feature_ServiceConnections, feature_Hydrant, feature_SystemValve,
                                            feature_ControlValve, feature_Main], output_folder)

def create_folder():
    # get the current time
    now = datetime.datetime.now()

    # Get the current date and time
    now = datetime.datetime.now()

    # Define the threshold for deleting files (7 days)
    threshold = datetime.timedelta(days=7)


    # Iterate over all the files in the directory
    for filename in os.listdir(destination_path):
        file_path = os.path.join(destination_path, filename)

        # Get the modification time of the file
        mod_time = datetime.datetime.fromtimestamp(os.path.getmtime(file_path))

        # Calculate the difference between the modification time and the current time
        delta = now - mod_time

        # Check if the file is older than the threshold correct way (delta > threshold)
        if delta > threshold:
            delete_list.append(file_path)
    # Print the list of files to be deleted
    print(delete_list)

def delete_old_folders():
    # Delete all the folders in the delete_list
    for folder in delete_list:
        if os.path.isdir(folder):
            shutil.rmtree(folder)
            print(f"{folder} has been deleted.")
        else:
            print(f"{folder} is not a folder and won't be deleted.")


grab_files()
create_folder()
delete_old_folders()