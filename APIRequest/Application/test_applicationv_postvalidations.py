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

    return response

def test_invalid_id():
    invalid_data = data_applicationv.copy()
    invalid_data['id'] = "invalid_uuid"
    response = post_request(invalid_data)
    print("response body: " + response.text)
    assert response.status_code == 400, f"Expected status code 400, but got {response.status_code}"
    print("Assertion passed: Invalid 'id' resulted in status code 400")
    print("=" * 50)

def test_invalid_updatedBy():
    invalid_data = data_applicationv.copy()
    invalid_data['updatedBy'] = 123  # Invalid type
    response = post_request(invalid_data)
    print("response body: " + response.text)
    assert response.status_code == 400, f"Expected status code 400, but got {response.status_code}"
    print("Assertion passed: Invalid 'updatedBy' resulted in status code 400")
    print("=" * 50)

def test_updatedBy_length():
    invalid_data = data_applicationv.copy()
    invalid_data['updatedBy'] = "a" * 121  # Exceeds maxLength of 120
    response = post_request(invalid_data)
    print("response body: " + response.text)
    assert response.status_code == 400, f"Expected status code 400, but got {response.status_code}"
    print("Assertion passed: 'updatedBy' exceeding maxLength resulted in status code 400")
    print("=" * 50)

def test_invalid_applicationId():
    invalid_data = data_applicationv.copy()
    invalid_data['applicationId'] = "invalid_uuid"
    response = post_request(invalid_data)
    print("response body: " + response.text)
    assert response.status_code == 400, f"Expected status code 400, but got {response.status_code}"
    print("Assertion passed: Invalid 'applicationId' resulted in status code 400")
    print("=" * 50)

def test_invalid_major():
    invalid_data = data_applicationv.copy()
    invalid_data['major'] = "invalid_integer"
    response = post_request(invalid_data)
    print("response body: " + response.text)
    assert response.status_code == 400, f"Expected status code 400, but got {response.status_code}"
    print("Assertion passed: Invalid 'major' resulted in status code 400")
    print("=" * 50)

def test_invalid_minor():
    invalid_data = data_applicationv.copy()
    invalid_data['minor'] = "invalid_integer"
    response = post_request(invalid_data)
    print("response body: " + response.text)
    assert response.status_code == 400, f"Expected status code 400, but got {response.status_code}"
    print("Assertion passed: Invalid 'minor' resulted in status code 400")
    print("=" * 50)

def test_invalid_revision():
    invalid_data = data_applicationv.copy()
    invalid_data['revision'] = "invalid_integer"
    response = post_request(invalid_data)
    print("response body: " + response.text)
    assert response.status_code == 400, f"Expected status code 400, but got {response.status_code}"
    print("Assertion passed: Invalid 'revision' resulted in status code 400")
    print("=" * 50)

def test_invalid_startDate():
    invalid_data = data_applicationv.copy()
    invalid_data['startDate'] = "invalid_date"
    response = post_request(invalid_data)
    print("response body: " + response.text)
    assert response.status_code == 400, f"Expected status code 400, but got {response.status_code}"
    print("Assertion passed: Invalid 'startDate' resulted in status code 400")
    print("=" * 50)

def test_invalid_endDate():
    invalid_data = data_applicationv.copy()
    invalid_data['endDate'] = "invalid_date"
    response = post_request(invalid_data)
    print("response body: " + response.text)
    assert response.status_code == 400, f"Expected status code 400, but got {response.status_code}"
    print("Assertion passed: Invalid 'endDate' resulted in status code 400")
    print("=" * 50)

# def test_startDate_after_endDate():
#     invalid_data = data_applicationv.copy()
#     invalid_data['startDate'] = "2024-10-01"  # Start date after end date
#     invalid_data['endDate'] = "2024-09-30"    # End date before start date
#     response = post_request(invalid_data)
#     print("response body: " + response.text)
#     assert response.status_code == 400, f"Expected status code 400, but got {response.status_code}"
#     print("Assertion passed: 'startDate' after 'endDate' resulted in status code 400")
#     print("="*50)

if __name__ == "__main__":
    pytest.main()
