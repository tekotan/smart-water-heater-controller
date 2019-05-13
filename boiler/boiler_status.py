import boiler.boiler_actions as core


class Boiler:
    def __init__(self):
        self.on = True
        self.temperature_perc = 0
        self.vacation = False
        self.power_saving = 1
        self.always_on = False

    def set_always_on(self, threshold):
        self.always_on = True
        if self.on == False:
            core.change_state(threshold)
        self.power_saving = 0
