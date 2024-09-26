import requests
import json

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

    # Extracting the 'id', 'rowVersion', and 'translationRowVersion' from the response
    valid_id = json_data["id"]
    row_version = json_data.get("rowVersion")
    translation_row_version = json_data.get("translationRowVersion")

    # Store the generated valid_id, rowVersion, and translationRowVersion in the config_data
    config_data["valid_id"] = valid_id
    config_data["rowVersion"] = row_version
    config_data["translationRowVersion"] = translation_row_version

    # Save the updated config back to config.json
    with open('config.json', 'w') as config_file:
        json.dump(config_data, config_file, indent=4)
    print(f"Stored valid_id, rowVersion, and translationRowVersion in config.json: {valid_id}, {row_version}, {translation_row_version}")

    return valid_id, row_version, translation_row_version

def test_sample():
    valid_id, row_version, translation_row_version = post_request()
    print(f"Extracted valid_id: {valid_id}")
    print(f"Extracted rowVersion: {row_version}")
    print(f"Extracted translationRowVersion: {translation_row_version}")

# Call the function
if __name__ == "__main__":
    post_request()
