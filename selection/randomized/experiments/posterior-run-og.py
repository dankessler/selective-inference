import numpy as np
from selection.randomized.tests.test_group_lasso_posterior import test_posterior_inference
from selection.randomized.query import naive_confidence_intervals
from pypet import Environment, cartesian_product
from selection.tests.instance import gaussian_group_instance
from selection.randomized.group_lasso import group_lasso, posterior


def main(nreps=1):
    # Create the environment
    env = Environment(trajectory='GrpLasso_OG_Balanced',
                      comment='Randomized Group lasso, OG, with balanced groups',
                      multiproc=True,
                      log_multiproc=True,
                      use_scoop=True,
                      wrap_mode='NETQUEUE',
                      overwrite_file=True,
                      filename='./hdf5/')

    # get the trajectory
    traj = env.traj

    # setup overlapping groups

    # Now add the parameters with defaults
    groups = {}
    for k in range(0, 34):
        groups[k] = range(k*3, k*3 + 4)

    traj.f_add_parameter('n', 500)
    traj.f_add_parameter('p', 103)
    traj.f_add_parameter('signal_fac', np.float64(0.))
    traj.f_add_parameter('groups', groups)
    traj.f_add_parameter('sgroup', 3)
    traj.f_add_parameter('sigma', 1)
    traj.f_add_parameter('rho', 0.35)
    traj.f_add_parameter('randomizer_scale', 0.3)
    traj.f_add_parameter('weight_frac', 1.0)
    traj.f_add_parameter('seed', 0)  # random seed
    traj.f_add_parameter('std', False)  # standardized mode
    traj.f_add_parameter('og', True)  # overlapping groups mode

    seeds = [19860 + i for i in range(nreps)]  # offset seed for each rep

    # specify parameters to explore
    traj.f_explore(cartesian_product({"signal_fac": np.linspace(0.1, 1.5, 15),
                                      'sgroup': [3],
                                      'seed': seeds}))

    env.run(coverage_experiment)

    env.disable_logging()


if __name__ == '__main__':
    # Let's make the python evangelists happy and encapsulate
    # the main function as you always should ;-)
    main(100)
