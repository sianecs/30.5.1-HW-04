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
    WebDriverWait(driver, 5).until(expected_conditions.presence_of_element_located((By.TAG_NAME, 'body')))
    yield driver
    driver.quit()


def test_check_table_my_pets(driver):
    driver.get('https://petfriends.skillfactory.ru/login')
    driver.find_element(By.ID, 'email').send_keys('avfedorov@gmail.com')
    driver.find_element(By.ID, 'pass').send_keys('qazwsx')
    driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
    WebDriverWait(driver, 5).until(
        expected_conditions.text_to_be_present_in_element((By.TAG_NAME, 'h1'), "PetFriends"))

    driver.get('https://petfriends.skillfactory.ru/my_pets')
    WebDriverWait(driver, 5).until(
        expected_conditions.presence_of_element_located((By.XPATH, '//div[@id="all_my_pets"]')))

    pets_num = driver.find_element(By.XPATH, '//div[@class=".col-sm-4 left"]').text.split('\n')[1].split(': ')[1]

    pets_count = driver.find_elements(By.XPATH, '//table[@class="table table-hover"]/tbody/tr')

    assert int(pets_num) == len(pets_count)

    images = driver.find_elements(By.XPATH, '//div[@id="all_my_pets"]//img')
    assert sum(1 for img in images if img.get_attribute('src') != '') >= len(pets_count) / 2

    pets = driver.find_elements(By.XPATH, '//div[@id="all_my_pets"]//tr[not(contains(@class, "thead-dark"))]')

    for pet in pets:
        pet_data = pet.text.split()[:-1]
        assert len(pet_data) == 3, f"Некорректные данные для питомца: {pet_data}"
        name, breed, age = pet_data
        assert name != '', "Имя питомца не может быть пустым"
        assert breed != '', "Порода питомца не может быть пустой"
        assert age != '', "Возраст питомца не может быть пустым"

    pet_names = [pet.text.split()[0] for pet in pets]
    assert len(pet_names) == len(set(pet_names))

    pet_info = [pet.text for pet in pets]
    assert len(pet_info) == len(set(pet_info))
