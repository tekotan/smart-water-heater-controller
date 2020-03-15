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
    def __init__(self, train=True):
        self._action_spec = array_spec.BoundedArraySpec(
            shape=(),
            dtype=np.int32,
            minimum=0,
            maximum=2,
            name="action"
        )
        self.num_steps = 0
        self.discount = 1
        self.history_buffer = 1  # days
        self.time_step_freq = 15  # mins
        self._boiler_state = 0
        self._usage_state = 0
        self._history = np.zeros(
            (self.history_buffer * 24 * 60 // self.time_step_freq,))
        self._day_usage = np.array([])
        self.boiler = Boiler(train=train)
        self._observation_spec = {
            "history": array_spec.BoundedArraySpec(
                shape=(self.history_buffer * 24 * 60 // self.time_step_freq,),
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
                dtype=np.int32,
                minimum=0,
                maximum=1,
                name="usage_state"
            )

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
        return ts.restart(
            {
                "history": self._history.astype(np.int32),
                "boiler_state": np.array([self._boiler_state]),
                "usage_state": np.array([self._usage_state])
            }
        )

    def _step(self, action):
        """Apply action and return new time_step."""
        if self.num_steps > 24 * 60 / 15:
            return self.reset()
        self.num_steps += 1
        if action == 1:
            self._boiler_state = 1
        elif action == 2:
            self._boiler_state = 0
        if self.num_steps > 24 * 60 / 15:
            return ts.termination({
                "history": self._history.astype(np.int32),
                "boiler_state": np.array([self._boiler_state]),
                "usage_state": np.array([self._usage_state])
            }, 0.0)
        self._history = np.delete(self._history, (0))
        self._history = np.append(self._history, [self._usage_state])
        self._usage_state = self.boiler.get_usage_state()

        if self._usage_state and self._boiler_state:
            reward = 10
        elif self._usage_state and not self._boiler_state:
            reward = -100
        elif not self._usage_state and not self._boiler_state:
            reward = 5
        elif not self._usage_state and self._boiler_state:
            reward = -5
        return ts.transition({
            "history": self._history.astype(np.int32),
            "boiler_state": np.array([self._boiler_state]),
            "usage_state": np.array([self._usage_state])
        }, reward=reward, discount=self.discount)

if __name__ == "__main__":
    env = DailyUsageEnv()
    utils.validate_py_environment(env, episodes=5)
