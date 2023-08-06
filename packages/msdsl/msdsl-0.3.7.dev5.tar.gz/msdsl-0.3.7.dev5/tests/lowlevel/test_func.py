# general imports
import numpy as np
import importlib
from pathlib import Path

# msdsl imports
from ..common import pytest_sim_params
from msdsl import Function

BUILD_DIR = Path(__file__).resolve().parent / 'build'

def pytest_generate_tests(metafunc):
    pytest_sim_params(metafunc)
    tests = [(0, 0.0105, 512),
             (1, 0.000318, 128)]
    if importlib.util.find_spec('cvxpy'):
        tests.append((2, 0.000232, 32))
    metafunc.parametrize('order,err_lim,numel', tests)
    metafunc.parametrize('f', [np.sin, np.cos])

def test_real_func(f, order, err_lim, numel):
    # set the random seed for repeatable results
    np.random.seed(0)

    # function parameters
    domain = [-np.pi, +np.pi]
    testfun = lambda x: f(np.clip(x, domain[0], domain[1]))

    # create the function
    func = Function(func=testfun, domain=domain, order=order, numel=numel)

    # evaluate function approximation
    samp = np.random.uniform(1.2*domain[0], 1.2*domain[1], 1000)
    approx = func.eval_on(samp)

    # evaluate exact function
    exact = testfun(samp)

    # check error
    err = np.sqrt(np.mean((exact-approx)**2))
    print(f'RMS error with order={order}: {err}')
    assert err <= err_lim
