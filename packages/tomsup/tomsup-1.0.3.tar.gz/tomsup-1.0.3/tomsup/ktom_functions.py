"""
This script contains all function related to the implementation of the
k-ToM agent.

For reference the parameter order of the k-ToM parameters is:
[1] Volatility
[2] Behavioural temperature
[3] Dilution
[4] Bias
"""
import numpy as np
from tomsup.payoffmatrix import PayoffMatrix
import copy


# Logit functions
def inv_logit(x):
    """
    This is the inverse logit (or sigmoid) function from the original VBA
    package
    It is slightly different from a standard inverse logit. Most importantly,
    it uses a finite precision, epsilon.
    Note that the VBA implementation has more options8changing scale, offset,
    etc.). These are not implemented here.
    Note also that we have here used the "quick version" from the VBA package.
    """
    # Set precision parameter (0 means perfect precision)
    epsilon = 1e-9

    # Set input bounds
    if np.any(x > 500):
        # For scalars
        if np.shape(x) == ():
            x = 500
        # Or vectors etc
        else:
            x[x > 500] = 500
        # warn("Logit input constrained at upper bound 0.9999 to avoid
        # rounding errors", Warning)
    if np.any(x < -500):
        if np.shape(x) == ():
            x = -500
        else:
            x[x < -500] = -500
        # warn("Logit input constrained at lower bound 0.0001 to avoid
        # rounding errors", Warning)

    # Calculate
    y = epsilon + (1 - 2 * epsilon) / (1 + np.exp(-x))

    return y


def logit(x):
    """
    This is the the logit function from the original VBA package. See that
    package for mor information.
    """
    # Calculate
    lx = (x) ** -1 - 1
    y = 0 - 1 ** -1 * np.log(lx)

    return y


# Learning subfunctions
def p_op_var0_update(prev_p_op_mean0, prev_p_op_var0, volatility):
    """
    prev_p_op_mean0   (float)
    prev_p_op_var0    (float)
    volatility        (float)

    0-ToM updates variance / uncertainty on choice probability estimate

    Examples:
    >>> p_op_var0_update(1, 0.2, 1)
    0.8348496471878395
    >>> #Higher volatility results in a higher variance
    >>> p_op_var0_update(1, 0.2, 1) < p_op_var0_update (1, 0.2, 2)
    True
    >>> #Mean close to 0.5 gives lower variance
    >>> p_op_var0_update(1, 0.45, 1) < p_op_var0_update (1, 0.2, 2)
    True
    """
    # Input variable transforms
    volatility = np.exp(volatility)
    prev_p_op_var0 = np.exp(prev_p_op_var0)

    prev_p_op_mean0 = inv_logit(prev_p_op_mean0)

    # Update
    new_p_op_var0 = 1 / (
        (1 / (volatility + prev_p_op_var0)) + prev_p_op_mean0 * (1 - prev_p_op_mean0)
    )

    # Output variable transform
    new_p_op_var0 = np.log(new_p_op_var0)

    return new_p_op_var0


def p_op_mean0_update(prev_p_op_mean0, p_op_var0, op_choice):
    """
    prev_p_op_mean0 (float)
    p_op_var0       (float)
    op_choice       (int)

    0-ToM updates mean choice probability estimate
    """
    # Input variable transforms
    p_op_var0 = np.exp(p_op_var0)

    # Update
    new_p_op_mean0 = prev_p_op_mean0 + p_op_var0 * (
        op_choice - inv_logit(prev_p_op_mean0)
    )

    # For numerical purposes, according to the VBA package
    new_p_op_mean0 = logit(inv_logit(new_p_op_mean0))

    return new_p_op_mean0


