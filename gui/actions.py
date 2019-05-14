import requests

BASE_SERVER_URL = "http://127.0.0.1:5000"


def get_on_or_off():
    state = requests.get(f"{BASE_SERVER_URL}/get_simple_state")
    return state.text


def update_gui(temp_slider, simple_radio, vacation, always_on):
    state = requests.get(f"{BASE_SERVER_URL}/get_boiler_state")
    values = state.text.split(",")
    temp_slider.value = int(values[0])
    simple_radio.value = values[1]
    vacation.value = int(values[2])  # 1 for check, 0 for unchecked
    always_on.value = int(values[3])  # See above


def change_state(temp_slider, simple_radio, vacation, always_on):
    url = f"{simple_radio.value}/{vacation.value}/{temp_slider.value}/{always_on.value}"
    requests.get(f"{BASE_SERVER_URL}/{url}")


def update_graph(pic_obj):
    pass
