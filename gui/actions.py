import requests

BASE_SERVER_URL = "http://192.168.43.129:5000"


def get_on_or_off():
    state = requests.get(f"{BASE_SERVER_URL}/get_simple_state")
    return state.text


def update_gui(temp_slider, simple_radio, vacation, always_on):
    state = requests.get(f"{BASE_SERVER_URL}/get_boiler_state")
    values = state.text.split(", ")
    temp_slider.value = int(values[0])
    if int(values[1]):
        simple_radio.value = "on"
    else:
        simple_radio.value = "off"
    vacation.value = int(values[2])  # 1 for check, 0 for unchecked
    always_on.value = int(values[3])  # See above


def change_state(temp_slider, simple_radio, vacation, always_on):
    url = f"{int(simple_radio.value == 'on')}/{vacation.value}/{temp_slider.value}/{always_on.value}"
    requests.get(f"{BASE_SERVER_URL}/{url}")


def update_graph(pic_obj):
    pass
