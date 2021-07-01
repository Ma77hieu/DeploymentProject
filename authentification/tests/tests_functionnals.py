from decouple import config
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
from substitution.constants import LOG_IN_OK, LOG_OUT_OK, WAIT_TIME
import time


class MySeleniumTests(StaticLiveServerTestCase):
    fixtures = ['users.json']

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.selenium = WebDriver()
        cls.selenium.implicitly_wait(10)

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()

    def test_login(self):
        """test the user login function with good credentials"""
        timeout = 2
        self.selenium.get('{}'.format(self.live_server_url + '/signin'))
        username_input = self.selenium.find_elements_by_name("username")[0]
        username_input.send_keys(config('USER_LOGIN'))
        password_input = self.selenium.find_elements_by_name("password")[0]
        password_input.send_keys(config('USER_PWD'))
        password_input.send_keys(Keys.RETURN)
        WebDriverWait(self.selenium, timeout).until(
            lambda driver: driver.find_element_by_tag_name('body'))
        login = False
        time.sleep(WAIT_TIME)
        if LOG_IN_OK in self.selenium.page_source:
            login = True
        assert login is True

    def test_signup(self):
        """test the user signup function with good credentials"""
        timeout = 5
        self.selenium.get('{}'.format(self.live_server_url + '/signin'))
        match_label_const = {"username": 'SIGNUP_USERNAME',
                             "password": "SIGNUP_PWD",
                             "email": "SIGNUP_EMAIL",
                             "first_name": "SIGNUP_FIRSTNAME"}
        for elem in match_label_const:
            if elem in ["username", "password"]:
                pos = 1
            else:
                pos = 0
            signup_input = self.selenium.find_elements_by_name(elem)[pos]
            signup_input.send_keys(config(match_label_const[elem]))
        signup_input.send_keys(Keys.RETURN)
        WebDriverWait(self.selenium, timeout).until(
            lambda driver: driver.find_element_by_tag_name('body'))
        signup = False
        time.sleep(WAIT_TIME)
        SIGNUP_OK = "Félicitations vous êtes désormais inscrit."
        if SIGNUP_OK in self.selenium.page_source:
            signup = True
        assert signup is True

    def test_logout(self):
        """test the logout function"""
        self.selenium.get('{}'.format(self.live_server_url + '/home'))
        timeout = 2
        collapsed_navbar_button = self.selenium.find_element_by_class_name(
            "navbar-toggler-icon")
        collapsed_navbar_button.click()
        signout_button = self.selenium.find_element_by_name("logout_button")
        signout_button.click()
        WebDriverWait(self.selenium, timeout).until(
            lambda driver: driver.find_element_by_tag_name('body'))
        logout = False
        time.sleep(WAIT_TIME)
        if LOG_OUT_OK in self.selenium.page_source:
            logout = True
        assert logout is True
