# ctrl-skills

面向**控制科学与工程**研究与投稿的 agent 技能包，覆盖五个方向。

[English](README.md) | 中文

| 方向 | 代号 | 范围 |
|---|---|---|
| 目标检测 | `det` | 通用目标检测，含航拍与遥感场景 |
| 目标跟踪 | `track` | 单目标与多目标跟踪 |
| 重识别 | `reid` | 行人重识别、车辆重识别与检索 |
| 协同导航 | `cnav` | 协同导航、协同定位、多机器人及无人机集群 |
| 滤波 | `filt` | 状态估计、多传感器融合、制导与控制 |

目标期刊覆盖四类：视觉与机器学习顶会顶刊（CVPR、ICCV、ECCV、NeurIPS、ICML、ICLR、T-PAMI），控制、机器人与导航类（IEEE TAC、Automatica、T-RO、RA-L、ICRA、IROS、TAES、CDC、ACC），遥感类（TGRS、JSTARS、ISPRS），以及中文期刊（自动化学报、控制理论与应用、控制与决策、航空学报、中国惯性技术学报）。

## 这个包解决什么问题

现有学术技能包大多面向自然科学（生物、医学、化学、材料）。它们的审稿标准、图表规范和证据习惯，无法直接迁移到工程类期刊——后者的贡献是一项机制、一个估计器或一套系统，而决定成败的问题是：**对比是否在同一协议下完成**。

本包正是围绕这个问题构建的。它的组织原则只有一句：**定量比较就是一次测量**。既然是测量，就必须满足测量的全部义务：明确的测量仪器、事先声明的协议、说明试验次数、如实给出不确定度。共享契约中几乎每一条规则都由此推出。

## 按任务使用

先看 [中文快速使用](docs/QUICKSTART.zh-CN.md)。局部编辑、诊断和设计不必重跑整条流水线；
最终科学主张必须检查适用门禁。各入口共用
[执行约定](skills/ctrl-shared/core/execution-contract.md)，规定工具不可用时的降级和新版产物交接。

## 八个技能

全部位于 `skills/` 目录。`ctrl-shared` 是其余七个共同遵守的契约，其余七个构成一条流水线。

| 技能 | 用途 | 触发词示例 |
|---|---|---|
| [ctrl-shared](skills/ctrl-shared/SKILL.md) | 共享契约：关卡、证据规则、期刊矩阵、审稿评分表、裁决枚举、术语规范、产物格式。其他技能按需读取；显式询问共享规范时可直接加载，不作为独立研究流程 | 这个包有什么要求、关卡与台账定义 |
| [ctrl-lit-radar](skills/ctrl-lit-radar/SKILL.md) | 文献检索、会议周期跟踪、基准数据集图谱、最接近竞品台账 | 文献综述, 相关工作, 找论文, 文献调研, literature review |
| [ctrl-idea-forge](skills/ctrl-idea-forge/SKILL.md) | 把研究缺口变成可证伪、有预算的研究构想；产出 G0 范围与 G1 冻结方案 | 选题, 开题, 创新点, research idea, hypothesis |
| [ctrl-experiment-suite](skills/ctrl-experiment-suite/SKILL.md) | 实验设计、审计与结果报告；各方向协议块、统计处理、消融实验、可复现性 | 实验设计, 消融实验, 结果分析, ablation, protocol |
| [ctrl-paper-craft](skills/ctrl-paper-craft/SKILL.md) | 逐节撰写与修改论文正文 | 写论文, 投稿, 论文写作, manuscript, abstract |
| [ctrl-pre-submission-review](skills/ctrl-pre-submission-review/SKILL.md) | 审稿人视角的投稿前自审，多审稿人互盲 | 审稿, 模拟审稿, 预审, 帮我审一下论文, mock review |
| [ctrl-response-craft](skills/ctrl-response-craft/SKILL.md) | 审稿意见回复、rebuttal、修订计划 | 回复审稿意见, rebuttal, response letter |
| [ctrl-paper-to-slides](skills/ctrl-paper-to-slides/SKILL.md) | 由论文生成会议报告、口头报告与答辩幻灯 | 论文做PPT, 学术汇报, conference talk, slides |

## 流水线

```text
ctrl-lit-radar          找到缺口与最接近的竞品
       |
ctrl-idea-forge         G0 范围 -> G1 冻结方案（可证伪、有预算）
       |
ctrl-experiment-suite   执行与审计；G2 证据冻结（声明台账）
       |
ctrl-paper-craft        依据台账撰写正文
       |
ctrl-pre-submission-review  三位互盲审稿人 -> G3 就绪
       |
ctrl-response-craft     修订轮次与逐条回复
       |
ctrl-paper-to-slides    面向听众的报告
```