def p_opk_approx_fun(prev_p_op_mean, prev_param_var, prev_gradient, level):
    """
    prev_p_op_mean  (numpy.ndarray)
    prev_param_var  (numpy.ndarray)
    prev_gradient   (numpy.ndarray)
    level           (int)

    Approximates the estimated choice probability of the opponent on the
    previous round.
    A semi-analytical approximation derived in Daunizeau, J. (2017)

    >>> p_opk_approx_fun(prev_p_op_mean = np.array([0]), \
        prev_param_var = np.array([[0, 0, 0]]), \
        prev_gradient = np.array([[0, 0, 0]]), level = 1)
    array([-0.69314718])
    """
    # Constants
    a = 0.205
    b = -0.319
    c = 0.781
    d = 0.870

    # Input variable transforms
    prev_param_var = np.exp(prev_param_var)

    # Prepare variance by weighing with gradient
    prev_var_prepped = np.zeros(level)
    for level_idx in range(level):
        prev_var_prepped[level_idx] = prev_param_var[level_idx, :].T.dot(
            prev_gradient[level_idx, :] ** 2
        )

    # Equation
    p_opk_approx = (prev_p_op_mean + b * prev_var_prepped ** c) / np.sqrt(
        1 + a * prev_var_prepped ** d
    )

    # Output variable transform
    p_opk_approx = np.log(inv_logit(p_opk_approx))

    return p_opk_approx


def p_k_udpate(prev_p_k, p_opk_approx, op_choice, dilution=None):
    """
    k-ToM updates its estimate of opponents sophistication level.
    If k-ToM has a dilution parameter, it does a partial forgetting of learned
    estimates.

    >>> p_k_udpate(prev_p_k = np.array([1.]), \
        p_opk_approx = np.array([-0.69314718]), op_choice = 1, dilution = None)
    array([1.])
    """
    # Input variable transforms
    p_opk_approx = np.exp(p_opk_approx)
    if dilution:
        dilution = inv_logit(dilution)

    # Do partial forgetting
    if dilution:
        prev_p_k = (1 - dilution) * prev_p_k + dilution / len(prev_p_k)

    # Calculate
    new_p_k = op_choice * (prev_p_k * p_opk_approx / sum(prev_p_k * p_opk_approx)) + (
        1 - op_choice
    ) * (prev_p_k * (1 - p_opk_approx) / sum(prev_p_k * (1 - p_opk_approx)))

    # Force probability sum to 1
    if len(new_p_k) > 1:
        new_p_k[0] = 1 - sum(new_p_k[1 : len(new_p_k)])

    return new_p_k


def param_var_update(
    prev_p_op_mean,
    prev_param_var,
    prev_gradient,
    p_k,
    volatility,
    volatility_dummy=None,
    **kwargs
):
    """
    k-ToM updates its uncertainty / variance on its estimates of opponent's
    parameter values
    >>> param_var_update(prev_param_mean = np.array([[0, 0, 0]]), \
        prev_param_var = np.array([[0, 0, 0]]), \
        prev_gradient = np.array([0, 0, 0]), p_k = np.array([1.]), \
        volatility = -2, volatility_dummy = None)
    array([[0.12692801, 0.        , 0.        ]])
    """
    # Dummy constant: sets volatility to 0 for all except volatility opponent
    # parameter estimates
    if volatility_dummy is None:
        volatility_dummy = np.zeros(prev_param_var.shape[1] - 1)
        volatility_dummy = np.concatenate(([1], volatility_dummy), axis=None)

    # Input variable transforms
    prev_p_op_mean = inv_logit(prev_p_op_mean)
    prev_param_var = np.exp(prev_param_var)
    volatility = np.exp(volatility) * volatility_dummy

    # Calculate
    new_var = 1 / (
        1 / (prev_param_var + volatility)
        + p_k[:, np.newaxis]
        * prev_p_op_mean[:, np.newaxis]
        * (1 - prev_p_op_mean[:, np.newaxis])
        * prev_gradient ** 2
    )

    # Output variable transform
    new_var = np.log(new_var)

    return new_var


