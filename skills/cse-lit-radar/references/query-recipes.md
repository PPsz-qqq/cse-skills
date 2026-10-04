# Query recipes per axis

Query construction is the main quality lever in a literature search, and it is axis-specific. The
same words mean different things in different subcommunities, and the class D venues use Chinese
terms that are not literal translations.

Write the query plan as a table before searching. Each row is one (axis, source, language) attempt
with an expected yield. After the run, fill in the actual yield and the marginal yield.

## Plan template

```text
| # | Axis | Source | Language | Boolean string | Field filters | Date window | Expected yield | Actual yield | New relevant |
|---|------|--------|----------|----------------|---------------|-------------|----------------|--------------|--------------|
```

## Naming traps to design around

| Term | Trap | Fix in the query |
|---|---|---|
| tracking | means multi-object tracking in vision, target tracking in estimation, and trajectory following in control | add the qualifier and a discipline term, for example `"multi-object tracking" AND (MOT OR HOTA)` for vision, `"target tracking" AND (Kalman OR particle filter)` for `filt` |
| detection | means object detection in vision and change or anomaly detection in remote sensing | pair with the task object and the sensor, for example `detection AND (aerial OR "remote sensing")` |
| localization | means position estimation in robotics and class localization in detection | use the axis term from [../../cse-shared/core/terminology-and-notation.md](../../cse-shared/core/terminology-and-notation.md) |
| fusion | ambiguous between measurement, state, track-to-track and covariance intersection | name the fusion type explicitly |
| robust | a marketing word without a perturbation class | require the noise, corruption or outlier model in the query |
| consistency | estimation consistency in `filt`, but also logical consistency in a dataset paper | pair with `NEES` or `ANEES` for `filt` |
| cooperative | does not imply distributed | add `distributed` or `decentralized` only when you mean it |
| estimation | state estimation in control, but also parameter or depth estimation in vision | pair with the model class or the sensor |

## `det` queries

English seed set.

```text
("object detection") AND (aerial OR UAV OR "remote sensing" OR "oriented bounding box")
("small object detection") AND (aerial OR satellite OR drone)
("oriented object detection") AND (DOTA OR "rotated bounding box")
("open-vocabulary detection" OR "zero-shot detection") AND (transfer OR prompt)
("detection transformer") AND (DETR OR "query-based")
("label assignment" OR "sample assignment") AND detection
("test-time augmentation" OR "multi-scale inference") AND detection AND evaluation
```

Chinese seed set.

```text
目标检测 遥感 图像
小目标检测 无人机
旋转目标检测 有向边界框
无锚框 检测
标签分配 检测
检测 消融实验 对比实验
```

Adjacent terms worth one sweep when the claim concerns deployment: `edge deployment`, `quantization`,
`inference latency`, and the exact compute platform names.

## `track` queries

English seed set.

```text
("multi-object tracking" OR MOT) AND (association OR "data association")
("tracking-by-detection") AND (public detections OR private detections)
("higher order tracking accuracy" OR HOTA) AND evaluation
("occlusion" OR "long-term tracking") AND MOT
("appearance model" OR "motion model") AND ("identity switch" OR IDF1)
("UAV tracking" OR "aerial tracking") AND ("crowded" OR "small object")
```

Chinese seed set.

```text
多目标跟踪 数据关联
检测跟踪 遮挡
目标跟踪 身份切换
航拍 多目标跟踪
```

Always resolve the public versus private detection protocol question inside the query, because the
two literatures are not comparable and mixing them corrupts the nearest-competitor ledger.

## `reid` queries

English seed set.

```text
("person re-identification") AND (MSMT17 OR "Market-1501") AND protocol
("vehicle re-identification") AND (VeRi OR VehicleID)
("unsupervised" OR "domain generalization") AND re-identification
("re-ranking") AND re-identification AND evaluation
("cross-camera" OR "cross-domain") AND re-identification
("metric learning") AND re-identification AND (triplet OR "circle loss")
```

Chinese seed set.

```text
行人重识别 度量学习
车辆重识别
跨域 重识别
重识别 评测协议
```

Protocol words belong in the query. A re-identification result without re-ranking status and query
mode is not comparable, so retrieval that omits those words tends to return the least useful papers.

## `cnav` queries

English seed set.

```text
("cooperative localization" OR "cooperative navigation") AND (UAV OR "multi-robot")
("distributed estimation") AND (consensus OR "covariance intersection")
("GNSS-denied" OR "GPS-denied") AND navigation AND (range OR "relative measurement")
("communication topology" OR "algebraic connectivity") AND estimation
("range-only" OR "bearing-only") AND cooperative AND observability
("multi-agent" OR "swarm") AND (formation OR navigation) AND estimation
```

Chinese seed set.

```text
协同导航 无人机
协同定位 测距
拒止环境 导航
分布式 滤波 编队
多智能体 状态估计
```

Add `simulation` or `field experiment` as a filter when the claim concerns deployment, since the
gap between the two is the single most common complaint about this axis.

## `filt` queries

English seed set.

```text
(Kalman OR "particle filter" OR "information filter") AND ("nonlinear" OR "non-Gaussian")
("consistency") AND (NEES OR ANEES) AND filter
("adaptive" OR "robust") AND ("noise covariance" OR "outlier") AND filtering
("cubature" OR "unscented" OR "sigma-point") AND filtering AND comparison
("Cramer-Rao" OR CRLB) AND (bound OR "performance limit") AND estimation
("distributed Kalman filter") AND (consensus OR "diffusion")
("interacting multiple model" OR IMM) AND tracking
```

Chinese seed set.

```text
卡尔曼滤波 非线性
容积卡尔曼滤波
滤波 一致性 均方根误差
自适应滤波 噪声协方差
粒子滤波 目标跟踪
克拉美-罗下界 估计
```

For `filt`, also search the venue names directly. TAC and Automatica papers often use a title with
no keyword that a general query would catch, such as "On the stability of ...".

## Cross-axis and bridge queries

Run one bridge query per project. These surface the work that a single-axis search systematically
misses and are frequently the source of the real nearest competitor.

```text
(detection AND tracking) AND ("joint" OR "unified") 
(tracking AND re-identification) AND ("appearance" OR "association")
(filtering AND tracking) AND ("motion model" OR "state estimation")
(cooperative AND filtering) AND ("distributed" OR "consensus")
(remote sensing AND tracking) AND (UAV OR satellite)
```

## Query hygiene rules

- Record the exact string you ran, including field filters and date window. A query that cannot be
  re-run is not evidence of coverage.
- Do not tune a query after seeing which of your own papers it returns. If you adjust it, record the
  adjustment and the reason, and re-run the previous expansion so the marginal-yield count stays
  honest.
- Three or fewer keyword variants returning nothing is the documented signal to drop the claim or
  rewrite the sentence, not to keep searching with synonyms until something appears.
- Use one date window per expansion and state it explicitly. An unbounded window silently mixes a
  current-cycle survey with decade-old results.