每个阶段都按**文件**读取上一阶段的产物，而不是依赖对话记忆。产物命名由 [ctrl-shared/core/artifact-contract.md](skills/ctrl-shared/core/artifact-contract.md) 固定。

## 四道关卡

包内其余一切机制都为这四道关卡服务。**关卡由产物通过，不能由声明通过。**

| 关卡 | 回答的问题 | 阻塞范围 |
|---|---|---|
| `G0` 范围 | 主张类型是否匹配可获得的证据？ | 提升该科学主张，不阻塞诊断或局部编辑 |
| `G1` 方案冻结 | 确认性方案是否具体且事先声明？ | 确认性执行，不阻塞探索性设计 |
| `G2` 证据冻结 | 范围内的主张是否有真实来源、比较是否成立？ | 未核验的最终主张，不阻塞诊断或草稿 |
| `G3` 投稿就绪 | 这篇稿子能否扛住自己的审稿人？ | 投稿 |

`G1` 与 `G2` 不可豁免。`G0` 与 `G3` 仅在用户明确指示时可豁免，且必须记录残余风险；豁免单独记录，原裁决不变，不是第七种裁决，也不等于 PASS。定义与通过标准见 [ctrl-shared/core/gate-contract.md](skills/ctrl-shared/core/gate-contract.md)。

## 领域专有之处

通用的学术写作建议，覆盖不到真正决定这些论文成败的东西。

- **协议对齐的对比。** 输入分辨率、测试时增强、预训练数据、检测器来源、re-ranking、query 构造、调参是否对称。每个方向都有一份「会使差值失效的差异清单」，见 [ctrl-shared/core/evidence-integrity.md](skills/ctrl-shared/core/evidence-integrity.md)。
- **各方向专属的证据义务。** 跟踪指标必须标注检测器来源以及 public/private detection；协同导航必须给出分布性证明和含时延、丢包的通信模型；滤波必须给出蒙特卡洛一致性证据，即 NEES 或 ANEES 对卡方界的检验。默认在每个时刻独立评估，自由度为 `N * n_x`；只有在独立性成立或相关性已被标定处理时才允许按 `N * T * n_x` 池化。
- **指标精度。** `mAP` 不写明平均方式就没有意义；`MOTA` 不写检测协议就无法与任何结果比较；`FPPI` 是工作点横轴，`LAMR` 才是汇总指标。相关规范固定在 [ctrl-shared/core/terminology-and-notation.md](skills/ctrl-shared/core/terminology-and-notation.md)。
- **不同期刊层级的审稿行为。** CVPR 类审稿人与 TAC 审稿人拒稿的理由并不相同，见 [ctrl-shared/core/venue-matrix.md](skills/ctrl-shared/core/venue-matrix.md)。
- **中文期刊要求。** 创新点要以条目形式明确列出；中文摘要必须是真正的中文摘要而不是英译；基金项目、中图分类号等字段齐备；参考文献按期刊指定的 GB/T 7714 版本著录（GB/T 7714-2025 已于 2026-07-01 全部代替 2015 版，过渡期以期刊投稿指南为准）。

## 包对自身施加的规则

- **不编造证据。** 缺失的值写成 `[MISSING: ...]`，绝不用一个看似合理的数字补上。参考文献条目绝不凭记忆生成。
- **证据分级。** 每个量都标注为 `measured`（实测）、`reported`（引用）、`assumed`（假设）。
- **阻塞优先。** 当前证据无法支撑请求时，先说明这一点，再动手，并指出唯一能解锁的缺项。
- **不凑审稿意见条数。** 审稿只报告真实存在的问题，不按要求的数量凑。
- **从中位数起步校准。** 评分从中位数开始，每一分移动都要有依据指向。高分要求零个 `Blocking` 问题。
- **互盲要么真的做到，要么明确声明。** 多审稿人输出先隔离、再冻结、最后才比对；若上下文无法隔离，就如实说明这一局限，而不是宣称独立性。
- **关卡不因截止压力让步。** 不因为用户不满就降低问题严重度。

## 安装

技能是普通的 `SKILL.md` 目录包。启用文件系统技能插件后，DSH 按 `<root>/<name>/SKILL.md` 发现技能。
只有已启用且健康的 watcher 才能无重启更新；离线校验通过不等于当前会话已加载。

八个技能位于本仓库的 `skills/` 目录，该目录只有技能、没有别的东西，因此可直接交给 DSH，或整体拷到其他机器。

```powershell
powershell -File tools/install.ps1 -WhatIf   # 只预览计划，不做任何改动
powershell -File tools/install.ps1           # 以 junction 链接到 ~/.dsh/skills
powershell -File tools/install.ps1 -Remove   # 只移除安装器自己拥有的内容
```

