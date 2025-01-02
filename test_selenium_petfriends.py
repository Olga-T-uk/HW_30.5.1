import time
import pickle
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def test_petfriends(selenium):
    """ Test login and check elements on the PetFriends page """

    # Установим неявные ожидания для веб-драйвера
    selenium.implicitly_wait(10)

    # Открыть главную страницу PetFriends
    selenium.get("https://petfriends1.herokuapp.com/")

    # Найти кнопку "Новый пользователь" и кликнуть по ней
    btn_newuser = selenium.find_element(By.XPATH, "//button[@onclick=\"document.location='/new_user';\"]")
    btn_newuser.click()

    # Найти ссылку "У меня уже есть аккаунт" и кликнуть по ней
    btn_exist_acc = selenium.find_element(By.LINK_TEXT, "У меня уже есть аккаунт")
    btn_exist_acc.click()

    # Ввести email и пароль
    field_email = selenium.find_element(By.ID, "email")
    field_email.click()
    field_email.clear()
    field_email.send_keys("isaid.zx@gmail.com")

    field_pass = selenium.find_element(By.ID, "pass")
    field_pass.click()
    field_pass.clear()
    field_pass.send_keys("qwerty1234")

    # Найти кнопку "Войти" и кликнуть по ней
    btn_submit = selenium.find_element(By.XPATH, "//button[@type='submit']")
    btn_submit.click()

    # Сохранить cookies после логина
    with open('my_cookies.txt', 'wb') as cookies:
        pickle.dump(selenium.get_cookies(), cookies)

    # Перейти на страницу с таблицей питомцев
    selenium.get("https://petfriends1.herokuapp.com/all_pets")

    # Использовать явные ожидания для проверки элементов на странице
    wait = WebDriverWait(selenium, 10)

    # Проверить, что на странице присутствуют фото питомцев
    photos = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".card-deck .card-img-top")))

    # Проверить, что на странице присутствуют имена питомцев
    names = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".card-deck .card-title")))

    # Проверить, что на странице присутствуют описания питомцев (возраст, порода)
    descriptions = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".card-deck .card-text")))

    # Вывести количество найденных элементов для проверки
    print(f"Photos found: {len(photos)}")
    print(f"Names found: {len(names)}")
    print(f"Descriptions found: {len(descriptions)}")

    # Сделать скриншот страницы
    selenium.save_screenshot('result_petfriends.png')

    # Проверить, что количество элементов совпадает
    assert len(photos) == len(names) == len(descriptions), "Количество элементов не совпадает"
