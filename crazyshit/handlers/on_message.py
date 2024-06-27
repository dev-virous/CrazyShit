from typing import Callable
import crazyshit


class OnMessage:
    def on_message(self: "crazyshit.Client", func: Callable = None):
        def decorator(func_: Callable) -> Callable:
            self.add_message_handler(func_, func)
            return func_

        return decorator
