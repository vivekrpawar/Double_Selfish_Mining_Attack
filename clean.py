import os

def delete_files_in_folder(folder_path):
    # Iterate over all files in the folder
    for file_name in os.listdir(folder_path):
        # Construct the full path to the file
        file_path = os.path.join(folder_path, file_name)
        try:
            # Check if the path points to a file
            if os.path.isfile(file_path):
                # Delete the file
                os.remove(file_path)
                print(f"Deleted file: {file_path}")
        except Exception as e:
            print(f"Error deleting {file_path}: {e}")

def delete_specific_file(file_path):
    try:
        # Check if the path points to a file
        if os.path.isfile(file_path):
            # Delete the file
            os.remove(file_path)
            print(f"Deleted file: {file_path}")
    except Exception as e:
        print(f"Error deleting {file_path}: {e}")

# Example usage:

# Delete all files from a particular folder 
delete_files_in_folder("./node_files")
delete_files_in_folder("./blockchain_tree_csv")

# Delete a specific file
file_path = "miner_mappings.csv"
delete_specific_file(file_path)
