from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import data
from urban_routes_page import UrbanRoutesPage
from helpers import retrieve_phone_code

class TestUrbanRoutes:

    def setup_method(self):
        self.driver = webdriver.Firefox()
        self.driver.set_window_size(1920, 1080)
        self.driver.get(data.BASE_URL)

        WebDriverWait(self.driver, 30).until(
            EC.presence_of_element_located((By.CLASS_NAME, "input"))
        )

        self.page = UrbanRoutesPage(self.driver)

    def teardown_method(self):
        self.driver.quit()

    def prepare_order(self):
        self.page.set_route(data.FROM, data.TO)

        self.page.wait_for_route_ready()
        self.page.click_order_taxi()
        self.page.select_comfort()
        import time
        time.sleep(3)

        self.driver.save_screenshot("debug_modal.png")
        print(self.driver.page_source)


        self.page.wait.until(
            EC.visibility_of_element_located(self.page.ORDER_MODAL)
        )

        self.page.wait_for_fare_options()
        self.page.select_comfort()

        self.page.wait_for_phone_input()
        self.page.set_phone(data.PHONE_NUMBER)


        self.page.wait_for_code_input()

        self.page.confirm_code(data.CODE)

    def test_add_card(self):
        self.prepare_order()

        self.page.add_card(
            data.CARD_NUMBER,
            data.CARD_CODE
        )

    def test_debug(self):
        print(hasattr(self, "prepare_order"))

    #
    def test_complete_taxi_flow(self):
        self.page.set_route("East 2nd Street, 601", "1300 1st St")

        self.page.wait_for_route_ready()
        self.page.click_order_taxi()

        self.page.select_comfort()

    # 1. Dirección
    def test_set_route(self):
        self.page.set_route("East 2nd Street, 601", "1300 1st St")
        import time
        time.sleep(10)

        assert "East 2nd Street, 601" in self.page.get_from()
        assert "1300 1st St" in self.page.get_to()

    def test_set_phone(self):
        self.page.set_route("East 2nd Street, 601", "1300 1st St")
        self.page.click_order_taxi()
        self.page.select_comfort()
        self.page.set_phone(data.PHONE_NUMBER)

    def test_set_phone(self):
        self.page.set_route("East 2nd Street, 601", "1300 1st St")


        button = self.page.driver.find_element(*self.page.ORDER_TAXI_BUTTON)
        print("Enabled:", button.is_enabled())

        self.page.click_order_taxi()

    # 5. Código
    def test_confirm_code(self):
        self.page.set_route("East 2nd Street, 601", "1300 1st St")

        self.page.wait_for_route_ready()
        self.page.click_order_taxi()

        self.page.wait_for_fare_options()
        self.page.select_comfort()


        self.page.wait.until(
            EC.element_to_be_clickable(self.page.PHONE_TRIGGER)
        ).click()

        self.page.set_phone(data.PHONE_NUMBER)

    def test_confirm_code_real(self):
        self.page.set_route("East 2nd Street, 601", "1300 1st St")

        self.page.wait_for_route_ready()
        self.page.click_order_taxi()

        self.page.wait_for_fare_options()
        self.page.select_comfort()


    # 7. Manta y pañuelos
    def test_select_blanket_tissues(self):
        self.prepare_order()
        self.page.select_blanket_and_tissues()

        assert self.page.is_blanket_selected()
        assert self.page.is_tissues_selected()

    # 8. Helados
    def test_add_icecream(self):
        self.prepare_order()
        self.page.add_ice_creams(2)

        assert self.page.get_icecream_count() == 2

    # 9. Modal taxi
    def test_order_taxi_modal(self):
        self.page.set_route(data.FROM, data.TO)

        self.page.wait_for_route_ready()
        self.page.click_order_taxi()

        self.page.wait.until(
            EC.presence_of_element_located((By.XPATH, "//div[contains(@class,'modal')]"))
        )

    # 10. Driver info (BONUS)
    def test_driver_info_visible(self):
        self.page.set_route("East 2nd Street, 601", "1300 1st St")

        self.page.close_phone_modal_if_present()

        self.page.click_order_taxi()

        self.page.close_phone_modal_if_present()

        self.page.wait_for_driver()

        assert self.page.is_driver_visible()


    def test_select_comfort(self):
        self.page.set_route("East 2nd Street, 601", "1300 1st St")
        self.page.select_comfort()

        assert True


































































































