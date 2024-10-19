import os
import shutil


def remove_all_in_directory(directory_path):
    # Check if the directory exists
    if os.path.exists(directory_path):
        # Loop through all files and directories in the given directory
        for filename in os.listdir(directory_path):
            file_path = os.path.join(directory_path, filename)

            # If it is a directory, remove it recursively
            if os.path.isdir(file_path):
                shutil.rmtree(file_path)
            # If it is a file, remove the file
            elif os.path.isfile(file_path):
                os.remove(file_path)
        print(f"All files and subdirectories removed from {directory_path}")
    else:
        print(f"The directory {directory_path} does not exist.")