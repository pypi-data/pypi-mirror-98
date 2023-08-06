# general imports
from pathlib import Path
import numpy as np
import importlib

# AHA imports
import magma as m

# msdsl imports
from ..common import *
from msdsl import MixedSignalModel, VerilogGenerator

BUILD_DIR = Path(__file__).resolve().parent / 'build'
DOMAIN = np.pi
RANGE = 1.0

def pytest_generate_tests(metafunc):
    pytest_sim_params(metafunc)
    pytest_real_type_params(metafunc)
    pytest_func_mode_params(metafunc)
    tests = [(0, 0.0105, 512),
             (1, 0.000318, 128)]
    if importlib.util.find_spec('cvxpy'):
        tests.append((2, 0.000232, 32))
    metafunc.parametrize('order,err_lim,numel', tests)
    metafunc.parametrize('func', [np.sin, np.cos])

def gen_model(myfunc, order=0, numel=512, real_type=RealType.FixedPoint, func_mode='sync'):
    # create mixed-signal model
    model = MixedSignalModel('model', build_dir=BUILD_DIR,
                             real_type=real_type)
    model.add_analog_input('in_')
    model.add_analog_output('out')
    model.add_digital_input('clk')
    model.add_digital_input('rst')

    # create function
    write_tables = (func_mode in {'sync'})
    real_func = model.make_function(
        myfunc, domain=[-DOMAIN, +DOMAIN], order=order, numel=numel, write_tables=write_tables)

    # apply function
    model.set_from_func(model.out, real_func, model.in_, clk=model.clk,
                        rst=model.rst, func_mode=func_mode)

    # write the model
    return model.compile_to_file(VerilogGenerator())

def test_func_sim(func, simulator, order, err_lim, numel, real_type, func_mode):
    # set the random seed for repeatable results
    np.random.seed(0)

    # create clipped version of function
    myfunc = lambda x: func(np.clip(x, -DOMAIN, +DOMAIN))

    # generate model
    model_file = gen_model(
        myfunc=myfunc, order=order, numel=numel, real_type=real_type, func_mode=func_mode)

    # declare circuit
    class dut(m.Circuit):
        name = 'test_func_sim'
        io = m.IO(
            in_=fault.RealIn,
            out=fault.RealOut,
            clk=m.In(m.Clock),
            rst=m.BitIn
        )

    # create the tester
    tester = MsdslTester(dut, dut.clk)

    # initialize
    tester.poke(dut.in_, 0)
    tester.poke(dut.clk, 0)
    tester.poke(dut.rst, 1)
    tester.eval()

    # apply reset
    tester.step(2)

    # clear reset
    tester.poke(dut.rst, 0)
    tester.step(2)

    # save the outputs
    inpts = np.random.uniform(-1.2*DOMAIN, +1.2*DOMAIN, 100)
    apprx = []
    for in_ in inpts:
        tester.poke(dut.in_, in_)
        if func_mode in {'sync'}:
            tester.step(2)
        else:
            tester.eval()
        apprx.append(tester.get_value(dut.out))

    # run the simulation
    parameters = {
        'in_range': 2*DOMAIN,
        'out_range': 2*RANGE
    }
    tester.compile_and_run(
        directory=BUILD_DIR,
        simulator=simulator,
        ext_srcs=[model_file, get_file('func_sim/test_func_sim.sv')],
        parameters=parameters,
        real_type=real_type
    )

    # evaluate the outputs
    apprx = np.array([elem.value for elem in apprx], dtype=float)

    # compute the exact response to inputs
    exact = myfunc(inpts)

    # uncomment to plot results
    # import matplotlib.pyplot as plt
    # plt.plot(inpts, apprx, '*')
    # plt.show()

    # check the result
    err = np.sqrt(np.mean((exact-apprx)**2))
    print(f'RMS error: {err}')
    assert err <= err_lim
