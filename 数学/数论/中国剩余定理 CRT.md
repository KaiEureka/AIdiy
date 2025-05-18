
## 定义

中国剩余定理 (Chinese Remainder Theorem, CRT) 可求解如下形式的一元线性同余方程组（其中 $n_1, n_2, \cdots, n_k$ 两两互质）：

$$
\begin{cases}
x &\equiv a_1 \pmod {n_1} \\
x &\equiv a_2 \pmod {n_2} \\
&\vdots \\
x &\equiv a_k \pmod {n_k} \\
\end{cases}
$$


## 过程

1.  计算所有模数的积 $n$；
2.  对于第 $i$ 个方程：
1.  计算 $m_i=\frac{n}{n_i}$；
2.  计算 $m_i$ 在模 $n_i$ 意义下的 [逆元](逆元.md)  $m_i^{-1}$；
3.  计算 $c_i=m_im_i^{-1}$（**不要对 $n_i$ 取模**）。
3.  方程组在模 $n$ 意义下的唯一解为：$x=\sum_{i=1}^k a_ic_i \pmod n$。

## 实现

```cpp
LL CRT(int k, LL* a, LL* r) {
LL n = 1, ans = 0;
for (int i = 1; i <= k; i++) n = n * r[i];
for (int i = 1; i <= k; i++) {
LL m = n / r[i], b, y;
exgcd(m, r[i], b, y);  // b * m mod r[i] = 1
ans = (ans + a[i] * m * b % n) % n;
}
return (ans % n + n) % n;
}
```

## Garner 算法

CRT 的另一个用途是用一组比较小的质数表示一个大的整数。

例如，若 $a$ 满足如下线性方程组，且 $a < \prod_{i=1}^k p_i$（其中 $p_i$ 为质数）：

$$
\begin{cases}
a &\equiv a_1 \pmod {p_1} \\
a &\equiv a_2 \pmod {p_2} \\
&\vdots \\
a &\equiv a_k \pmod {p_k} \\
\end{cases}
$$

我们可以用以下形式的式子（称作 $a$ 的混合基数表示）表示 $a$：

$$
a = x_1 + x_2 p_1 + x_3 p_1 p_2 + \ldots + x_k p_1 \ldots p_{k-1}
$$

**Garner 算法** 将用来计算系数 $x_1, \ldots, x_k$。

令 $r_{ij}$ 为 $p_i$ 在模 $p_j$ 意义下的 [逆](逆元.md)：

$$
p_i \cdot r_{i,j} \equiv 1 \pmod{p_j}
$$

把 $a$ 代入我们得到的第一个方程：

$$
a_1 \equiv x_1 \pmod{p_1}
$$

代入第二个方程得出：

$$
a_2 \equiv x_1 + x_2 p_1 \pmod{p_2}
$$

方程两边减 $x_1$，除 $p_1$ 后得

$$
\begin{aligned}
a_2 - x_1           &\equiv x_2 p_1             &\pmod{p_2} \\
(a_2 - x_1) r_{1,2} &\equiv x_2                 &\pmod{p_2} \\
x_2                 &\equiv (a_2 - x_1) r_{1,2} &\pmod{p_2}
\end{aligned}
$$

类似地，我们可以得到：

$$
x_k=(\dots((a_k-x_1)r_{1,k}-x_2)r_{2,k})-\dots)r_{k-1,k} \bmod p_k
$$

"实现"
```cpp
for (int i = 0; i < k; ++i) {
  x[i] = a[i];
  for (int j = 0; j < i; ++j) {
	x[i] = r[j][i] * (x[i] - x[j]);
	x[i] = x[i] % p[i];
	if (x[i] < 0) x[i] += p[i];
  }
}
```

该算法的时间复杂度为 $O(k^2)$。实际上 Garner 算法并不要求模数为质数，只要求模数两两互质，我们有如下伪代码：

