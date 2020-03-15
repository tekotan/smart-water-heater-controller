import numpy as np

THRESHOLD = 10

class DummyBoiler:
    def __init__(self):
        self.states = np.array([0] * 6 * 4 + [1] * 4 *
                               4 + [0] * 6 * 4 + [1] * 4 * 4 + [0] * 4 * 4)
        self.generator = self.get_state_generator

    def get_state_generator(self):
        for i in self.states:
            yield np.random.choice([i, 0, 1], p=[0.90, 0.05, 0.05])

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
    def __init__(self, train=True):
        if train:
            self.core = DummyBoiler()
        else:
            self.core = RealBoiler()
    def get_usage_state(self):
        return self.core.get_usage_state()
    def reset_states(self):
        return self.core.reset_states()
