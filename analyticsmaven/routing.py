from channels.routing import route
from .consumers import ws_connect, ws_disconnect, ws_message

routing = [
    route('websocket.connect', ws_connect, path="^/messagebox/"),
    route("websocket.receive", ws_message),
    route('websocket.disconnect', ws_disconnect),
]
