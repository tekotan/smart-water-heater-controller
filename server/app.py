from flask import Flask
import boiler.boiler_actions as core
import server.mechanical_ops as mo

app = Flask(__name__)


@app.route("/get_simple_state")
def get_simple_state():
    if core.my_boiler.on == True:
        return "on"
    else:
        return "off"


@app.route("/get_boiler_state")
def get_full_state():
    return core.my_boiler.get_state()


@app.route("/simple_state/<simple_state>")
def turn_on(simple_state):
    if simple_state == "on":
        core.turn_on()
    elif simple_state == "off":
        core.turn_off()


@app.route("/<int:on_or_off>/<int:vacation>/<int:temperature_perc>/<int:always_on>")
def change_state(on_or_off, vacation, temperature_perc, always_on):
    core.change_state(on_or_off, vacation, temperature_perc, always_on)
    # Dummy servo spin
    temp_diff = temperature_perc - core.my_boiler.temperature_perc
    mo.update(temp_diff / 100)
    return "Worked"


@app.route("/data/<data_list>")
def change_data(data_list):
    core.my_boiler.change_data(data_list)


@app.route("/get_data")
def get_data():
    return ", ".join(core.my_boiler.data)


def run():
    app.run(host="0.0.0.0")


if __name__ == "__main__":
    app.run()
