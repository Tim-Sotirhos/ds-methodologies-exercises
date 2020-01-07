import matplotlib.pyplot as plt
import numpy as np
from scipy import stats
import itertools as it
import pandas as pd



np.random.seed(123)

# Warmup
# What probability distribution would you use to model the scenario outlined above?
# I would use a Binomial Distribution (number of successes after a number of trials)

# Calculate all the requested probabilities.

# Prob only 1 subject leaves
stats.binom(10, .70).cdf(1)
stats.binom(20, .70).cdf(1)
stats.binom(10, .80).cdf(1)
stats.binom(20, .80).cdf(1)
stats.binom(10, .90).cdf(1)
stats.binom(20, .90).cdf(1)

# Prob only half of the subjects leaves
stats.binom(10, .70).cdf(5)
stats.binom(20, .70).cdf(10)
stats.binom(10, .80).cdf(5)
stats.binom(20, .80).cdf(10)
stats.binom(10, .90).cdf(5)
stats.binom(20, .90).cdf(10)

# Prob all subjects stay
stats.binom(10, .70).pmf(0)
stats.binom(20, .70).pmf(0)
stats.binom(10, .80).pmf(0)
stats.binom(20, .80).pmf(0)
stats.binom(10, .90).pmf(0)
stats.binom(20, .90).pmf(0)

def distributions_example5():
    x = np.arange(1, 21)
    y = stats.binom(10, .70).pmf(x)
    plt.bar(x, y, width=1, edgecolor='black', color='white')

    plt.bar(0, stats.binom(10, .70).pmf(0), width=1, color='darkseagreen', edgecolor='black')
    plt.title('Binomial Distribution for n=10, p=.70')
    plt.xlabel('x')
    plt.ylabel('pmf(x)')

    plt.annotate('$P(X = 0) = {:.3f}$'.format(stats.binom(10, .70).pmf(0)),
                 (0, stats.binom(10, .70).pmf(0)), xytext=(5, .25),
                 arrowprops={'arrowstyle': '->'})

distributions_example5()


def distributions_example4():
    plt.figure(figsize=(8, 5))

    x1 = np.arange(0, 11)
    y1 = stats.binom(20, .70).pmf(x1)
    plt.bar(x1, y1, width=1, edgecolor='black', color='white')

    x2 = np.arange(11, 20)
    y2 = stats.binom(20, .70).pmf(x2)
    plt.bar(x2, y2, width=1, edgecolor='black', color='darkseagreen')

    plt.title('Binomial Distribution with n=20, p=.70')
    plt.ylabel('pmf(x)')
    plt.xlabel('x')

    plt.annotate('', xy=(11, .07), xytext=(20, .07), xycoords='data', textcoords='data', arrowprops={'arrowstyle': '|-|'})
    plt.text(20, .08, 'P(X > 10)', ha='center', va='center')

distributions_example4()

ps = [.7, .8, .9]
ns = [10, 20]

for p in ps:
    for n in ns:
        print('\n--- p =', p, 'n =', n)
        print('  P(half or more stay) =', stats.binom(n, p).sf(n / 2))
        print('  P(one leaves) =', stats.binom(n, p).pmf(n - 1))
        print('  P(all stay) =', stats.binom(n, p).pmf(n))

def calc_probs(n, p):
    return {
        'n subjects': n,
        'P(subject stays)': p,
        'P(half or more stay)': stats.binom(n, p).sf(n / 2),
        'P(one leaves)': stats.binom(n, p).pmf(n - 1),
        'P(all stay)': stats.binom(n, p).pmf(n),
    }
    
pd.DataFrame([calc_probs(n, p) for n, p in it.product(ns, ps)])
