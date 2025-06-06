# 欧拉函数与欧拉反演(SigmaGCD)
## 定义

欧拉函数（Euler's totient function），即 $\varphi(n)$，表示的是小于等于 $n$ 和 $n$ 互质的数的个数。

## 性质

-   欧拉函数是 [积性函数](基础.md#积性函数)。

-   $n = \sum_{d \mid n}{\varphi(d)}$。

-   若 $n = p^k$，其中 $p$ 是质数，那么 $\varphi(n) = p^k - p^{k - 1}$。

-   由唯一分解定理，设 $n = \prod_{i=1}^{s}p_i^{k_i}$，其中 $p_i$ 是质数，有 $\varphi(n) = n \times \prod_{i = 1}^s{\dfrac{p_i - 1}{p_i}}$。

-   对任意不全为 $0$ 的整数 $m,n$，$\varphi(mn)\varphi(\gcd(m,n))=\varphi(m)\varphi(n)\gcd(m,n)$。

## 计算

如果只要求一个数的欧拉函数值，那么直接根据定义质因数分解的同时求就好了。这个过程可以用 [Pollard Rho](快速分解质因数——Rho算法.md) 算法优化。

参考实现
```cpp
#include <cmath>
int euler_phi(int n) {
  int ans = n;
  for (int i = 2; i * i <= n; i++)
	if (n % i == 0) {
	  ans = ans / i * (i - 1);
	  while (n % i == 0) n /= i;
	}
  if (n > 1) ans = ans / n * (n - 1);
  return ans;
}
```


如果是多个数的欧拉函数值，可以利用线性筛法来求得。

## 应用

欧拉函数常常用于化简一列最大公约数的和。国内有些文章称它为 **欧拉反演**[^1]。

在结论

$$
n=\sum_{d|n}\varphi(d)
$$

中代入 $n=\gcd(a,b)$，则有

$$
\gcd(a,b) = \sum_{d|\gcd(a,b)}\varphi(d) = \sum_d [d|a][d|b]\varphi(d),
$$

其中，$[\cdot]$ 称为 [Iverson 括号](https://mathworld.wolfram.com/IversonBracket.html)，只有当命题 $P$ 为真时 $[P]$ 取值为 $1$，否则取 $0$。

对上式求和，就可以得到

$$
\sum_{i=1}^n\gcd(i,n)=\sum_{d}\sum_{i=1}^n[d|i][d|n]\varphi(d)=\sum_d\left\lfloor\frac{n}{d}\right\rfloor[d|n]\varphi(d)=\sum_{d|n}\left\lfloor\frac{n}{d}\right\rfloor\varphi(d).
$$

这里关键的观察是 $\sum_{i=1}^n[d|i]=\lfloor\frac{n}{d}\rfloor$，即在 $1$ 和 $n$ 之间能够被 $d$ 整除的 $i$ 的个数是 $\lfloor\frac{n}{d}\rfloor$。

利用这个式子，就可以遍历约数求和了。需要多组查询的时候，可以预处理欧拉函数的前缀和，利用数论分块查询

举个例子：给定 $n\le 100000$，求

$$
\sum_{i=1}^n\sum_{j=1}^n\gcd(i,j).
$$

"思路"
仿照上文的推导，可以得出

$$
\sum_{i=1}^n\sum_{j=1}^n\gcd(i,j) = \sum_{d=1}^n\left\lfloor\frac{n}{d}\right\rfloor^2\varphi(d).
$$

此时需要从 $1$ 遍历到 $n$ 求欧拉函数，用线性筛做就可以 $O(n)$ 得到答案。


