import requests
import json
import pytest

# Load the configuration data
with open('config.json', 'r') as config_file:
    config_data = json.load(config_file)

# Extract the valid_id and update the data_applicationv dictionary
valid_id = config_data['valid_id']
data_applicationv = config_data['data_applicationv']
data_applicationv['applicationId'] = valid_id  # Replace placeholder with actual valid_id

base_url = "https://localhost:7084"

def post_request(data):
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

    # Update rowVersion dynamically if present in response
    if response.status_code == 201:
        if 'rowVersion' in response_data:
            config_data['rowVersionv'] = response_data['rowVersion']
            with open('config.json', 'w') as config_file:
                json.dump(config_data, config_file, indent=4)
            print("rowVersion updated and saved in config.json")

    return response

def test_post_request():
    try:
        response = post_request(data_applicationv)
        assert response.status_code == 201, f"Expected status code 201, but got {response.status_code}"
        print("Assertion passed: Status code is 201")

        # Additional assertions
        response_data = response.json()

        # Update id dynamically if present in response
        if response.status_code == 201:
            if 'id' in response_data:
                config_data['idv'] = response_data['id']
                with open('config.json', 'w') as config_file:
                    json.dump(config_data, config_file, indent=4)
                print("idv updated and saved in config.json")

        # Check if 'id' is a valid UUID
        assert isinstance(response_data['id'], str) and len(
            response_data['id']) == 36, f"Expected 'id' to be a valid UUID, but got {response_data['id']}"
        print("Assertion passed: 'id' is a valid UUID")

        # Check if 'rowVersion' is a valid byte string
        assert isinstance(response_data['rowVersion'],
                          str), f"Expected 'rowVersion' to be a valid byte string, but got {response_data['rowVersion']}"
        print("Assertion passed: 'rowVersion' is a valid byte string")

        # Check if 'applicationId' is a valid UUID
        assert isinstance(response_data['applicationId'], str) and len(response_data[
                                                                           'applicationId']) == 36, f"Expected 'applicationId' to be a valid UUID, but got {response_data['applicationId']}"
        print("Assertion passed: 'applicationId' is a valid UUID")

        # Check if 'updatedBy' is a string
        assert isinstance(response_data['updatedBy'],
                          str), f"Expected 'updatedBy' to be a string, but got {type(response_data['updatedBy'])}"
        print("Assertion passed: 'updatedBy' is a string")

        # Check if 'major' is an integer
        assert isinstance(response_data['major'],
                          int), f"Expected 'major' to be an integer, but got {type(response_data['major'])}"
        print("Assertion passed: 'major' is an integer")

        # Check if 'minor' is an integer
        assert isinstance(response_data['minor'],
                          int), f"Expected 'minor' to be an integer, but got {type(response_data['minor'])}"
        print("Assertion passed: 'minor' is an integer")

        # Check if 'revision' is an integer
        assert isinstance(response_data['revision'],
                          int), f"Expected 'revision' to be an integer, but got {type(response_data['revision'])}"
        print("Assertion passed: 'revision' is an integer")

        # Check if 'startDate' is a string (assuming it follows the date format)
        assert isinstance(response_data['startDate'],
                          str), f"Expected 'startDate' to be a string, but got {type(response_data['startDate'])}"
        print("Assertion passed: 'startDate' is a string")

        # Check if 'endDate' is a string (assuming it follows the date format)
        assert isinstance(response_data['endDate'],
                          str), f"Expected 'endDate' to be a string, but got {type(response_data['endDate'])}"
        print("Assertion passed: 'endDate' is a string")


    except AssertionError as e:
        print(e)
        raise



if __name__ == "__main__":
    pytest.main()
