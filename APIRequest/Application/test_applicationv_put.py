import requests
import json
import pytest
import random
import string

# Define the base URL
base_url = "https://localhost:7084"

# Read the configuration file
with open('config.json', 'r') as file:
    config = json.load(file)

# Get the "appvgetid", "nonexisting_id", and "invalid_id" values from the configuration file
appvgetid = config['appvgetid']
nonexisting_id = config['nonexisting_id']
invalid_id = config['invalid_id']

# Generate a random 5-character string
def generate_random_string(length=5):
    return ''.join(random.choices(string.ascii_letters, k=length))

# Define the function to send a PUT request
def put_request(application_version):
    url = f"{base_url}/api/ApplicationVersion/{application_version['id']}?api-version=1.0"
    print("PUT URL: " + url)

    # Update the "updatedBy" field with a random 5-character string
    application_version['updatedBy'] = generate_random_string()

    # Send the PUT request
    response = requests.put(url, json=application_version, verify=False)  # verify=False to ignore SSL certificate warnings

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

# Function to update the rowVersion in config.json
def update_row_version_in_config(new_row_version):
    config['appvgetid']['rowVersion'] = new_row_version
    with open('config.json', 'w') as file:
        json.dump(config, file, indent=4)
    print(f"rowVersion updated in config.json to {new_row_version}")

# Test function for PUT request with valid idv
def test_put_request_valid_idv():
    print("==== Testing PUT request with valid idv ====")
    # Call the put_request function
    response, response_data = put_request(appvgetid)

    # Assert that the response status code is 201
    assert response.status_code == 200, f"Expected status code 200, but got {response.status_code}"
    print("Assertion passed: Status code is 200")

    # Assert that the id in the request matches the id in the response body
    assert response_data.get("id") == appvgetid['id'], f"Expected id {appvgetid['id']}, but got {response_data.get('id')}"
    print("Assertion passed: id in the request matches the id in the response body")

    # Update the rowVersion in config.json with the new rowVersion from the response body
    new_row_version = response_data.get("rowVersion")
    update_row_version_in_config(new_row_version)
    print("==== End of test for PUT request with valid idv ====")

# Test function for PUT request with nonexisting_id
def test_put_request_nonexisting_id():
    print("==== Testing PUT request with nonexisting_id ====")
    # Create a payload with nonexisting_id
    payload = {
        "id": nonexisting_id,
        "updatedBy": generate_random_string(),
        "rowVersion": appvgetid['rowVersion']
    }

    # Call the put_request function
    response, response_data = put_request(payload)

    # Assert that the response status code is 404
    assert response.status_code == 404, f"Expected status code 404, but got {response.status_code}"
    print("Assertion passed: Status code is 404 for nonexisting_id")
    print("==== End of test for PUT request with nonexisting_id ====")

# Test function for PUT request with invalid_id
def test_put_request_invalid_id():
    print("==== Testing PUT request with invalid_id ====")
    # Create a payload with invalid_id
    payload = {
        "id": invalid_id,
        "updatedBy": generate_random_string(),
        "rowVersion": appvgetid['rowVersion']
    }

    # Call the put_request function
    response, response_data = put_request(payload)

    # Assert that the response status code is 404
    assert response.status_code == 404, f"Expected status code 404, but got {response.status_code}"
    print("Assertion passed: Status code is 404 for invalid_id")
    print("==== End of test for PUT request with invalid_id ====")

# Run the tests with pytest
if __name__ == "__main__":
    pytest.main()
