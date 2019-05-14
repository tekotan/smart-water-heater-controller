import requests

BASE_SERVER_URL = "127.0.0.1:5000"


def change_temperature(slider_value):
    pass


def get_on_or_off():
    state = requests.get(f"{BASE_SERVER_URL}/get_simple_state")
    return state.text


def update_gui():
    state = requests.get(f"{BASE_SERVER_URL}/get_boiler_state")

    pass


def get_on_or_off():

    return "on"


def update_graph(pic_obj):
    pass
