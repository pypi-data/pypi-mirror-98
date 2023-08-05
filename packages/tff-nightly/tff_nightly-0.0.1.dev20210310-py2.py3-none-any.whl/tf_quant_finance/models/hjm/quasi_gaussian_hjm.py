# Lint as: python3
# Copyright 2020 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Multi-Factor Quasi-Gaussian HJM Model."""

import tensorflow.compat.v2 as tf

from tf_quant_finance.math import gradient
from tf_quant_finance.models import euler_sampling
from tf_quant_finance.models import generic_ito_process
from tf_quant_finance.models import utils


class QuasiGaussianHJM(generic_ito_process.GenericItoProcess):
  r"""Quasi-Gaussian HJM model for term-structure modeling.

  Heath-Jarrow-Morton (HJM) model for the interest rate term-structre
  modelling specifies the dynamics of the instantaneus forward rate `f(t,T)`
  with maturity `T` at time `t` as follows:

  ```None
    df(t,T) = mu(t,T) dt + sum_i sigma_i(t,  T) * dW_i(t),
    1 <= i <= n,
  ```
  where `mu(t,T)` and `sigma_i(t,T)` denote the drift and volatility
  for the forward rate and `W_i` are Brownian motions with instantaneous
  correlation `Rho`. The model above represents an `n-factor` HJM model. Under
  the risk-neutral measure, the drift `mu(t,T)` is computed as

  ```
    mu(t,T) = sum_i sigma_i(t,T)  int_t^T sigma_(t,u) du
  ```
  Using the separability condition, the HJM model above can be formulated as
  the following Markovian model:

  ```None
    sigma(t,T) = sigma(t) * h(T)    (Separability condition)
  ```
  A common choice for the function h(t) is `h(t) = exp(-kt)`. Using the above
  parameterization of sigma(t,T), we obtain the following Markovian
  formulation of the HJM model [1]:

  ```None
    HJM Model
    dx(t) = (y(t) - k * x(t)) dt + sigma(t) dW
    dy(t) = (sigma(t)^2 - 2 * k * y(t)) dt
    r(t) = sum_i x_i(t) + f(0, t)
  ```
  where `x` and `y` are `n`-dimensional vectors. The HJM class implements the
  model outlined above by jointly simulating the state [x_t, y_t].

  The price at time `t` of a zero-coupon bond maturing at `T` is given by
  (Ref. [1]):

  ```None
  P(t,T) = P(0,T) / P(0,t) *
           exp(-x(t) * G(t,T) - 0.5 * y(t) * G(t,T)^2)
  ```

  The HJM model implentation supports constant mean-reversion rate `k` and
  `sigma(t)` can be an arbitrary function of `t` and `r`. We use Euler
  discretization to simulate the HJM model.

  #### Example. Simulate a 4-factor HJM process.

  ```python
  import numpy as np
  import tensorflow.compat.v2 as tf
  import tf_quant_finance as tff

  dtype = tf.float64
  def discount_fn(x):
    return 0.01 * tf.ones_like(x, dtype=dtype)

  process = tff.experimental.hjm.QuasiGaussianHJM(
      dim=4,
      mean_reversion=[0.03, 0.01, 0.02, 0.005],  # constant mean-reversion
      volatility=[0.01, 0.011, 0.015, 0.008],  # constant volatility
      initial_discount_rate_fn=discount_fn,
      dtype=dtype)
  times = np.array([0.1, 1.0, 2.0, 3.0])
  short_rate_paths, discount_paths, _, _ = process.sample_paths(
      times,
      num_samples=100000,
      time_step=0.1,
      random_type=tff.math.random.RandomType.STATELESS_ANTITHETIC,
      seed=[1, 2],
      skip=1000000)
  ```

  #### References:
    [1]: Leif B. G. Andersen and Vladimir V. Piterbarg. Interest Rate Modeling.
    Volume II: Term Structure Models.
  """

  def __init__(self,
               dim,
               mean_reversion,
               volatility,
               initial_discount_rate_fn,
               corr_matrix=None,
               dtype=None,
               name=None):
    """Initializes the HJM model.

    Args:
      dim: A Python scalar which corresponds to the number of factors
        comprising the model.
      mean_reversion: A real positive `Tensor` of shape `[dim]`. Corresponds
        to the mean reversion rate of each factor.
      volatility: A real positive `Tensor` of the same `dtype` and shape as
        `mean_reversion` or a callable with the following properties:
        (a)  The callable should accept a scalar `Tensor` `t` and a 1-D `Tensor`
        `r(t)` of shape `[num_samples]` and returns a 2-D `Tensor` of shape
        `[num_samples, dim]`. The variable `t`  stands for time and `r(t)` is
        the short rate at time `t`.  The function returns instantaneous
        volatility `sigma(t) = sigma(t, r(r))`.
        When `volatility` is specified is a real `Tensor`, each factor is
        assumed to have a constant instantaneous volatility  and the  model is
        effectively a Gaussian HJM model.
        Corresponds to the instantaneous volatility of each factor.
      initial_discount_rate_fn: A Python callable that accepts expiry time as
        a real `Tensor` of the same `dtype` as `mean_reversion` and returns a
        `Tensor` of shape `input_shape + dim`.
        Corresponds to the zero coupon bond yield at the present time for the
        input expiry time.
      corr_matrix: A `Tensor` of shape `[dim, dim]` and the same `dtype` as
        `mean_reversion`.
        Corresponds to the correlation matrix `Rho`.
      dtype: The default dtype to use when converting values to `Tensor`s.
        Default value: `None` which means that default dtypes inferred by
          TensorFlow are used.
      name: Python string. The name to give to the ops created by this class.
        Default value: `None` which maps to the default name
        `quasi_gaussian_hjm_model`.
    """
    self._name = name or 'quasi_gaussian_hjm_model'
    with tf.name_scope(self._name):
      self._dtype = dtype or None
      # x has dimensionality of `dim` and y `dim * dim`
      self._dim = dim + dim**2
      self._factors = dim

      def _instant_forward_rate_fn(t):
        t = tf.convert_to_tensor(t, dtype=self._dtype)
        def _log_zero_coupon_bond(x):
          r = tf.convert_to_tensor(
              initial_discount_rate_fn(x), dtype=self._dtype)
          return -r * x

        rate = -gradient.fwd_gradient(
            _log_zero_coupon_bond, t, use_gradient_tape=True,
            unconnected_gradients=tf.UnconnectedGradients.ZERO)
        return rate

      def _initial_discount_rate_fn(t):
        return tf.convert_to_tensor(
            initial_discount_rate_fn(t), dtype=self._dtype)

      self._instant_forward_rate_fn = _instant_forward_rate_fn
      self._initial_discount_rate_fn = _initial_discount_rate_fn
      self._mean_reversion = tf.convert_to_tensor(
          mean_reversion, dtype=dtype, name='mean_reversion')

      # Setup volatility
      if callable(volatility):
        self._volatility = volatility
      else:
        volatility = tf.convert_to_tensor(volatility, dtype=dtype)
        def _tensor_to_volatility_fn(t, r):
          del t, r
          return volatility

        self._volatility = _tensor_to_volatility_fn

      if corr_matrix is None:
        corr_matrix = tf.eye(dim, dim, dtype=self._dtype)
      self._rho = tf.convert_to_tensor(corr_matrix, dtype=dtype, name='rho')
      self._sqrt_rho = tf.linalg.cholesky(self._rho)

    # Volatility function
    def _vol_fn(t, state):
      """Volatility function of qG-HJM."""
      # Get parameter values at time `t`
      x = state[..., :self._factors]
      num_samples = x.shape.as_list()[0]
      r_t = self._instant_forward_rate_fn(t) + tf.reduce_sum(x, axis=-1,
                                                             keepdims=True)
      volatility = self._volatility(t, r_t)
      volatility = tf.expand_dims(volatility, axis=-1)

      diffusion_x = tf.broadcast_to(
          self._sqrt_rho * volatility,
          (num_samples, self._factors, self._factors))
      paddings = tf.constant(
          [[0, 0], [0, self._factors**2], [0, self._factors**2]],
          dtype=tf.int32)
      diffusion = tf.pad(diffusion_x, paddings)

      return diffusion

    # Drift function
    def _drift_fn(t, state):
      """Drift function of qG-HJM."""
      x = state[..., :self._factors]
      y = state[..., self._factors:]
      num_samples = x.shape.as_list()[0]
      y = tf.reshape(y, [num_samples, self._factors, self._factors])
      r_t = (self._instant_forward_rate_fn(t) +
             tf.reduce_sum(x, axis=-1, keepdims=True))
      volatility = self._volatility(t, r_t)
      volatility = tf.expand_dims(volatility, axis=-1)
      # create matrix v(i,j) = vol(i)*vol(j)
      volatility_squared = tf.linalg.matmul(
          volatility, volatility, transpose_b=True)
      # create a matrix k2(i,j) = k(i) + k(j)
      mr2 = tf.expand_dims(self._mean_reversion, axis=-1)
      mr2 = mr2 + tf.transpose(mr2)

      drift_x = tf.math.reduce_sum(y, axis=-1) - self._mean_reversion * x
      drift_y = (self._rho * volatility_squared - mr2 * y)
      drift_y = tf.reshape(
          drift_y, [num_samples, self._factors * self._factors])
      drift = tf.concat([drift_x, drift_y], axis=-1)
      return drift

    super(QuasiGaussianHJM, self).__init__(
        self._dim, _drift_fn, _vol_fn, dtype, name)

  def sample_paths(self,
                   times,
                   num_samples,
                   time_step,
                   random_type=None,
                   seed=None,
                   skip=0,
                   name=None):
    """Returns a sample of short rate paths from the HJM process.

    Uses Euler sampling for simulating the short rate paths. The code closely
    follows the notations in [1], section ###.

    Args:
      times: Rank 1 `Tensor` of positive real values. The times at which the
        path points are to be evaluated.
      num_samples: Positive scalar `int32` `Tensor`. The number of paths to
        draw.
      time_step: Scalar real `Tensor`. Maximal distance between time grid points
        in Euler scheme. Used only when Euler scheme is applied.
        Default value: `None`.
      random_type: Enum value of `RandomType`. The type of (quasi)-random
        number generator to use to generate the paths.
        Default value: `None` which maps to the standard pseudo-random numbers.
      seed: Seed for the random number generator. The seed is
        only relevant if `random_type` is one of
        `[STATELESS, PSEUDO, HALTON_RANDOMIZED, PSEUDO_ANTITHETIC,
          STATELESS_ANTITHETIC]`. For `PSEUDO`, `PSEUDO_ANTITHETIC` and
        `HALTON_RANDOMIZED` the seed should be an Python integer. For
        `STATELESS` and  `STATELESS_ANTITHETIC `must be supplied as an integer
        `Tensor` of shape `[2]`.
        Default value: `None` which means no seed is set.
      skip: `int32` 0-d `Tensor`. The number of initial points of the Sobol or
        Halton sequence to skip. Used only when `random_type` is 'SOBOL',
        'HALTON', or 'HALTON_RANDOMIZED', otherwise ignored.
        Default value: `0`.
      name: Python string. The name to give this op.
        Default value: `sample_paths`.

    Returns:
      A `Tensor` of shape [num_samples, k, dim] where `k` is the size
      of the `times` and `dim` is the dimension of the process.

    Raises:
      ValueError:
        (a) If `times` has rank different from `1`.
        (b) If Euler scheme is used by times is not supplied.
    """
    name = name or self._name + '_sample_path'
    with tf.name_scope(name):
      times = tf.convert_to_tensor(times, self._dtype)
      if len(times.shape) != 1:
        raise ValueError('`times` should be a rank 1 Tensor. '
                         'Rank is {} instead.'.format(len(times.shape)))
      return self._sample_paths(
          times, time_step, num_samples, random_type, skip, seed)

  def sample_discount_curve_paths(self,
                                  times,
                                  curve_times,
                                  num_samples,
                                  time_step,
                                  random_type=None,
                                  seed=None,
                                  skip=0,
                                  name=None):
    """Returns a sample of simulated discount curves for the Hull-white model.

    Args:
      times: Rank 1 `Tensor` of positive real values. The times at which the
        discount curves are to be evaluated.
      curve_times: Rank 1 `Tensor` of positive real values. The maturities
        at which discount curve is computed at each simulation time.
      num_samples: Positive scalar `int`. The number of paths to draw.
      time_step: Scalar real `Tensor`. Maximal distance between time grid points
        in Euler scheme. Used only when Euler scheme is applied.
        Default value: `None`.
      random_type: Enum value of `RandomType`. The type of (quasi)-random
        number generator to use to generate the paths.
        Default value: None which maps to the standard pseudo-random numbers.
      seed: Seed for the random number generator. The seed is
        only relevant if `random_type` is one of
        `[STATELESS, PSEUDO, HALTON_RANDOMIZED, PSEUDO_ANTITHETIC,
          STATELESS_ANTITHETIC]`. For `PSEUDO`, `PSEUDO_ANTITHETIC` and
        `HALTON_RANDOMIZED` the seed should be an Python integer. For
        `STATELESS` and  `STATELESS_ANTITHETIC` must be supplied as an integer
        `Tensor` of shape `[2]`.
        Default value: `None` which means no seed is set.
      skip: `int32` 0-d `Tensor`. The number of initial points of the Sobol or
        Halton sequence to skip. Used only when `random_type` is 'SOBOL',
        'HALTON', or 'HALTON_RANDOMIZED', otherwise ignored.
        Default value: `0`.
      name: Str. The name to give this op.
        Default value: `sample_discount_curve_paths`.

    Returns:
      A tuple containing two `Tensor`s. The first element is a `Tensor` of
      shape [num_samples, m, k, dim] and contains the simulated bond curves
      where `m` is the size of `curve_times`, `k` is the size of `times` and
      `dim` is the dimension of the process. The second element is a `Tensor`
      of shape [num_samples, k, dim] and contains the simulated short rate
      paths.

    ### References:
      [1]: Leif B.G. Andersen and Vladimir V. Piterbarg. Interest Rate Modeling,
      Volume II: Term Structure Models. 2010.
    """
    name = name or self._name + '_sample_discount_curve_paths'
    with tf.name_scope(name):
      times = tf.convert_to_tensor(times, self._dtype)
      num_times = times.shape.as_list()[0]
      curve_times = tf.convert_to_tensor(curve_times, self._dtype)
      rate_paths, discount_factor_paths, x_t, y_t = self._sample_paths(
          times, time_step, num_samples, random_type, skip, seed)
      # Reshape x_t to (num_samples, 1, num_times, nfactors)
      x_t = tf.expand_dims(x_t, axis=1)
      # Reshape y_t to (num_samples, 1, num_times, nfactors**2)
      y_t = tf.expand_dims(y_t, axis=1)

      # Reshape all `Tensor`s so that they have the dimensions same as (or
      # broadcastable to) the output shape
      # ([num_smaples,num_curve_times,num_sim_times]).
      num_curve_nodes = curve_times.shape.as_list()[0]  # m
      num_sim_steps = times.shape.as_list()[0]  # k
      times = tf.reshape(times, (1, 1, num_sim_steps, 1))
      curve_times = tf.reshape(curve_times, (1, num_curve_nodes, 1, 1))

      return (self._bond_reconstitution(times, times + curve_times,
                                        self._mean_reversion, x_t, y_t,
                                        num_samples, num_times), rate_paths,
              discount_factor_paths)

  def _sample_paths(self, times, time_step, num_samples, random_type, skip,
                    seed):
    """Returns a sample of paths from the process."""
    initial_state = tf.zeros((self._dim,), dtype=self._dtype)
    # Note that we need a finer simulation grid (determnied by `dt`) to compute
    # discount factors accurately. The `times` input might not be granular
    # enough for accurate calculations.
    times, keep_mask, _ = utils.prepare_grid(
        times=times, time_step=time_step, dtype=self._dtype)
    # Add zeros as a starting location
    dt = times[1:] - times[:-1]

    # xy_paths.shape = (num_samples, num_times, nfactors+nfactors^2)
    xy_paths = euler_sampling.sample(
        self._dim,
        self._drift_fn,
        self._volatility_fn,
        times,
        num_samples=num_samples,
        initial_state=initial_state,
        random_type=random_type,
        seed=seed,
        time_step=time_step,
        skip=skip)

    x_paths = xy_paths[..., :self._factors]
    y_paths = xy_paths[..., self._factors:]

    f_0_t = self._instant_forward_rate_fn(times)  # shape=(num_times,)
    rate_paths = tf.math.reduce_sum(
        x_paths, axis=-1) + f_0_t  # shape=(num_samples, num_times)

    discount_factor_paths = tf.math.exp(-rate_paths[:, :-1] * dt)
    discount_factor_paths = tf.concat(
        [tf.ones((num_samples, 1), dtype=self._dtype), discount_factor_paths],
        axis=1)  # shape=(num_samples, num_times)
    discount_factor_paths = utils.cumprod_using_matvec(discount_factor_paths)

    return (
        tf.boolean_mask(rate_paths, keep_mask, axis=1),
        tf.boolean_mask(discount_factor_paths, keep_mask, axis=1),
        tf.boolean_mask(x_paths, keep_mask, axis=1),
        tf.boolean_mask(y_paths, keep_mask, axis=1)
        )

  def _bond_reconstitution(self,
                           times,
                           maturities,
                           mean_reversion,
                           x_t,
                           y_t,
                           num_samples,
                           num_times):
    """Computes discount bond prices using Eq. 10.18 in Ref [2]."""
    # p_0_t.shape = (1, 1, num_sim_steps, 1)
    p_0_t = tf.math.exp(-self._initial_discount_rate_fn(times) * times)
    # p_0_t_tau.shape = (1, num_curve_times, num_sim_steps, 1)
    p_0_t_tau = tf.math.exp(
        -self._initial_discount_rate_fn(maturities) *
        (maturities)) / p_0_t
    # g_t_tau.shape = (1, num_curve_times, num_sim_steps, dim)
    g_t_tau = (1. - tf.math.exp(
        -mean_reversion * (maturities - times))) / mean_reversion
    # term1.shape = (num_samples, num_curve_times, num_sim_steps)
    term1 = tf.math.reduce_sum(x_t * g_t_tau, axis=-1)
    # y_t: (num_samples, 1, num_times, nfactors**2) ->
    # (num_samples, 1, num_times, nfactors, nfactors)
    y_t = tf.reshape(
        y_t, [num_samples, 1, num_times, self._factors, self._factors])
    # now compute g_t_tau * y_t * g_t_tau
    # term2.shape = (num_samples, num_curve_times, num_sim_steps)
    term2 = tf.math.reduce_sum(
        g_t_tau * tf.linalg.matvec(y_t, g_t_tau), axis=-1)

    p_t_tau = p_0_t_tau[..., 0] * tf.math.exp(-term1 - 0.5 * term2)
    # p_t_tau.shape=(num_samples, num_curve_times, num_sim_steps)
    return p_t_tau
