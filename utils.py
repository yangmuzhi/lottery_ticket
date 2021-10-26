import numpy as np
from tqdm import tqdm

# 彩票奖金
LOTTERY_PRIZE= {-1:0, 1:1e7, 2:5e6, 3:3e3, 4:200, 5:10, 6:5}

class simulator:
    """
    彩票simulator，用于测试策略等
    """
    def __init__(self,strategy, strategy_n):
        self.strategy = strategy
        self.strategy_n = strategy_n

    def run(self, n=10000):
        """
        strategy_n: 买几张
        n: 试验次数
        """
        self.n = n

        buys = gen_jack(n)
        buys = buys.tolist()
        jacks = gen_jack(n)
        jacks = jacks.tolist()
        self.is_spots = []
        for i in range(n):
            # 判断是否中奖
            is_spot = []
            strategy_buys = self.strategy(buys[i], self.strategy_n)
            # print("strategy_buys: ", strategy_buys)
            is_spot = list(map(lambda x: check(jacks[i], x), strategy_buys))
            # print("strategy_buys: ", strategy_buys)
            # print("jacks: ", jacks[i])
            # print("is_spot: ", is_spot)
            self.is_spots.append(is_spot)
        return self.is_spots

    @property
    def profile(self):
        self.cost_daily = self.strategy_n * 2.0
        self.cost = self.cost_daily * self.n
        jack = np.array(self.is_spots).reshape(-1).tolist()
        self.income_daily = list(map(lambda x: LOTTERY_PRIZE[x], jack))
        self.income = sum(self.income_daily)
        self.profile_ = np.sum(np.array(self.income_daily)-2.0)
        return self.profile_
    
    def stock_style(self, title="彩票K线走势图", name='test', n_size=100):
        """股票风格
        开盘价格，最高价格，最低价格，收盘价格
        """
        profile = np.cumsum(np.array(self.income_daily)).reshape(-1,5)
        # .sum(axis=1) 
        # profile_sum = (profile- 5).reshape(-1,100)
        data = list(map(lambda x: [x[0], x[-1],max(x), min(x)], profile))
        return data

def draw_k_line(data ,title, name):
    """
    画k线图
    [{'date': '2021-10-01', "start_price": 0, 'max_price':5, 'min_price': -1, 'stop_price': 3}, ]
    """
    from pyecharts import options as opts
    from pyecharts.charts import Kline

    y_data = data
    x_data = list(map(str, list(range(len(y_data)))))

    c = (
        Kline(init_opts=opts.InitOpts(width="1440px", height="800px"))
        .add_xaxis(xaxis_data=x_data)
        .add_yaxis(
            "kline",
            y_data,
            itemstyle_opts=opts.ItemStyleOpts(
                color="#ec0000",
                color0="#00da3c",
                border_color="#8A0000",
                border_color0="#008F28",
            ),
        )
        .set_global_opts(
            xaxis_opts=opts.AxisOpts(is_scale=True),
            yaxis_opts=opts.AxisOpts(
                is_scale=True,
                splitarea_opts=opts.SplitAreaOpts(
                    is_show=True, areastyle_opts=opts.AreaStyleOpts(opacity=1)
                ),
            ),
            datazoom_opts=[opts.DataZoomOpts(type_="inside")],
            title_opts=opts.TitleOpts(title=title),
        )
        .render("{}.html".format(name))
    )

class exp_simulator:
    """
    用于进行大批量实验
    """
    def __init__(self, strategy, strategy_n=5):
        
        self.sim = simulator(strategy,strategy_n)
        self.strategy = strategy
        self.strategy_n = strategy_n

    def run_exp(self, exp_n=100):
        res_list = []
        self.profile = 0
        self.income = 0
        self.cost = 0
        for i in tqdm(range(exp_n)):
            res = self.sim.run()
            res_list.extend(res)
            self.profile += self.sim.profile
            self.income += self.sim.income
            self.cost += self.sim.cost
        res = np.array(res_list)
        for j in range(1,7):
            print("{} prob {}".format(j, (res==j).astype(int).sum()/(np.array(res).shape[0]*np.array(res).shape[1])))
        print("unspot prob ", (res==-1).astype(int).sum()/(np.array(res).shape[0]*np.array(res).shape[1]))
        print("total profile: ", self.profile, "total income: ", self.income, "total cost: ", self.cost)


