import requests
import json
import pytest

# Define the base URL
base_url = "https://localhost:7084"

# Read the configuration file
with open('config.json', 'r') as file:
    config = json.load(file)

# Get the "idv", "nonexisting_id", and "invalid_id" values from the configuration file
idv_value = config['idv']
nonexisting_id = config['nonexisting_id']
invalid_id = config['invalid_id']

# Define the function to send a GET request
def get_request(application_version_id):
    url = f"{base_url}/api/ApplicationVersion/{application_version_id}?api-version=1.0"
    print("GET URL: " + url)

    # Send the GET request
    response = requests.get(url, verify=False)  # verify=False to ignore SSL certificate warnings

    # Print the response status code
    print(f"Response status code: {response.status_code}")

    # Try to print the response body as formatted JSON, if it's valid JSON
    try:
        response_data = response.json()
        print("Response body: " + json.dumps(response_data, indent=4))
    except json.JSONDecodeError:
        response_data = response.text
        print("Response body is not in JSON format: " + response_data)

    return response, response_data

# Function to save response data to config.json
def save_response_to_config(response_data, key):
    config[key] = response_data
    with open('config.json', 'w') as file:
        json.dump(config, file, indent=4)
    print(f"Response data saved to config.json under key '{key}'")

# Test function for valid idv
def test_get_request_valid_idv():
    print("==== Testing valid idv ====")
    # Call the get_request function
    response, response_data = get_request(idv_value)

    # Save the response data to config.json
    save_response_to_config(response_data, 'appvgetid')

    # Assert that the response status code is 200
    assert response.status_code == 200, f"Expected status code 200, but got {response.status_code}"
    print("Assertion passed: Status code is 200")

    # Assert that the idv matches the id in the response body
    assert response_data.get("id") == idv_value, f"Expected id {idv_value}, but got {response_data.get('id')}"
    print("Assertion passed: idv matches the id in the response body")
    print("==== End of test for valid idv ====")

# Test function for nonexisting_id
def test_get_request_nonexisting_id():
    print("==== Testing nonexisting_id ====")
    # Call the get_request function
    response, response_data = get_request(nonexisting_id)

    # Assert that the response status code is 404
    assert response.status_code == 404, f"Expected status code 404, but got {response.status_code}"
    print("Assertion passed: Status code is 404 for nonexisting_id")
    print("==== End of test for nonexisting_id ====")

# Test function for invalid_id
def test_get_request_invalid_id():
    print("==== Testing invalid_id ====")
    # Call the get_request function
    response, response_data = get_request(invalid_id)

    # Assert that the response status code is 404
    assert response.status_code == 404, f"Expected status code 404, but got {response.status_code}"
    print("Assertion passed: Status code is 404 for invalid_id")
    print("==== End of test for invalid_id ====")

# Run the tests with pytest
if __name__ == "__main__":
    pytest.main()
