# 模意义下组合数的速算——Lucas定理
前置知识：[阶乘取模](模意义下的阶乘计算.md)


组合数，又称二项式系数，指表达式：

$$
\binom{n}{k} = \dfrac{n!}{k!(n-k)!}.
$$


基于 Lucas 定理及其推广，存在一种可以在模数不太大 ($m \sim 10^6$) 时求解组合数的方法。更准确地说，只要模数的唯一分解 $m=\prod p_i^{e_i}$ 中所有素数幂的和（即 $\sum p_i^{e_i}$）在 $10^6$ 规模时就可以使用该方法，因为算法的预处理大致相当于这一规模。

## Lucas 定理

首先讨论模数为素数 $p$ 的情形。此时，有 Lucas 定理：
对于素数 $p$，有

$$
\binom{n}{k}\equiv \binom{\lfloor n/p\rfloor}{\lfloor k/p\rfloor}\binom{n\bmod p}{k\bmod p}\pmod p.
$$

其中，当 $n<k$ 时，二项式系数 $\dbinom{n}{k}$ 规定为 $0$。

在求解素数模下组合数时，利用 Lucas 定理和利用 exLucas 算法得到的结果是等价的。

Lucas 定理指出，模数为素数 $p$ 时，大组合数的计算可以转化为规模更小的组合数的计算。在右式中，第一个组合数可以继续递归，直到 $n,k<p$ 为止；第二个组合数则可以直接计算，或者提前预处理出来。写成代码的形式就是：

代码
```cpp
long long Lucas(long long n, long long k long long p) {
  if (k == 0) return 1;
  return (C(n % p, k % p, p) * Lucas(n / p, k / p, p)) % p;
}
```

其中，`C(n, k, p)` 用于计算小规模的组合数。

递归至多进行 $O(\log_p n)$ 次，因而算法的复杂度为 $O(f(p)+g(p)\log_p n)$，其中，$f(p)$ 为预处理组合数的复杂度，$g(p)$ 为单次计算组合数的复杂度。

### 参考实现

此处给出的参考实现在 $O(p)$ 时间内预处理 $p$ 以内的阶乘及其逆元后，可以在 $O(1)$ 时间内计算单个组合数：

```cpp
#include <iostream>
#include <vector>

class BinomModPrime {
  int p;
  std::vector<int> fa, ifa;

  // Calculate binom(n, k) mod p for n, k < p.
  int calc(int n, int k) {
    if (n < k) return 0;
    long long res = fa[n];
    res = (res * ifa[k]) % p;
    res = (res * ifa[n - k]) % p;
    return res;
  }

 public:
  BinomModPrime(int p) : p(p), fa(p), ifa(p) {
    // Factorials mod p till p.
    fa[0] = 1;
    for (int i = 1; i < p; ++i) {
      fa[i] = (long long)fa[i - 1] * i % p;
    }
    // Inverse of factorials mod p till p.
    ifa[p - 1] = p - 1;  // Wilson's theorem.
    for (int i = p - 1; i; --i) {
      ifa[i - 1] = (long long)ifa[i] * i % p;
    }
  }

  // Calculate binom(n, k) mod p.
  int binomial(long long n, long long k) {
    long long res = 1;
    while (n || k) {
      res = (res * calc(n % p, k % p)) % p;
      n /= p;
      k /= p;
    }
    return res;
  }
};

int main() {
  int t, p;
  std::cin >> t >> p;
  BinomModPrime bm(p);
  for (; t; --t) {
    long long n, k;
    std::cin >> n >> k;
    std::cout << bm.binomial(n, k) << '\n';
  }
  return 0;
}
```

该实现的时间复杂度为 $O(p+T\log_p n)$，其中，$T$ 为询问次数。

## exLucas 算法(用于模数非质数)

Lucas 定理中对于模数 $p$ 要求必须为素数，那么对于 $p$ 不是素数的情况，就需要用到 exLucas 算法。虽然名字如此，该算法实际操作时并没有用到 Lucas 定理。

### 素数幂模的情形

首先考虑模数为素数幂 $p^\alpha$ 的情形。将阶乘 $n!$ 中的 $p$ 的幂次和其他幂次分开，可以得到分解：

$$
n! = p^{\nu_p(n!)}(n!)_p.
$$

其中，$\nu_p(n!)$ 为 $n!$ 的素因数分解中 $p$ 的幂次，而 $(n!)_p$ 显然与 $p$ 互素。因此，组合数可以写作：

$$
\binom{n}{k} = p^{\nu_p(n!)-\nu_p(k!)-\nu_p((n-k)!)}\dfrac{(n!)_p}{(k!)_p((n-k)!)_p}.
$$

