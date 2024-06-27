from .send_message import SendMessage
from .get_last_message import GetLastMessage
from .esc import Escap


class Methods(SendMessage, GetLastMessage, Escap):
    pass
