import requests
import json
from data import data_applicationpost  # Importing the specific dataset from data.py

base_url = "https://localhost:7084"

# Modified data with name as an empty string
data_applicationpostnameempty = data_applicationpost.copy()
data_applicationpostnameempty["name"] = ""

def post_request(data):
    url = f"{base_url}/api/Application?api-version=1.0"
    print("post url: " + url)

    # Sending the POST request
    response = requests.post(url, json=data, verify=False)  # verify=False to ignore SSL certificate warnings
    assert response.status_code == 400, f"Expected status code 400, but got {response.status_code}"
    print("Status code is 400 passed")

    # Parsing the response text
    response_text = response.text
    assert "String" in response_text, "Expected response to include 'String'"
    print("Body matches string passed")

# Call the function with modified data
print("Testing with empty name:")
post_request(data_applicationpostnameempty)
