import requests
import json
import pytest

# Load the configuration data
with open('config.json', 'r') as config_file:
    config_data = json.load(config_file)

data_applicationpost = config_data['data_applicationpost']

base_url = "https://localhost:7084"

# Modified data with name as an empty string
data_applicationpostnameempty = data_applicationpost.copy()
data_applicationpostnameempty["name"] = ""

# Modified data with name as an integer
data_applicationpostnamenotstring = data_applicationpost.copy()
data_applicationpostnamenotstring["name"] = 12345

# Modified data with name exceeding maximum length
data_applicationpostnametoolong = data_applicationpost.copy()
data_applicationpostnametoolong["name"] = "a" * 121  # Assuming the max length is 120

# Modified data with name as null
data_applicationpostnamenull = data_applicationpost.copy()
data_applicationpostnamenull["name"] = None

# Modified data with description as a non-string
data_applicationpostdescriptionnotstring = data_applicationpost.copy()
data_applicationpostdescriptionnotstring["description"] = 12345

# Modified data with description exceeding maximum length
data_applicationpostdescriptiontoolong = data_applicationpost.copy()
data_applicationpostdescriptiontoolong["description"] = "a" * 8193  # Assuming the max length is 8192

# Modified data with description as null
data_applicationpostdescriptionnull = data_applicationpost.copy()
data_applicationpostdescriptionnull["description"] = None

# Modified data with translationUpdatedBy exceeding maximum length
data_applicationposttranslationupdatedbytoolong = data_applicationpost.copy()
data_applicationposttranslationupdatedbytoolong["translationUpdatedBy"] = "a" * 121  # Assuming the max length is 120

# Modified data with translationUpdatedBy as a number instead of string
data_applicationposttranslationupdatedbynotstring = data_applicationpost.copy()
data_applicationposttranslationupdatedbynotstring["translationUpdatedBy"] = 12345

# Modified data with translationUpdatedBy as null
data_applicationposttranslationupdatedbynull = data_applicationpost.copy()
data_applicationposttranslationupdatedbynull["translationUpdatedBy"] = None

# Modified data with cultureCode exceeding maximum length
data_applicationpostculturecodetoolong = data_applicationpost.copy()
data_applicationpostculturecodetoolong["cultureCode"] = "a" * 11  # Assuming the max length is 10

# Modified data with cultureCode as a number instead of string
data_applicationpostculturecodenotstring = data_applicationpost.copy()
data_applicationpostculturecodenotstring["cultureCode"] = 12345

# Modified data with cultureCode as an empty string
data_applicationpostculturecodeempty = data_applicationpost.copy()
data_applicationpostculturecodeempty["cultureCode"] = ""

# Modified data with translationRowVersion as null
data_applicationposttranslationrowversionnull = data_applicationpost.copy()
data_applicationposttranslationrowversionnull["translationRowVersion"] = None

def post_request(data):
    url = f"{base_url}/api/Application?api-version=1.0"
    print("post url: " + url)

    # Sending the POST request
    response = requests.post(url, json=data, verify=False)  # verify=False to ignore SSL certificate warnings
    return response

def test_post_request_with_empty_name():
    response = post_request(data_applicationpostnameempty)
    assert response.status_code == 400, f"Expected status code 400, but got {response.status_code}"
    print("Status code is 400 passed")

    response_text = response.text
    assert "The Name field is required." in response_text, "Expected response to include 'The Name field is required.'"
    print("Body matches string passed")

def test_post_request_with_name_not_string():
    response = post_request(data_applicationpostnamenotstring)
    assert response.status_code == 400, f"Expected status code 400, but got {response.status_code}"
    print("Status code is 400 passed")

    response_text = response.text
    assert "The Name field is required." in response_text, "Expected response to include 'The Name field is required.'"
    print("Body matches string passed")

def test_post_request_with_name_too_long():
    response = post_request(data_applicationpostnametoolong)
    assert response.status_code == 400, f"Expected status code 400, but got {response.status_code}"
    print("Status code is 400 passed")

    response_text = response.text
    assert "The field Name must be a string or array type with a maximum length of '120'." in response_text, "Expected response to include 'The field Name must be a string or array type with a maximum length of '120'.'"
    print("Body matches string passed")