def strategy_random(buy, n):
    # 机选n注, n为返回的buys个数
    # 把一个buy转换为n个list
    buys = gen_jack(n-1).tolist()
    buys.append(buy) 

    return buys

# 复式投注
# 单纯的蓝复式
def strategy_blue_complex(buy, n):
    # 把一个buy转换为n个list
    # 随机改变蓝球, n为返回的buys个数
    blue_ball = np.random.choice(np.arange(1,17), n, replace=False).tolist()
    buys = [buy]
    for i in range(n):
        buys.append(buy[0:-1] + [blue_ball[i]])

    return buys

# 单纯的红复式
def strategy_red_complex(buy, n):
    # 把一个buy转换为n个list
    # 随机改变红球, n为返回的buys个数，任意改变一个红球.n最大为169
    # 红球去重
    red_balls = np.random.choice(np.arange(1,34), 33, replace=False).tolist()
    red_balls = list(set(red_balls) - set(buy[0:-1]))
    buys = [buy]
    blue_ball = buy[-1]
    red_ball = buy[0:-1]
    cnt = 0
    for i in range(6):
        for red in red_balls:
            if cnt >= n:
                return buys
            red_ball[i] = red
#             print(i, red, red_ball)
            red_ball.sort()
            buys.append(red_ball + [blue_ball])
            red_ball = buy[0:-1]
            cnt += 1
    return buys
# 单纯的shuffle红复式
def strategy_red_complex_shuffle(buy, n):
    # 把一个buy转换为n个list
    # 随机改变红球, n为返回的buys个数，任意改变一个红球.n最大为169
    # 红球去重
    red_balls = np.random.choice(np.arange(1,34), 33, replace=False).tolist()
    red_balls = list(set(red_balls) - set(buy[0:-1]))
    buys = [buy]
    blue_ball = buy[-1]
    red_ball = buy[0:-1]
    for i in range(6):
        for red in red_balls:
            red_ball[i] = red
            red_ball.sort()
            buys.append(red_ball + [blue_ball])
            red_ball = buy[0:-1]
    np.random.shuffle(buys)
    return buys[0:n]
# 8+3 https://www.sohu.com/a/485535050_120231328



def gen_red(n_sample):
    # 生产红球，不重复
    ball = np.arange(1,34)
    res = list(map(lambda x: np.random.choice(ball, 6, replace=False), range(n_sample)))
    res = np.array(res)
    res.sort() #从小到大排序
    return res

def gen_jack(n_sample):
    red = gen_red(n_sample)
    blue = np.random.randint(1, 17, [n_sample, 1])
    jacks = np.concatenate([red, blue], axis=1)
    return jacks

def check(jack, buy):
    # 检查中几等奖, 输入一个jack和一个buy
    if buy == jack:
        return 1
    elif buy[0:-1] == jack[0:-1]:
        return 2
    else:
        red = buy[0:-1]
        red.extend(jack[0:-1])
        l = len(set(red))
        if l==7 and buy[-1]==jack[-1]:
            return 3
        elif (l==7 and buy[-1]!=jack[-1]) or (l==8 and buy[-1]==jack[-1]):
            return 4
        elif (l==8 and buy[-1]!=jack[-1]) or (l==9 and buy[-1]==jack[-1]):
            return 5
        elif buy[-1]==jack[-1]:
            return 6
    return -1



# def gen_all_kinds_of_jacks(jack):
#     # 罗列所有的奖, jack是一个list
#     #1st
#     res = {1:[jack]}
    
#     #2nd,15个没中奖的蓝球
#     blue = list(range(1,17))
#     blue.remove(jack[-1])
#     res[2] = list(map(lambda x:x[0][0:-1]+[x[1]] , zip(jack*15, blue)))
#     #3rd,33-6个没中奖的红球 
#     res[2] = list(map(lambda x:x[0]+[x[1]] , zip(jack[0:-1]*15, list(range(1,17)))))
#     return 