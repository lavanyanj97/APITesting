from time import sleep
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
import time

@pytest.fixture
def driver():
    driver = webdriver.Chrome()
    driver.implicitly_wait(10)
    yield driver
    driver.quit()

def test_open_url(driver):
    driver.get("http://localhost:8081/")

    add_new_client_button = driver.find_element(By.CLASS_NAME, "items-center")
    add_new_client_button.click()

    name = driver.find_element(By.NAME, "name")
    name.click()
    name.send_keys("t")
    sleep(7)
    # Check if the warning message is displayed while entering text
    warning_message = "Invalid length: Expected >=2 but received 1"
    try:
        warning_element = driver.find_element(By.XPATH, f"//*[contains(text(), '{warning_message}')]")
        if warning_element.is_displayed():
            assert False, f"Test failed: Warning message '{warning_message}' displayed while entering text."
    except Exception as e:
        print(f"An error occurred: {e}")
        assert False, "Test failed because the error message Invalid length: Expected >=2 but received 1 displayed while entering the name."



