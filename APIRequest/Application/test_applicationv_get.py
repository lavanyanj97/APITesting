import requests
import pytest
import json

# Define the base URL
base_url = "https://localhost:7084"

# Define the function to send a GET request
def get_request():
    url = f"{base_url}/api/ApplicationVersion?api-version=1.0"
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
        print("Response body is not in JSON format: " + response.text)

    return response

# Test function using pytest
def test_get_request():
    # Call the get_request function
    response = get_request()

    # Assert that the response status code is 200
    assert response.status_code == 200, f"Expected status code 200, but got {response.status_code}"
    print("Assertion passed: Status code is 200")

    # Read the configuration file
    with open('config.json', 'r') as file:
        config = json.load(file)

    # Get the "idv" value from the configuration file
    idv_value = config['idv']

    # Parse the JSON response
    response_data = response.json()

    # Assert that the "idv" value is present in the response body
    idv_present = any(item.get("id") == idv_value for item in response_data)
    assert idv_present, f"Expected idv {idv_value} not found in the response"
    print("Assertion passed: idv value is present in the response")

# Run the test with pytest
if __name__ == "__main__":
    pytest.main()
