似乎定时自动push的功能并未生效
# 彩票问题求解过程详解 (易懂版)

## 1. 问题是啥？

想象你开了家彩票店，有个叫小 A 的顾客天天来买彩票。

*   **选号规则**：他每天从 $1$ 到 $n$ 之间选 $k$ 个数字，可以重复选。他选号的方式是固定的：第 $i$ 天，他选的第 $j$ 个号是 $a_{i,j} = ((i \cdot j + i + j) \pmod n) + 1$。
*   **开奖规则 (有猫腻!)**：每天开奖时，会从 $1$ 到 $n$ 中抽出 $m$ 个数字，也可能重复。但**秘密**是：第 $i$ 天开奖时，数字 $forbidden_i = (i \pmod n) + 1$ 这个号码**永远不会**被抽中！开奖实际上是从剩下的 $n-1$ 个数字里抽的。
*   **中奖金额**：对每个数字 $u$ (从 $1$ 到 $n$)，看它在小 A 选的号里出现了 $c_u$ 次，在开奖号码里出现了 $d_u$ 次。小 A 当天的奖金就是所有数字的 $c_u \times d_u$ 加起来：$$ W_i = \sum_{u=1}^n c_u d_u $$
*   **你的目标**：小 A 的奖金是你付的。你需要定一个最低的**整数**票价 $P$，保证你在这 $T$ 天里，从小 A 身上赚到的钱（期望上）不会亏本。

## 2. 怎么定价才能不亏本？

你的总收入是 $P \times T$ (卖 $T$ 天，每天一张票)。
你付出的总奖金是 $\sum_{i=1}^T W_i$。但因为开奖是随机的，我们只能算**期望**的总奖金，记作 $E[\text{总奖金}]$。

为了不亏本，需要：
$$ \text{总收入} \ge E[\text{总奖金}] $$
$$ P \times T \ge E[\text{总奖金}] $$
$$ P \ge \frac{E[\text{总奖金}]}{T} $$
因为票价 $P$ 必须是整数，所以最小的 $P$ 就是把右边的结果**向上取整**：
$$ P_{\min} = \left\lceil \frac{E[\text{总奖金}]}{T} \right\rceil $$
所以，我们的核心任务就是算出 $E[\text{总奖金}]$。

## 3. 计算期望总奖金

期望有个好性质：**总体的期望等于各个部分期望的和**。
$$ E[\text{总奖金}] = E\left[\sum_{i=1}^T W_i\right] = \sum_{i=1}^T E[W_i] $$
我们先算**每天的期望奖金** $E[W_i]$。

### 3.1. 计算单日期望奖金 $E[W_i]$

回忆一下 $W_i = \sum_{u=1}^n c_{u,i} d_{u,i}$。这里 $c_{u,i}$ 是第 $i$ 天小 A 选号里数字 $u$ 的次数（固定的），$d_{u,i}$ 是第 $i$ 天开奖号码里数字 $u$ 的次数（随机的）。
再次利用期望的性质：
$$ E[W_i] = E\left[\sum_{u=1}^n c_{u,i} d_{u,i}\right] = \sum_{u=1}^n c_{u,i} E[d_{u,i}] $$
现在计算 $E[d_{u,i}]$，也就是数字 $u$ 在第 $i$ 天开奖中**期望出现多少次**。

*   第 $i$ 天的“禁号”是 $forbidden_i = (i \pmod n) + 1$。
*   开奖是从剩下的 $n-1$ 个“好号”里，随机抽 $m$ 次（每次抽完可能还会抽到）。
*   对**任何一次**抽取：
    *   如果 $u$ 是今天的“禁号” $forbidden_i$，抽中它的概率是 $0$。
    *   如果 $u$ 是“好号”，抽中它的概率是 $1 / (n-1)$ （因为有 $n-1$ 个好号，机会均等）。
*   我们总共抽 $m$ 次，所以：
    *   如果 $u = forbidden_i$，那么 $E[d_{u,i}] = m \times 0 = 0$。
    *   如果 $u \neq forbidden_i$，那么 $E[d_{u,i}] = m \times \frac{1}{n-1} = \frac{m}{n-1}$。