$$
\begin{array}{ll}
&\textbf{Chinese Remainder Algorithm }\operatorname{cra}(\mathbf{v}, \mathbf{m})\text{:} \\
&\textbf{Input}\text{: }\mathbf{m}=(m_0,m_1,\dots ,m_{n-1})\text{, }m_i\in\mathbb{Z}^+\land\gcd(m_i,m_j)=1\text{ for all } i\neq j\text{,} \\
&\qquad \mathbf{v}=(v_0,\dots ,v_{n-1}) \text{ where }v_i=x\bmod m_i\text{.} \\
&\textbf{Output}\text{: }x\bmod{\prod_{i=0}^{n-1} m_i}\text{.} \\
1&\qquad \textbf{for }i\text{ from }1\text{ to }(n-1)\textbf{ do} \\
2&\qquad \qquad C_i\gets \left(\prod_{j=0}^{i-1}m_j\right)^{-1}\bmod{m_i} \\
3&\qquad x\gets v_0 \\
4&\qquad \textbf{for }i\text{ from }1\text{ to }(n-1)\textbf{ do} \\
5&\qquad \qquad u\gets (v_i-x)\cdot C_i\bmod{m_i} \\
6&\qquad \qquad x\gets x+u\prod_{j=0}^{i-1}m_j \\
7&\qquad \textbf{return }(x)
\end{array}
$$

可以发现在第六行中的计算过程对应上述混合基数的表示。

## 应用

某些计数问题或数论问题出于加长代码、增加难度、或者是一些其他原因，给出的模数：**不是质数**！

但是对其质因数分解会发现它没有平方因子，也就是该模数是由一些不重复的质数相乘得到。

那么我们可以分别对这些模数进行计算，最后用 CRT 合并答案。

下面这道题就是一个不错的例子。

"[洛谷 P2480 \[SDOI2010\] 古代猪文](https://www.luogu.com.cn/problem/P2480)"
给出 $G,n$（$1 \leq G,n \leq 10^9$），求：

$$
G^{\sum_{k\mid n}\binom{n}{k}} \bmod 999~911~659
$$

首先，当 $G=999~911~659$ 时，所求显然为 $0$。

否则，根据 [欧拉定理](降幂的基本原理：费马小定理及其推广.md)，可知所求为：

$$
G^{\sum_{k\mid n}\binom{n}{k} \bmod 999~911~658} \bmod 999~911~659
$$

现在考虑如何计算：

$$
\sum_{k\mid n}\binom{n}{k} \bmod 999~911~658
$$

因为 $999~911~658$ 不是质数，无法保证 $\forall x \in [1,999~911~657]$，$x$ 都有逆元存在，上面这个式子我们无法直接计算。

注意到 $999~911~658=2 \times 3 \times 4679 \times 35617$，其中每个质因子的最高次数均为一，我们可以考虑分别求出 $\sum_{k\mid n}\binom{n}{k}$ 在模 $2$，$3$，$4679$，$35617$ 这几个质数下的结果，最后用中国剩余定理来合并答案。

也就是说，我们实际上要求下面一个线性方程组的解：

$$
\begin{cases}
x \equiv a_1 \pmod 2\\
x \equiv a_2 \pmod 3\\
x \equiv a_3 \pmod {4679}\\
x \equiv a_4 \pmod {35617}
\end{cases}
$$

而计算一个组合数对较小的质数取模后的结果，可以利用 [卢卡斯定理](模意义下组合数的速算——Lucas定理.md)。

## 扩展：模数不互质的情况

### 两个方程

设两个方程分别是 $x\equiv a_1 \pmod {m_1}$、$x\equiv a_2 \pmod {m_2}$；

将它们转化为不定方程：$x=m_1p+a_1=m_2q+a_2$，其中 $p, q$ 是整数，则有 $m_1p-m_2q=a_2-a_1$。

由 [裴蜀定理](./bezouts.md)，当 $a_2-a_1$ 不能被 $\gcd(m_1,m_2)$ 整除时，无解；

其他情况下，可以通过 [扩展欧几里得算法](GCD&EXGCD.md) 解出来一组可行解 $(p, q)$；

则原来的两方程组成的模方程组的解为 $x\equiv b\pmod M$，其中 $b=m_1p+a_1$，$M=\text{lcm}(m_1, m_2)$。

### 多个方程

用上面的方法两两合并即可。