def param_mean_update(
    prev_p_op_mean, prev_param_mean, prev_gradient, p_k, param_var, op_choice
):
    """
    k-ToM updates its estimates of opponent's parameter values

    >>> param_mean_update(prev_p_op_mean, \
        prev_param_mean = np.array([[0, 0, 0]]), \
        prev_gradient = np.array([0, 0, 0]), \
        p_k = np.array([0, 0, 0]), param_var, op_choice)
        array([[0.12692801, 0.        , 0.        ]])
    """
    # Input variable transforms
    param_var = np.exp(param_var) * prev_gradient

    # Calculate
    new_param_mean = (
        prev_param_mean
        + p_k[:, np.newaxis]
        * param_var
        * (op_choice - inv_logit(prev_p_op_mean))[:, np.newaxis]
    )

    # Used for numerical purposes (similar to the VBA package)
    new_param_mean = logit(inv_logit(new_param_mean))

    return new_param_mean


def gradient_update(
    params,
    p_op_mean,
    param_mean,
    sim_prev_internal_states,
    sim_self_choice,
    sim_op_choice,
    sim_level,
    sim_agent,
    p_matrix,
    **kwargs
):
    """"""
    # Make empty list for fillin in gradients
    gradient = np.zeros(len(param_mean))

    # The gradient is calculated for each parameter one at a time
    for param in range(len(param_mean)):
        # Calculate increment
        increment = max(abs(1e-4 * param_mean[param]), 1e-4)
        # Use normal parameter estimates
        param_mean_incr = np.copy(param_mean)
        # But increment the current parameter
        param_mean_incr[param] = param_mean[param] + increment

        # Make parameter structure similar to own
        sim_params_incr = copy.deepcopy(params)
        # Populate it with estimated values, including the increment
        for param_idx, param_key in enumerate(params):
            sim_params_incr[param_key] = param_mean_incr[param_idx]

        # Simulate opponent learning using the incremented
        sim_new_internal_states_incr = learning_function(
            sim_prev_internal_states,
            sim_params_incr,
            sim_self_choice,
            sim_op_choice,
            sim_level,
            sim_agent,
            p_matrix,
            **kwargs
        )

        # Simulate opponent decision using incremented parameters
        p_op_mean_incr = decision_function(
            sim_new_internal_states_incr,
            sim_params_incr,
            sim_agent,
            sim_level,
            p_matrix,
        )[
            0
        ]  # only use the first part of the output

        # Calculate the gradient: a measure of the size of the influence of
        # the incremented parameter value
        gradient[param] = (p_op_mean_incr - p_op_mean) / increment
    return gradient


# Decision subfunctions
def p_op0_fun(p_op_mean0, p_op_var0):
    """
    0-ToM combines the mean and variance of its parameter estimate into a
    final choice probability estimate.
    NB: This is the function taken from the VBA package (Daunizeau 2014),
    which does not use 0-ToM's volatility parameter to avoid unidentifiability
    problems.

    >>> p_op0_fun(p_op_mean0 = 0.7, p_op_var0 = 0.3)
    0.6397417553178626
    """
    # Constants
    a = 0.36

    # Input variable transforms
    p_op_var0 = np.exp(p_op_var0)

    # Calculate
    p_op0 = p_op_mean0 / np.sqrt(1 + a * p_op_var0)

    # Output variable transforms
    p_op0 = inv_logit(p_op0)
    return p_op0


def p_opk_fun(p_op_mean, param_var, gradient):
    """
    k-ToM combines the mean choice probability estimate and the variances of
    its parameter estimates into a final choice probability estimate.
    NB: this is the function taken from the VBA package (Daunizeau 2014),
    which does not use k-ToM's volatility parameter to avoid unidentifiability
    issues.
    """
    # Constants
    a = 0.36

    # Input variable transforms
    param_var = np.exp(param_var)

    # Prepare variance by weighing with gradient
    var_prepped = np.sum((param_var * gradient ** 2), axis=1)

    # Calculate
    p_opk = p_op_mean / np.sqrt(1 + a * var_prepped)

    # Output variable transform
    p_opk = inv_logit(p_opk)

    return p_opk


