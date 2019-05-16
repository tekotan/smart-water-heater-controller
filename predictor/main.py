import time
import requests
import predictor.sensor_ops as sns
import predictor.predict as predict

INTERVAL_SEC = 1
RECORD_INTERVAL_MINS = 15
MAX_PREDICT_INTERVAL_HOURS = 24
BASE_SERVER_URL = "http://127.0.0.1:5000"

total_data = []
try:
    while True:
        raw_data = []
        for i in range((RECORD_INTERVAL_MINS*60)/INTERVAL_SEC):
            raw_data.append(sns.get_data()==True)
            time.sleep(INTERVAL_SEC)
        total_data.append(sum(raw_data)/len(raw_data))
        del raw_data
        if len(total_data) > (MAX_PREDICT_INTERVAL_HOURS*60)/RECORD_INTERVAL_MINS:
            del total_data[-1]
        prediction = int(predict.predict(total_data))
        if prediction == 0:
            requests.get(BASE_SERVER_URL + "/simple_state/off")
        elif prediction == 1:
            requests.get(BASE_SERVER_URL + "/simple_state/on")
except:
    sns.cleanup()
    print("Exiting...")