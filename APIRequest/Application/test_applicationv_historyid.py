import requests
import json

# Define the base URL
base_url = "https://localhost:7084"  # Replace with your actual base URL

# Read the configuration file
with open('config.json', 'r') as file:
    config = json.load(file)

# Get the "idv", "startdate", "enddate", "nonexisting_id", and "invalid_id" values from the configuration file
idv = config['idv']
start_date = config['startdate']
end_date = config['enddate']
nonexisting_id = config['nonexisting_id']
invalid_id = config['invalid_id']

# Define the function to send a GET request
def get_request(id_value):
    url = f"{base_url}/api/ApplicationVersion/History/{id_value}?dateFrom={start_date}&dateTo={end_date}&api-version=1.0"
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

# Function to test the GET request with valid idv
def test_get_request_valid_idv():
    print("==== Testing GET request with valid idv ====")
    # Call the get_request function
    response, response_data = get_request(idv)

    # Assert that the response status code is 200
    assert response.status_code == 200, f"Expected status code 200, but got {response.status_code}"
    print("Assertion passed: Status code is 200")
    print("==== End of test for GET request with valid idv ====")

# Function to test the GET request with nonexisting_id
def test_get_request_nonexisting_id():
    print("==== Testing GET request with nonexisting_id ====")
    # Call the get_request function
    response, response_data = get_request(nonexisting_id)

    # Assert that the response status code is 404
    assert response.status_code == 404, f"Expected status code 404, but got {response.status_code}"
    print("Assertion passed: Status code is 404 for nonexisting_id")
    print("==== End of test for GET request with nonexisting_id ====")

# Function to test the GET request with invalid_id
def test_get_request_invalid_id():
    print("==== Testing GET request with invalid_id ====")
    # Call the get_request function
    response, response_data = get_request(invalid_id)

    # Assert that the response status code is 404
    assert response.status_code == 404, f"Expected status code 404, but got {response.status_code}"
    print("Assertion passed: Status code is 404 for invalid_id")
    print("==== End of test for GET request with invalid_id ====")

# Run the tests
if __name__ == "__main__":
    test_get_request_valid_idv()
    test_get_request_nonexisting_id()
    test_get_request_invalid_id()
