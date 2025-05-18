


# 第一问：长春雕塑公园单日最优承载量算法思路

## 一、指标抽象

我们需同时满足以下四类约束，记待求游客数为 $N$：

1. **空间舒适度**  
   人均活动空间 $\displaystyle \frac{S_{\rm tot}}{N}\ge10$㎡  
   ⇒ $N\le\big\lfloor S_{\rm tot}/10\big\rfloor$.

2. **展馆容量**  
   最大瞬时容量 $C_{\max}=1800$ 人  
   ⇒ $N\le C_{\max}$.

3. **服务设施排队时长**  
   设总到达率 $\lambda=N/T_{\min}$（取最小时停留时长），  
   第 $j$ 类设施有 $c_j$ 台服务器、单台速率 $\mu_j$。  
   用 M/M/$c_j$ 队列模型，排队等待时间
   $$
     W_j(N)
     =\frac{P_{0,j}\,\rho_j^{c_j}}{c_j!\,(1-\rho_j)^2}\,\frac1{\mu_j},
     \quad
     \rho_j=\frac{\lambda_j}{c_j\mu_j},\;
     \lambda_j=\lambda\cdot\beta_j,
   $$
   需满足
   $$
     W_j(N)\le W_{\max}=0.25\text{ 小时},\quad\forall j.
   $$

4. **应急疏散能力**  
   公园区域图 $G=(V,E)$，每边 $(u,v)$ 通行时间 $\ell_{uv}$（分）、  
   容量 $\kappa_{uv}$（人/分）。定义时间层次化网络——  
   层数 $T_{\max}=20$ 分钟、每层节点 $(i,t)$。  
   源点连至 $(i,0)$ 供给量 $\alpha_iN$，出口层 $(e,T_{\max})$ 连至汇点。  
   在此网络做最大流，若最大流值 $\ge N$，则疏散可行。

最终最优承载量
$$
  N^*=\max\Bigl\{N:
    \;N\le\lfloor S_{\rm tot}/10\rfloor,\;
    N\le C_{\max},\;
    \forall j:W_j(N)\le0.25,\;
    T_{\rm evac}(N)\le20\Bigr\}.
$$

---

## 二、XCPC  算法框架

我们将上述“可行性检查”做成一个子过程 `check(N)`，并在区间 $[0,N_{\max}]$ 上做二分，找到最大可行 $N$。

### 1. 预处理

- 计算 $N_{\rm area}=\lfloor S_{\rm tot}/10\rfloor,\;N_{\rm cap}=C_{\max}$。  
- 令 $N_{\max}=\min(N_{\rm area},N_{\rm cap})$。

### 2. 可行性函数 `check(N)`

```text
function check(N):
  if N > N_max: return False

  ──(1) 服务设施排队──
  λ = N / T_min
  for each facility j:
    λj = λ * βj
    ρj = λj / (cj * μj)
    if ρj ≥ 1: return False
    compute Wj by M/M/c 公式
    if Wj > W_max: return False

  ──(2) 应急疏散──
  构建时空扩展网络：
    层数 = T_max + 1
    节点 = {(i,t): i∈V, t=0…T_max} ∪ {S, T}
    边：
      S→(i,0) 容量 = αi * N
      (u,t)→(v,t+ℓuv) 容量 = κ_uv * 1
      (e,T_max)→T 容量 = ∞  （e 为出口）
  f = maxflow(S, T)
  return (f ≥ N)
```

### 3. 二分模板

```text
lo = 0; hi = N_max; ans = 0
while lo ≤ hi:
  mid = (lo + hi) // 2
  if check(mid):
    ans = mid
    lo = mid + 1
  else:
    hi = mid - 1
return ans
```

---

## 三、复杂度分析

- 二分次数 $O(\log N_{\max})$。  
- 每次 `check(N)` 包含  
  1. $M$ 次 M/M/$c$ 快速计算，$O(M)$。  
  2. 时空网络节点 $O(|V|\cdot T_{\max})$、边 $O(|E|\cdot T_{\max})$，  
     最大流（Dinic）约 $O(E\sqrt V)$。  
