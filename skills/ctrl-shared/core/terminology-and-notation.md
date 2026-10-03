# Terminology and notation conventions

One object, one symbol, one name, throughout a manuscript, its figures, its slides, and its
response letter. Notation drift is the most reliable signal of an unrevised paper, and in
estimation papers it is also a correctness risk.

## Bilingual term mapping

Prefer the English term in English manuscripts, the Chinese term in Chinese manuscripts, and
give both at first use when the audience is mixed. The Chinese terms below are the standard
ones used in 控制科学与工程, not literal translations.

| Concept | Chinese | Notes |
|---|---|---|
| object detection | 目标检测 | class-agnostic localization is 目标定位 |
| tracking-by-detection | 检测跟踪 | the dominant paradigm with an external detector |
| joint detection and tracking | 联合检测跟踪 | one network does both |
| re-identification | 重识别 | 行人重识别 for person, 车辆重识别 for vehicle |
| metric learning | 度量学习 | |
| appearance model | 外观模型 | |
| motion model | 运动模型 | |
| data association | 数据关联 | |
| identity switch | 身份切换 | the ID switch metric |
| cooperative navigation | 协同导航 | also 协同定位 for the localization aspect |
| cooperative localization | 协同定位 | |
| formation control | 编队控制 | distinct from navigation; do not conflate |
| state estimation | 状态估计 | |
| Kalman filter | 卡尔曼滤波 | |
| extended Kalman filter | 扩展卡尔曼滤波 | |
| unscented Kalman filter | 无迹卡尔曼滤波 | |
| particle filter | 粒子滤波 | |
| cubature Kalman filter | 容积卡尔曼滤波 | |
| information filter | 信息滤波 | |
| consistency | 一致性 | NEES and ANEES based; also 滤波一致性 |
| observability | 可观测性 | |
| bounded-input bounded-state | 有界输入有界状态 | |
| globally asymptotically stable | 全局渐近稳定 | |
| communication topology | 通信拓扑 | |
| GNSS-denied | 拒止环境 | 卫星导航拒止环境 |
| line-of-sight | 视距 | non-line-of-sight is 非视距 |
| belief propagation | 置信传播 | |
| factor graph | 因子图 | |
| pose graph | 位姿图 | |
| ablation study | 消融实验 | |
| state of the art | 研究现状 | do not literally write 艺术状态 |
| benchmark | 基准 | |
| ground truth | 真值 | |
| hyperparameter | 超参数 | |
| cross-validation | 交叉验证 | |
| upper bound | 上界 | |
| lower bound | 下界 | |
| Cramer-Rao lower bound | 克拉美-罗下界 | |
| root mean square error | 均方根误差 | |
| cumulative distribution function | 累积分布函数 | |

English usage that is commonly wrong in this field:

- "detection" versus "localization": detection includes classification, localization is
  position only. Do not use them interchangeably.
- "tracking" versus "trajectory prediction": tracking estimates the current state, prediction
  estimates the future. A tracking paper that evaluates prediction horizons must say so.
- "re-identification" versus "retrieval": re-identification is a specific retrieval task with a
  query and a gallery; do not call a general image-retrieval experiment re-identification.
- "cooperative" versus "centralized" versus "decentralized": cooperative means information is
  exchanged among agents; it does not by itself imply a distributed implementation. State the
  computation distribution separately.
- "fusion" is ambiguous. Say which: measurement fusion, state fusion, track-to-track fusion, or
  covariance intersection.
- "robust" without a stated perturbation class is a marketing word. Name the corruption,
  outlier model, or failure mode.

## Symbol conventions

Use one consistent symbol set. The set below is the pack default; if the user's draft already
uses another consistently, keep the user's set and note the deviation rather than rewriting
notation mid-manuscript.

### State estimation and filtering

| Symbol | Meaning |
|---|---|
| `x_k` | state vector at time `k` |
| `z_k` | measurement vector at time `k` |
| `u_k` | control input at time `k` |
| `f(.)` | process model |
| `h(.)` | measurement model |
| `F_k` | process Jacobian |
| `H_k` | measurement Jacobian |
| `Q_k` | process noise covariance |
| `R_k` | measurement noise covariance |
| `P_k` | state error covariance |
| `K_k` | Kalman gain |
| `w_k`, `v_k` | process and measurement noise |
| `N` | number of Monte Carlo runs |
| `epsilon_k` | state estimation error |

Report consistency with NEES `epsilon_k^T P_k^{-1} epsilon_k` against its chi-square bounds with
`n_x` degrees of freedom, and ANEES as the average over runs and time. The degrees of freedom
depend on what is being averaged, and getting this wrong invalidates the whole claim:

- a single time step of a single run has `n_x` degrees of freedom;
- an average over `N` runs at one time step has `N * n_x` degrees of freedom, and the bound is
  that chi-square quantile divided by `N`;
