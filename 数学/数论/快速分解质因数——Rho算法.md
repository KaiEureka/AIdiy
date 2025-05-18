想要分解质因数，本质上相当于解决下列问题：

给定一个正整数 $N \in \mathbf{N}_{+}$，试快速找到它的一个 [非平凡因数](基础.md)。

显然朴素算法时间复杂度为 $O(\sqrt N)$，太慢了，故引入Rho算法

这里提供 Brent 判环且加上倍增优化的 Pollard-Rho 算法实现。

```cpp
ll Pollard_Rho(ll x) {
  ll t = 0;
  ll c = rand() % (x - 1) + 1;
  ll s = t;
  int step = 0, goal = 1;
  ll val = 1;
  for (goal = 1;; goal <<= 1, s = t, val = 1) {
	for (step = 1; step <= goal; ++step) {
	  t = f(t, c, x);
	  val = val * abs(t - s) % x;
	  // 如果 val 为 0，退出重新分解
	  if (!val) return x;
	  if (step % 127 == 0) {
		ll d = gcd(val, x);
		if (d > 1) return d;
	  }
	}
	ll d = gcd(val, x);
	if (d > 1) return d;
  }
}
```

#### 复杂度

Pollard-Rho 算法中的期望迭代次数为 $O(\sqrt p)$，这里 $p$ 是 $N$ 的最小素因子。具体实现无论是采用 Floyd 判环还是 Brent 判环，如果不使用倍增优化，期望复杂度都是 $O(\sqrt p\log N)$；在加上倍增优化后，可以近似得到 $O(\sqrt p)$ 的期望复杂度。