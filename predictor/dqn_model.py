import base64
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import PIL.Image

import tensorflow as tf

from tf_agents.agents.dqn import dqn_agent
from tf_agents.drivers import dynamic_step_driver
from tf_agents.environments import suite_gym
from tf_agents.environments import tf_py_environment
from tf_agents.eval import metric_utils
from tf_agents.metrics import tf_metrics
from tf_agents.networks import q_network
from tf_agents.policies import random_tf_policy
from tf_agents.replay_buffers import tf_uniform_replay_buffer
from tf_agents.trajectories import trajectory
from tf_agents.utils import common

learning_rate = 1e-3
fc_layer_params = (10, )

class DQNModel:
    def __init__(self, environment):
        self.preprocessing_layers = {
            'history': tf.keras.models.Sequential([#tf.keras.layers.Reshape((96, 1), dtype=tf.int32),
                                                #tf.keras.layers.LSTM(1),
                                                #tf.keras.layers.Flatten(),
                                                tf.keras.layers.Dense(50, activation="linear")]),
            'boiler_state': tf.keras.layers.Dense(1, activation="linear"),
            "usage_state": tf.keras.layers.Dense(1, activation="linear"),
        }

        self.preprocessing_combiner = tf.keras.layers.Concatenate(axis=-1)
        self.q_net = q_network.QNetwork(
            environment.observation_spec(),
            environment.action_spec(),
            fc_layer_params=fc_layer_params,
            preprocessing_layers=self.preprocessing_layers,
            preprocessing_combiner=self.preprocessing_combiner
        )

class DQNAgent:
    def __init__(self, environment, model):
        self.optimizer = tf.compat.v1.train.AdamOptimizer(learning_rate=learning_rate)
        self.train_step_counter = tf.Variable(0)
        self.agent = dqn_agent.DqnAgent(
            environment.time_step_spec(),
            environment.action_spec(),
            q_network=model.q_net,
            optimizer=self.optimizer,
            td_errors_loss_fn=common.element_wise_squared_loss,
            train_step_counter=self.train_step_counter
        )
