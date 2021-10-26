from utils import gen_red, gen_jack, check, simulator, \
strategy_random, LOTTERY_PRIZE, exp_simulator, \
strategy_blue_complex, strategy_red_complex, draw_k_line, \
check, strategy_red_complex_shuffle

import numpy as np
import matplotlib.pyplot as plt
from collections import Counter

# 实验次数 = exp_n * 10000
exp_n = 10

print("随机")
exp = exp_simulator(strategy_random)
exp.run_exp(exp_n)

print("蓝球复式")
exp = exp_simulator(strategy_blue_complex)
exp.run_exp(exp_n)

print("红球复式")
exp = exp_simulator(strategy_red_complex_shuffle)
exp.run_exp(exp_n)
 

