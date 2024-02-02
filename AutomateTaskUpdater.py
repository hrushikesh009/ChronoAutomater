import os
import time

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from constants import CHROME_DRIVER_PATH
from helper.helper import is_smaller_than_9_hours


class ChromeOptionsConfigurator:
    @staticmethod
    def configure(driver_path):
        options = Options()
        prefs = {"profile.default_content_setting_values.notifications": 2}
        options.add_argument("--headless=new")
        options.add_experimental_option("prefs", prefs)
        os.environ['PATH'] += driver_path
        return options


class LoginPage:
    def __init__(self, driver: webdriver.Chrome):
        self.driver = driver

    def _enter_username(self, username):
        username_parts = username.split('@')
        self.driver.find_element(By.ID, 'login_email').send_keys(username_parts[0])

    def _select_sub_domain(self, username):
        sub_domain_element = self.driver.find_element(By.CSS_SELECTOR, "select[name=subdomain]")
        sub_domain_list = sub_domain_element.find_elements(By.CSS_SELECTOR, '*')

        for sub_domain in sub_domain_list:
            if sub_domain.get_attribute('innerHTML').strip() == "@" + username.split('@')[1]:
                sub_domain.click()

    def _enter_otp(self, otp):
        assert len(otp) == 6, "OTP length should be 6"
        otp_input_element_div = self.driver.find_element(By.CSS_SELECTOR, "div[is-input-num=true]")
        otp_input_list_elements = otp_input_element_div.find_elements(By.CSS_SELECTOR, "input[class=otp-input]")

        for i, digit in enumerate(otp):
            otp_input_list_elements[i].send_keys(int(digit))

    def _click_login_button(self):
        login_button = self.driver.find_element(By.CSS_SELECTOR, "div[class=login-btn]")
        login_button.find_element(By.CSS_SELECTOR, "*").click()

    def login(self, username, otp):
        self._enter_username(username)
        self._select_sub_domain(username)
        self._enter_otp(otp)
        self._click_login_button()


class WorkspaceSwitcher:
    def __init__(self, driver:webdriver.Chrome):
        self.driver = driver

    def _click_user_content_box(self):
        self.driver.find_element(By.CSS_SELECTOR, "div[class=user-content-box]").click()
        time.sleep(5)

    def _get_clients_list(self):
        return self.driver.find_elements(By.CSS_SELECTOR, "div[class*=workplace-box]")

    def _get_parent_client_element(self, client):
        return client

    def _get_client_name(self, client):
        return client.find_element(By.TAG_NAME, 'h4').text

    def _click_client_icon(self, client):
        self._get_parent_client_element(client).find_element(By.TAG_NAME, 'i').click()

    def switch_workspace(self, workplace):
        self._click_user_content_box()
        clients_list = self._get_clients_list()

        for client in clients_list:
            if self._get_client_name(client) == workplace:
                self._click_client_icon(client)
                break

class TimeSheetHandler:
    def __init__(self, driver:webdriver.Chrome):
        self.driver = driver

    def _wait_for_element(self, selector, timeout=5):
        return WebDriverWait(self.driver, timeout).until(EC.presence_of_element_located((By.CSS_SELECTOR, selector)))

    def switch_to_timesheet(self):
        time.sleep(2)
        self.driver.find_element(By.CSS_SELECTOR, "div a[href='#/timesheet']").click()

    def _get_task_divs(self):
        return self.driver.find_elements(By.CSS_SELECTOR, "#collapse-1473 > *")

    def _click_child_span(self, child):
        child.find_element(By.TAG_NAME, "span").click()

    def submit_time_block(self, task):
        try:
            self._wait_for_element("div[class=timesheet_tasks__selection]")
            task_list = list(map(str.lower, task.split("|")))

            work_time_element = self._wait_for_element("div[class=work-time]")
            work_time = work_time_element.get_attribute("innerText")

            if is_smaller_than_9_hours(work_time):
                task_divs = self._get_task_divs()

                for task_div in task_divs:
                    parent_ul_element = task_div.find_element(By.TAG_NAME, "ul")
                    child_li_elements = parent_ul_element.find_elements(By.TAG_NAME, "li")

                    for child in child_li_elements:
                        task_text = child.text.strip().lower()
                        if task_text in task_list:
                            self._click_child_span(child)

                # capture the start-timer-btn and intercept the click
                self.driver.find_element(By.CLASS_NAME, "start-timer-btn").click()
                print("Successfully Submitted a TimeBlock!")
            else:
                print("Skipping! Time Blocks are Completed!")

        except TimeoutException:
            print("Skipping! Time Block is Running!")

        except Exception as e:
            print("Something Went Wrong! Please check your TimeSheet!")



class AutomateTaskUpdater(webdriver.Chrome):
    def __init__(self, driver_path=CHROME_DRIVER_PATH):
        super(AutomateTaskUpdater, self).__init__(options=ChromeOptionsConfigurator.configure(driver_path))
        self.implicitly_wait(30)
        self.maximize_window()

        self.login_page = LoginPage(self)
        self.workspace_switcher = WorkspaceSwitcher(self)
        self.time_sheet_handler = TimeSheetHandler(self)

    def landing_page(self, page):
        self.get(page)

    def __exit__(self, exc_type, exc, traceback):
        self.quit()
        # Below Code is used to keep the Browser Open
        # while True:
        #     pass


