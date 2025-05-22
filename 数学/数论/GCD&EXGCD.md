# GCD&EXGCD
## GCD
### 迭代写法
```cpp
int gcd(int a, int b) {
	while (b != 0) {
		int tmp = a;
		a = b;
		b = tmp % b;
	}
	return a;
}
```

对于 C++17，我们可以使用 [`<numeric>`](https://en.cppreference.com/w/cpp/header/numeric) 头中的 [`std::gcd`](https://en.cppreference.com/w/cpp/numeric/gcd) 与 [`std::lcm`](https://en.cppreference.com/w/cpp/numeric/lcm) 来求最大公约数和最小公倍数。

要求多个数的gcd， 由于gcd满足$gcd(a, b, c) = gcd(a, gcd(b, c))$ ,依次求解即可

### O(1)GCD
下面这个做法，可以实现O(值域)的预处理，O(1)的查询。

```cpp
#include <iostream>
using namespace std;

const int Mod = 998244353;

namespace GCD
{
    const int V = 1e6, T = 1e3; // T = sqrt(V)
    int pre[T + 5][T + 5];
    array<int, 3> fac[V + 5];
    bool isnp[V + 5];
    int p[V + 5], tot = 0;
    int TT;
    void init(const int v = V)
    {
        fac[1] = {1, 1, 1};
        for (int i = 2; i <= v; i++)
        {
            if (!isnp[i])
                fac[i] = {i, 1, 1}, p[tot++] = i;
            for (int j = 0; j < tot && i * p[j] <= v; j++)
            {
                int t = i * p[j];
                isnp[t] = true;
                fac[t] = fac[i], *min_element(fac[t].begin(), fac[t].end()) *= p[j];
                if (i % p[j] == 0)
                    break;
            }
        }
        TT = sqrt(v);
        for (int i = 1; i <= TT; i++)
            pre[0][i] = pre[i][0] = i;
        for (int i = 1; i <= TT; i++)
            for (int j = 1; j <= i; j++)
                pre[i][j] = pre[j][i] = pre[j][i % j];
    }
    int g(int x, int y)
    {
        int t = x % y;
        if (t == 0)
            return y;
        return y > TT ? 1 : pre[y][t];
    }
    int gcd(int a, int b)
    {
        if (a == 1 || b == 1)
            return 1;
        int a0 = g(a, fac[b][0]), a1 = g(a /= a0, fac[b][1]), a2 = g(a /= a1, fac[b][2]);
        return a0 * a1 * a2;
    }
}

int main()
{
    GCD::init();
    cin >> a >> b;
    cout << GCD::gcd(a, b) << endl;
    return 0;
}
```

## LCM

 $\gcd(a, b) \times \operatorname{lcm}(a, b) = a \times b$

要求两个数的最小公倍数，先求出最大公约数即可。

要求多个数的lcm， 由于lcm满足$lcm(a, b, c) = lcm(a, lcm(b, c))$ ,依次求解即可

## EXGCD

扩展欧几里得算法（EXGCD)，常用于求 $ax+by=\gcd(a,b)$ 的一组可行解。
### 实现

```cpp
int Exgcd(int a, int b, int &x, int &y) {
	if (!b) {
	x = 1;
	y = 0;
	return a;
	}
	int d = Exgcd(b, a % b, x, y);
	int t = x;
	x = y;
	y = t - (a / b) * y;
	return d;
}
```

函数返回的值为 $\gcd$，在这个过程中计算 $x,y$ 即可。

$ax+by=\gcd(a,b)$ 的解有无数个，那么求解出的 $x,y$ 是哪个呢？可以保证若$b\not= 0$ ，扩展欧几里得算法求出的可行解必有 $|x|\le b,|y|\le a$，处理下正负号即可

### 迭代法编写扩展欧几里得算法

首先，当 $x = 1$，$y = 0$，$x_1 = 0$，$y_1 = 1$ 时，显然有：

$$
\begin{cases}
ax + by     & = a \\
ax_1 + by_1 & = b
\end{cases}
$$

成立。

已知 $a\bmod b = a - (\lfloor \frac{a}{b} \rfloor \times b)$，下面令 $q = \lfloor \frac{a}{b} \rfloor$。参考迭代法求 gcd，每一轮的迭代过程可以表示为：

$$
(a, b) \rightarrow (b, a - qb)
$$

将迭代过程中的 $a$ 替换为 $ax + by = a$，$b$ 替换为 $ax_1 + by_1 = b$，可以得到：

$$
\begin{aligned}
		& \begin{cases}
			  ax + by     & = a \\
			  ax_1 + by_1 & = b
		  \end{cases}                    \\
\rightarrow & \begin{cases}
			  ax_1 + by_1               & = b      \\
			  a(x - qx_1) + b(y - qy_1) & = a - qb
		  \end{cases}
\end{aligned}
$$

据此就可以得到迭代法求 exgcd。

因为迭代的方法避免了递归，所以代码运行速度将比递归代码快一点。

```cpp
int gcd(int a, int b, int& x, int& y) {
	x = 1, y = 0;
	int x1 = 0, y1 = 1, a1 = a, b1 = b;
	while (b1) {
		int q = a1 / b1;
		tie(x, x1) = make_tuple(x1, x - q * x1);
		tie(y, y1) = make_tuple(y1, y - q * y1);
		tie(a1, b1) = make_tuple(b1, a1 - q * b1);
	}
	return a1;
}
```

最后我们知道 $a_1$ 就是要求的 $\gcd$，有 $x \cdot a +y \cdot b = g$。

将这个做法改写成矩阵乘法，则有下面这个等价求法

```cpp
int exgcd(int a, int b, int &x, int &y) {
	int x1 = 1, x2 = 0, x3 = 0, x4 = 1;
	while (b != 0) {
		int c = a / b;
		tie(x1, x2, x3, x4, a, b) =
		make_tuple(x3, x4, x1 - x3 * c, x2 - x4 * c, b, a - b * c);
	}
	x = x1, y = x2;
	return a;
}
```

