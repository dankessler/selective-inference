import numpy as np

from selection.randomized.group_lasso import group_lasso
from selection.tests.instance import gaussian_group_instance, gaussian_instance

import matplotlib.pyplot as plt
from statsmodels.distributions.empirical_distribution import ECDF
from scipy.stats import norm as ndist

def test_selected_targets(n=500,
                          p=200,
                          signal_fac=1.5,
                          sgroup=3,
                          s =10,
                          groups=np.arange(50).repeat(4),
                          sigma=1.,
                          rho=0.4,
                          randomizer_scale=1,
                          weight_frac=1.5):

    inst = gaussian_group_instance
    #inst = gaussian_instance
    const = group_lasso.gaussian
    signal = np.sqrt(signal_fac * 2 * np.log(p))

    # X, Y, beta = inst(n=n,
    #                   p=p,
    #                   signal=signal,
    #                   s=s,
    #                   equicorrelated=False,
    #                   rho=rho,
    #                   sigma=sigma,
    #                   random_signs=True)[:3]

    X, Y, beta = inst(n=n,
                      p=p,
                      signal=signal,
                      sgroup=sgroup,
                      groups=groups,
                      equicorrelated=False,
                      rho=rho,
                      sigma=sigma,
                      random_signs=True)[:3]

    n, p = X.shape

    sigma_ = np.std(Y)
    weights = dict([(i, weight_frac * sigma_ * 2 * np.sqrt(2)) for i in np.unique(groups)])
    conv = const(X, Y, groups, weights, randomizer_scale=randomizer_scale * sigma_)
    signs = conv.fit()
    nonzero = signs != 0
    print("check dimensions of selected set ", nonzero.sum())

    if nonzero.sum() > 0:
        if n>p:
            dispersion = np.linalg.norm(Y - X.dot(np.linalg.pinv(X).dot(Y))) ** 2 / (n - p)
        else:
            dispersion = sigma_ ** 2

        estimate, observed_info_mean, _, pval, intervals, _ = conv.selective_MLE(dispersion=dispersion)

        beta_target = np.linalg.pinv(X[:, nonzero]).dot(X.dot(beta))

        pivot_MLE = ndist.cdf((estimate - beta_target)/np.sqrt(np.diag(observed_info_mean)))

        coverage = (beta_target > intervals[:, 0]) * (beta_target <
                                                      intervals[:, 1])
        return pval[beta[nonzero] == 0], pval[
            beta[nonzero] != 0], coverage, intervals, pivot_MLE



def main(nsim=500):
    P0, PA, cover, pivot = [], [], [], []

    n, p, sgroup = 500, 200, 5

    for i in range(nsim):
        p0, pA, cover_, intervals, pivot_ = test_selected_targets(n=n, p=p, sgroup=sgroup)
        avg_length = intervals[:, 1] - intervals[:, 0]

        cover.extend(cover_)
        pivot.extend(pivot_)
        P0.extend(p0)
        PA.extend(pA)
        print(np.mean(cover), np.mean(avg_length),
            'coverage + length so far')

    plt.clf()
    ecdf_MLE = ECDF(np.asarray(pivot))
    grid = np.linspace(0, 1, 101)
    plt.plot(grid, ecdf_MLE(grid), c='blue', marker='^')
    plt.plot(grid, grid, 'k--')
    plt.show()

main(nsim=100)
