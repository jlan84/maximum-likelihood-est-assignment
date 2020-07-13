import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as stats

plt.style.use('ggplot')


def flip_coin(n, p):
    """Flip a coin of fairness p, n times.
    
    Parameters
    ----------
    n: int
      The number of times to flip the coin.

    p: float, between zero and one.
      The probability the coin flips heads.

    Returns
    -------
    flips: np.array of ints
      The results of the coin flips, where 0 is a tail and 1 is a head.
    """
    return np.random.binomial(1, 0.5, size=n)
flips = flip_coin(10,0.5)
print(flips)


def coin_log_likelihood(p, flips):
    """Return the log-likelihood of a parameter p given a sequence of coin flips.
    """
    binomial = stats.binom(n=1, p=p)
    log_sum = 0
    for flip in flips:
        log_sum += np.log(binomial.pmf(flip))
    return log_sum



flip_data = np.array([1,0,0,0,1,1,0,0,0,0])
print(coin_log_likelihood(0.5, flip_data), coin_log_likelihood(0.25, flip_data))



def plot_coin_likelihood(ax, ps, data):
    logList = []
    for i in range(len(ps)):
      logList.append(coin_log_likelihood(ps[i], data))
    tick_loc = np.arange(len(logList))
    ax.bar(tick_loc, [x for x in logList], width=0.8, alpha=0.7)
    ax.set_xticks(ticks=tick_loc)
    ax.set_xticklabels([str(x) for x in ps])
    

# fig, ax = plt.subplots()
# plot_coin_likelihood(ax, [.25, .5], flip_data)

# plt.show()

# fig, axs = plt.subplots(2,5,figsize=(16,8))

data = np.array([[1], [1,0], [1,0,0], [1,0,0,0], [1,0,0,0,1], [1,0,0,0,1,1], [1,0,0,0,1,1,0], [1,0,0,0,1,1,0,0], [1,0,0,0,1,1,0,0,0], [1,0,0,0,1,1,0,0,0,0]])
# ps = [0.25, 0.5]


# for datum, ax in zip(data, axs.flatten()):
#     plot_coin_likelihood(ax, ps, datum)
#     print(datum)
#     ax.set_title(f'flips = {np.array(["T","H"])[datum]}')





# plt.tight_layout()
# plt.show()







def maximum_coin_likelihood(data):
  x = np.linspace(0.01,.99,100)
  likelihoods = [coin_log_likelihood(p=p, flips=data) for p in x]
  return x[np.argmax(likelihoods)]


def plot_coin_likelihood_continuous(ax, data):
  x = np.linspace(0.01,.99,100)
  likelihoods = [coin_log_likelihood(p=p, flips=data) for p in x]
  ax.plot(x, likelihoods)
  maxLike = maximum_coin_likelihood(data)
  ax.axvline(maxLike, color='grey', linestyle='--')

fig, ax = plt.subplots()
plot_coin_likelihood_continuous(ax, flip_data)
plt.show()

print(f'{maximum_coin_likelihood(flip_data):.2f}')


fig, axs = plt.subplots(2,5, figsize=(12,12))

for datum, ax in zip(data, axs.flatten()):
  plot_coin_likelihood_continuous(ax, datum)
  ax.set_title(f'flips = {np.array(["T","H"])[datum]} {maximum_coin_likelihood(datum)}')
  
plt.show() 


