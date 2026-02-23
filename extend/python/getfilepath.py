
############################################################################
# getfilepath.py
############################################################################

def read_file_paths(file_path):
    import pandas as pd
    import string
    import math
    from datetime import datetime
    
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            paths = file.readlines()
            # Strip whitespace (like newlines) from each line
            paths = [path.strip() for path in paths]
        return paths
    except FileNotFoundError:
        print(f"The file {file_path} does not exist.")
        return []
    except UnicodeDecodeError:
        print(f"Could not decode the file {file_path} due to an encoding error.")
        return []
    

    