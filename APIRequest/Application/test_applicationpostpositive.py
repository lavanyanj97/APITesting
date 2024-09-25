import requests
import json
import pytest

# Load the configuration data
with open('config.json', 'r') as config_file:
    config_data = json.load(config_file)

data_applicationpost = config_data['data_applicationpost']

base_url = "https://localhost:7084"

def post_request():
    url = f"{base_url}/api/Application?api-version=1.0"
    print("post url: " + url)

    # Assertions for the data provided
    assert isinstance(data_applicationpost["name"], str), "Expected 'name' to be a string"
    assert 1 <= len(data_applicationpost["name"]) <= 120, "Expected 'name' length to be between 1 and 120"
    print("Check name data type and length passed")

    assert isinstance(data_applicationpost["description"], str), "Expected 'description' to be a string"
    assert len(data_applicationpost["description"]) <= 8192, "Expected 'description' length to be at most 8192"
    print("Check description data type and length passed")

    assert isinstance(data_applicationpost["cultureCode"], str), "Expected 'cultureCode' to be a string"
    print("Check cultureCode data type passed")

    assert isinstance(data_applicationpost["translationUpdatedBy"], str), "Expected 'translationUpdatedBy' to be a string"
    assert len(data_applicationpost["translationUpdatedBy"]) <= 120, "Expected 'translationUpdatedBy' length to be at most 120"
    print("Check translationUpdatedBy data type and length passed")

    assert isinstance(data_applicationpost["updatedBy"], str), "Expected 'updatedBy' to be a string"
    assert len(data_applicationpost["updatedBy"]) <= 120, "Expected 'updatedBy' length to be at most 120"
    print("Check updatedBy data type and length passed")

    assert data_applicationpost["id"] is None, "Expected 'id' to be null"
    print("Check id is null passed")

    assert isinstance(data_applicationpost["isActive"], bool), "Expected 'isActive' to be a boolean"
    print("Check isActive data type passed")

    # Sending the POST request
    response = requests.post(url, json=data_applicationpost, verify=False)  # verify=False to ignore SSL certificate warnings
    assert response.status_code == 201, f"Expected status code 201, but got {response.status_code}"

    # Parsing the JSON response
    json_data = response.json()
    assert len(json_data) > 0, "Expected response to contain applications, but it was empty"

    # Print the JSON response body
    print("json response body:", json.dumps(json_data, indent=4))

    # Extracting the 'id' from the response
    user_id = json_data["id"]

    return user_id

def test_sample():
    user_id = post_request()
    print(f"Extracted user_id: {user_id}")

# Call the function
if __name__ == "__main__":
    post_request()
