from guizero import App, Text, Slider, CheckBox, PushButton, Picture, ButtonGroup, Box
import actions as actions

app = App(title="Smart Boiler Controller", layout="grid", width=480, height=200)
title = Text(app, text="Smart Boiler Controller", size=20, grid=[0, 0, 2, 1])
title_message = Text(
    app,
    text="The Boiler is Currently " + actions.get_on_or_off(),
    size=15,
    grid=[0, 1, 2, 1],
)

controls = Box(app, grid=[0, 2], width=240, height=210)
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
update = PushButton(
    controls,
    text="Update Settings",
    padx=5,
    pady=5,
    command=actions.change_state,
    args=[temp_slider, simple_radio, vacation, always_on],
)
update.bg = "blue"
controls.repeat(
    10000, actions.update_gui, args=[temp_slider, simple_radio, vacation, always_on]
)

data = Box(app, grid=[1, 2], width=240, height=210)
data.bg = "beige"
data_title = Text(data, text="Data", size=18)
graph = Picture(data, image="test.png", width=150, height=150)
data.repeat(900000, actions.update_graph, args=[graph])
app.display()