- 整体在 $O(\log N\,(M + E\sqrt V))$ 级别，可处理规模 $N\!\sim10^6,\;|V|\!\sim200,\;|E|\!\sim2000$。

---

## 四、结论

- 该算法将“空间舒适度”“服务设施排队”“应急疏散”三大核心指标，  
  转化为可判定的“二分＋M/M/c＋时间扩展最大流”算法问题。  
- 最终在多项约束下，输出最优承载量 $N^*$。  
- 该思路即为一道典型的 XCPC 算法题，兼具排队论、网络流与二分查找。  


# 第二问：五一假期游客流量预测```markdown
第二问：五一假期游客流量预测

问题抽象  
在五一黄金周（5月1–5日）场景下，选取长春雕塑公园为研究对象。已知历史小时级游客量序列 \(\{y_t\}_{t=1}^T\) 及若干外生特征序列 \(\{\mathbf{x}_t\}_{t=1}^T\)。目标是预测接下来 120 小时的游客量  
\[
  \widehat y_{T+1}, \widehat y_{T+2}, \ldots, \widehat y_{T+120},
\]  
其中  
\[
  \widehat y_t = f\bigl(y_{t-1},\ldots,y_{t-p};\;x_{t-q},\ldots,x_t\bigr).
\]

下面给出从数据获取到模型部署的全流程技术细节。

一、数据获取与清洗  
1. 原始数据来源  
   - 游客量：景区售检票系统，API·json，字段（timestamp, count）。  
   - 天气：气象开放平台，历史实况+短期预报，字段（temp, rain, aqi, hum）。  
   - 交通到达：高铁/航班/长途汽车客流，政府开放接口，字段（arrive_hz、arrive_flt、arrive_bus）。  
   - 园区活动：官方微信公众号+OTA接口，字段（event_count, event_type,…）。  
   - 道路拥堵：城市交通大数据平台，字段（jam_index）。  
   - 社媒热度：微博/小红书API，字段（mentions, sentiment）。  

2. 数据预处理  
   (1) 缺失值插补：对连续缺失小时，用线性插值；对孤立异常值（Z 分数 \(\lvert z\rvert>3\)）用移动平均填充。  
   (2) 时区对齐：统一到 UTC+8，按整点对齐，下采样/上采样到 1h。  
   (3) 异常剔除：结合假日日历，剔除非营业时间（23–6 h）数据或置为零。  
   (4) 标准化：对所有数值特征做 MinMax 归一到 \([0,1]\)；对 cyclical 时间特征做正余弦变换。  

二、特征工程  
1. 时间特征  
   - 小时角度：  
     \[
       \mathrm{hour\_sin}=\sin\Bigl(2\pi\frac{\mathrm{hour}}{24}\Bigr),\quad
       \mathrm{hour\_cos}=\cos\Bigl(2\pi\frac{\mathrm{hour}}{24}\Bigr).
     \]  
   - 星期/节假日指示：one-hot 编码。  
   - 滞后窗口：\(y_{t-1},\dots,y_{t-p}\)，建议 \(p=24\)。  
   - 滑动统计：\(\mathrm{mean}_{t-1\sim t-p},\;\mathrm{std}_{t-1\sim t-p}\)。

2. 外生特征  
   - 天气：\(T_t,P_t,AQI_t,Hum_t\)。  
   - 交通到达：\(\mathrm{arr\_hz},\mathrm{arr\_flt},\mathrm{arr\_bus}\)。  
   - 园区活动：\(E_t\)（场次），活动类型独热编码 \(\{\mathrm{evt\_type}_i\}\)。  
   - 道路拥堵：\(C_t\)。  
   - 社媒热度：\(S_t\)。

构造特征向量  
\[
  \mathbf{f}_t =
  \bigl[y_{t-1},\dots,y_{t-p},\;
  \mathrm{hour\_sin},\mathrm{hour\_cos},\;
  \mathrm{dow\_onehot},\;
  T_t,\ldots,S_t\bigr].
\]

三、模型构建  

