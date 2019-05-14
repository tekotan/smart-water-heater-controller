from guizero import App, Text, Slider, CheckBox, PushButton, Picture, ButtonGroup, Box
import actions as actions

app = App(title="Smart Boiler Controller", layout="grid", width=480, height=320)
title = Text(app, text="Smart Boiler Controller", size=30, grid=[0, 0, 2, 1])
title_message = Text(
    app,
    text="The Boiler is Currently " + actions.get_boiler_state(),
    size=23,
    grid=[0, 1, 2, 1],
)

controls = Box(app, grid=[0, 2], width=240, height=310)
controls.repeat(1000, actions.update_gui, args=())
controls.bg = "beige"
controls_title = Text(controls, text="Controls", size=18)
temp_title = Text(controls, text="Temperature", size=12)
temp_slider = Slider(controls)
temp_slider.text_size = 7
simple_title = Text(controls, text="Simple Controls for Boiler", size=12)
simple_radio = ButtonGroup(
    controls, options=["on", "off"], horizontal=True, selected=actions.get_on_or_off()
)
vacation = CheckBox(controls, text="Vacation Settings")
always_on = CheckBox(controls, text="Always On")
update = PushButton(controls, text="Update Settings", padx=5, pady=5)
update.bg = "blue"

data = Box(app, grid=[1, 2], width=240, height=310)
data.bg = "beige"
data_title = Text(data, text="Data", size=18)
graph = Picture(data, image="test.png", width=200, height=200)
data.repeat(1000, actions.update_graph, args=[graph])
app.display()