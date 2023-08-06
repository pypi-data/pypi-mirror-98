import gym
import numpy as np
import tensorflow as tf

from tfmpc.envs.diffenv import DiffEnv
from tfmpc.envs.gymenv import GymEnv


class Reservoir(DiffEnv, GymEnv):

    def __init__(self,
                 max_res_cap,
                 lower_bound,
                 upper_bound,
                 low_penalty,
                 high_penalty,
                 set_point_penalty,
                 downstream,
                 rain_shape,
                 rain_scale):
        super().__init__()

        self.max_res_cap = max_res_cap
        self.lower_bound = lower_bound
        self.upper_bound = upper_bound
        self.low_penalty = low_penalty
        self.high_penalty = high_penalty
        self.set_point_penalty = set_point_penalty
        self.downstream = downstream
        self.rain_shape = rain_shape
        self.rain_scale = rain_scale

        self.obs_space = gym.spaces.Box(
            low=np.zeros_like(self.max_res_cap), high=np.array(self.max_res_cap))

        self.action_space = gym.spaces.Box(
            shape=[self.action_size, 1], low=0.0, high=1.0)

    @property
    def state_size(self):
        return len(self.lower_bound)

    @property
    def action_size(self):
        return self.state_size

    @tf.function(input_signature=[
        tf.TensorSpec(shape=[None, None, 1], dtype=tf.float32),
        tf.TensorSpec(shape=[None, None, 1], dtype=tf.float32),
    ])
    def transition(self, state, action):
        rlevel = state
        batch_size = tf.shape(rlevel)[0]

        outflow = self._outflow(action, state)
        inflow = self._inflow(outflow)

        vaporated = self._vaporated(state)
        rainfall = self._rainfall(batch_size)

        rlevel_ = (
            rlevel
            + rainfall + inflow
            - vaporated - outflow
        )
        return rlevel_

    @tf.function(input_signature=[
        tf.TensorSpec(shape=[None, None, 1], dtype=tf.float32),
        tf.TensorSpec(shape=[None, None, 1], dtype=tf.float32)
    ])
    def cost(self, state, action):
        return self._rlevel_penalty_cost(state)

    @tf.function(input_signature=[
        tf.TensorSpec(shape=[None, 1], dtype=tf.float32)
    ])
    def final_cost(self, state):
        state = tf.expand_dims(state, axis=0)
        return tf.squeeze(self._rlevel_penalty_cost(state))

    @tf.function(input_signature=[
        tf.TensorSpec(shape=[None, None, 1], dtype=tf.float32)
    ])
    def _vaporated(self, rlevel):
        return (1.0 / 2.0) * tf.sin(rlevel / self.max_res_cap) * rlevel

    @tf.function(input_signature=[
        tf.TensorSpec(shape=[None, None, 1], dtype=tf.float32)
    ])
    def _inflow(self, outflow):
        return tf.matmul(self.downstream, outflow, transpose_a=True)

    @tf.function(input_signature=[
        tf.TensorSpec(shape=[None, None, 1], dtype=tf.float32),
        tf.TensorSpec(shape=[None, None, 1], dtype=tf.float32),
    ])
    def _outflow(self, relative_flow, rlevel):
        return relative_flow * rlevel

    @tf.function
    def _rainfall(self, batch_size):
        return tf.reshape(
            tf.tile(self.rain_shape * self.rain_scale, [batch_size, 1]),
            shape=[batch_size, -1, 1])

    @tf.function(input_signature=[
        tf.TensorSpec(shape=[None, None, 1], dtype=tf.float32)
    ])
    def _rlevel_penalty_cost(self, rlevel):
        low = self.lower_bound
        high = self.upper_bound

        c1 = -self.low_penalty * tf.maximum(0.0, low - rlevel)
        c2 = -self.high_penalty * tf.maximum(0.0, rlevel - high)
        c3 = -self.set_point_penalty * tf.abs((low + high) / 2.0 - rlevel)

        penalty = tf.reduce_sum(tf.squeeze(c1 + c2 + c3, axis=-1), axis=-1)
        return penalty

    def __repr__(self):
        return f"Reservoir({self.state_size})"

    def __str__(self):
        bounds = ", ".join(
            f"[{float(l):.2f}, {float(u):.2f}]"
            for l, u in zip(self.lower_bound, self.upper_bound))

        topology = self.downstream

        rain = ", ".join(
            f"Gamma(shape={float(shape):.2f}, scale={float(scale):.2f})"
            for shape, scale in zip(self.rain_shape, self.rain_scale))

        return f"Reservoir(\nbounds={bounds},\ntopology=\n{topology},\nrain={rain})"

    @classmethod
    def load(cls, config):
        kwargs = {
            key: tf.constant(val, dtype=tf.float32)
            for key, val in config.items()
        }
        return cls(**kwargs)