- the ANEES averaged over `N` runs and `T` time steps has `N * T * n_x` degrees of freedom, and
  the bound is that chi-square quantile divided by `N * T`.

The expected value of ANEES is `n_x` in every case. Bounds computed with too few degrees of
freedom cluster near 1 rather than near `n_x`, which makes a consistent filter look inconsistent.
State the run count, the time-step count, `n_x`, the confidence level, and the degrees of freedom
you used. An ANEES claim without those is not evidence.

### Detection

| Symbol | Meaning |
|---|---|
| `NMS` | non-maximum suppression. Define whether it is greedy, soft, or learned |
| `IoU` | intersection over union. State the matching threshold when reporting AP |
| `AP`, `mAP` | average precision. State the averaging convention: VOC-style 11-point, VOC-style all-point, or COCO 101-point interpolated |
| `AP_50`, `AP_75`, `AP_S/M/L` | state the subscripts explicitly; do not write "AP" alone when the threshold matters |
| `FPPI` | false positives per image, the operating rate used for pedestrian detection. `FPPI` is the abscissa, not the headline metric |
| `LAMR` | log-average miss rate, the summary metric for pedestrian detection, obtained by integrating the miss rate over `FPPI` on a log scale. State the `FPPI` range used, commonly 10^-2 to 10^0 |

Never write "mAP" without the dataset and the averaging convention. "mAP 45.2" is not a
measurement, it is an ambiguity.

### Tracking

| Symbol | Meaning |
|---|---|
| `MOTA` | multiple object tracking accuracy; state the detector provenance |
| `IDF1` | identity F1 |
| `HOTA` | higher order tracking accuracy; state `DetA` and `AssA` separately |
| `IDSW` | identity switches |
| `Frag` | fragmentations |
| `MT`, `ML` | mostly tracked, mostly lost; state the percentage thresholds used |
| `MOTP` | multiple object tracking precision |

State online or offline, and public or private detection, next to every tracking number. A
`MOTA` without those two labels is not comparable to anything.

### Re-identification

| Symbol | Meaning |
|---|---|
| `mAP` | mean average precision; state whether re-ranking is applied |
| `Rank-1`, `Rank-5` | cumulative matching characteristics; state single or multi query |
| `mINP` | mean inverse negative penalty, if used |
| `CMC` | cumulative matching characteristic curve |

### Cooperative navigation

| Symbol | Meaning |
|---|---|
| `N` | number of agents |
| `p_i` | position of agent `i` |
| `r_ij` | relative range measurement between `i` and `j` |
| `A` | adjacency matrix of the communication graph |
| `L` | Laplacian |
| `lambda_2` | algebraic connectivity; state the graph and whether it is time-varying |
| `RMSE`, `CEP` | position error metrics; state the 2D or 3D convention |

State for every cooperative result: which agents exchange which quantities, whether any agent
holds global information, and the communication model with its delay and loss assumptions.

## Units, precision, and reporting hygiene

- SI units. State the frame for every quantity that has one (world, body, camera, ENU, NED).
- One precision per quantity type across the manuscript. Keep extra digits in tables only when
  the uncertainty justifies them.
- Always give the uncertainty or dispersion with a mean. "RMSE 0.42 m" without a run count and
  a spread is incomplete.
- Percentages state absolute or relative. A delta of 1.2 mAP on a base of 45.0 is absolute
  1.2 and relative 2.7 percent; write which one you mean.
- Hardware states the exact part: not "an embedded GPU" but the model, the memory, and the
  power mode, because throughput numbers are meaningless without them.
- Time and date formats follow the target venue's style; do not mix.

## Figure and table naming

Use a stable scheme so that text, captions, and responses refer unambiguously:

- figures `Fig. 1`, `Fig. 2`, with sub-panels `Fig. 2(a)`, `Fig. 2(b)`;
- tables `Table 1`, `Table 2`;
- equations numbered `(1)`, `(2)`, referenced as `Eq. (1)`;
- algorithms `Algorithm 1` with a named caption;
- claims `C1`, `C2`; concerns `det-C1`, `filt-C2`; gates `G0` to `G3`.

## Consistency sweep

Before any freeze, check the manuscript against itself:

- every symbol is defined at first use and used identically everywhere;
- every acronym is expanded at first use and used consistently after;
- every figure and table is cited in the text, in numerical order;
- every number in the abstract appears identically in the body;
- every claim carries its validity boundary;
- bilingual terminology does not drift between the Chinese and English abstracts;
- no em dash, en dash, or colon is used as a habitual sentence connector; use a new sentence, a
  comma, a semicolon, parentheses, or a short heading instead. Keep ordinary hyphens in
  compounds and in identifiers such as `det-C1` and `G2`.
