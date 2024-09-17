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

    description = driver.find_element(By.NAME, "description")
    description.click()
    description.send_keys("test1")

    sleep(3)

    dropdown_button = driver.find_element(By.XPATH,
                                          "//button[contains(@role, 'combobox') and contains(@aria-controls, 'radix-')]")
    driver.execute_script("arguments[0].scrollIntoView(true);", dropdown_button)
    dropdown_button.click()

    first_option = driver.find_element(By.XPATH, "//div[@role='option'][1]")
    first_option.click()

    sleep(3)

    discard_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Discard')]")
    discard_button.click()


