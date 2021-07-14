import tensorflow as tf
import numpy as np

from tf_agents.environments import py_environment
from tf_agents.environments import tf_environment
from tf_agents.environments import tf_py_environment
from tf_agents.environments import utils
from tf_agents.specs import array_spec
from tf_agents.environments import wrappers
from tf_agents.environments import suite_gym
from tf_agents.trajectories import time_step as ts
try:
    from boiler_state import Boiler
except:
    from predictor.boiler_state import Boiler
class DailyUsageEnv(py_environment.PyEnvironment):
    def __init__(self, train=True, heating_power=8, time_step_freq=15, water_thres=150, capacity=100):
        super().__init__()
        self.HEATER_CAPACITY = capacity # liters
        self.HEATING_POWER = heating_power # kW
        self.ROOM_TEMP = 72 # fahrenheit
        self.COOLING_RATE = 0.16
        self.HOT_WATER_THRES = water_thres # fahrenheit
        self._action_spec = array_spec.BoundedArraySpec(
            shape=(),
            dtype=np.int32,
            minimum=0,
            maximum=2,
            name="action"
        )
        self.num_steps = 0
        self._num_cooling_steps = 0
        self.discount = 1
        self.history_buffer = 1  # days
        self.time_step_freq = time_step_freq  # mins
        self._boiler_state = 0 # boiler on or off
        self._usage_state = 0 # is water being used or not
        self._water_temperature = 72
        self._cooling_temp_start = 72
        self._history = np.zeros(
            (int(self.history_buffer * 24 * 60 // self.time_step_freq),))
        self._day_usage = np.array([])
        self.boiler = Boiler(train=train, time_step_freq=time_step_freq)
        self._observation_spec = {
            "history": array_spec.BoundedArraySpec(
                shape=(int(self.history_buffer * 24 * 60 // self.time_step_freq),),
                dtype=np.int32,
                minimum=0,
                maximum=1,
                name="history"
            ),
            "boiler_state": array_spec.BoundedArraySpec(
                shape=(1,),
                dtype=np.int32,
                minimum=0,
                maximum=1,
                name="boiler_state"
            ),
            "usage_state": array_spec.BoundedArraySpec(
                shape=(1,),
                dtype=np.float32,
                minimum=0,
                maximum=1,
                name="usage_state"
            ),
            "water_temperature": array_spec.BoundedArraySpec(
                shape=(1,),
                dtype=np.int32,
                minimum=70,
                maximum=212,
                name="water_temperature"
            ),
        }

    def observation_spec(self):
        """Return observation_spec."""
        return self._observation_spec

    def action_spec(self):
        """Return action_spec."""
        return self._action_spec

    def _reset(self):
        """Return initial_time_step."""
        self.num_steps = 0
        self.boiler.reset_states()
        self._water_temperature = 72
        self._boiler_state = 0
        self._usage_state = 0
        return ts.restart(
            {
                "history": self._history.astype(np.int32),
                "boiler_state": np.array([self._boiler_state]),
                "usage_state": np.array([self._usage_state]).astype(np.float32),
                "water_temperature": np.array([self._water_temperature]).astype(np.int32),
            }
        )

    def _step(self, action):
        """Apply action and return new time_step."""
        # Set water temperature according to equations in paper
        if self._boiler_state == 1 and self._water_temperature <= 212:
            self._num_cooling_steps = 0
            self._water_temperature += (3600 * self.HEATING_POWER * self.time_step_freq / 60) / (4.2 * self.HEATER_CAPACITY)
            if self._water_temperature > 212:
                self._water_temperature = 212
        elif self._boiler_state == 0:
            self._water_temperature = self.ROOM_TEMP + (self._cooling_temp_start - self.ROOM_TEMP) * \
                                        np.exp(-1 * self.COOLING_RATE * self._num_cooling_steps * self.time_step_freq / 60)
            self._num_cooling_steps += 1
        if self.num_steps > 24 * 60 / self.time_step_freq:
            return self.reset()

        self.num_steps += 1

        if action == 1:
            self._boiler_state = 1
        elif action == 2:
            self._boiler_state = 0
            self._cooling_temp_start = self._water_temperature

        if self.num_steps > 24 * 60 / self.time_step_freq:
            return ts.termination({
                "history": self._history.astype(np.int32),
                "boiler_state": np.array([self._boiler_state]),
                "usage_state": np.array([self._usage_state]).astype(np.float32),
                "water_temperature": np.array([self._water_temperature]).astype(np.int32),
            }, 0.0)
        self._history = np.delete(self._history, (0))
        self._history = np.append(self._history, [self._usage_state])
        self._usage_state = self.boiler.get_usage_state()

        if self._boiler_state:
            reward = -50
        else:
            reward = 0
        if self._usage_state and self._water_temperature > self.HOT_WATER_THRES:
            reward += 25 * self._usage_state
        elif self._usage_state and self._water_temperature < self.HOT_WATER_THRES:
            reward += -400 * self._usage_state
        else:
            reward +=  0
        return ts.transition({
            "history": self._history.astype(np.int32),
            "boiler_state": np.array([self._boiler_state]),
            "usage_state": np.array([self._usage_state]).astype(np.float32),
            "water_temperature": np.array([self._water_temperature]).astype(np.int32),
        }, reward=reward, discount=self.discount)

if __name__ == "__main__":
    env = DailyUsageEnv()
    utils.validate_py_environment(env, episodes=5)