def expected_payoff_fun(p_op, agent, p_matrix):
    """
    p_op (0 <= float <= 1): The probability of the opponent choosing 1
    agent (0 <= int <= 1): the perspective of the agent
    p_matrix (PayoffMatix): a payoff matrix

    Calculate expected payoff of choosing 1 over 0

    Examples:
    >>> staghunt = PayoffMatrix(name = 'staghunt')
    >>> expected_payoff_fun(1, agent = 0, p_matrix = staghunt)
    2
    """
    # Calculate
    expected_payoff = p_op * (
        p_matrix.payoff(1, 1, agent) - p_matrix.payoff(0, 1, agent)
    ) + (1 - p_op) * (p_matrix.payoff(1, 0, agent) - p_matrix.payoff(0, 0, agent))

    return expected_payoff


def softmax(expected_payoff, params):
    """
    Softmax function for calculating own probability of choosing 1
    """
    # Extract necessary parameters
    b_temp = params["b_temp"]
    if "bias" in params:
        bias = params["bias"]

    # Input variable transforms
    b_temp = np.exp(b_temp)

    # Divide by temperature parameter
    expected_payoff = expected_payoff / b_temp

    # Add bias, optional
    if "bias" in params:
        expected_payoff = expected_payoff + bias

    # The logit transform completes the softmax function
    p_self = inv_logit(expected_payoff)

    # Set output bounds
    if p_self > 0.999:
        p_self = 0.999
        # warn("Choice probability constrained at upper bound 0.999 to avoid
        # rounding errors", Warning)
    if p_self < 0.001:
        p_self = 0.001
        # warn("Choice probability constrained at lower bound 0.001 to avoid
        # rounding errors", Warning)

    return p_self


# Full learning and decision functions
def learning_function(
    prev_internal_states,
    params,
    self_choice,
    op_choice,
    level,
    agent,
    p_matrix,
    **kwargs
):
    """
    Examples:
    >>> penny = PayoffMatrix(name = "penny_competitive")
    >>> prev_internal_states = {'opponent_states': {}, \
        'own_states': {'p_op_mean0': 0, 'p_op_var0': 0}}
    >>> params = {'volatility': -2, 'b_temp': -1}
    >>> learning_function(prev_internal_states, params, self_choice=1, \
        op_choice=1, level=0, agent=0, p_matrix=penny)
    {'opponent_states': {},
    'own_states': {'p_op_mean0': 0.44216598162254866,
    'p_op_var0': -0.12292276280308079}}
    """
    # Extract needed parameters
    volatility = params["volatility"]
    if "dilution" in params:
        dilution = params["dilution"]
    else:
        dilution = None

    # Make empty dictionary for storing updates states
    new_internal_states = {}
    opponent_states = {}

    # If the (simulated) agent is a 0-ToM
    if level == 0:
        # Extract needed variables
        prev_p_op_mean0 = prev_internal_states["own_states"]["p_op_mean0"]
        prev_p_op_var0 = prev_internal_states["own_states"]["p_op_var0"]

        # Update 0-ToM's uncertainty of opponent choice probability
        p_op_var0 = p_op_var0_update(prev_p_op_mean0, prev_p_op_var0, volatility)

        # Update 0-ToM's mean estimate of opponent choice probability
        p_op_mean0 = p_op_mean0_update(prev_p_op_mean0, p_op_var0, op_choice)

        # Gather own internal states
        own_states = {"p_op_mean0": p_op_mean0, "p_op_var0": p_op_var0}

    # If the (simulated) agent is a k-ToM
    else:
        # Extract needed variables
        prev_p_k = prev_internal_states["own_states"]["p_k"]
        prev_p_op_mean = prev_internal_states["own_states"]["p_op_mean"]
        prev_param_mean = prev_internal_states["own_states"]["param_mean"]
        prev_param_var = prev_internal_states["own_states"]["param_var"]
        prev_gradient = prev_internal_states["own_states"]["gradient"]

        # Update opponent level probabilities
        p_opk_approx = p_opk_approx_fun(
            prev_p_op_mean, prev_param_var, prev_gradient, level
        )
        p_k = p_k_udpate(prev_p_k, p_opk_approx, op_choice, dilution)

        # Update parameter estimates
        param_var = param_var_update(
            prev_p_op_mean, prev_param_var, prev_gradient, p_k, volatility, **kwargs
        )
        param_mean = param_mean_update(
            prev_p_op_mean, prev_param_mean, prev_gradient, p_k, param_var, op_choice
        )

        # Do recursive simulating of opponent
        # Make empty structure for new means and gradients
        p_op_mean = np.zeros(level)
        gradient = np.zeros([level, param_mean.shape[1]])

        # Prepare simulated opponent perspective
        # simulated perspective swtiches own and opponent role
        sim_agent = 1 - agent
        # And previous choices
        sim_self_choice, sim_op_choice = op_choice, self_choice

        # k-ToM simulates an opponent for each level below its own
        for sim_level in range(level):

            # Further preparation of simulated perspective
            sim_prev_internal_states = copy.deepcopy(
                prev_internal_states["opponent_states"][sim_level]
            )

            # Make parameter structure similar to own
            sim_params = copy.deepcopy(params)

            # Populate it with estimated values
            for param_idx, param_key in enumerate(params):
                sim_params[param_key] = param_mean[sim_level, param_idx]

            # Simulate opponent learning (recursive)
            sim_new_internal_states = learning_function(
                sim_prev_internal_states,
                sim_params,
                sim_self_choice,
                sim_op_choice,
                sim_level,
                sim_agent,
                p_matrix,
                **kwargs
            )

            # Simulate opponent deciding
            p_op_mean[sim_level] = decision_function(
                sim_new_internal_states, sim_params, sim_agent, sim_level, p_matrix
            )[
                0
            ]  # only use the first part of the output

            # Update gradient (recursive)
            gradient[sim_level] = gradient_update(
                params,
                p_op_mean[sim_level],
                param_mean[sim_level],
                sim_prev_internal_states,
                sim_self_choice,
                sim_op_choice,
                sim_level,
                sim_agent,
                p_matrix,
                **kwargs
            )

            # Save opponent's states
            opponent_states[sim_level] = sim_new_internal_states

        # Gather own internal states
        own_states = {
            "p_k": p_k,
            "p_op_mean": p_op_mean,
            "param_mean": param_mean,
            "param_var": param_var,
            "gradient": gradient,
        }

    # Save the updated estimated and own internal states
    new_internal_states["opponent_states"] = opponent_states
    new_internal_states["own_states"] = own_states

    return new_internal_states


