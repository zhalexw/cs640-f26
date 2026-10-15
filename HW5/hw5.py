import random

import numpy as np

BANKRUPTCY_REWARD = 0
SIMULATION_SCALE = 200
INIT_DOLLARS_MIN = 500_000 // SIMULATION_SCALE
INIT_DOLLARS_MAX = 1_000_000 // SIMULATION_SCALE
DEBT_DOLLARS = 500_000 // SIMULATION_SCALE
SIMULATION_DOLLARS_MAX = 2_000_000 // SIMULATION_SCALE
PORTFOLIOS = ((0.001, 0.0), (0.02, 0.01), (0.10, 0.10))

def normal_cdf(z):
    a = np.abs(z)
    t = 1.0 / (1.0 + 0.2316419 * a)
    tail = np.exp(-0.5 * a * a) * 0.3989422804014327 * t * (
        0.319381530 + t * (-0.356563782 + t * (1.781477937 + t *
        (-1.821255978 + t * 1.330274429)))
    )
    return np.where(z >= 0, 1.0 - tail, tail)


def simulate_action(balance, mean_return, std_return, next_values):
    if balance <= 0:
        return 0.0
    if std_return == 0:
        next_balance = min(int(balance * (1 + mean_return)), SIMULATION_DOLLARS_MAX)
        return float(next_values[next_balance])

    mean = balance * (1 + mean_return)
    std = balance * std_return
    lo = max(0, int(np.floor(mean - 8 * std)))
    hi = min(SIMULATION_DOLLARS_MAX - 1, int(np.ceil(mean + 8 * std)))
    value = 0.0
    if lo <= hi:
        outcomes = np.arange(lo, hi + 1)
        edges = (np.arange(lo, hi + 2) - mean) / std
        cdf = normal_cdf(edges)
        probabilities = np.diff(cdf)
        if lo == 0:
            probabilities[0] = cdf[1]
        value = float(np.dot(probabilities, next_values[outcomes]))
    if hi == SIMULATION_DOLLARS_MAX - 1:
        cap_z = np.array([(SIMULATION_DOLLARS_MAX - mean) / std])
        value += float((1 - normal_cdf(cap_z)[0])
                       * next_values[SIMULATION_DOLLARS_MAX])
    return value


def estimate_q_values():
    next_values = np.arange(SIMULATION_DOLLARS_MAX + 1, dtype=float)
    Q = {}
    returns = ((0.001, 0.0), (0.02, 0.01), (0.10, 0.10))
    for period in range(4, -1, -1):
        current_values = np.zeros(SIMULATION_DOLLARS_MAX + 1)
        for dollars in range(SIMULATION_DOLLARS_MAX + 1):
            invested = dollars - DEBT_DOLLARS if period == 2 else dollars
            for action, (mean_return, std_return) in enumerate(returns):
                Q[(period, dollars), action] = simulate_action(
                    invested, mean_return, std_return, next_values
                )
            current_values[dollars] = max(Q[(period, dollars), a] for a in range(3))
        next_values = current_values
    return Q




q_values = estimate_q_values()

with open("q_values.tsv", "w") as f:
        f.write("period\tdollars\taction\tvalue\n")
        for period in range(5):
            for dollars in range(SIMULATION_DOLLARS_MAX + 1):
                for action in range(3):
                    f.write(f"{period}\t{dollars}\t{action}\t"
                            f"{q_values[(period, dollars), action]:.8f}\n")
