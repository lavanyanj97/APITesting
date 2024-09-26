import requests
import json

# Load the configuration data
with open('config.json', 'r') as config_file:
    config_data = json.load(config_file)

base_url = "https://localhost:7084"

def get_request(culture_code, id):
    url = f"{base_url}/api/Application/{id}?cultureCode={culture_code}&api-version=1.0"
    print("GET URL: " + url)

    # Sending the GET request
    response = requests.get(url, verify=False)  # verify=False to ignore SSL certificate warnings
    return response

def test_get_request_with_valid_id_and_culture_code():
    valid_id = config_data.get("valid_id")  # Fetch the valid ID from the config data
    culture_code = "en-US"  # Assuming valid culture code
    response = get_request(culture_code, valid_id)

    assert response.status_code == 200, f"Expected status code 200, but got {response.status_code}"
    print("Status code 200 for valid ID and culture code passed")

    # Print the response body
    print("Response Body:", json.dumps(response.json(), indent=4))


def test_get_request_with_invalid_id():
    invalid_id = config_data.get('invalid_id')  # Fetch the invalid ID from the config data
    culture_code = "en-US"  # Valid culture code
    response = get_request(culture_code, invalid_id)

    assert response.status_code == 404, f"Expected status code 404 for invalid ID, but got {response.status_code}"
    print("Status code 404 for invalid ID passed")

    # Optionally print the response body or error message
    print("Response Body:", response.text)


def test_get_request_with_non_existing_id():
    non_existing_id = config_data.get('nonexisting_id')
    culture_code = "en-US"  # Valid culture code
    response = get_request(culture_code, non_existing_id)

    assert response.status_code == 404, f"Expected status code 404 for non-existing ID, but got {response.status_code}"
    print("Status code 404 for non-existing ID passed")

    # Optionally print the response body or error message
    print("Response Body:", response.text)


# Run the tests
if __name__ == "__main__":
    test_get_request_with_valid_id_and_culture_code()
    test_get_request_with_invalid_id()
    test_get_request_with_non_existing_id()
