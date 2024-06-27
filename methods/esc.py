from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import CrazyShit

class Escap:
    async def ESCAPE(
        self: "CrazyShit.Client",
    ):
        actions = ActionChains(self.session)
        actions.send_keys(Keys.ESCAPE)
        actions.perform()