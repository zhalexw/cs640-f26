import random

import numpy as np

BANKRUPTCY_REWARD = 0
SIMULATION_SCALE = 200
INIT_DOLLARS_MIN = 500_000 // SIMULATION_SCALE
INIT_DOLLARS_MAX = 1_000_000 // SIMULATION_SCALE
DEBT_DOLLARS = 500_000 // SIMULATION_SCALE
SIMULATION_DOLLARS_MAX = 2_000_000 // SIMULATION_SCALE

EPSILON = 0.2
LEARNING_RATE = 0.1

def initialize_state():
    #create initial portfolio
    return (0, random.randrange(INIT_DOLLARS_MIN, INIT_DOLLARS_MAX + 1))

def simulate_action(input_state, input_action):
    (input_period, input_dollars) = input_state

    assert input_action in (0, 1, 2)

    if input_period >= 5:
        return (None, 0)

    if input_period == 2:
        input_dollars -= DEBT_DOLLARS

    if input_dollars <= 0:
        return (None, BANKRUPTCY_REWARD)

    if input_action == 0:
        portfolio_return = 0.001
        portfolio_std = 0.000
    elif input_action == 1:
        portfolio_return = 0.02
        portfolio_std = 0.01
    else:
        portfolio_return = 0.10
        portfolio_std = 0.10

    output_period = input_period + 1
    output_dollars = int(input_dollars * np.random.normal(1 + portfolio_return, portfolio_std))
    # truncate distribution to control number of states
    output_dollars = min(output_dollars, SIMULATION_DOLLARS_MAX)

    output_state = (output_period, output_dollars)
    # Only the final portfolio size counts toward the objective.
    output_reward = output_dollars if output_period == 5 else 0

    return output_state, output_reward


#state = (year, dollars/200)

#one action per year

#actions = 0, 1, 2

def is_terminal(state):
    return state is None or state[0] == 5

def get_q_value(Q, state, action):
    return Q.get((state, action), 0.)

def get_value(Q, state):
    if is_terminal(state): return 0
    return max(get_q_value(Q, state, a) for a in [0,1,2])

def get_best_policy(Q, state):
    if is_terminal(state): return None
    best = max(get_q_value(Q, state, a) for a in [0,1,2])
    return random.choice([a for a in [0,1,2] if get_q_value(Q, state, a) == best])

def get_action(Q, state, epsilon):
    if is_terminal(state): return None
    if random.random() < epsilon:
        return random.choice([0,1,2])
    return get_best_policy(Q, state)

def update(Q, state, action, next_state, reward, learning_rate):
    # Q(s,a) = (1 - α) Q(s,a) + α (R + γ V(s'))
    sample = reward + get_value(Q, next_state)
    Q[state, action] = (1 - learning_rate) * get_q_value(Q, state, action) + learning_rate * sample


def run_episode(Q, learning_rate, epsilon):
    state = initialize_state()
    total = 0.

    while not is_terminal(state):
        action = get_action(Q, state, epsilon)
        next_state, reward = simulate_action(state, action)
        update(Q, state, action, next_state, reward, learning_rate)
        total += reward
        state = next_state
    return total


def estimate_q_values():
    Q = {}
    for _ in range(4, -1, -1):
        for _ in range(SIMULATION_DOLLARS_MAX + 1):
            run_episode(Q, LEARNING_RATE, EPSILON)
    return Q


q_values = estimate_q_values()

with open("q_values.tsv", "w") as f:
        f.write("period\tdollars\taction\tvalue\n")
        for period in range(5):
            for dollars in range(SIMULATION_DOLLARS_MAX + 1):
                for action in range(3):
                    if q_values.get(((period, dollars), action), None) is not None:
                        f.write(f"{period}\t{dollars}\t{action}\t"
                            f"{q_values[(period, dollars), action]:.8f}\n")
