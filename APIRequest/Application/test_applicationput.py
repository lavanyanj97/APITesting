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
def generate_random_string(length=5):
    return ''.join(random.choices(string.ascii_lowercase, k=length))

# PUT request function
def put_request(data_applicationput, valid_id):
    base_url = "https://localhost:7084"
    url = f"{base_url}/api/Application/{valid_id}?api-version=1.0"
    response = requests.put(url, json=data_applicationput, verify=False)  # Verify=False to ignore SSL certificate warnings
    return response

# Assertion functions for request data validation
def validate_name(data):
    assert isinstance(data['name'], str), "Name should be a string"
    assert 1 <= len(data['name']) <= 120, "Name length should be between 1 and 120 characters"

def validate_description(data):
    assert isinstance(data['description'], str), "Description should be a string"
    assert len(data['description']) <= 8192, "Description length should be at most 8192 characters"

def validate_culture_code(data):
    assert isinstance(data['cultureCode'], str), "Culture code should be a string"

def validate_translation_updated_by(data):
    assert isinstance(data['translationUpdatedBy'], str), "Translation updated by should be a string"
    assert len(data['translationUpdatedBy']) <= 120, "Translation updated by length should be at most 120 characters"

def validate_updated_by(data):
    assert isinstance(data['updatedBy'], str), "Updated by should be a string"
    assert len(data['updatedBy']) <= 120, "Updated by length should be at most 120 characters"

def validate_is_active(data):
    assert isinstance(data['isActive'], bool), "IsActive should be a boolean"

# Test for PUT request and assertions
@pytest.mark.parametrize("validation_func", [
    validate_name,
    validate_description,
    validate_culture_code,
    validate_translation_updated_by,
    validate_updated_by,
    validate_is_active,
])
def test_put_request(validation_func):
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
    data_applicationput["updatedBy"] = generate_random_string()  # Random 5-letter string

    # Call the PUT request
    response = put_request(data_applicationput, valid_id)

    # Assertions for response
    assert response.status_code == 200, f"Expected status code 200, but got {response.status_code}"
    json_data = response.json()
    assert len(json_data) > 0, "Expected response to contain applications, but it was empty"

    # Call the validation function
    validation_func(data_applicationput)

    # Update rowVersion and translationRowVersion in config_data
    config_data["rowVersion"] = json_data.get("rowVersion")
    config_data["translationRowVersion"] = json_data.get("translationRowVersion")

    # Save the updated config back to config.json
    save_config(config_data)

    # Print the updated config data
    print("Updated config.json:", json.dumps(config_data, indent=4))
# Test for non-existing ID
def test_nonexisting_id():
    config_data = load_config()
    nonexisting_id = config_data.get("nonexisting_id")

    # Call the PUT request with the non-existing ID
    response = put_request(config_data["data_applicationpost"], nonexisting_id)

    # Assertions for non-existing ID
    assert response.status_code == 404, f"Expected status code 404, but got {response.status_code}"
    # Check if the response body contains the expected error message
    assert "URI Id must match Model Id" in response.text, "Response body should contain URI Id must match Model Id"

# Call the function
if __name__ == "__main__":
    pytest.main()
