from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import crazyshit


class SendMessage:
    async def send_message(
        self: "crazyshit.Client",
        to: str,
        text: str,
    ):
        """Sending message to specific chat.

        Args:
            to (str): The chat title.
            text (str): Text message.
        """
        WebDriverWait(self.session, 30).until(
            ec.presence_of_element_located(
                (By.XPATH, f"//span[contains(@title, '{to}')]")
            )
        ).click()
        textbox = WebDriverWait(self.session, 30).until(
            ec.presence_of_element_located((By.XPATH, "//div[@spellcheck='true']"))
        )
        textbox.send_keys(text)
        textbox.send_keys(Keys.ENTER)
        textbox.send_keys(Keys.ESCAPE)
