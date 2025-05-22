# 原根primitive-root

阶和原根是定义 [离散对数](离散对数.md) 的关键工具。其在抽象代数中的推广可参见 [群论](../抽象代数/group-theory.md#阶) 和 [环论](../抽象代数/ring-theory.md#应用整数同余类的乘法群) 的相关章节。

## 阶

### 定义
由欧拉定理可知，对 $a\in \mathbf{Z}$，$m\in\mathbf{N}^{*}$，若 $(a,m)=1$，则 $a^{\varphi(m)}\equiv 1\pmod m$.

因此满足同余式 $a^n \equiv 1 \pmod m$ 的最小正整数 $n$ 存在，这个 $n$ 称作 $a$ 模 $m$ 的阶，记作 $\delta_m(a)$ 或 $\operatorname{ord}_m(a)$.
### 性质 1

$a,a^2,\cdots,a^{\delta_m(a)}$ 模 $m$ 两两不同余。
### 性质 2

若 $a^n \equiv 1 \pmod m$，则 $\delta_m(a)\mid n$.
### 性质 3

设 $m\in\mathbf{N}^{*}$，$a,b\in\mathbf{Z}$，$(a,m)=(b,m)=1$，则
$$
\delta_m(ab)=\delta_m(a)\delta_m(b)
$$
的充分必要条件是

$$
\left(\delta_m(a), \delta_m(b)\right)=1
$$
### 性质 4

设 $k \in \mathbf{N}$，$m\in \mathbf{N}^{*}$，$a\in\mathbf{Z}$，$(a,m)=1$，则

$$
\delta_m(a^k)=\dfrac{\delta_m(a)}{\left(\delta_m(a),k\right)}
$$
## 原根

### 定义
设 $m \in \mathbf{N}^{*}$，$g\in \mathbf{Z}$. 若 $(g,m)=1$，且 $\delta_m(g)=\varphi(m)$，则称 $g$ 为模 $m$ 的原根。

即 $g$ 满足 $\delta_m(g) = \left| \mathbf{Z}_m^* \right| = \varphi(m)$.

若一个数 $m$ 有原根 $g$，则 $g,g^2,\ldots,g^{\varphi(m)}$ 构成模 $m$ 的简化剩余系。

特别地，当 $m$ 是质数时，有 $g^i\bmod m$，$0 < i < m$ 的结果两两不同。

在 [抽象代数](../抽象代数/ring-theory.md#应用整数同余类的乘法群) 中，原根就是循环群的生成元。这个概念只在模 $m$ 缩剩余系关于乘法形成的群中有「原根」这个名字，在一般的循环群中都称作「生成元」。

并非每个模 $m$ 缩剩余系关于乘法形成的群都是循环群，存在原根就表明它同构于循环群，如果不存在原根就表明不同构。

### 原根判定定理

设 $m \geqslant 3, (g,m)=1$，则 $g$ 是模 $m$ 的原根的充要条件是，对于 $\varphi(m)$ 的每个素因数 $p$，都有 $g^{\frac{\varphi(m)}{p}}\not\equiv 1\pmod m$.

### 原根个数

若一个数 $m$ 有原根 $g$，那么对于任意 $\varphi(m)$ 的因子 $d$，模 $m$ 的 $d$ 阶元素存在且个数为 $\varphi(d)$。

特别地，$m$ 的原根个数为 $\varphi(\varphi(m))$。

### 原根存在定理

一个数 $m$ 存在原根当且仅当 $m=2,4,p^{\alpha},2p^{\alpha}$，其中 $p$ 为奇素数，$\alpha\in \mathbf{N}^{*}$.

### 最小原根的范围估计

王元证明了素数 $p$ 的最小原根 $g_p=O\left(p^{0.25+\epsilon}\right)$，其中 $\epsilon>0$.

Fridlander证明了素数 $p$ 的最小原根 $g_p=\Omega(\log p)$.

这保证了我们暴力找一个数的最小原根的复杂度是可以接受的。

