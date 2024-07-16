import os
import shutil

# Define the directory to remove
def delete_directory(persist_dir):
    try:
        # Check if the directory exists
        if os.path.exists(persist_dir):
        # Remove the directory and its contents
            shutil.rmtree(persist_dir)
            print(f"Removed directory: {persist_dir}")
        else:
            print(f"Directory does not exist: {persist_dir}")
    except Exception as e:
        print(f"Error removing directory: {e}")
