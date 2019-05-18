class Boiler:
    def __init__(self):
        self.on = True
        self.temperature_perc = 0
        self.vacation = False
        self.always_on = False
        self.data = []

    def change_state(self, on_or_off, vacation, temperature_perc, always_on):
        self.always_on = True
        self.on = on_or_off == "on"
        self.temperature_perc = temperature_perc
        self.vacation = bool(vacation)
        self.always_on = bool(always_on)
        print("changed_state")

    def get_state(self):
        ret_list = ", ".join(
            [
                int(self.temperature_perc),
                int(self.on),
                int(self.vacation),
                int(self.always_on),
            ]
        )
        print(ret_list)
        return ret_list

    def change_data(self, data):
        self.data = data.split(", ")


my_boiler = Boiler()


def change_state(on_or_off, vacation, temperature_perc, always_on):
    """
    Function will use pi controller to turn boiler on or off based on the
    threshold between 0 and 100
    """
    my_boiler.change_state(on_or_off, vacation, temperature_perc, always_on)
    print(on_or_off, vacation, temperature_perc, always_on)


def turn_on():
    pass


def turn_off():
    pass
