import base64
import io
import matplotlib
import matplotlib.pyplot as plt
import os
import tensorflow as tf

from tf_agents.agents.dqn import dqn_agent
from tf_agents.drivers import dynamic_step_driver
from tf_agents.environments import suite_gym
from tf_agents.environments import tf_py_environment
from tf_agents.eval import metric_utils
from tf_agents.metrics import tf_metrics
from tf_agents.networks import q_network
from tf_agents.policies import policy_saver
from tf_agents.policies import py_tf_eager_policy
from tf_agents.policies import random_tf_policy
from tf_agents.replay_buffers import tf_uniform_replay_buffer
from tf_agents.trajectories import trajectory
from tf_agents.utils import common

import predictor.dqn_model as model
import predictor.environment as env
import predictor.dqn_train_util as utils


fine_tune_env_py = env.DailyUsageEnv(train=True)
fine_tune_env = tf_py_environment.TFPyEnvironment(fine_tune_env_py)
q_net = model.DQNModel(fine_tune_env)
q_agent = model.DQNAgent(fine_tune_env, q_net, n_step_update=1)

q_agent.agent.initialize()

replay_buffer = tf_uniform_replay_buffer.TFUniformReplayBuffer(
    data_spec=q_agent.agent.collect_data_spec,
    batch_size=1,
    max_length=2
)

train_py_env = env.DailyUsageEnv()
train_env = tf_py_environment.TFPyEnvironment(train_py_env)

utils.collect_data(train_env, q_agent.agent.policy, replay_buffer, steps=5)

dataset = replay_buffer.as_dataset(
    num_parallel_calls=3,
    sample_batch_size=1,
    num_steps=2
)
iterator = iter(dataset)

train_checkpointer = common.Checkpointer(
    ckpt_dir="./models/checkpoint",
    max_to_keep=1,
    agent=q_agent.agent,
    policy=q_agent.agent.policy,
    replay_buffer=replay_buffer,
    global_step=q_agent.agent.train_step_counter
)
train_checkpointer.initialize_or_restore()

class Predictor:
    def __init__(self):
        self.time_step = fine_tune_env.reset()
        
    def predict_and_fine_tune(self):
        prev_step = self.time_step
        action_step = q_agent.agent.policy.action(self.time_step)
        self.time_step = fine_tune_env.step(action_step.action)
        traj = trajectory.from_transition(prev_step, action_step, self.time_step)
        replay_buffer.add_batch(traj)
        experience, _ = next(iterator)
        train_loss = q_agent.agent.train(experience)
        return action_step.action
