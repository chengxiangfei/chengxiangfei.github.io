import numpy as np

# 状态转移概率
"""
        sunny cloudy rainy
sunny   0.5,  0.375,  0.125
cloudy  0.25, 0.125,  0.625
rainy   0.25, 0.375,  0.375
"""
tran = np.array([[0.5, 0.375, 0.125],
                 [0.25, 0.125, 0.625],
                 [0.25, 0.375, 0.375]])

"""
输出观测概率, 即发射概率
        dry,  dryish,   damp,   soggy
sunny   0.6,   0.2,     0.15,   0.05
cloudy  0.25,  0.25,    0.25,   0.25
rainy   0.05,  0.10,    0.35,   0.50
"""
laun = np.array([[0.6, 0.2, 0.15, 0.05],
                 [0.25, 0.25, 0.25, 0.25],
                 [0.05, 0.1, 0.35, 0.5]])
"""
初始状态的概率, sunny, cloudy, rainy
"""
init = np.array([0.63, 0.17, 0.2])  # 初始状态

"""
观测系列(dry, damp, soggy)
"""
look = np.array([0, 2, 3])  # 观测序列
kind = ['Sunny', 'Cloudy', 'Rainy']


def forward(tran, laun, init, look):
    #初始化 前向因子1  alpha(1) = init(i) * launch(look[0])
    alpha = init * laun[:, look[0]]
    T = len(look)
    N = tran.shape[0]
    for i in range(1, T):
        # 归纳T个时刻

        tmp = np.copy(alpha)
        for j in range(N):
            # j 代表每个状态，算出每个状态的概率之后，求和
            alpha[j] = sum(tmp*tran[:,j]) *laun[j, look[i]]
    return sum(alpha)


def backup(tran, laun, init, look):
    # 初始化beta（1） = [1,1,1,]
    T = len(look)
    N = tran.shape[0]
    beta = np.array([1.0]*N)
    print(beta)
    for i in range(T-2, -1, -1):
        tmp = np.copy(beta)
        for j in range(N):
            # print(tmp, tran[:,j], laun[:, look[i+1]])
            beta[j] = sum(tmp*tran[:,j] * laun[:, look[i+1]])
    return sum(beta * init * laun[:, look[0]])


def viterbi(tran, laun, init, look):
    # 初始化delta
    T = len(look)
    N = tran.shape[0]
    delta = init * laun[:, look[0]]
    phi = [np.argmax(delta)]
    for i in range(1, T):
        tmp = np.copy(delta)
        for j in range(N):
            delta[j] = max(tmp * tran[:, j]) * laun[j, look[i]]
        phi.append(np.argmax(delta))
    return phi


print(forward(tran, laun, init, look), "************")
print(backup(tran, laun, init, look))
print(viterbi(tran, laun, init, look))
a = np.array([1,2])
b = np.array([3,4])
c = np.array([5,6])
print(a*b*c)


