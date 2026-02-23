

def call_cpp_program(template_path, similarity_threshold, cpp_program):

    import subprocess
    import json
    
    command = [cpp_program, template_path, str(similarity_threshold)]

    try:
        # Run the subprocess and capture its output
        result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)

        # Process the output
        cpp_output = result.stdout.strip()

        # Check if the C++ program returned "not found"
        if cpp_output == "\"not found\"":
            #print("No matches found.")
            return False

        # Parse the output as a dictionary
        match_data = json.loads(cpp_output)

        return match_data

    except subprocess.CalledProcessError as e:
        print(f"Error: Subprocess exited with return code {e.returncode}")
        print(e.stderr)
        return None
    except FileNotFoundError:
        print(f"Error: Executable '{cpp_program}' not found.")
        return None
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON from C++ output: {e}")
        return None
    except Exception as e:
        print(f"Unexpected error: {e}")
        return None



def get_highest_key(data):
    """Finds the highest key in a dictionary of dictionaries."""
    # Convert keys to integers, find the maximum, and convert back to string
    highest_key = str(max(int(key) for key in data.keys()))
    return highest_key


def search_coordinate_text_on_screen(text, exe_path):
    import subprocess
    import json
    import os
    
    #exe_path = os.path.abspath(exefilepath)
    proc = subprocess.run([exe_path, text],
                          capture_output=True, text=True)
    if proc.returncode != 0:
        raise RuntimeError(f"OCR binary error: {proc.stderr.strip()}")
    out = proc.stdout.strip()
    if out.strip('"') == "not found":
        return False
    return json.loads(out)


def search_coordinate_text_on_screen_region_search(text, exe_path, x1, y1, x2, y2):
    """
    Run the OCR binary on the sub‑region [x1,y1]–[x2,y2] of the screen
    and return the parsed JSON if found, or False otherwise.
    """
    import subprocess, json, os

    # Ensure all coords are strings
    coords = [str(x1), str(y1), str(x2), str(y2)]
    # Build the command: <exe> "<text>" x1 y1 x2 y2
    proc = subprocess.run(
        [exe_path, text] + coords,
        capture_output=True, text=True
    )
    if proc.returncode != 0:
        raise RuntimeError(f"OCR binary error: {proc.stderr.strip()}")
    out = proc.stdout.strip()
    if out.strip('"') == "not found":
        return False
    return json.loads(out)


