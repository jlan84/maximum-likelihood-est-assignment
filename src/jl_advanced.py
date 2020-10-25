import numpy as np
import scipy.stats as stats
import matplotlib.pyplot as plt
from scipy.special import factorial

plt.style.use('seaborn-dark-palette')

def bar_chart(ax, data, title=None):
    tick_loc = np.arange(len(data))
    xlabel = np.arange(len(data))
    ax.bar(tick_loc, data, label= 'Observed alpha Particle Counts', alpha=0.8)
    ax.set_xticks(ticks=tick_loc)
    ax.set_xticklabels([str(x) for x in xlabel])
    ax.set_title(title)
    ax.set_ylabel('# of Events')
    ax.set_xlabel('# of alpha Particles')

def impose_poisson(ax, lam, data):
    x_range = np.linspace(0, lam*3, 100)
    y = [np.sum(data)*(np.exp(-lam)*np.power(lam, x)/factorial(x)) for x in x_range]
    ax.plot(x_range, y, label=f'Poisson Distribution lamda={lam}')
    

def log_like(lam, data):
    likelihoods = np.sum(count*np.log(stats.poisson(mu=lam).pmf(k)) for k, count
                         in enumerate(data))
    return likelihoods

    





if __name__ == "__main__":

    alpha_particle_counts = np.array([
    57, 203, 383, 525, 532, 408, 273, 139, 49, 27, 10, 4, 2, 0])
    fig, ax = plt.subplots()
    
    bar_chart(ax, alpha_particle_counts, title='Alpha Particle Counts')
    impose_poisson(ax, 3.87, alpha_particle_counts)
    
    """
    #2 The data appears to be normally distributed
    """
    # lamdas = np.linspace(0.1,12, num=250)
    # y = [log_like(lam, alpha_particle_counts) for lam in lamdas]
    # max_likelihood = lamdas[np.argmax(y)]
    
    
    # fig, ax = plt.subplots()
    # ax.plot(lamdas,y)
    # ax.axvline(max_likelihood, linestyle='--', color='red', linewidth=1)
    plt.legend()
    plt.show()


    