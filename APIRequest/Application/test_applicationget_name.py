import requests
import json
import pytest

# Load the configuration data
def load_config():
    with open('config.json', 'r') as config_file:
        return json.load(config_file)

# GET request function
def get_application_name(application_name):
    base_url = "https://localhost:7084"  # Replace with your base URL
    url = f"{base_url}/api/Application/name/{application_name}?cultureCode=en-US&api-version=1.0"
    response = requests.get(url, verify=False)  # Verify=False to ignore SSL certificate warnings
    return response

def test_get_application_name_status_code():
    config_data = load_config()

    # Extract application name from the config
    application_name = config_data["data_applicationpost"]["name"]

    # Call the GET request
    response = get_application_name(application_name)

    # Assertions for the application name request
    assert response.status_code == 200, f"Expected status code 200, but got {response.status_code}"

def test_get_application_name_response_body():
    config_data = load_config()

    # Extract application name from the config
    application_name = config_data["data_applicationpost"]["name"]

    # Call the GET request
    response = get_application_name(application_name)

    # Assertions for the response body name
    json_data = response.json()
    assert 'name' in json_data, "Response JSON does not contain 'name' field."
    assert json_data['name'] == application_name, f"Expected application name '{application_name}', but got '{json_data['name']}'"

def test_get_application_name_invalid_name():
    config_data = load_config()

    # Extract invalid application name from the config
    invalid_name = config_data.get("invalid_name")

    # Call the GET request with the invalid name
    response = get_application_name(invalid_name)

    # Assertions for the invalid application name request
    assert response.status_code == 404, f"Expected status code 404, but got {response.status_code}"

# Call the functions if running the script directly
if __name__ == "__main__":
    test_get_application_name_status_code()
    test_get_application_name_response_body()
    test_get_application_name_invalid_name()
