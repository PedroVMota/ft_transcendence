import os
import shutil

def delete_migration_folders(project_path):
    for root, dirs, files in os.walk(project_path):
        if 'migrations' in dirs:
            migration_path = os.path.join(root, 'migrations')
            # Remove all files and subdirectories within the migrations folder
            for file_name in os.listdir(migration_path):
                file_path = os.path.join(migration_path, file_name)
                try:
                    if os.path.isfile(file_path) or os.path.islink(file_path):
                        os.remove(file_path)
                    elif os.path.isdir(file_path):
                        shutil.rmtree(file_path)
                except Exception as e:
                    print(f"Failed to delete {file_path}. Reason: {e}")
            # Remove the migrations folder itself
            try:
                os.rmdir(migration_path)
                print(f"Deleted migration folder: {migration_path}")
            except OSError as e:
                print(f"Could not delete {migration_path}, {e}")

# Replace 'your_project_path' with the path to your Django project
your_project_path = './Django/Code'
delete_migration_folders(your_project_path)