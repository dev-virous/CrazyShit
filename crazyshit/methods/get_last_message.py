from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from html import unescape
import crazyshit


class GetLastMessage:
    async def get_last_message(self: "crazyshit.Client", from_: str):
        """Get last message from specific chat."""
        WebDriverWait(self.session, 30).until(
            ec.presence_of_element_located(
                (By.XPATH, f"//span[contains(@title, '{from_}')]")
            )
        ).click()
        element = WebDriverWait(self.session, 30).until(
            ec.presence_of_element_located(
                (
                    By.CSS_SELECTOR,
                    "span[dir='ltr'][aria-label=''], span[dir='rtl'][aria-label='']",
                )
            )
        )
        message = unescape(element.text)
        ActionChains(self.session).send_keys(Keys.ESCAPE).perform()
        return message
