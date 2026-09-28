import numpy as np
import matplotlib.pyplot as plt

class BernoulliBandit:
    """Stationary k-armed Bernoulli bandit (the §2.3 testbed with 0/1 rewards)."""

    def __init__(self, k=10, rng=None):
        self.k = k
        self.rng = rng if rng is not None else np.random.default_rng()
        self.p = self.rng.uniform(0.0, 1.0, size=k)   # hidden true conversion rates

    @property
    def optimal_arm(self):
        return int(np.argmax(self.p))

    def pull(self, a):
        return float(self.rng.random() < self.p[a])


class BernoulliBanditDrift(BernoulliBandit):
    """Nonstationary variant: p*(a) random-walks after every pull."""

    def __init__(self, k=10, rng=None, sigma=0.01):
        super().__init__(k, rng)
        self.sigma = sigma

    def pull(self, a):
        reward = float(self.rng.random() < self.p[a])          # reward from current rates
        self.p = np.clip(self.p + self.rng.normal(0.0, self.sigma, size=self.k), 0.0, 1.0)
        return reward


class EpsilonGreedyAgent:
    def __init__(self, k=10, epsilon=0.1, step="sample_average", alpha=0.1, rng=None):
        assert step in ("sample_average", "constant")
        self.k = k
        self.epsilon = epsilon
        self.step = step
        self.alpha = alpha
        self.rng = rng if rng is not None else np.random.default_rng()
        self.Q = np.zeros(k)          # value estimates
        self.N = np.zeros(k, int)     # times each arm was chosen

    def select(self):
        if self.rng.random() < self.epsilon:
            return int(self.rng.integers(self.k))          # explore
        best = np.flatnonzero(self.Q == self.Q.max())      # greedy, random tie-break
        return int(self.rng.choice(best))

    def update(self, a, r):
        self.N[a] += 1
        step = (1.0 / self.N[a]) if self.step == "sample_average" else self.alpha
        self.Q[a] += step * (r - self.Q[a])


class UCBAgent:
    """UCB1 action selection (Sutton & Barto 2.7 with c = sqrt(2))."""

    def __init__(self, k=10, c=np.sqrt(2.0), rng=None):
        self.k = k
        self.c = c
        self.rng = rng if rng is not None else np.random.default_rng()
        self.Q = np.zeros(k)
        self.N = np.zeros(k, int)
        self.t = 0

    def select(self):
        self.t += 1
        if 0 in self.N:
            return int(np.flatnonzero(self.N == 0)[0])  # explore untried actions first
        ucb = self.Q + self.c * np.sqrt(np.log(self.t) / self.N)  #Q(a) + c * sqrt(ln t / N(a))
        best = np.flatnonzero(ucb == ucb.max())      
        return int(self.rng.choice(best))

    def update(self, a, r):
        self.N[a] += 1
        self.Q[a] = (self.N[a] - 1) / self.N[a] * self.Q[a] + r / self.N[a]





def run(make_bandit, make_agent, n_steps, n_runs, rng):
    optimal = np.zeros(n_steps)
    rewards = np.zeros(n_steps)
    for _ in range(n_runs):
        bandit = make_bandit(rng)
        agent = make_agent(rng)
        for t in range(n_steps):
            opt = bandit.optimal_arm     # read before pull (drift moves it)
            a = agent.select()
            r = bandit.pull(a)
            agent.update(a, r)
            optimal[t] += (a == opt)
            rewards[t] += r
    return optimal / n_runs, rewards / n_runs


rng = np.random.default_rng(2)
n_runs, n_steps = 200, 1000

plt.figure(figsize=(8, 5))
for label, make_agent in [
    ("UCB1 (c = sqrt 2)", lambda r: UCBAgent(10, c=np.sqrt(2.0), rng=r)),
    ("UCB (c = 1)", lambda r: UCBAgent(10, c=1.0, rng=r)),
    ("epsilon-greedy (eps = 0.1)", lambda r: EpsilonGreedyAgent(10, epsilon=0.1, rng=r)),
]:
    optimal, _ = run(lambda r: BernoulliBandit(10, rng=r), make_agent, n_steps, n_runs, rng)
    plt.plot(100 * optimal, label=label)

plt.xlabel("Step")
plt.ylabel("% Optimal action")
plt.title("Experiment C - UCB1 vs. epsilon-greedy (stationary)")
plt.legend()
plt.tight_layout()
plt.savefig("experiment_C.png", dpi=120)
plt.show()