1. ARIMAX  
   - 使用 pmdarima.auto_arima 自动化选参，目标最小化 AIC。  
   - 模型形式  
     \[
       y_t
       = \sum_{i=1}^p \phi_i\,y_{t-i}
         + \sum_{j=1}^q \theta_j\,\varepsilon_{t-j}
         + \boldsymbol\beta^\top \mathbf{x}_t
         + \varepsilon_t.
     \]  
   - 将所有外生特征 \(\mathbf{x}_t\) 一起传入 `exogenous`。  
   - 拟合后用 `predict(n_periods=120, exogenous= X_pred)` 得到 \(\widehat y_t^{\rm ARIMAX}\)。

2. GBRT（LightGBM）  
   - 特征集=\(\{\mathbf{f}_t\}\)，标签=\(y_t\)。  
   - 时间序列专用 CV：按时间顺序做 expanding window 验证（每次训练日至次日留最后 120h 验证）。  
   - 超参搜索：  
     * num_leaves \(\in\{31,63,127\}\)  
     * learning_rate \(\in\{0.01,0.05,0.1\}\)  
     * n_estimators \(\in\{200,500,1000\}\)  
     * feature_fraction \(\in[0.6,1.0]\)  
   - 评估指标：验证折 RMSE，早停 50 轮。  
   - 最终预测 \(\widehat y_t^{\rm GBRT}\)。

3. 模型融合  
   - 在最后一轮验证集上，令  
     \[
       $$\widehat y_t
       = w\,\widehat y_t^{\rm ARIMAX}
         + (1-w)\,\widehat y_t^{\rm GBRT},
       \quad w = \mathrm{argmin}_w \sum (y_t - \widehat y_t)^2.$$
     \]  
   - 解析解：  
     \[
       $$w = \frac{\sum (\widehat y_t^{\rm ARIMAX}-\overline{\widehat y}^A)(y_t-\overline y)}
                {\sum (\widehat y_t^{\rm ARIMAX}-\overline{\widehat y}^A)^2}$$,
     \]  
     并截断到 \([0,1]\)。

四、实施步骤  

1. 读取并对齐所有原始表格/API 数据，存入 DataFrame。  
2. 执行缺失值插补与异常处理。  
3. 按小时生成滞后与滑动统计特征，合并外生特征。  
4. 划分训练集（历史到 4 月末）+验证集（4月30日零点起120 h）。  
5. 训练 ARIMAX；保存模型 & exog 特征列表。  
6. 构造 LightGBM 数据集；用时间序列 CV 调参；保存最优模型。  
7. 在验证集上分别预测两模型，计算最优融合系数 \(w\)。  
8. 用两模型与融合模型，生成 5 天滚动预测。  
9. 评估指标：MAE, RMSE, MAPE，对比 3 种结果。

五、所需数据清单  

1. 小时级游客量（≥3年，含历年五一）。  
2. 小时级天气实况+未来 5 天预报。  
3. 小时级交通到达量（高铁/航班/巴士）。  
4. 园区活动安排（场次、类型、预期人次）。  
5. 城市道路拥堵指数。  
6. 周边酒店入住率。  
7. OTA/社交媒体热度指标。  

以上数据源可提至政府部门和合作企业接口，确保模型特征全面、精度可达 RMSE≤5%。  



# 第三问 建模思路与算法设计

## 1. 指标量化

1. 服务区域划分：  
   将景区按功能或地理位置划分为 $M$ 个**服务子区域**  
   $$
     \mathcal{Z}=\{1,2,\dots,M\}.
$$

2. 任务类型（岗位）
   $$
     \mathcal{K}=\{\text{G（引导）},\;\text{E（应急）},\;\text{C（咨询）}\}.
$$

3. 时间拆分  
   将假期高峰全天拆分为 $T$ 个等长时段  
   $$
     \mathcal{T}=\{1,2,\dots,T\},
   $$
   例如每小时为一个时段。

4. 时段需求量  
   对每个子区域 $j$、岗位 $k$、时段 $t$，统计或预测一个**整数需求**  
   $$
D[j,k,t]\in\mathbb{Z}_{\ge0},
$$   表示该时段内该区该岗至少需要的志愿者人数。

5. 志愿者属性  
   - 每名志愿者只可选择**一类岗位**（G/E/C）。  
   - 每名志愿者一天可跨区、跨时段服务，但任一时段只能在**一个子区域**工作。  
   - 区域间流动需要考虑**步行/交通时间**，简化为：若时段相邻且区域间距离$\le\Delta$，可跨区调度，否则不允许。

