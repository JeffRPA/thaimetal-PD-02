
###########################################################################
#pythonAPI.py
###########################################################################

def send_api_data(url, resultlistofarrays_allstring):

    import requests
    import json    
    
    """
    Sends API data to a specified URL.

    :param url: Target URL for the API endpoint.
    :param resultlistofarrays_allstring: List of arrays containing string data to send.
    :return: Response object or error message.
    """
    payload = {"data": resultlistofarrays_allstring}
    headers = {"Content-Type": "application/json"}

    try:
        # Send POST request
        response = requests.post(url, data=json.dumps(payload), headers=headers)

        # Check response
        if response.status_code == 200:
            print("Data sent successfully!")
            return response.json()  # Return the JSON response
        else:
            print(f"Failed to send data. Status code: {response.status_code}")
            return response.text  # Return the response text for debugging
    except Exception as e:
        print("An error occurred:", e)
        return str(e)  # Return the error message as a string

