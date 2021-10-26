## 彩票策略回测模拟器
- onwer: 小木吱吱
- 联系方式：公众号
- 在彩票模拟器上，模拟测试不同的策略的期望收益
- 在彩票模拟器上，像炒股一样，在一段时间回测不同的策略

## 用法

- 模拟
```{shell}
python run.py
```
- 回测策略画K线图
```{shell}
from utils import gen_red, gen_jack, check, simulator, \
strategy_random, LOTTERY_PRIZE, exp_simulator, \
strategy_blue_complex, strategy_red_complex, draw_k_line, \
check, strategy_red_complex_shuffle
import numpy as np

exp_n = 1
print("随机")
exp = exp_simulator(strategy_random)
exp.run_exp(exp_n)

profile = np.cumsum(np.array(exp.sim.income_daily)-1).reshape(-1,5)
data = list(map(lambda x: [x[0], x[-1],max(x), min(x)], profile))
data = data[0:100]

# 画K线图，生成在test.html里
draw_k_line(data, title="K线图", name="test")
```