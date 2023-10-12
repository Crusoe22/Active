#This code takes all files from the file walarchive moves it to PortalBackup
#Then deletes all files in PortalBackup once they have been in there for over a week

# Move and Delete
# importing required modules 
import os
import shutil
import time 
#import sys

# Update user on how to use the code
print ("This is a Python script that will grab all files from the folder walarchive and move them to PortalBackup. This will also delete all files in PortalBack up that have been there longer than 7 days.")
print ()
print ("Press the X button in the top right to close the window and not run the Python script.")
print ()
input("Press Enter to continue...")
print()
print("This may take a few minutes.")
print()

# Set path (locations)
src_dir = r"\\portalserver\walarchive" # change for \\portalserver\walarchive C:\Users\Nolan\Documents\Python test folder
dst_dir = r"\\portalserver\PortalBackup" # change for  C:\Users\Nolan\Documents\Python test folder2

# Set number of days to wait before deleting files

def delete_old_files(dir_path, days = 7):
    #Deletes all files in the given directory that are older than `days` days.
    # 86400 is the number of seconds in a day
    # time() requires the time to be entered in seconds 
    time_cutoff = time.time() - (days * 86400)
    for f in os.listdir(dir_path):
        file_path = os.path.join(dir_path, f)
        if os.path.isfile(file_path) and os.stat(file_path).st_mtime < time_cutoff:
            # remove all files in folder
            os.remove(file_path)


# Get a list of all files in the source directory. os returns a list of all files in the source directory
files = os.listdir(src_dir)

# Iterate over each file and move it to the destination directory. 
# f acts as a variable that we use to refer to each file name in the files list as we iterate over it
for f in files:
    src_path = os.path.join(src_dir, f) #This allows the join of various path components
    dst_path = os.path.join(dst_dir, f)
    shutil.move(src_path, dst_path)

# Delete old files in destination directory
delete_old_files(dst_dir, days=7)


print("-----------------------------------")
print("All files have been moved and/or deleted!")
print()
input("Press Enter to close window.")