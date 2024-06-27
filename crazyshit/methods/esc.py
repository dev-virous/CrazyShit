from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import crazyshit


class Escap:
    async def ESCAPE(
        self: "crazyshit.Client",
    ):
        actions = ActionChains(self.session)
        actions.send_keys(Keys.ESCAPE)
        actions.perform()
