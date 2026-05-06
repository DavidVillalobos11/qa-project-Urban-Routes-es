from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from webdriver_manager.firefox import GeckoDriverManager
import time


class UrbanRoutesPage:
    ORDER_TAXI_BUTTON = (
        By.XPATH, "//button[contains(.,'Pedir un taxi')]"
    )

    COMFORT_BUTTON = (By.XPATH, "(//div[contains(@class,'tcard')])[3]")

    ORDER_MODAL = (By.XPATH, "//div[contains(@class,'modal') and contains(@class,'show')]")

    PHONE_TRIGGER = (By.CLASS_NAME, "np-button")

    PAYMENT_METHOD_BUTTON = (
        By.XPATH, "//div[contains(@class,'pp-row')][1]"
    )

    ADD_CARD_BUTTON = (
        By.XPATH, "//button[contains(.,'Agregar') or contains(.,'Add')]"
    )

    CARD_NUMBER_INPUT = (By.CSS_SELECTOR, "input[name='number']")
    CARD_CODE_INPUT = (By.CSS_SELECTOR, "input[name='code']")

    FARE_OPTIONS = (By.CLASS_NAME, "tariff-cards")
    PHONE_NEXT_BUTTON = (
        By.XPATH, "//button[contains(.,'Siguiente') or contains(.,'Next') or contains(.,'Continuar')]"
    )
    PAYMENT_TRIGGER = (
        By.XPATH, "//div[contains(@class,'pp')]"
    )
    ORDER_BUTTON = (By.CSS_SELECTOR, ".order-btn-group .order-button")

    DRIVER_NAME = (By.XPATH, "//div[contains(@class,'order-btn-group')]//div[text()]")
    DRIVER_INFO = (By.CSS_SELECTOR, ".o-d-h")

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def set_route(self, from_address, to_address):
        from_input = self.wait.until(
            EC.visibility_of_element_located((By.ID, "from"))
        )
        from_input.clear()
        from_input.send_keys(from_address)

        # pequeña pausa para que carguen sugerencias
        import time
        time.sleep(1)

        from_input.send_keys(Keys.ARROW_DOWN)
        from_input.send_keys(Keys.ENTER)

        to_input = self.wait.until(
            EC.visibility_of_element_located((By.ID, "to"))
        )
        to_input.clear()
        to_input.send_keys(to_address)

        time.sleep(1)

        to_input.send_keys(Keys.ARROW_DOWN)
        to_input.send_keys(Keys.ENTER)


    def get_from(self):
        return self.driver.find_element(By.ID, "from").get_attribute("value")

    def get_to(self):
        return self.driver.find_element(By.ID, "to").get_attribute("value")

    # ---------- TARIFA ----------
    def select_comfort(self):
        comfort = self.wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, "//div[contains(@class,'tcard')][.//div[contains(text(),'Comfort')]]")
            )
        )
        self.driver.execute_script("arguments[0].click();", comfort)

    def click_order_taxi(self):
        button = self.wait.until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'Pedir un taxi')]"))
        )
        button.click()

    # ---------- TELÉFONO ----------
    def set_phone(self, phone):
        phone_input = self.wait.until(
            EC.presence_of_element_located((By.ID, "phone"))
        )

        self.driver.execute_script("arguments[0].scrollIntoView(true);", phone_input)
        self.wait.until(EC.element_to_be_clickable((By.ID, "phone")))

        phone_input.clear()
        phone_input.send_keys(phone)


        try:
            next_btn = self.wait.until(
                EC.element_to_be_clickable(self.PHONE_NEXT_BUTTON)
            )
            self.driver.execute_script("arguments[0].click();", next_btn)
        except:
            pass

    def get_phone(self):
        return self.wait.until(EC.visibility_of_element_located(self.PHONE_INPUT)).get_attribute("value")

    # ---------- TARJETA ----------
    def add_card(self, number, code):


        payment_trigger = self.wait.until(
            EC.element_to_be_clickable(self.PAYMENT_METHOD_BUTTON)
        )
        payment_trigger.click()


        payment_modal = self.wait.until(
            EC.visibility_of_element_located((By.CLASS_NAME, "payment-picker"))
        )


        add_card_btn = self.wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, "//button[contains(., 'Agregar') or contains(., 'Add')]")
            )
        )
        add_card_btn.click()


        number_input = self.wait.until(
            EC.visibility_of_element_located(self.CARD_NUMBER_INPUT)
        )
        number_input.clear()
        number_input.send_keys(number)


        code_input = self.wait.until(
            EC.visibility_of_element_located(self.CARD_CODE_INPUT)
        )
        code_input.clear()
        code_input.send_keys(code)


        save_btn = self.wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, "//button[contains(., 'Guardar') or contains(., 'Save')]")
            )
        )
        save_btn.click()
    # ---------- MENSAJE ----------
    def set_message(self, message):
        message_input = self.wait.until(EC.visibility_of_element_located((By.ID, "comment")))
        message_input.clear()
        message_input.send_keys(message)

    def get_message(self):
        return self.wait.until(EC.visibility_of_element_located((By.ID, "comment"))).get_attribute("value")

    # ---------- OPCIONES ----------
    def select_blanket_and_tissues(self):
        self.wait.until(EC.element_to_be_clickable((By.ID, "blanket"))).click()
        self.wait.until(EC.element_to_be_clickable((By.ID, "tissues"))).click()

    def is_blanket_selected(self):
        return "active" in self.driver.find_element(By.ID, "blanket").get_attribute("class")

    def is_tissues_selected(self):
        return "active" in self.driver.find_element(By.ID, "tissues").get_attribute("class")

    # ---------- HELADOS ----------
    def add_ice_creams(self, amount):
        for _ in range(amount):
            self.wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "counter-plus"))).click()

    def get_icecream_count(self):
        value = self.wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "counter-value"))).text
        return int(value)

    # ---------- PEDIDO ----------
    def order_taxi(self):
        order_button = self.wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, "(//button[contains(@class,'order-button')])[1]")
            )
        )
        order_button.click()

    # ---------- DRIVER ----------
    def wait_driver(self):
        self.wait.until(EC.visibility_of_element_located(self.DRIVER_MODAL))

    def is_driver_visible(self):
        return len(self.driver.find_elements(*self.DRIVER_INFO)) > 0

    def is_comfort_selected(self):
        cards = self.driver.find_elements(By.CLASS_NAME, "tcard")
        return "active" in cards[1].get_attribute("class")

    def confirm_code(self, code):

        code_input = self.wait.until(
            EC.visibility_of_element_located(
                (By.XPATH, "//input[contains(@type,'tel') or contains(@name,'code')]")
            )
        )

        code_input.send_keys(code)

        confirm_button = self.wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, "//button[contains(.,'Confirm') or contains(.,'Aceptar')]")
            )
        )

        self.driver.execute_script("arguments[0].click();", confirm_button)

    def wait_for_code_input(self):
        self.wait.until(
            EC.visibility_of_element_located((By.ID, "code"))
        )

    def trigger_phone_confirmation(self):


        button = self.wait.until(
            EC.presence_of_element_located(
                (By.XPATH, "//button[contains(.,'Next') or contains(.,'Siguiente') or contains(.,'Continuar')]")
            )
        )


        self.driver.execute_script("arguments[0].scrollIntoView(true);", button)
        self.driver.execute_script("arguments[0].click();", button)


        self.wait.until(
            EC.presence_of_element_located(
                (By.XPATH, "//input[contains(@type,'tel') or contains(@name,'code')]")
            )
        )

    def wait_for_phone_input(self):
        import time


        time.sleep(2)

        self.wait.until(
            EC.presence_of_element_located(
                (By.NAME, "phone")
            )
        )

        time.sleep(1)

    def wait_for_order_button(self):
        self.wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button.button_full"))
        )

    def wait_for_fare_options(self):
        self.wait.until(
            EC.visibility_of_element_located(self.FARE_OPTIONS)
        )

        self.wait.until(
            lambda d: len(d.find_elements(By.CLASS_NAME, "tcard")) > 0
        )

    def select_first_tariff(self):
        self.wait.until(
            EC.element_to_be_clickable(self.FIRST_TARIFF)
        ).click()

    def wait_for_comfort(self):
        self.wait.until(
            EC.presence_of_element_located(
                (By.XPATH, "//*[contains(text(),'Comfort')]")
            )
        )

    def wait_for_route_ready(self):
        self.wait.until(
            EC.element_to_be_clickable(self.ORDER_TAXI_BUTTON)
        )

    def wait_for_modal_visible(self):
        self.wait.until(
            lambda d: any(
                m.is_displayed()
                for m in d.find_elements(By.XPATH, "//div[contains(@class,'modal')]")
            )
        )

    def wait_for_driver_info(self):
        self.wait.until(
            EC.visibility_of_element_located((By.CLASS_NAME, "order"))
        )

    def wait_for_driver(self):
        print("🔎 Buscando texto en el DOM...")

        time.sleep(5)  # pausa temporal para debug

        html = self.driver.page_source

        if "Más información" in html:
            print("✅ TEXTO SÍ ESTÁ EN EL DOM")
        else:
            print("❌ TEXTO NO ESTÁ EN EL DOM")

        self.wait.until(
            EC.presence_of_element_located(self.DRIVER_INFO)
        )

    def close_phone_modal_if_present(self):
        try:
            close_btn = WebDriverWait(self.driver, 3).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, ".number-picker .close-button"))
            )
            close_btn.click()
        except:
            pass
