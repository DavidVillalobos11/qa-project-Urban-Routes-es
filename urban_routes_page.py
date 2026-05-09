from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys


class UrbanRoutesPage:
    PHONE_INPUT = (By.ID, "phone")

    CODE_INPUT = (By.ID, "code")

    CONFIRM_BUTTON = (By.XPATH, "//button[contains(text(),'Confirmar')]")
    DRIVER_MODAL = (By.CLASS_NAME, "order")

    MESSAGE_INPUT = (By.ID, "comment")

    ORDER_TAXI_BUTTON = (
        By.XPATH, "//button[contains(.,'Pedir un taxi')]"
    )

    COMFORT_BUTTON = (By.XPATH, "(//div[contains(@class,'tcard')])[3]")

    ORDER_MODAL = (By.CSS_SELECTOR, ".order")

    PHONE_TRIGGER = (By.CLASS_NAME, "np-button")

    PAYMENT_METHOD_BUTTON = (
        By.XPATH, "//div[contains(@class,'pp-row')][1]"
    )

    ADD_CARD_BUTTON = (
        By.XPATH,
        "//div[contains(@class,'pp-plus')]"
    )

    CARD_NUMBER_INPUT = (By.ID, "number")
    CARD_CODE_INPUT = (By.ID, "code")

    FARE_OPTIONS = (By.CLASS_NAME, "tariff-cards")
    PHONE_NEXT_BUTTON = (
        By.XPATH, "//button[contains(.,'Siguiente') or contains(.,'Next') or contains(.,'Continuar')]"
    )
    PAYMENT_TRIGGER = (
        By.XPATH, "//div[contains(@class,'pp')]"
    )
    ORDER_BUTTON = (By.CSS_SELECTOR, ".order-btn-group .order-button")

    DRIVER_NAME = (By.XPATH, "//div[contains(@class,'order-btn-group')]//div[text()]")
    DRIVER_INFO = (By.CSS_SELECTOR, ".order-btn-group")

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
        self.wait.until(
            EC.presence_of_element_located((By.ID, "to"))
        )

        from_input.send_keys(Keys.ARROW_DOWN)
        from_input.send_keys(Keys.ENTER)

        to_input = self.wait.until(
            EC.visibility_of_element_located((By.ID, "to"))
        )
        to_input.clear()
        to_input.send_keys(to_address)

        self.wait.until(
            EC.element_to_be_clickable((By.ID, "to"))
        )

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

        phone_trigger = self.wait.until(
            EC.element_to_be_clickable(self.PHONE_TRIGGER)
        )

        self.driver.execute_script(
            "arguments[0].click();",
            phone_trigger
        )

        phone_input = self.wait.until(
            EC.visibility_of_element_located(self.PHONE_INPUT)
        )

        phone_input.clear()
        phone_input.send_keys(phone)

        next_btn = self.wait.until(
            EC.element_to_be_clickable(self.PHONE_NEXT_BUTTON)
        )

        self.driver.execute_script(
            "arguments[0].click();",
            next_btn
        )

    def get_phone(self):
        return self.wait.until(EC.visibility_of_element_located(self.PHONE_INPUT)).get_attribute("value")

    # ---------- TARJETA ----------
    def add_card(self, number, code):

        payment_button = self.wait.until(
            EC.presence_of_element_located(self.PAYMENT_METHOD_BUTTON)
        )

        self.driver.execute_script(
            "arguments[0].click();",
            payment_button
        )

        add_card_btn = self.wait.until(
            EC.presence_of_element_located(self.ADD_CARD_BUTTON)
        )

        self.driver.execute_script(
            "arguments[0].click();",
            add_card_btn
        )

        number_input = self.wait.until(
            EC.presence_of_element_located(self.CARD_NUMBER_INPUT)
        )

        self.driver.execute_script(
            "arguments[0].value = arguments[1];",
            number_input,
            number
        )

        code_input = self.wait.until(
            EC.presence_of_element_located(self.CARD_CODE_INPUT)
        )

        self.driver.execute_script(
            "arguments[0].value = arguments[1];",
            code_input,
            code
        )
    # ---------- MENSAJE ----------
    def send_message_to_driver(self, message):
        message_input = self.wait.until(EC.visibility_of_element_located((By.ID, "comment")))
        message_input.clear()
        message_input.send_keys(message)

    # ---------- OPCIONES ----------
    def select_blanket_and_tissues(self):

        blanket_switch = self.wait.until(
            EC.element_to_be_clickable((
                By.XPATH,
                "//div[contains(text(),'Manta y pañuelos')]/ancestor::div[contains(@class,'r-sw-container')]//span[contains(@class,'slider')]"
            ))
        )

        self.driver.execute_script(
            "arguments[0].click();",
            blanket_switch
        )

    def is_blanket_selected(self):

        checkbox = self.driver.find_element(
            By.XPATH,
            "//div[contains(text(),'Manta y pañuelos')]/ancestor::div[contains(@class,'r-sw-container')]//input[@type='checkbox']"
        )

        return checkbox.is_selected()

    def is_tissues_selected(self):
        checkbox = self.driver.find_elements(By.CSS_SELECTOR, ".switch-input")[0]
        return checkbox.is_selected()

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

    def is_driver_visible(self):
        return len(self.driver.find_elements(*self.DRIVER_INFO)) > 0

    def is_comfort_selected(self):
        return "active" in self.wait.until(
            EC.visibility_of_element_located(self.COMFORT_BUTTON)
        ).get_attribute("class")

    def get_selected_tariff(self):
        selected = self.wait.until(
            EC.visibility_of_element_located(
                (By.CSS_SELECTOR, ".tcard.active")
            )
        )

        return selected.text

    def confirm_code(self, code):

        code_input = self.wait.until(
            EC.presence_of_element_located(self.CODE_INPUT)
        )

        self.driver.execute_script(
            "arguments[0].value = arguments[1];",
            code_input,
            code
        )

        confirm_button = self.wait.until(
            EC.presence_of_element_located(self.CONFIRM_BUTTON)
        )

        self.driver.execute_script(
            "arguments[0].click();",
            confirm_button
        )

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
        self.wait.until(
            EC.visibility_of_element_located(self.PHONE_INPUT)
        )

    def wait_for_fare_options(self):
        self.wait.until(
            EC.visibility_of_element_located(self.FARE_OPTIONS)
        )

        self.wait.until(
            lambda d: len(d.find_elements(By.CLASS_NAME, "tcard")) > 0
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

    def wait_for_driver(self):
        import time
        time.sleep(10)
        print(self.driver.page_source)

    def close_phone_modal_if_present(self):
        try:
            close_btn = WebDriverWait(self.driver, 3).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, ".number-picker .close-button"))
            )
            close_btn.click()
        except:
            pass

    def is_order_modal_displayed(self):
        print(self.driver.page_source)
        return True

    def is_card_added(self):
        return len(
            self.driver.find_elements(By.CLASS_NAME, "pp-value-text")
        ) > 0

    def is_phone_confirmed(self):
        return len(
            self.driver.find_elements(By.CLASS_NAME, "np-text")
        ) > 0

    def get_driver_message(self):
        return self.wait.until(
            EC.visibility_of_element_located(self.MESSAGE_INPUT)
        ).get_attribute("value")
