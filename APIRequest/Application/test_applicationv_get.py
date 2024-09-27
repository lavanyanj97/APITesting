import requests
import json
import pytest

# Load the configuration data
with open('config.json', 'r') as config_file:
    config_data = json.load(config_file)

base_url = "https://localhost:7084"

def get_request(data):
    url = f"{base_url}/api/ApplicationVersion?api-version=1.0"
    print("post url: " + url)

    # Sending the POST request
    response = requests.post(url, json=data, verify=False)  # verify=False to ignore SSL certificate warnings

    # Print the response body using json.dumps for formatting
    try:
        response_data = response.json()
        print("response body: " + json.dumps(response_data, indent=4))
    except json.JSONDecodeError:
        print("response body: " + response.text)

    return response

def test_get_request():
    # Define the data to be sent in the request
    data_applicationv = {
        "key1": "value1",
        "key2": "value2"
        # Add other necessary key-value pairs
    }

    response = get_request(data_applicationv)
    assert response.status_code == 200, f"Expected status code 200, but got {response.status_code}"
    print("Assertion passed: Status code is 200")

if __name__ == "__main__":
    pytest.main([__file__])