def decision_function(new_internal_states, params, agent, level, p_matrix):
    """

    Examples:
    >>> penny = PayoffMatrix(name = "penny_competitive")
    >>> new_internal_states = {'opponent_states': {}, \
    'own_states': {'p_op_mean0': 30, 'p_op_var0': 2}}
    >>> params = {'volatility': -2, 'b_temp': -1}
    >>> decision_function(new_internal_states, params, agent = 0, \
        level = 0, p_matrix = penny)
    -5.436561973742046
    """
    # If (simulated) agent is a 0-ToM
    if level == 0:
        # Extract needed variables
        p_op_mean0 = new_internal_states["own_states"]["p_op_mean0"]
        p_op_var0 = new_internal_states["own_states"]["p_op_var0"]

        # Estimate probability of opponent choice
        p_op = p_op0_fun(p_op_mean0, p_op_var0)

    # If the (simulated) agent is a k-ToM
    else:
        # Extract needed variables
        p_op_mean = new_internal_states["own_states"]["p_op_mean"]
        param_var = new_internal_states["own_states"]["param_var"]
        gradient = new_internal_states["own_states"]["gradient"]
        p_k = new_internal_states["own_states"]["p_k"]

        # Estimate probability of opponent choice for each simulated level
        p_opk = p_opk_fun(p_op_mean, param_var, gradient)

        # Weigh choice probabilities by level probabilities for aggregate
        # choice probability estimate
        p_op = np.sum(p_opk * p_k)

    # Calculate expected payoff
    expected_payoff = expected_payoff_fun(p_op, agent, p_matrix)

    # Softmax
    p_self = softmax(expected_payoff, params)

    # Output variable transform
    p_self = logit(p_self)

    return (p_self, p_op)


