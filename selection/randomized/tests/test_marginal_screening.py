import numpy as np

from selection.randomized.marginal_screening import BH, marginal_screening
import selection.randomized.marginal_screening
from importlib import reload; reload(selection.randomized.marginal_screening)
from selection.tests.instance import gaussian_instance

def test_BH(n=500, 
            p=100, 
            signal_fac=1.6, 
            s=5, 
            sigma=3, 
            rho=0.4, 
            randomizer_scale=0.25,
            use_MLE=True):

    while True:
        inst = gaussian_instance
        signal = np.sqrt(signal_fac * 2 * np.log(p))
        X, Y, beta = inst(n=n,
                          p=p,
                          signal=signal,
                          s=s,
                          equicorrelated=False,
                          rho=rho,
                          sigma=sigma,
                          random_signs=True)[:3]

        idx = np.arange(p)
        sigmaX = rho ** np.abs(np.subtract.outer(idx, idx))

        n, p = X.shape

        q = 0.1
        BH_select = BH(-X.T.dot(Y),
                       sigma**2 * X.T.dot(X),
                       randomizer_scale * sigma,
                       q)

        boundary = BH_select.fit()
        nonzero = boundary != 0

        if nonzero.sum() > 0:
            observed_target, cov_target, crosscov_target_score, alternatives = BH_select.form_targets(nonzero)
            if use_MLE:
                estimate, _, _, pval, intervals, _ = BH_select.selective_MLE(observed_target,
                                                                             cov_target,
                                                                             crosscov_target_score)
                # run summary
            else:
                _, pval, intervals = BH_select.summary(observed_target, 
                                                       cov_target, 
                                                       crosscov_target_score, 
                                                       alternatives,
                                                       compute_intervals=True)

            beta_target = np.linalg.pinv(X[:, nonzero]).dot(X.dot(beta))
            print("beta_target and intervals", beta_target, intervals)
            coverage = (beta_target > intervals[:, 0]) * (beta_target < intervals[:, 1])
            print("coverage for selected target", coverage.sum()/float(nonzero.sum()))
            return pval[beta[nonzero] == 0], pval[beta[nonzero] != 0], coverage, intervals

def test_marginal(n=500, 
                  p=50, 
                  s=5, 
                  sigma=3, 
                  rho=0.4, 
                  randomizer_scale=0.25,
                  use_MLE=True):

    while True:
        X = gaussian_instance(n=n,
                              p=p,
                              equicorrelated=False,
                              rho=rho)[0]
        W = rho**(np.fabs(np.subtract.outer(np.arange(p), np.arange(p))))
        sqrtW = np.linalg.cholesky(W)
        sigma = 1.5
        Z = np.random.standard_normal(p).dot(sqrtW.T) * sigma
        beta = np.ones(p) * 5 * sigma
        beta[s:] = 0
        np.random.shuffle(beta)

        true_mean = W.dot(beta)
        score = Z + true_mean

        idx = np.arange(p)

        n, p = X.shape

        q = 0.1
        marginal_select = marginal_screening(score,
                                             W * sigma**2,
                                             randomizer_scale * sigma,
                                             q)

        boundary = marginal_select.fit()
        nonzero = boundary != 0

        if nonzero.sum() > 0:
            observed_target, cov_target, crosscov_target_score, alternatives = marginal_select.form_targets(nonzero)
            if use_MLE:
                estimate, _, _, pval, intervals, _ = marginal_select.selective_MLE(observed_target,
                                                                                   cov_target,
                                                                                   crosscov_target_score)
            # run summary
            else:
                _, pval, intervals = marginal_select.summary(observed_target, 
                                                             cov_target, 
                                                             crosscov_target_score, 
                                                             alternatives,
                                                             compute_intervals=True)

            print(pval)
            beta_target = cov_target.dot(true_mean[nonzero])
            print("beta_target and intervals", beta_target, intervals)
            coverage = (beta_target > intervals[:, 0]) * (beta_target < intervals[:, 1])
            print("coverage for selected target", coverage.sum()/float(nonzero.sum()))
            return pval[beta[nonzero] == 0], pval[beta[nonzero] != 0], coverage, intervals

def test_simple(n=100,
                p=5,
                s=3,
                use_MLE=False):

    while True:
        Z = np.random.standard_normal(p)
        beta = np.ones(p) * 5
        beta[s:] = 0
        np.random.shuffle(beta)

        true_mean = beta
        score = Z + true_mean

        idx = np.arange(p)

        q = 0.1
        marginal_select = marginal_screening(score,
                                             np.identity(p),
                                             1.,
                                             q)

        boundary = marginal_select.fit()
        nonzero = boundary != 0

        if nonzero.sum() > 0:

            observed_target, cov_target, crosscov_target_score, alternatives = marginal_select.form_targets(nonzero)
            stop

            if use_MLE:
                estimate, _, _, pval, intervals, _ = marginal_select.selective_MLE(observed_target,
                                                                                   cov_target,
                                                                                   crosscov_target_score)
            # run summary
            else:
                _, pval, intervals = marginal_select.summary(observed_target, 
                                                             cov_target, 
                                                             crosscov_target_score, 
                                                             alternatives,
                                                             compute_intervals=True)

            print(pval)
            beta_target = cov_target.dot(true_mean[nonzero])
            print("beta_target and intervals", beta_target, intervals)
            coverage = (beta_target > intervals[:, 0]) * (beta_target < intervals[:, 1])
            print("coverage for selected target", coverage.sum()/float(nonzero.sum()))
            return pval[beta[nonzero] == 0], pval[beta[nonzero] != 0], coverage, intervals


def main(nsim=5000, test_fn=test_BH, use_MLE=False):

    P0, PA, cover, length_int = [], [], [], []
    for i in range(nsim):
        p0, pA, cover_, intervals = test_fn(use_MLE=use_MLE)

        cover.extend(cover_)
        P0.extend(p0)
        PA.extend(pA)
        print(np.mean(cover),'coverage so far')


