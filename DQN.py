#!/usr/bin/env python
# coding: utf-8

# In[3]:


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


# In[22]:


class DailyUsageEnv(py_environment.PyEnvironment):
    def __init__(self):
        self._action_spec = array_spec.BoundedArraySpec(
            shape=(),
            dtype=np.int32,
            minimum=0,
            maximum=2,
            name="action"
        )
        self._observation_spec = array_spec.BoundedArraySpec(
            shape=(1, ),
            dtype=np.int32,
            minimum=0,
            maximum=2,
            name="observation"
        )
        self.num_steps = 0
        self.discount = 1
        self.history_buffer = 1
        self.time_step_freq = 15
        self._boiler_state = 0
        self._usage_state = 0
        self._history = np.zeros((24*4))
        self._day_usage = np.array([])
        self._dummy_boiler = Boiler()
    def observation_spec(self):
        """Return observation_spec."""
        return self.observation_spec

    def action_spec(self):
        """Return action_spec."""
        return self._action_spec

    def _reset(self):
        """Return initial_time_step."""
        if self._history.shape[0] < (self.history_buffer * 24 * 60 // 15):
            self._history = np.append(self._history, self._day_usage)
        else:
            self._history = np.delete(self._history, np.s_[:24 * 60 // 15])
            self._history = np.append(self._history, self._day_usage)
        self._day_usage = np.array([])
        self.num_steps = 0
        self._dummy_boiler.reset_states()
        return ts.restart((self._boiler_state, self._usage_state, self._history, self._day_usage))

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
            return ts.termination((self._boiler_state, self._usage_state, self._history, self._day_usage), 0.0)
        self._day_usage = np.append(self._day_usage, [self._usage_state])
        self._usage_state = self._dummy_boiler.get_usage_state()

        if self._usage_state and self._boiler_state:
            reward = 10
        elif self._usage_state and not self._boiler_state:
            reward = -100
        elif not self._usage_state and not self._boiler_state:
            reward = 5
        elif not self._usage_state and self._boiler_state:
            reward = -5
        return ts.transition((
                                self._boiler_state,
                                self._usage_state,
                                self._history,
                                self._day_usage
                            ), reward=reward, discount=self.discount)
        


# In[23]:


class Boiler:
    def __init__(self):
        self.states = np.ones((24 * 60 // 15))
        self.generator = self.get_state_generator
    def get_state_generator(self):
        for i in self.states:
            yield i
    def get_usage_state(self):
        return next(self.generator)
    def reset_states(self):
        del self.generator
        self.generator = self.get_state_generator()


# In[24]:


env = DailyUsageEnv()


# In[25]:


utils.validate_py_environment(env, episodes=5)


# In[ ]:




