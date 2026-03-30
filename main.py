from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
import data
from helpers import retrieve_phone_code


class UrbanRoutesPage:

    DRIVER_MODAL = (By.CLASS_NAME, "driver-info")

    def __init__(self, driver):
        self.driver = driver

    def wait_driver(self):
        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(self.DRIVER_MODAL)
        )

    def set_route(self, from_text, to_text):
        self.driver.find_element(By.ID, "from").send_keys(from_text)
        self.driver.find_element(By.ID, "to").send_keys(to_text)

    def select_comfort(self):
        self.driver.find_element(By.XPATH, "//div[text()='Comfort']").click()

    def set_phone(self, phone):
        self.driver.find_element(By.ID, "phone").send_keys(phone)

    def add_card(self, number, code):
        self.driver.find_element(By.CLASS_NAME, "pp-button").click()
        self.driver.find_element(By.ID, "number").send_keys(number)

        code_input = self.driver.find_element(By.ID, "code")
        code_input.send_keys(code)

        code_input.send_keys(Keys.TAB)

        self.driver.find_element(By.XPATH, "//button[text()='Link']").click()

    def set_message(self, message):
        self.driver.find_element(By.ID, "comment").send_keys(message)

    def select_blanket_and_tissues(self):
        self.driver.find_element(By.ID, "blanket").click()
        self.driver.find_element(By.ID, "tissues").click()

    def add_ice_creams(self, amount):
        for _ in range(amount):
            self.driver.find_element(By.CLASS_NAME, "counter-plus").click()

    def order_taxi(self):
        self.driver.find_element(By.XPATH, "//button[text()='Pedir taxi']").click()

class TestUrbanRoutes:

    def setup_method(self):
        self.driver = webdriver.Chrome()
        self.driver.get(data.BASE_URL)

    def teardown_method(self):
        self.driver.quit()

    def test_order_taxi(self):
        page = UrbanRoutesPage(self.driver)

        page.set_route("A", "B")
        page.select_comfort()
        page.set_phone(data.PHONE_NUMBER)

        code = retrieve_phone_code(self.driver)
        print(code)

        page.add_card("4111111111111111", "123")
        page.set_message("Por favor llegar rápido")
        page.select_blanket_and_tissues()
        page.add_ice_creams(2)
        page.order_taxi()

    
        page.wait_driver()


































































































