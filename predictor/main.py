import time
import requests
from predictor.predict import Predictor
from predictor.sensor_ops import cleanup
INTERVAL_SEC = 1
RECORD_INTERVAL_MINS = 15
MAX_PREDICT_INTERVAL_HOURS = 24
BASE_SERVER_URL = "http://127.0.0.1:5000"

total_data = []

predictor = Predictor()
try:
    while True:
        prediction = predictor.predict_and_fine_tune()
        if prediction == 0:
            requests.get(BASE_SERVER_URL + "/simple_state/off")
        elif prediction == 1:
            requests.get(BASE_SERVER_URL + "/simple_state/on")
        requests.get("data/" + ", ".join(total_data))
except:
    print("Exiting...")
    cleanup()