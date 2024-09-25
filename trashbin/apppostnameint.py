import requests
import json
from data import data_applicationpost  # Importing the specific dataset from data.py

base_url = "https://localhost:7084"

# Modified data with name as an integer
data_applicationpostnamenotstring = data_applicationpost.copy()
data_applicationpostnamenotstring["name"] = 12345

def post_request(data):
    url = f"{base_url}/api/Application?api-version=1.0"
    print("post url: " + url)

    # Assertions for the data provided
    assert isinstance(data["name"], str), "Expected 'name' to be a string"
    assert 1 <= len(data["name"]) <= 120, "Expected 'name' length to be between 1 and 120"
    print("Check name data type and length passed")

    assert isinstance(data["description"], str), "Expected 'description' to be a string"
    assert len(data["description"]) <= 8192, "Expected 'description' length to be at most 8192"
    print("Check description data type and length passed")

    assert isinstance(data["cultureCode"], str), "Expected 'cultureCode' to be a string"
    print("Check cultureCode data type passed")

    assert isinstance(data["translationUpdatedBy"], str), "Expected 'translationUpdatedBy' to be a string"
    assert len(data["translationUpdatedBy"]) <= 120, "Expected 'translationUpdatedBy' length to be at most 120"
    print("Check translationUpdatedBy data type and length passed")

    assert isinstance(data["updatedBy"], str), "Expected 'updatedBy' to be a string"
    assert len(data["updatedBy"]) <= 120, "Expected 'updatedBy' length to be at most 120"
    print("Check updatedBy data type and length passed")

    assert data["id"] is None, "Expected 'id' to be null"
    print("Check id is null passed")

    assert isinstance(data["isActive"], bool), "Expected 'isActive' to be a boolean"
    print("Check isActive data type passed")

    # Sending the POST request
    response = requests.post(url, json=data, verify=False)  # verify=False to ignore SSL certificate warnings
    assert response.status_code == 201, f"Expected status code 201, but got {response.status_code}"

    # Parsing the JSON response
    json_data = response.json()
    assert len(json_data) > 0, "Expected response to contain applications, but it was empty"

    print("json response body:", json.dumps(json_data, indent=4))

    # Extracting the 'id' from the response
    user_id = json_data["id"]

    return user_id

# Call the function with modified data
print("Testing with modified data:")
post_request(data_applicationpostnamenotstring)