def test_post_request_with_name_null():
    response = post_request(data_applicationpostnamenull)
    assert response.status_code == 400, f"Expected status code 400, but got {response.status_code}"
    print("Status code is 400 passed")

    response_text = response.text
    assert "The Name field is required." in response_text, "Expected response to include 'The Name field is required.'"
    print("Body matches string passed")

def test_post_request_with_description_not_string():
    response = post_request(data_applicationpostdescriptionnotstring)
    assert response.status_code == 400, f"Expected status code 400, but got {response.status_code}"
    print("Status code is 400 passed")

    response_text = response.text
    assert "Description must be a string." in response_text, "Expected response to include 'Description must be a string.'"
    print("Body matches string passed")

def test_post_request_with_description_too_long():
    response = post_request(data_applicationpostdescriptiontoolong)
    assert response.status_code == 400, f"Expected status code 400, but got {response.status_code}"
    print("Status code is 400 passed")

    response_text = response.text
    assert "The field Description must be a string or array type with a maximum length of '8192'." in response_text, "Expected response to include 'The field Description must be a string or array type with a maximum length of '8192'.'"
    print("Body matches string passed")

def test_post_request_with_description_null():
    response = post_request(data_applicationpostdescriptionnull)
    assert response.status_code == 201, f"Expected status code 201, but got {response.status_code}"
    print("Status code is 201 passed")

def test_post_request_with_translationUpdatedBy_too_long():
    response = post_request(data_applicationposttranslationupdatedbytoolong)
    assert response.status_code == 400, f"Expected status code 400, but got {response.status_code}"
    print("Status code is 400 passed")

    response_text = response.text
    assert "The field TranslationUpdatedBy must be a string or array type with a maximum length of '120'." in response_text, "Expected response to include 'The field TranslationUpdatedBy must be a string or array type with a maximum length of '120'.'"
    print("Body matches string passed")

def test_post_request_with_translationUpdatedBy_not_string():
    response = post_request(data_applicationposttranslationupdatedbynotstring)
    assert response.status_code == 400, f"Expected status code 400, but got {response.status_code}"
    print("Status code is 400 passed")

    response_text = response.text
    assert "translationUpdatedBy must be a string" in response_text, "Expected response to include 'translationUpdatedBy must be a string'"
    print("Body matches string passed")

def test_post_request_with_translationUpdatedBy_null():
    response = post_request(data_applicationposttranslationupdatedbynull)
    assert response.status_code == 400, f"Expected status code 400, but got {response.status_code}"
    print("Status code is 400 passed")

    response_text = response.text
    assert "TranslationUpdatedBy is required for updates" in response_text, "Expected response to include 'TranslationUpdatedBy is required for updates'"
    print("Body matches string passed")

def test_post_request_with_cultureCode_too_long():
    response = post_request(data_applicationpostculturecodetoolong)
    assert response.status_code == 400, f"Expected status code 400, but got {response.status_code}"
    print("Status code is 400 passed")

    response_text = response.text
    assert "The field CultureCode must be a string or array type with a maximum length of '10'." in response_text, "Expected response to include 'cultureCode must not exceed 10 characters'"
    print("Body matches string passed")

def test_post_request_with_cultureCode_not_string():
    response = post_request(data_applicationpostculturecodenotstring)
    assert response.status_code == 400, f"Expected status code 400, but got {response.status_code}"
    print("Status code is 400 passed")

    response_text = response.text
    assert "cultureCode must be a string" in response_text, "Expected response to include 'cultureCode must be a string'"
    print("Body matches string passed")

def test_post_request_with_cultureCode_empty():
    response = post_request(data_applicationpostculturecodeempty)
    assert response.status_code == 400, f"Expected status code 400, but got {response.status_code}"
    print("Status code is 400 passed")

    response_text = response.text
    assert "The CultureCode field is required." in response_text, "Expected response to include 'cultureCode is required'"
    print("Body matches string passed")

def test_post_request_with_translationRowVersion_null():
    response = post_request(data_applicationposttranslationrowversionnull)
    assert response.status_code == 201, f"Expected status code 201, but got {response.status_code}"
    print("Status code is 201 passed")



# Run the tests
if __name__ == "__main__":
    pytest.main()
