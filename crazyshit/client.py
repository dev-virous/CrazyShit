from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By
from typing import Callable
from .methods import Methods
from .handlers import Handlers
from typing import Optional
from time import sleep, time
from re import findall
from html import unescape
from .types.update import dtc
import phonenumbers, os, threading, sys
import asyncio, datetime


class Client(Methods, Handlers):
    """
        Client class for handling automation tasks for a WhatsApp bot using Selenium.

        Args:
            client_name (str): The name of the client.
            number (str): A unique identifier (phone number) for the client.
            options (Optional[webdriver.ChromeOptions], optional): Chrome options for configuring the WebDriver instance.
            executable_path (str, optional): Path to the ChromeDriver executable. Default is None, in which case the default system path for the ChromeDriver is used.
    """
    def __init__(
        self,
        client_name: str,
        number: str,
        options: Optional[webdriver.ChromeOptions] = None,
        executable_path: str = None,
    ):
        number = phonenumbers.parse(number)
        self.country_code = number.country_code
        self.national_number = number.national_number
        if options is None:
            options = webdriver.ChromeOptions()
            options.add_argument("--disable-extensions")
            options.add_argument("--disable-gpu")
            options.add_experimental_option("excludeSwitches", ["enable-automation"])
            options.add_experimental_option("useAutomationExtension", False)
            options.add_experimental_option(
                "prefs",
                {
                    "credentials_enable_service": False,
                    "profile.password_manager_enabled": False,
                    "profile.default_content_setting_values.notifications": 2,
                    "profile.default_content_settings.popups": 2,
                },
            )
        self.options = options
        self.options.add_argument(
            "user-data-dir={path}".format(
                path=os.path.join(sys.path[0] + f"/session/{self.national_number}")
            )
        )
        service = Service(executable_path=executable_path)
        self.session = webdriver.Chrome(options=self.options, service=service)
        self.session.get("https://web.whatsapp.com/")
        self.client_name = client_name
        self.__message_handlers = []

    async def start(self):
        if not os.path.exists(
            os.path.join(sys.path[0] + f"/session/{self.national_number}")
        ):
            while not findall(r'data-ref="(.*?)"', self.session.page_source):
                sleep(1)
            print(f"[{self.client_name}] Wait To Click Link With Phone Number")
            WebDriverWait(self.session, 30).until(
                ec.element_to_be_clickable((By.CSS_SELECTOR, "span[role='button']"))
            ).click()
            print(f"[{self.client_name}] Wait To Enter Phone Number")
            element = WebDriverWait(self.session, 30).until(
                ec.presence_of_element_located((By.CSS_SELECTOR, "input[type='text']"))
            )
            self.session.execute_script(
                f'arguments[0].value = "{self.country_code}";', element
            )
            element.send_keys(self.national_number)
            print(f"[{self.client_name}] Phone Number Entered")
            WebDriverWait(self.session, 30).until(
                ec.element_to_be_clickable(
                    (
                        By.XPATH,
                        '//*[@id="app"]/div/div[2]/div[3]/div[1]/div/div[3]/div[2]/button',
                    )
                )
            ).click()
            element = WebDriverWait(self.session, 30).until(
                ec.presence_of_element_located((By.CSS_SELECTOR, "[data-link-code]"))
            )
            code = element.get_attribute("data-link-code").replace(",", " ")
            print(f"[{self.client_name}] Auth Code: {code}")
            start_time = time()
            is_login = False
            while time() - start_time < 60:
                if findall(
                    r'role="button"\s*?aria-label="(.*?)"', self.session.page_source
                ):
                    is_login = True
                    break
            if not is_login:
                print(f"[{self.client_name}] Code Expire")
                self.session.quit()
                raise SystemError(f"[{self.client_name}] Code Expire")
            else:
                print(f"[{self.client_name}] Login Successfully")
        else:
            print(f"[{self.client_name}] Login Successfully")
        task = threading.Thread(target=asyncio.run, args=(self.get_updates(),))
        task.start()

    async def get_updates(self):
        while True:
            page_source = unescape(self.session.page_source)
            title = findall(
                r'dir="auto"\s*?title=".*?"\s*?aria-label=".*?"\s*?class=".*?"\s*?style=".*?">\s*?(.*?)\s*?</span>',
                page_source,
            )
            img = findall(
                r'<img\s*?src="(.*?)"\s*?alt=".*?"\s*?draggable=".*?"\s*?class=".*?"\s*?tabindex=".*?"\s*?style=".*?"',
                page_source,
            )
            text = findall(
                r'<span\s*?dir="(?:ltr|rtl)"\s*?aria-label=".*?"\s*?class=".*?"\s*?style=".*?">\s*?(.*?)\s*?</span>',
                page_source,
            )
            for title, img, text in zip(title, img, text):
                title, img, message = title.strip(), img.strip(), text.strip()
                for i, (func) in enumerate(self.__message_handlers):
                    if func["filter_func"](message):
                        update = {
                            "chat": {"title": title, "photo": img},
                            "date": datetime.datetime.now(),
                            "text": message,
                        }
                        try:
                            await func["func"](self, dtc(update))
                        except:
                            pass

    def add_message_handler(self, func_: Callable, func: Callable = None):
        self.__message_handlers.append({"func": func_, "filter_func": func})