式子中的 $\nu_p(n!)$ 等可以通过 [Legendre 公式](模意义下的阶乘计算.md#legendre-公式) 计算，$(n!)_p$ 等则可以通过 [递推关系](模意义下的阶乘计算.md#素数幂模的情形) 计算。因为后者与 $p^\alpha$ 互素，所以分母上的乘积的逆元可以通过 [扩展欧几里得算法](逆元.md#扩展欧几里得法) 计算。问题就得以解决。

注意，如果幂次 $\nu_p(n!)-\nu_p(k!)-\nu_p((n-k)!)\ge\alpha$，余数一定为零，不必再做更多计算。

### 一般模数的情形

对于 $m$ 是一般的合数的情形，只需要首先对它做 [素因数分解](快速分解质因数——Rho算法.md)：

$$
m = p_1^{\alpha_1}p_2^{\alpha_2}\cdots p_s^{\alpha_s}.
$$

然后，分别计算出模 $p_i^{\alpha_i}$ 下组合数 $\dbinom{n}{k}$ 的余数，就得到 $s$ 个同余方程：

$$
\begin{cases}
\dbinom{n}{k} \equiv r_1, &\pmod{p_1^{\alpha_1}}, \\
\dbinom{n}{k} \equiv r_2, &\pmod{p_2^{\alpha_2}}, \\
\quad\quad\cdots\\
\dbinom{n}{k} \equiv r_s, &\pmod{p_s^{\alpha_s}}.
\end{cases}
$$

最后，利用 [中国剩余定理](中国剩余定理%20CRT.md) 求出模 $m$ 的余数。

### 参考实现

最后，给出模板题目 [二项式系数](https://loj.ac/p/181) 的参考实现。

"参考实现"
```cpp
#include <iostream>
#include <vector>

// Extended Euclid.
void ex_gcd(int a, int b, int& x, int& y) {
  if (!b) {
    x = 1;
    y = 0;
  } else {
    ex_gcd(b, a % b, y, x);
    y -= a / b * x;
  }
}

// Inverse of a mod m.
int inverse(int a, int m) {
  int x, y;
  ex_gcd(a, m, x, y);
  return (x % m + m) % m;
}

// Coefficient in CRT.
int crt_coeff(int m_i, int m) {
  long long mm = m / m_i;
  mm *= inverse(mm, m_i);
  return mm % m;
}

// Binominal Coefficient Calculator Modulo Prime Power.
class BinomModPrimePower {
  int p, a, pa;
  std::vector<int> f;

  // Obtain multiplicity of p in n!.
  long long nu(long long n) {
    long long count = 0;
    do {
      n /= p;
      count += n;
    } while (n);
    return count;
  }

  // Calculate (n!)_p mod pa.
  long long fact_mod(long long n) {
    bool neg = p != 2 || pa <= 4;
    long long res = 1;
    while (n > 1) {
      if ((n / pa) & neg) res = pa - res;
      res = res * f[n % pa] % pa;
      n /= p;
    }
    return res;
  }

 public:
  BinomModPrimePower(int p, int a, int pa) : p(p), a(a), pa(pa), f(pa) {
    // Pretreatment.
    f[0] = 1;
    for (int i = 1; i < pa; ++i) {
      f[i] = i % p ? (long long)f[i - 1] * i % pa : f[i - 1];
    }
  }

  // Calculate Binom(n, k) mod pa.
  int binomial(long long n, long long k) {
    long long v = nu(n) - nu(n - k) - nu(k);
    if (v >= a) return 0;
    auto res = fact_mod(n - k) * fact_mod(k) % pa;
    res = fact_mod(n) * inverse(res, pa) % pa;
    for (; v; --v) res *= p;
    return res % pa;
  }
};

// Binominal Coefficient Calculator.
class BinomMod {
  int m;
  std::vector<BinomModPrimePower> bp;
  std::vector<long long> crt_m;

 public:
  BinomMod(int n) : m(n) {
    // Factorize.
    for (int p = 2; p * p <= n; ++p) {
      if (n % p == 0) {
        int a = 0, pa = 1;
        for (; n % p == 0; n /= p, ++a, pa *= p);
        bp.emplace_back(p, a, pa);
        crt_m.emplace_back(crt_coeff(pa, m));
      }
    }
    if (n > 1) {
      bp.emplace_back(n, 1, n);
      crt_m.emplace_back(crt_coeff(n, m));
    }
  }

  // Calculate Binom(n, k) mod m.
  int binomial(long long n, long long k) {
    long long res = 0;
    for (size_t i = 0; i != bp.size(); ++i) {
      res = (bp[i].binomial(n, k) * crt_m[i] + res) % m;
    }
    return res;
  }
};

int main() {
  int t, m;
  std::cin >> t >> m;
  BinomMod bm(m);
  for (; t; --t) {
    long long n, k;
    std::cin >> n >> k;
    std::cout << bm.binomial(n, k) << '\n';
  }
  return 0;
}
```

该算法在预处理时将模数 $m$ 分解为素数幂，然后对所有 $p^\alpha$ 预处理了自 $1$ 至 $p^\alpha$ 所有非 $p$ 倍数的自然数的乘积，以及它在中国剩余定理合并答案时对应的系数。预处理的时间复杂度为 $O(\sqrt{m}+\sum_ip_i^{\alpha_i})$。每次询问时，复杂度为 $O(\log m+\sum_i\log_{p_i}n)$，复杂度中的两项分别是计算逆元和计算幂次、阶乘余数的复杂度。
