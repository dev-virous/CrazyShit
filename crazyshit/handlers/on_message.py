from typing import Callable
import crazyshit


class OnMessage:
    def on_message(self: "crazyshit.Client", func: Callable = None):
        """An decorator add new messages handler."""
        def decorator(func_: Callable) -> Callable:
            self.add_message_handler(func_, func)
            return func_

        return decorator