# Full k-ToM Function
def k_tom(
    prev_internal_states,
    params,
    self_choice,
    op_choice,
    level,
    agent,
    p_matrix,
    **kwargs
):
    """"""

    # Update estimates of opponent based on behaviour
    if self_choice is not None:
        new_internal_states = learning_function(
            prev_internal_states,
            params,
            self_choice,
            op_choice,
            level,
            agent,
            p_matrix,
            **kwargs
        )

    else:  # If first round or missed round, make no update
        new_internal_states = prev_internal_states

    # Calculate own decision probability
    p_self, p_op = decision_function(
        new_internal_states, params, agent, level, p_matrix
    )

    # Probability transform
    p_self = inv_logit(p_self)

    # Save own choice probability
    new_internal_states["own_states"]["p_self"] = p_self
    new_internal_states["own_states"]["p_op"] = p_op

    # Make decision
    choice = np.random.binomial(1, p_self)

    return (choice, new_internal_states)


# Initializing function
def init_k_tom(params, level, priors="default"):
    """
    >>> init_k_tom(params = {'volatility': -2, 'b_temp': -1, 'bias':0 }, \
        level=1, priors='default')
    """
    # If no priors are specified
    if priors == "default":
        # Set default priors
        priors = {"p_op_mean0": 0, "p_op_var0": 0}  # Agnostic
        if level > 0:  # the following is not used by 0-ToM
            priors["p_op_mean"] = 0
            priors["param_mean"] = np.repeat(0.0, len(params))
            priors["param_var"] = np.repeat(0.0, len(params))
            priors["gradient"] = np.repeat(0.0, len(params))
            if "bias" in params:  # Following the original VBA implementation
                priors["gradient"][-1] = 0.999999997998081

    # Make empty list for prior internal states
    internal_states = {}
    opponent_states = {}

    # If the (simulated) agent i a 0-ToM
    if level == 0:
        # Set priors for choice probability estimate and its uncertainty
        p_op_var0 = priors["p_op_var0"]
        p_op_mean0 = priors["p_op_mean0"]

        # Gather own internal states
        own_states = {"p_op_mean0": p_op_mean0, "p_op_var0": p_op_var0}

    # If the (simulated) agent is a k-ToM
    else:
        # Set priors
        p_k = np.repeat((1 / level), level)
        p_op_mean = np.repeat(priors["p_op_mean"], level)
        param_var = np.tile(priors["param_var"], (level, 1))
        param_mean = np.tile(priors["param_mean"], (level, 1))
        gradient = np.tile(priors["gradient"], (level, 1))

        # k-ToM simulates an opponent for each level below its own
        for level_index in range(level):
            # Simulate opponents to create the recursive data structure
            sim_new_internal_states = init_k_tom(params, level_index, priors)
            # Save opponent's states
            opponent_states[level_index] = sim_new_internal_states

        # Gather own internal states
        own_states = {
            "p_k": p_k,
            "p_op_mean": p_op_mean,
            "param_mean": param_mean,
            "param_var": param_var,
            "gradient": gradient,
        }

    # Save own choice probability
    own_states["p_self"] = np.nan
    own_states["p_op"] = np.nan

    # Save the updated estimated and own internal states
    internal_states["opponent_states"] = opponent_states
    internal_states["own_states"] = own_states

    return internal_states


# Testing function
if __name__ == "__main__":
    import doctest

    doctest.testmod(verbose=True)


if __name__ == "__main__":
    p_matrix = PayoffMatrix(name="penny_competitive")

    prev_internal_states = {
        "opponent_states": {
            0: {"opponent_states": {}, "own_states": {"p_op_mean0": 0, "p_op_var0": 0}}
        },
        "own_states": {
            "p_k": np.array([1.0]),
            "p_op_mean": np.array([0]),
            "param_mean": np.array([[0, 0, 0]]),
            "param_var": np.array([[0, 0, 0]]),
            "gradient": np.array([[0, 0, 0]]),
        },
    }

    params = {"volatility": -2, "b_temp": -1, "bias": 0}

    k_tom(
        prev_internal_states,
        params,
        self_choice=1,
        op_choice=1,
        level=1,
        agent=0,
        p_matrix=p_matrix,
    )
