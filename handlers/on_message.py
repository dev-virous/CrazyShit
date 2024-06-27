from typing import Callable
import CrazyShit

class OnMessage:
    def on_message(
        self: "CrazyShit.Client",
        func: Callable = None
    ):
        def decorator(func_: Callable) -> Callable:
            self.add_message_handler(func_, func)
            return func_
        return decorator