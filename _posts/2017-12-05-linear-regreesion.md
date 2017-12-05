---
layout: post
category: "meachine"
title:  "线性回归"
tags: [meachine learing]
---
## 线性回归
<script type="text/javascript" src="http://cdn.mathjax.org/mathjax/latest/MathJax.js?config=default"></script>

回归是指学习任务的预测目标是连续值。如根据银行客户的信息预测该这个客户的信用卡额度就是一个回归任务。
假设客户有d个属性，表示为$x=(x_1，x_2,...,x_d)$线性回归试图学得一个
通过属性的线性组合来进行预测的函数,即：

$$h(x) = w_1x_1 + w_2x_2 + ... + w_dx_d + b$$

一般用向量的形式写成

$$h(x) = w^Tx+b$$

如果我们在$x$向量中加入一个分量1，使$x$=(1;x_1;x_2;...;x_d)，那么可以把b吸收进权值向量$w$，线性回归的函数就是：

$$h(x)=w^Tx$$

当$x$是一维向量的时候$h(x)$是一条直线，当$x$是二维向量的时候，$h(x)$是一个平面，当$x$超过二维的时候，$h(x)$是一个超平面。总之，$h(x)$的假设空间是无穷的。那么如何评价假设空间中的那一条先或者超平面是最好的呢？

线性回归是统计学中研究的很多的一个学习模型。通常用均方误差$err(y^`,y)=(y^`-y)^2$来衡量预测值和真实值之间的差异。那么线性回归的学习误差可以表示为：

$$E_{in}(h)=\frac{1}{N}\sum_{n=1}^{N}(h(x_n)-y_n)^2=\frac{1}{N}\sum_{n=1}^{N}(w^Tx_n-y_n)^2$$

那么接下来的问题就是如何找到一个w使得$E_{in}(w)$最小。
为了表示方便，我们把$E_{in}(w)$做一下变形

$$E_{in}(w) = \frac{1}{N}\sum_{n=1}^N(w^Tx_n-y^n)$$
$$=\frac{1}{N}\sum_{n=1}^N(x_n^Tw-y^n)$$
$$=\frac{1}{N}\left[\begin{matrix}
x_1^Tw-y_1 \\
x_2^Tw-y_2 \\
...  \\
x_N^Tw-y_N \\
\end{matrix} \right] ^2$$

$$= \frac{1}{N}\left|\left[\begin{matrix}
x_1^T \\
x_2^T \\
...  \\
x_N^T \\
\end{matrix} \right]w - 
\left[\begin{matrix}
y_1 \\
y_2 \\
...\\
y_n \\
\end{matrix}\right]\right| ^2$$

$$=\frac{1}{N}(Xw-y)^2$$

其中$X=[x_1;x_2;...x_N]$是所有样本组成的$N*(d+1)$维矩阵，$w$是$d+1$维向量，y是每个样本对应得真实值组成的$N$维向量。

由上面的公式可以看出$E_{in}(w)$是一个关于$w$的连续的可微分的凸函数。$E_{in}(w)$取得最小值的一个必要条件就是其导数等于0。