把这个结果代回 $E[W_i]$：
$$ E[W_i] = \sum_{u \neq forbidden_i} c_{u,i} \cdot \frac{m}{n-1} + c_{forbidden_i, i} \cdot 0 $$
$$ E[W_i] = \frac{m}{n-1} \sum_{u \neq forbidden_i} c_{u,i} $$
小 A 每天总共选 $k$ 个数字，所以所有 $c_{u,i}$ 加起来是 $k$。
那么，所有“好号”的 $c_{u,i}$ 加起来就是 $k$ 减去“禁号”的 $c_{forbidden_i, i}$：
$$ \sum_{u \neq forbidden_i} c_{u,i} = k - c_{forbidden_i, i} $$
因此，每天的期望奖金是：
$$ E[W_i] = \frac{m}{n-1} (k - c_{forbidden_i, i}) $$

### 3.2. 汇总得到总期望奖金

现在把每天的期望加起来：
$$ E[\text{总奖金}] = \sum_{i=1}^T E[W_i] = \sum_{i=1}^T \frac{m}{n-1} (k - c_{forbidden_i, i}) $$
把常数 $\frac{m}{n-1}$ 提出去：
$$ E[\text{总奖金}] = \frac{m}{n-1} \sum_{i=1}^T (k - c_{forbidden_i, i}) $$
$$ E[\text{总奖金}] = \frac{m}{n-1} \left( \sum_{i=1}^T k - \sum_{i=1}^T c_{forbidden_i, i} \right) $$
$$ E[\text{总奖金}] = \frac{m(kT - S)}{n-1} $$
这里的 $S = \sum_{i=1}^T c_{forbidden_i, i}$。 这个 $S$ 是什么意思呢？它代表了在**所有 $T$ 天里，小 A 选中的号码正好是当天“禁号”的总次数**。这是我们接下来要计算的关键！

## 4. 计算核心和 $S$

我们需要算出 $S = \sum_{i=1}^T c_{forbidden_i, i}$。

### 4.1. 先看一天：怎么算 $c_{forbidden_i, i}$？

$c_{forbidden_i, i}$ 是在第 $i$ 天，小 A 选的 $k$ 个号码中有多少个等于当天的禁号 $forbidden_i$。
小 A 选的号是 $a_{i,j} = ((i \cdot j + i + j) \pmod n) + 1$。
我们要找有多少个 $j$ (从 $1$ 到 $k$) 使得 $a_{i,j} = forbidden_i$。
经过一些数学推导（在另一个文档里有详细过程），这个条件等价于：
$$ ((i \pmod n + 1) \cdot j) \pmod n = 0 $$
令 $r = i \pmod n$，条件变成 $((r+1)j)$ 必须是 $n$ 的倍数。

这什么时候会发生呢？这和 $r+1$ 与 $n$ 的**最大公约数**（Greatest Common Divisor, 简称 GCD）有关。GCD 就是能同时整除两个数的最大正整数。例如 $\gcd(12, 18) = 6$。
设 $g = \gcd(r+1, n)$。那么 $((r+1)j)$ 是 $n$ 的倍数，当且仅当 $j$ 是 $\frac{n}{g}$ 的倍数。

所以，$c_{forbidden_i, i}$ 等于在 $1, 2, \dots, k$ 这些数里面，有多少个是 $\frac{n}{\gcd((i \pmod n) + 1, n)}$ 的倍数。
这个数量就是 $k$ 除以 $\frac{n}{\gcd((i \pmod n) + 1, n)}$ 然后**向下取整**（即去掉小数部分）。
我们把这个值记作 $N(i)$:
$$ N(i) = \left\lfloor \frac{k}{n / \gcd((i \pmod n) + 1, n)} \right\rfloor $$
那么 $S = \sum_{i=1}^T N(i)$。

### 4.2. 利用“重复”规律 (周期性)

你会发现 $N(i)$ 的值只跟 $p = (i \pmod n) + 1$ 有关。
当 $i$ 从 1, 2, 3... 这样增加时，$p$ 的值会是 $2, 3, \dots, n, 1, 2, 3, \dots, n, 1, \dots$ 这样不断重复，每 $n$ 天重复一次。
这意味着 $N(i)$ 的值也是每 $n$ 天重复一次！这个重复的长度 $n$ 叫做**周期**。

