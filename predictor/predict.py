import tensorflow as tf
from tf_agents.policies import py_tf_eager_policy
import os


class Predictor:
    def __init__(self, env, policy_dir="./predictor/models/policy"):
        self.policy = py_tf_eager_policy.SavedModelPyTFEagerPolicy(
                        policy_dir, env.time_step_spec(), env.action_spec())

        self.env = env
        self.time_step = self.env.reset()
    def predict(self):
        action_step = self.policy.action(self.time_step)
        self.time_step = self.env.step(action_step.action)
        return action_step.action, self.time_step
