
###########################################################################
#convertalltostring.py
###########################################################################

def convert_all_to_strings(data):
    """
    Converts all elements in a list of arrays to strings.
    
    Args:
        data (list of list/array): A list containing arrays or nested lists.
        
    Returns:
        list of list: A list of arrays or lists with all elements as strings.
    """
    return [[str(item) for item in array] for array in data]

