from selenium import webdriver
import data

from urban_routes_page import UrbanRoutesPage
from helpers import retrieve_phone_code
import time


class TestUrbanRoutes:

    def setup_method(self):
        self.driver = webdriver.Firefox()

        self.driver.set_window_size(1920, 1080)

        self.driver.get(data.BASE_URL)

        self.driver.implicitly_wait(5)

        self.page = UrbanRoutesPage(self.driver)

    def teardown_method(self):
        self.driver.quit()

    def prepare_order(self):
        self.page.set_route(data.FROM, data.TO)

        self.page.wait_for_route_ready()

        self.page.click_order_taxi()

        self.page.wait_for_fare_options()

        self.page.select_comfort()

    # 1. Dirección
    def test_set_route(self):

        self.page.set_route(data.FROM, data.TO)

        assert self.page.get_from() == data.FROM
        assert self.page.get_to() == data.TO

    # 2. Tarifa comfort
    def test_select_comfort(self):

        self.prepare_order()

        assert "Comfort" in self.page.get_selected_tariff()

    # 3. Teléfono
    def test_set_phone(self):

        self.prepare_order()

        self.page.set_phone(data.PHONE_NUMBER)

        assert data.PHONE_NUMBER[-4:] in self.page.get_phone()

    # 4. Tarjeta
    def test_add_card(self):
        self.prepare_order()

        self.page.set_phone(data.PHONE_NUMBER)

        self.page.add_card(
            data.CARD_NUMBER,
            data.CARD_CODE
        )

        assert self.page.is_card_added()

    # 5. Código
    def test_confirm_code(self):

        self.prepare_order()

        self.page.set_phone(data.PHONE_NUMBER)

        code = retrieve_phone_code(self.driver)

        self.page.confirm_code(code)

        assert self.page.is_phone_confirmed()

    # 6. Mensaje conductor
    def test_driver_message(self):

        self.prepare_order()

        self.page.send_message_to_driver("Hola")

        assert self.page.get_driver_message() == "Hola"

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

        self.prepare_order()

        assert self.page.is_order_modal_displayed()

    # BONUS
    def test_driver_info_visible(self):

        self.prepare_order()

        self.page.wait_for_driver()

        assert self.page.is_driver_visible()


































































































