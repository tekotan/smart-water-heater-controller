from flask import Flask
import boiler.boiler_actions as core

app = Flask(__name__)


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
    try:
        core.change_state(on_or_off, vacation, temperature_perc, always_on)
        return "Worked"
    except:
        return "There was an unexpected issue"


if __name__ == "__main__":
    app.run()
