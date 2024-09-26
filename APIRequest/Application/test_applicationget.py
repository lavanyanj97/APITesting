import requests
import json

# Load the configuration data
with open('config.json', 'r') as config_file:
    config_data = json.load(config_file)

base_url = "https://localhost:7084"

# Extract the non-existing culture code from the config
non_existing_culture_code = config_data.get("non_existing_culture_code", "ects")


def get_request(culture_code):
    url = f"{base_url}/api/Application?cultureCode={culture_code}&api-version=1.0"
    print("GET URL: " + url)

    # Sending the GET request
    response = requests.get(url, verify=False)  # verify=False to ignore SSL certificate warnings
    return response


def test_get_request_with_valid_culture_code():
    response = get_request("en-US")
    assert response.status_code == 200, f"Expected status code 200, but got {response.status_code}"
    print("Status code is 200 passed")

    # Print the response body
    response_data = response.json()
    print("Response Body:", json.dumps(response_data, indent=2))  # Pretty-printing the JSON response

    assert isinstance(response_data, list), "Expected response data to be a list"
    print("Response data is a list passed")

    # Separator line
    print("=" * 80)


def test_get_request_with_non_existing_culture_code():
    response = get_request(non_existing_culture_code)  # Use the value from the config
    assert response.status_code == 200, f"Expected status code 200, but got {response.status_code}"
    print("Status code is 200 passed for non-existing culture code")

    # Print the response body
    response_data = response.json()
    print("Response Body for non-existing culture code:", json.dumps(response_data, indent=2))

    # Check that each application has cultureCode as 'en-US' or null
    for application in response_data:
        assert application['cultureCode'] in ['en-US',
                                              None], f"Expected cultureCode to be 'en-US' or null, but got {application['cultureCode']}"
    print("All cultureCode values are either 'en-US' or null passed")

    # Separator line
    print("=" * 80)


# Run the tests
if __name__ == "__main__":
    test_get_request_with_valid_culture_code()
    test_get_request_with_non_existing_culture_code()
