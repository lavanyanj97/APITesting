import requests
import json
import random
import string
import pytest

# Load the configuration data
def load_config():
    with open('config.json', 'r') as config_file:
        return json.load(config_file)

def save_config(config_data):
    with open('config.json', 'w') as config_file:
        json.dump(config_data, config_file, indent=4)

# Generate a random string
def generate_random_string(length=10):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

# PUT request function
def put_request(data_applicationput, valid_id):
    base_url = "https://localhost:7084"
    url = f"{base_url}/api/Application/{valid_id}?api-version=1.0"
    response = requests.put(url, json=data_applicationput, verify=False)  # Verify=False to ignore SSL certificate warnings
    return response

# Test for PUT request and assertions
def test_put_request():
    config_data = load_config()

    # Extract necessary fields from the config
    valid_id = config_data.get("valid_id")
    row_version = config_data.get("rowVersion")
    translation_row_version = config_data.get("translationRowVersion")

    # Prepare the data for the PUT request from config
    data_applicationput = config_data["data_applicationpost"].copy()

    # Update specific fields in the data_applicationput dictionary
    data_applicationput["id"] = valid_id
    data_applicationput["translationRowVersion"] = translation_row_version
    data_applicationput["rowVersion"] = row_version
    data_applicationput["updatedBy"] = generate_random_string(10)  # Random 10-letter string for updatedBy

    # Generate a random name each time
    data_applicationput["name"] = f"Updated Applications {generate_random_string(5)}"

    # Call the PUT request
    response = put_request(data_applicationput, valid_id)

    # Assertions for response
    assert response.status_code == 200, f"Expected status code 200, but got {response.status_code}"
    print(f"Response status code: {response.status_code}")

    json_data = response.json()
    assert len(json_data) > 0, "Expected response to contain applications, but it was empty"

    # Inline assertions for validation
    assert isinstance(data_applicationput['name'], str), "Name should be a string"
    assert 1 <= len(data_applicationput['name']) <= 120, "Name length should be between 1 and 120 characters"

    assert isinstance(data_applicationput['description'], str), "Description should be a string"
    assert len(data_applicationput['description']) <= 8192, "Description length should be at most 8192 characters"

    assert isinstance(data_applicationput['cultureCode'], str), "Culture code should be a string"

    assert isinstance(data_applicationput['translationUpdatedBy'], str), "Translation updated by should be a string"
    assert len(data_applicationput['translationUpdatedBy']) <= 120, "Translation updated by length should be at most 120 characters"

    assert isinstance(data_applicationput['updatedBy'], str), "Updated by should be a string"
    assert len(data_applicationput['updatedBy']) <= 120, "Updated by length should be at most 120 characters"

    assert isinstance(data_applicationput['isActive'], bool), "IsActive should be a boolean"

    # Update rowVersion and translationRowVersion in config_data
    config_data["rowVersion"] = json_data.get("rowVersion")
    config_data["translationRowVersion"] = json_data.get("translationRowVersion")

    # Save the updated config back to config.json
    save_config(config_data)

    # Print the updated JSON
    print("Updated request body:")
    print(json.dumps(data_applicationput, indent=4))


# Call the function
if __name__ == "__main__":
    pytest.main()
