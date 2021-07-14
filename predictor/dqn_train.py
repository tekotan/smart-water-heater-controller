import os
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
from tf_agents.policies import policy_saver


import environment as environment
import dqn_model as model
import dqn_train_util as utils

from tqdm import tqdm

num_iterations = 500000
initial_collect_steps = 2000
collect_steps_per_iteration = 1
replay_buffer_max_length = 10000

batch_size = 32

log_interval = 200

num_eval_episodes = 5
eval_interval = 10000

train_py_env = environment.DailyUsageEnv()
eval_py_env = environment.DailyUsageEnv()

train_env = tf_py_environment.TFPyEnvironment(train_py_env)
eval_env = tf_py_environment.TFPyEnvironment(eval_py_env)
q_net = model.DQNModel(train_env)
q_agent = model.DQNAgent(train_env, q_net)

q_agent.agent.initialize()

eval_policy = q_agent.agent.policy
collect_policy = q_agent.agent.collect_policy

random_policy = random_tf_policy.RandomTFPolicy(train_env.time_step_spec(),
                                                train_env.action_spec())



replay_buffer = tf_uniform_replay_buffer.TFUniformReplayBuffer(
    data_spec=q_agent.agent.collect_data_spec,
    batch_size=train_env.batch_size,
    max_length=replay_buffer_max_length)

print("collecting data")
utils.collect_data(train_env, random_policy, replay_buffer, steps=initial_collect_steps)

dataset = replay_buffer.as_dataset(
    num_parallel_calls=3,
    sample_batch_size=batch_size,
    num_steps=3).prefetch(3)

iterator = iter(dataset)

q_agent.agent.train = common.function(q_agent.agent.train)

# Reset the train step
q_agent.agent.train_step_counter.assign(0)

# Checkpoint setup
checkpoint_dir = os.path.join("models", 'checkpoint')
train_checkpointer = common.Checkpointer(
    ckpt_dir=checkpoint_dir,
    max_to_keep=1,
    agent=q_agent.agent,
    policy=q_agent.agent.policy,
    replay_buffer=replay_buffer,
    global_step=q_agent.agent.train_step_counter
)
policy_dir = os.path.join("models", 'policy')
tf_policy_saver = policy_saver.PolicySaver(q_agent.agent.policy)

# Evaluate the agent's policy once before training.
print("computing avg return")
avg_return = utils.compute_avg_return(eval_env, q_agent.agent.policy, num_eval_episodes)
returns = [avg_return]
for _ in tqdm(range(num_iterations)):

    # Collect a few steps using collect_policy and save to the replay buffer.
    for _ in range(collect_steps_per_iteration):
        utils.collect_step(train_env, q_agent.agent.collect_policy, replay_buffer)

    # Sample a batch of data from the buffer and update the agent's network.
    experience, unused_info = next(iterator)
    train_loss = q_agent.agent.train(experience).loss

    step = q_agent.agent.train_step_counter.numpy()

    # if step % log_interval == 0:
    #     tqdm.write('step = {0}: loss = {1}'.format(step, train_loss))

    if step % eval_interval == 0:
        avg_return = utils.compute_avg_return(
            eval_env, q_agent.agent.policy, num_eval_episodes)
        tqdm.write('step = {0}: Average Return = {1}'.format(step, avg_return))
        train_checkpointer.save(q_agent.agent.train_step_counter)
        if avg_return > max(returns):
            tf_policy_saver.save(policy_dir)
        returns.append(avg_return)

iterations = range(0, num_iterations + 1, eval_interval)
plt.plot(iterations, returns)
plt.ylabel('Average Return')
plt.xlabel('Iterations')
plt.ylim(top=250)
plt.savefig("reward.svg")

train_checkpointer.save(q_agent.agent.train_step_counter)
tf_policy_saver.save("./models/policy_final")