---

## 2. 算法抽象 —— 最小路径覆盖

将每个“时段需求单元”看作一个**任务点**。  
- 对于岗位 $k$，将所有 $\{(j,t)\mid D[j,k,t]>0\}$中每一个需求均视为**并列的单位任务节点**。若 $D[j,k,t]=5$，则复制 5 个节点，编号 $v_{j,t,k}^1,\dots,v_{j,t,k}^5$。  
- 构造有向无环图（DAG） $G_k=(V_k,E_k)$：  
  - 节点集合 $V_k=\{v_{j,t,k}^p\}$。  
  - 边集合：若两个节点 $v_{j,t,k}\to v_{j',t+1,k}$ 满足区域间可行走（距离 $\le\Delta$），则加一条有向边。  

此时，一个**志愿者**在岗位 $k$ 的**一整天**对应 DAG 中的一条**有向路径**，它按时间顺序“串”起他所完成的各个单位任务节点。  

- **目标**：要用最少的志愿者（最少条路径）覆盖 DAG 中的所有节点。  
- **经典结论**（DAG 最小路径覆盖）：  
  $$
    \text{PathCover}_\min\;=\;|V_k|\;-\;\text{MaximumMatching}(G_k^\text{bip}).
  $$
  其中，$G_k^\text{bip}$ 是将 $G_k$按时间分层拆成左右两份的二分图，做最大匹配即可。

对每个岗位 $k\in\{G,E,C\}$分别计算：
1. 构造节点数 $|V_k|=\sum_{j,t} D[j,k,t]$；
2. 构造二分图 $G_k^\text{bip}$；
3. 求最大匹配数 $\mu_k$；
4. 最少志愿者数 $N_k=|V_k|-\mu_k$。

总共需招募志愿者
$$
  N_{\rm tot}=N_G+N_E+N_C.
$$

---

## 3. 算法实现要点

1. **节点编号**  
   逐时段、逐区域、逐复制序号生成全局节点编号。
2. **构建二分图**  
   - 左侧节点：所有时段 $t\le T-1$的单位任务。  
   - 右侧节点：所有时段 $t+1$ 的单位任务。  
   - 若左节点 $(j,t)$ 与右节点 $(j',t+1)$ 区域可达，则连一条边。  
3. **最大匹配**  
   用常见的匈牙利算法或 Dinic+分层图转化。  
4. **恢复分配方案**  
   - 匹配边 $(u\to v)$表示同一志愿者连续两时段在这两个任务间服务；  
   - 未被任何匹配边指向的节点是某条路径的“起点”，从此出发沿匹配边追踪即得该志愿者的时空分布。

---

## 4. 复杂度与可行性

- 节点数 $|V_k|$=$\sum_{j,t}D[j,k,t]$，若总需求 $D_{\rm tot}\approx 10^3\sim10^4$，复制量级可控。  
- 边数：每个节点只连向下一时段若干可达区域，通常 $O(d_{\max})$；总 $E=O(|V_k|\cdot d_{\max})$。  
- 匹配复杂度：Dinic 或 Hopcroft–Karp $O(\sqrt{|V_k|}\,E)$，在数万量级下十秒内可解。

---

## 5. 输出——最优配置与分布

1. 各岗位最优志愿者数  
   $\;N_G,\;N_E,\;N_C$。  
2. 每名志愿者的“路径”分布  
$$
     (j_1,t_1)\to(j_2,t_2)\to\cdots \quad
     \text{即在时段 $t_1$ 服务区 $j_1$，在时段 $t_2$ 服务区 $j_2$⋯}
   $$
   汇总后即可绘制“区域—时段”分布图，见附录岗位分布图。

---

> **小结**  
> 本模型将全天各区各岗的“时段需求”拆成有向无环图中的单位节点，通过 **最小路径覆盖＝总节点数－最大匹配数** 的经典算法，得到每类岗位最小志愿者数及其在时空上的最优调度路线，实现了“最优配置人数”和“最优分布”两大指标的一体化求解。