import numpy as np
import scipy.stats as stats
import matplotlib.pyplot as plt

plt.style.use('fivethirtyeight')
font= {'size':10}
plt.rc('font', **font)

def flip_coin(n,p=0.5):
    return stats.binomial(1, p=p).rvs(n)

def coin_log_likelihood(p, flips):
    return np.sum(np.log(np.array([1-p,p])[flips]))

def bar_chart(ax, probs, flips):
    bars = [coin_log_likelihood(p, flips) for p in probs]
    title_lst = np.where(flips, 'H','T')
    title = ' '.join(title_lst)
    tick_loc = np.arange(len(probs))
    xlabel = probs
    ax.bar(tick_loc, bars, label=probs, alpha=0.8)
    ax.set_xticklabels([f'{x:.1f}' for x in xlabel])
    ax.set_xticks(ticks=tick_loc)
    ax.set_title(title)
    ax.set_xlabel('p')
    ax.set_ylabel('Log Likelihood')

def max_likelihood(arr):
    return np.argmax(arr)

def plot_coin_likelihood_continuous(ax, flips):
    title_lst = np.where(flips, 'H','T')
    title = ' '.join(title_lst)
    x = np.linspace(0,1,250)
    y = [coin_log_likelihood(p, flips) for p in x]
    max = x[max_likelihood(y)]
    ax.plot(x,y)
    ax.set_title(title)
    ax.set_xlabel('p')
    ax.set_ylabel('Log Likelihood')
    ax.axvline(max, linestyle='--', color='red', linewidth=1, label='Max Likelihood')


    

if __name__ == "__main__":
    data = np.array([1,0,0,0,1,1,0,0,0,0])
    probs = np.linspace(0,1,11)
    bars = [coin_log_likelihood(p,data) for p in probs]
    # fig, ax = plt.subplots()
    # bar_chart(ax, probs, data)
    fig, axs = plt.subplots(2,5, figsize=(14,4))
    plt_lst = [[1],[1,0],[1,0,0],[1,0,0,0],[1,0,0,0,1],[1,0,0,0,1,1],
               [1,0,0,0,1,1,0],[1,0,0,0,1,1,0,0],[1,0,0,0,1,1,0,0,0],
               [1,0,0,0,1,1,0,0,0,0]]
    for plot, ax in zip(plt_lst, axs.flatten()):
        plot_coin_likelihood_continuous(ax, plot)

    plt.tight_layout()

    # fig, ax = plt.subplots()
    # plot_coin_likelihood_continuous(ax, data)
    plt.legend()
    plt.show()
    
    
    """
    #4 0.25 is more likely to be the probability of this dataset because it has
    the highest log likelihood.
    """