我们定义 $Val(p) = \lfloor k / (n / \gcd(p, n)) \rfloor$。
我们可以先算一个完整周期（$n$ 天）的总和：
$$ S_{\text{period}} = \sum_{p=1}^n Val(p) $$
现在看总共 $T$ 天。$T$ 天里有多少个完整的周期呢？是 $Q = \lfloor T/n \rfloor$ 个。
还剩下多少天？是 $R = T \pmod n$ 天。
所以，总和 $S$ 就等于 $Q$ 个完整周期的和，再加上剩下 $R$ 天的和。
剩下的 $R$ 天对应的 $p$ 值是从 $2$ 开始，一直到 $R+1$。
$$ S = Q \cdot S_{\text{period}} + \sum_{p=2}^{R+1} Val(p) $$
我们把后面这部分剩余的和记作 $S_{\text{rem}}$:
$$ S_{\text{rem}} = \sum_{p=2}^{R+1} Val(p) $$
最终：
$$ S = Q \cdot S_{\text{period}} + S_{\text{rem}} $$
现在问题就变成了分别计算 $S_{\text{period}}$ 和 $S_{\text{rem}}$。

## 5. 计算 $S_{\text{period}}$ (周期和)

$$ S_{\text{period}} = \sum_{p=1}^n \left\lfloor \frac{k}{n / \gcd(p, n)} \right\rfloor $$
直接算 $n$ 次可能还是有点慢。我们可以换个角度。
考虑 $g = \gcd(p, n)$。$g$ 肯定是 $n$ 的一个约数（能整除 $n$ 的数）。
我们可以按 $g$ 的不同取值来分组计算。

这里需要一个数学工具：**欧拉函数** $\phi(m)$。它表示从 1 到 $m$ 中，有多少个数和 $m$ 的最大公约数是 1（我们称它们与 $m$ **互质**）。例如 $\phi(6)=2$，因为 1, 2, 3, 4, 5, 6 中，只有 1 和 5 与 6 的 GCD 是 1。
有个结论：在 1 到 $n$ 中，使得 $\gcd(p, n) = g$ 的 $p$ 的个数正好是 $\phi(n/g)$。

利用这个结论，我们可以把 $S_{\text{period}}$ 按 $g$ 来分组：
$$ S_{\text{period}} = \sum_{g|n} \phi(n/g) \cdot \left\lfloor \frac{k}{n/g} \right\rfloor $$
(这里的 $\sum_{g|n}$ 表示对 $n$ 的所有约数 $g$ 求和)。
为了写起来方便，我们令 $d = n/g$。当 $g$ 取遍 $n$ 的所有约数时，$d$ 也正好取遍 $n$ 的所有约数。
所以公式变成：
$$ S_{\text{period}} = \sum_{d|n} \phi(d) \cdot \left\lfloor \frac{k}{d} \right\rfloor $$
这个公式就好算多了：
1.  找到 $n$ 的所有约数 $d$。
2.  对每个约数 $d$，计算它的欧拉函数 $\phi(d)$。
3.  计算 $\phi(d) \times \lfloor k/d \rfloor$。
4.  把所有约数的结果加起来。

## 6. 计算 $S_{\text{rem}}$ (剩余部分的和)

$$ S_{\text{rem}} = \sum_{p=2}^{R+1} Val(p) = \sum_{p=2}^{R+1} \left\lfloor \frac{k}{n / \gcd(p, n)} \right\rfloor $$
如果 $R$ 很小，可以直接算。但如果 $R$ 很大，也需要优化。
方法和算 $S_{\text{period}}$ 类似，也是按 $g = \gcd(p, n)$ 分组：
$$ S_{\text{rem}} = \sum_{g|n} \left\lfloor \frac{k}{n/g} \right\rfloor \times (\text{在 } 2 \text{ 到 } R+1 \text{ 之间，有多少个 } p \text{ 满足 } \gcd(p, n) = g) $$
计算括号里的那个数量比较麻烦。
条件 $\gcd(p, n) = g$ 意味着 $p$ 可以写成 $p = gx$，并且 $\gcd(x, n/g) = 1$（即 $x$ 和 $n/g$ 互质）。
$p$ 的范围是 $2 \le p \le R+1$，所以 $x$ 的范围是 $\lceil 2/g \rceil \le x \le \lfloor (R+1)/g \rfloor$。
令 $L' = \lceil 2/g \rceil$ (向上取整)，$U' = \lfloor (R+1)/g \rfloor$ (向下取整)，$m = n/g$。
我们就是要找在 $L'$ 和 $U'$ 之间（包含两端），有多少个 $x$ 跟 $m$ 互质。