安装器会自动定位 `skills/`；若技能改为内联存放，则回退到仓库根目录。它不会删除不属于自己的数据：
移除链接时不触碰链接目标；复制模式写入所有权记录；`-Force` 只把不属于安装器的目录移到备份文件夹，
而不是删除。完整参数、根目录优先级、验证步骤与手动安装方式见 [INSTALL.md](INSTALL.md)。

## 校验

```powershell
node tools/validate-skills.cjs              # 默认检查 skills/
node tools/validate-skills.cjs --fix-bom    # 同时就地修复 UTF-8 BOM
node tools/check-dsh-discovery.cjs skills   # 离线兼容检查，不是实时启用检测
node --test tools/skill-tools.test.cjs      # 结构和发现逻辑的回归测试
node --test tools/install.test.cjs          # 安装器所有权规则（仅 Windows，只用临时目录）
```

校验器检查：frontmatter 是否存在及字段是否合法、`name` 是否为 kebab-case 且与目录名一致、调用开关的布尔拼写、frontmatter 是否闭合、是否存在 UTF-8 BOM、是否有未处理的 `TODO`/`TBD` 标记、每一条相对 Markdown 链接，以及每一条行内代码路径（例如 [gate-contract.md](skills/ctrl-shared/core/gate-contract.md)）。

行内路径要双向检查：在 `SKILL.md` 中正确的 `../` 路径放进 `references/` 后会多上溯一层，而 `references/x.md` 这类相对技能根目录的写法放进 `references/` 后又会多下钻一层，**没有其他工具会报告这些问题**。

description 超过 500 个字符（空白归一化后）会被判失败：DSH 的技能目录（catalog）默认在 500 字符处截断描述，末尾的触发词将永远到不了模型。此外，若一个技能都没扫到，校验器会以非零码退出，而不是报告「通过」——避免根目录写错却看起来像成功。

[发现检查](tools/check-dsh-discovery.cjs) 使用真实 YAML 解析和核查过的调用字段约定，检查八个不同的预期技能名称。
这只是离线兼容检查；运行时插件启用、扫描目录及会话可见性需单独核实。结构修改后应运行它。
工具说明见 [tools/README.md](tools/README.md)。

## 评测

[evals/evals.json](evals/evals.json) 包含 33 条行为评测，覆盖全部八个技能。每条针对一条契约规则，断言的是**行为**而非措辞。例如：拒绝未对齐协议的对比、拒绝由单次随机种子得出「达到最优」、拒绝为幻灯修改数字、拒绝在缺产物时报告关卡通过。

## 来源与移植

本包的构建方式是：盘点现有学术技能集合，提取其中可迁移的机制，再针对这五个方向重写。来源项目到落地机制的映射见 [docs/INTEGRATION.md](docs/INTEGRATION.md)，其中包含经核实的仓库身份、许可证、星标数，以及需要避开的 fork 陷阱。

上游集合的工作流机制被适配到这些领域；数值阈值只是本包默认值，不是已经验证的科学定律。
后续维护修正了统计假设、门禁适用范围、预算量纲与工具限制，把描述压到 DSH 目录长度限制以内，按第一手来源核对了基准数据集与期刊事实，并让安装器不再有破坏性操作，详见 [完善记录](docs/IMPROVEMENTS.zh-CN.md)。

## 目录结构

```text
ctrl-skills/                 仓库根目录
  README.md             英文说明
  README.zh.md          本文件
  INSTALL.md            安装、验证与卸载
  skills/               技能根目录：只有八个技能，别无其他
    ctrl-shared/          共享契约
    ctrl-lit-radar/       文献情报
    ctrl-idea-forge/      选题与规划
    ctrl-experiment-suite/ 实验与统计
    ctrl-paper-craft/     论文写作
    ctrl-pre-submission-review/ 审稿人视角自审
    ctrl-response-craft/  修订往来
    ctrl-paper-to-slides/ 报告幻灯
  tools/                校验器、DSH 发现检查、安装器及其测试
  evals/                行为评测用例
  docs/                 来源到机制的映射、中文快速使用、完善记录
  _research/            构建本包所依据的调研报告
```

要把 DSH 指向某个目录，或拷到另一台机器，用 `skills/` 即可。仓库其余部分存放支撑本包、但本身不是技能的内容。

## 许可证

默认不授予任何许可。本包实现的是从上游项目观察到的机制，这些项目许可证不一（MIT、Apache-2.0、CC BY-NC 4.0、CC BY-SA 4.0），本包未复制任何上游文件；但若你打算商业再分发或复用，请自行审阅 [docs/INTEGRATION.md](docs/INTEGRATION.md) 及各上游许可证。
