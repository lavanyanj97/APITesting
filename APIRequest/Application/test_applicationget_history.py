import requests
import json
import pytest

# Load the configuration data
def load_config():
    with open('config.json', 'r') as config_file:
        return json.load(config_file)

# GET request function
def get_history(valid_id, startdate, enddate):
    base_url = "https://localhost:7084"  # Replace with your base URL
    url = f"{base_url}/api/Application/History/{valid_id}?cultureCode=en-US&dateFrom={startdate}&dateTo={enddate}&api-version=1.0"
    response = requests.get(url, verify=False)  # Verify=False to ignore SSL certificate warnings
    return response

def test_get_application_history():
    config_data = load_config()

    # Extract necessary fields from the config
    valid_id = config_data.get("valid_id")
    startdate = config_data.get("startdate")  # Make sure to add this to your config
    enddate = config_data.get("enddate")      # Make sure to add this to your config

    # Call the GET request with a valid ID
    response = get_history(valid_id, startdate, enddate)

    # Assertions for valid ID
    assert response.status_code == 200, f"Expected status code 200, but got {response.status_code}"
    json_data = response.json()

    # Optionally print the response body or error message
    #print("Valid ID response body:", json.dumps(json_data, indent=4))

def test_get_application_history_with_nonexisting_id():
    config_data = load_config()

    # Extract necessary fields from the config
    nonexisting_id = config_data.get("nonexisting_id")
    startdate = config_data.get("startdate")  # Make sure to add this to your config
    enddate = config_data.get("enddate")      # Make sure to add this to your config

    # Call the GET request with a non-existing ID
    response = get_history(nonexisting_id, startdate, enddate)

    # Assertions for non-existing ID
    assert response.status_code == 404, f"Expected status code 404, but got {response.status_code}"

    # Only attempt to decode JSON if the status code is 200
    if response.status_code == 200:
        json_data = response.json()
        print("Response body:", json.dumps(json_data, indent=4))
    else:
        print("Non-existing ID response has no JSON body.")

# Call the function if running the script directly
if __name__ == "__main__":
    test_get_application_history()
    test_get_application_history_with_nonexisting_id()
