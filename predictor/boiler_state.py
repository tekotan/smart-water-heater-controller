import numpy as np

THRESHOLD = 10

class DummyBoiler:
    def __init__(self, time_step_freq=15):
        self.states = np.array([0] * 6 * (60//time_step_freq) + [1] * 4 *
                               (60//time_step_freq) + [0] * 6 * (60//time_step_freq) + [1] * 4 * (60//time_step_freq) + [0] * 4 * (60//time_step_freq))
        self.generator = self.get_state_generator()

    def get_state_generator(self):
        for i in self.states:
            yield np.random.choice([i, 0.5], p=[0.95, 0.05])

    def get_usage_state(self):
        return next(self.generator)

    def reset_states(self):
        del self.generator
        self.generator = self.get_state_generator()

class RealBoiler:
    def __init__(self):
        import predictor.sensor_ops as sensor
        self.sensor = sensor
    def get_usage_state(self):
        ir_data = self.sensor.get_data()
        if ir_data > THRESHOLD:
            return 1
        else:
            return 0
    def reset_states(self):
        pass

class Boiler:
    def __init__(self, train=True, time_step_freq=15):
        if train:
            self.core = DummyBoiler(time_step_freq=time_step_freq)
        else:
            self.core = RealBoiler()
    def get_usage_state(self):
        return self.core.get_usage_state()
    def reset_states(self):
        return self.core.reset_states()
