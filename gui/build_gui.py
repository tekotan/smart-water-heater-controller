import PySimpleGUI as sg
from . import actions

control_column = [
    [sg.Text("Controls", justification="center", font=("Helvetica", 15), size=(23, 1))],
    [
        sg.Text("Boiler Temperature: "),
        sg.Slider(
            range=(1, 100), orientation="h", size=(10, 20), default_value=25, key="temp"
        ),
    ],
    [
        sg.Text("Simple Control:"),
        sg.Radio("On", "RADIO1", key="on", default=True, size=(5, 1)),
        sg.Radio("Off", "RADIO1", key="off"),
    ],
    [sg.Checkbox("Vacation Setting", key="vac_set")],
    [sg.Checkbox("Keep Boiler On Always", key="always_on")],
    [
        sg.Text("Power Saving Level"),
        sg.InputOptionMenu(("High", "Medium", "Low"), key="saver_level"),
    ],
    [sg.Button("Update Settings")],
]
graph_column = [
    [
        sg.Text(
            "Data Collected",
            font=("Helvetica", 15),
            justification="center",
            size=(27, 1),
        )
    ],
    [sg.Image(filename="test.png", key="graph", size=(300, 300))],
]
layout = [
    [
        sg.Text(
            "The boiler is currently " + actions.get_boiler_state(),
            size=(32, 1),
            justification="center",
            font=("Helvetica", 25),
            key="On/Off",
        )
    ],
    [
        sg.Column(control_column, background_color="#F7F3EC"),
        sg.Column(graph_column, background_color="#F7F3EC"),
    ],
]

window = sg.Window("Window Title", layout)


def main():
    while True:  # Event Loop
        event, values = window.Read()
        window.Element("On/Off").Update(
            "The boiler is currently " + actions.get_boiler_state()
        )
        print(event, values)
        if event is None or event == "Exit":
            break
    window.Close()


if __name__ == "__main__":
    main()
