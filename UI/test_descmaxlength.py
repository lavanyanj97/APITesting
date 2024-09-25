from time import sleep
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By

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
    name.send_keys("test")
    description = driver.find_element(By.NAME, "description")
    description.click()

    long_description = "a" * 8193
    description.send_keys(long_description)

    dropdown_button = driver.find_element(By.XPATH,
                                          "//button[contains(@role, 'combobox') and contains(@aria-controls, 'radix-')]")
    driver.execute_script("arguments[0].scrollIntoView(true);", dropdown_button)
    dropdown_button.click()

    first_option = driver.find_element(By.XPATH, "//div[@role='option'][1]")
    first_option.click()

    save = driver.find_element(By.CSS_SELECTOR, "button.bg-rivieraParadise")

    # Check if the Save button is available
    save = driver.find_element(By.CSS_SELECTOR, "button.bg-rivieraParadise")
    if save.is_enabled():
        assert False, "Test failed: Save button is available despite validation errors with maximum name field length"