我们定义一个函数 `Count(N, m)`，表示 $1$ 到 $N$ 之间有多少个数和 $m$ 互质。
那么，我们需要的数量就是 `Count(U', m) - Count(L'-1, m)`。（用 $U'$ 以内的互质数，减去 $L'-1$ 以内的互质数）。

计算 `Count(N, m)` 需要另一个数学工具：**莫比乌斯函数** $\mu(d)$ 和**莫比乌斯反演**。
$\mu(d)$ 这个函数的值是这样定的：
*   $\mu(1) = 1$。
*   如果 $d$ 能被某个平方数（比如 4, 9, 25...）整除，那么 $\mu(d) = 0$。
*   如果 $d$ 是 $k$ 个**不同**质数的乘积，那么 $\mu(d) = (-1)^k$ (即 $k$ 是奇数时为 -1，偶数时为 1)。
例如 $\mu(6) = \mu(2 \times 3) = (-1)^2 = 1$；$\mu(30) = \mu(2 \times 3 \times 5) = (-1)^3 = -1$；$\mu(12) = \mu(2^2 \times 3) = 0$。

莫比乌斯反演给出了一个计算 `Count(N, m)` 的公式：
$$ \text{Count}(N, m) = \sum_{d|m, \mu(d) \neq 0} \mu(d) \cdot \left\lfloor \frac{N}{d} \right\rfloor $$
这个公式是说，我们找到 $m$ 的所有**没有平方因子**的约数 $d$ (也就是 $\mu(d)$ 不为 0 的那些)，然后计算 $\mu(d) \times \lfloor N/d \rfloor$，最后把它们加起来。

所以，计算 $S_{\text{rem}}$ 的步骤是：
1.  对 $n$ 的每个约数 $g$：
2.  计算 $m = n/g$, $L' = \lceil 2/g \rceil$, $U' = \lfloor (R+1)/g \rfloor$。
3.  如果 $L' > U'$，说明这个区间是空的，跳过这个 $g$。
4.  用莫比乌斯反演公式计算 `Count_U = Count(U', m)` 和 `Count_L = Count(L'-1, m)`。
5.  得到区间内的互质数数量 `RangeCount = Count_U - Count_L`。
6.  把 $\lfloor k / m \rfloor \times RangeCount$ 加到 $S_{\text{rem}}$ 的总和里。

## 7. 算法总结

好了，现在我们把所有步骤串起来：

1.  **读入** $n, k, m, T$。
2.  **预计算**：
    *   找到 $n$ 的所有质因数。
    *   找到 $n$ 的所有约数。
    *   找到 $n$ 的所有没有平方因子的约数，并计算它们的莫比乌斯函数 $\mu$ 值。
    *   计算 $n$ 的所有约数的欧拉函数 $\phi$ 值。
3.  **计算周期和** $S_{\text{period}}$：
    *   使用公式 $S_{\text{period}} = \sum_{d|n} \phi(d) \cdot \lfloor k/d \rfloor$。
4.  **计算剩余和** $S_{\text{rem}}$：
    *   算出 $Q = \lfloor T/n \rfloor$ 和 $R = T \pmod n$。
    *   如果 $R=0$，则 $S_{\text{rem}} = 0$。
    *   如果 $R>0$，按照第 6 节的方法，使用莫比乌斯反演计算 $S_{\text{rem}}$。
5.  **计算总和 S**：
    *   $S = Q \cdot S_{\text{period}} + S_{\text{rem}}$。
6.  **计算最终票价 P**：
    *   计算期望总奖金的分子：$Numerator = m \times (k \times T - S)$。（注意：如果 $k \times T < S$，结果应该是 0，因为奖金不能是负的。所以是 $m \times \max(0, k \times T - S)$）
    *   计算分母：$Denominator = T \times (n - 1)$。
    *   计算向上取整得到 $P = (Numerator + Denominator - 1) / Denominator$。
7.  **输出** $P$。

**特别注意**：在计算过程中，像 $S$, $S_{\text{period}}$, $S_{\text{rem}}$, $k \times T$, $Numerator$, $Denominator$ 这些中间值可能会非常大，超过普通整数类型（比如 C++ 的 `long long`）能表示的范围。这时候需要使用特殊的大整数类型，比如 C++ 里的 `__int128_t`。