

def delete_gen_py_folder():
    import os
    import shutil   
    import subprocess 

    #folder_path = r"C:\Users\Admin\AppData\Local\Temp\gen_py"
    folder_path = r"C:\Users\jeffr\AppData\Local\Temp\gen_py"
    
    # Check if the folder exists
    if os.path.exists(folder_path):
        try:
            # Remove the folder and its contents
            shutil.rmtree(folder_path)
            print(f"Folder '{folder_path}' deleted successfully.")
        except PermissionError:
            print(f"Permission denied: Could not delete '{folder_path}'. Please check your permissions.")
        except FileNotFoundError:
            print(f"Folder '{folder_path}' not found during deletion.")
        except Exception as e:
            print(f"An error occurred while deleting the folder: {e}")
    else:
        print(f"Folder '{folder_path}' does not exist.")


    # Run the win32com makepy command for Excel.Application
    try:
        subprocess.run(["python", "-m", "win32com.client.makepy", "Excel.Application"], check=True)
        print("Command executed successfully: python -m win32com.client.makepy 'Excel.Application'")
    except subprocess.CalledProcessError as e:
        print(f"An error occurred while running the command: {e}")
    except FileNotFoundError:
        print("Python executable not found. Ensure Python is installed and available in the PATH.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")



