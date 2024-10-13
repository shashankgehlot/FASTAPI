import os

def print_tree(startpath, level=0, skip_folders=None):
    if skip_folders is None:
        skip_folders = []

    # Print the current directory name
    print('    ' * level + os.path.basename(startpath) + '/')
    
    # List all files and directories in the current directory
    try:
        for item in os.listdir(startpath):
            item_path = os.path.join(startpath, item)
            if os.path.isdir(item_path):
                # Skip the specified folders
                if item in skip_folders:
                    continue
                # Recursively print the directory tree
                print_tree(item_path, level + 1, skip_folders)
            else:
                # Print the file name
                print('    ' * (level + 1) + item)
    except PermissionError:
        print('    ' * level + '[Permission Denied]')

if __name__ == "__main__":
    # Specify the directory you want to display
    project_dir = '.'  # Change this to your project directory if needed
    skip_folders = ['venv','__pycache__','.git']  # List of folders to skip
    print_tree(project_dir, skip_folders=skip_folders)