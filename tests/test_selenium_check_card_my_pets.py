import chromedriver_autoinstaller
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions

chromedriver_autoinstaller.install()


@pytest.fixture(scope='function')
def driver(request):
    from selenium import webdriver
    driver = webdriver.Chrome()
    driver.implicitly_wait(5)
    yield driver
    driver.quit()


def test_check_cards_my_pets(driver):
    driver.get('https://petfriends.skillfactory.ru/login')
    driver.find_element(By.ID, 'email').send_keys('avfedorov@gmail.com')
    driver.find_element(By.ID, 'pass').send_keys('qazwsx')
    driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()

    driver.get('https://petfriends.skillfactory.ru/my_pets')

    images = driver.find_elements(By.XPATH, '//div[@id="all_my_pets"]//img')
    names = driver.find_elements(By.XPATH, '//div[@id="all_my_pets"]//td[1]')
    breed = driver.find_elements(By.XPATH, '//div[@id="all_my_pets"]//td[2]')
    age = driver.find_elements(By.XPATH, '//div[@id="all_my_pets"]//td[3]')

    for i in range(len(names)):
        assert images[i].get_attribute('src') != ''
        assert names[i].text != ''
        assert breed[i].text != ''
        assert age[i].text != ''
