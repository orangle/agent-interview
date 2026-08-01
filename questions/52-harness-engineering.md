# 什么是 Harness Engineering？它与 Prompt、Context、Agent Runtime 有什么关系？

- ID：Q052
- 难度：进阶 / 系统设计
- 标签：Harness Engineering、Agent Runtime、Context Engineering、Guardrails、Evaluation
- 时效性：术语仍在快速演化，回答日期为 2026-08-01

## 同义问法

- 什么是 Agent Harness？
- 为什么生产级 Agent 不能只靠 Prompt？
- “模型负责冲，Harness 负责控”是什么意思？
- Harness、Runtime、Scaffolding 和 Guardrails 有什么区别？
- Coding Agent 的工作环境应该如何设计？

## 来源

### 原始题目线索

- 用户提供的二手题库：`11.1`—`11.11 Harness Engineering`
- 用户提供的二手题库：`12.3 四个 Engineering 有何区别`
- 原文将 Harness 固定拆成 Agent、Evaluation、Guardrails 三层。这是一种可用的整理方法，但不是统一行业标准。

### 技术依据

- OpenAI, *Harness engineering: leveraging Codex in an agent-first world*：强调为 Agent 设计可理解的仓库、工具、约束、反馈循环和持续治理。
  - https://openai.com/index/harness-engineering/
- Anthropic, *Effective harnesses for long-running agents*：讨论跨上下文窗口的状态衔接、环境初始化和增量进展。
  - https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents
- Anthropic, *Harness design for long-running application development*：讨论通过 Harness 设计提升长时间自主软件开发效果。
  - https://www.anthropic.com/engineering/harness-design-long-running-apps
- LangChain, *Frameworks, runtimes, and harnesses*：区分 Framework、Runtime 与 Harness 的价值层次。
  - https://docs.langchain.com/oss/python/concepts/products

## 核心结论

**Harness 是包围模型的工作环境和控制系统，使模型能够在明确边界内持续行动、获得真实反馈并证明任务完成。Harness Engineering 就是系统性设计这套环境。**

可以用一句话表达：

> 模型负责提出下一步和生成候选结果；Harness 负责提供可理解的环境、执行动作、反馈结果、限制风险并验证完成。

它不是单独一个库，也不只是 Prompt、沙箱或 Agent Loop，而是这些能力围绕任务形成的整体工程系统。

## 为什么需要 Harness

裸模型擅长生成和推理，但缺少以下保证：

- 不知道真实仓库和系统如何工作；
- 不能自行确认工具是否执行成功；
- 容易在长任务中丢失状态；
- 不天然遵守权限、事务和资源限制；
- 无法仅凭语言判断代码或业务结果是否正确；
- 失败后可能重复动作或编造完成；
- 人类难以追踪它为什么这么做。

Harness 的作用不是让模型“更聪明”，而是让模型的能力能够落在可控、可验收的工程闭环里。

## Harness 通常包含什么

## 1. 可理解的任务环境

Agent 能接触到的信息必须：

- 可发现；
- 有结构；
- 保持最新；
- 能与真实代码和系统对应。

Coding Agent 常见内容：

```text
AGENTS.md / CLAUDE.md       # 入口与导航，不是百科全书
ARCHITECTURE.md             # 系统边界和依赖关系
docs/                       # 设计、规范和运行手册
schemas/                    # 数据契约
scripts/                    # 可执行的标准操作
skills/                     # 按需加载的领域 SOP
```

重点是“给地图，而不是把一千页手册全部塞进上下文”。知识需要版本化、可导航，并通过 CI 检查陈旧和断链。

## 2. Context 构建与状态管理

Harness 决定每轮模型看到：

- 当前目标；
- 相关文件和文档；
- 已确认事实；
- 已完成步骤；
- 工具结果摘要；
- 剩余预算和风险。

长任务还需要：

- Checkpoint；
- 进度文件或执行计划；
- 决策日志；
- 跨会话恢复；
- 上下文压缩与按需检索。

Context Engineering 解决“当前给模型看什么”；Harness 还负责“这些信息如何生成、维护、验证和反馈”。

## 3. 工具与执行环境

包括：

- 文件、Git、Shell、浏览器、数据库和内部 API；
- Tool schema 与路由；
- 命令白名单；
- 沙箱和网络隔离；
- 资源、时间和并发限制；
- Tool Result 的结构化、裁剪和引用。

模型通常只负责提议动作，真正执行由 Harness 中的 Tool Executor 完成。

## 4. 硬约束和 Guardrails

Prompt 中的规则不是权限边界。Harness 需要用确定性机制实现：

- 最小权限；
- 高风险操作审批；
- 文件和网络访问范围；
- 参数校验；
- Secret 脱敏；
- 幂等、事务和补偿；
- 最大步数、成本和超时；
- Prompt Injection 与供应链风险防护。

## 5. 反馈与验证 Oracle

Agent 必须看到真实反馈：

- 编译结果；
- 单元测试和集成测试；
- 类型检查和 Linter；
- 静态安全扫描；
- 浏览器自动化；
- 性能指标；
- 业务断言；
- 人工 Review。

Oracle 是判断结果是否正确的外部标准。没有 Oracle 的“自我反思”很可能只是模型再次评价自己。

## 6. Orchestration 与 Runtime

Runtime 通常负责：

- Agent Loop；
- 节点和状态流转；
- 并发调度；
- 暂停、恢复和取消；
- 错误分类、重试和降级；
- Human-in-the-Loop；
- 长任务生命周期。

Runtime 是 Harness 的重要组成部分，但 Harness 范围更宽，还包括仓库设计、知识组织、测试反馈、权限和运维治理。

## 7. Observability 与 Evaluation

至少记录：

- 模型输入输出；
- 状态变化；
- 工具调用、参数和结果；
- Token、延迟和成本；
- 重试、循环和失败原因；
- 最终验证证据；
- 人工审批和修改。

Evaluation 不只是上线前打分，还要从线上失败中判断问题属于：

- 模型能力；
- Context 构建；
- Tool 设计；
- Harness 策略；
- Runtime 故障；
- 任务本身不可验证。

## 8. 持续治理和“垃圾回收”

Agent 会复制仓库中已有模式，坏模式也会被快速放大。Harness 因此需要持续治理：

- 架构规则机械化；
- 文档陈旧检测；
- 重复代码和坏模式扫描；
- 定期回归评测；
- 失败经验转成规则、测试或 Skill；
- 废弃过期指令和工具。

这不是一次性搭建，而是持续演化的工程系统。

## 与相关概念的边界

## Harness vs Prompt Engineering

- Prompt Engineering：优化模型这一轮如何理解和输出；
- Harness Engineering：优化模型在多步环境中如何行动、反馈、恢复和验收。

Prompt 是 Harness 的一个组件，但不能替代执行和验证机制。

## Harness vs Context Engineering

- Context Engineering：决定模型当前看见哪些信息；
- Harness：还负责信息的来源、工具执行、状态更新、安全、反馈和完成验证。

## Harness vs Agent Runtime

- Runtime：运行循环、状态机、调度、Checkpoint 和恢复；
- Harness：包含 Runtime，并扩展到知识、工具、沙箱、测试、评估和仓库治理。

## Harness vs Framework

- Framework 提供通用抽象和集成；
- Harness 是针对具体任务和环境形成的完整工作系统。

使用同一个框架的两个团队，Harness 质量可能完全不同。

## Harness vs Scaffolding

Scaffolding 通常指项目结构和基础脚手架；Harness 关注整个执行与反馈闭环。脚手架可以是 Harness 的一部分，但没有工具、验证、状态和治理时还不够。

## “三层 Harness”是不是标准答案

可以按执行、评估、防护三层帮助表达：

```text
Execution Harness   → 工具、状态、调度、恢复
Evaluation Harness  → 测试、Judge、回归集、发布门禁
Guardrails Harness  → 权限、沙箱、输入输出拦截
```

但面试时应说明：这是便于分析的分类，不是唯一或统一行业标准。实际能力还包括知识组织、Context、可观测性和持续治理，并且三层之间有重叠。

## 一个 Coding Agent Harness 示例

```text
用户任务
  ↓
任务契约与验收条件
  ↓
仓库导航 + Skill + Relevant Context
  ↓
Planner / Agent Loop
  ↓
Sandboxed Tools：read / edit / test / browser / git
  ↓
Mechanical Feedback：test / lint / type / security / performance
  ↓
Review：Agent Reviewer / Human Approval
  ↓
Trace + Checkpoint + PR Artifact
  ↓
通过验收或升级人工
```

## 如何判断 Harness 是否有效

不要只看 Agent 输出是否“像样”，要做消融实验：

- 去掉某个 Skill，任务成功率是否下降；
- 去掉测试反馈，假完成是否增加；
- 更换模型后，Harness 是否仍能稳定约束行为；
- 相同模型在不同仓库结构下表现差多少；
- 失败来自模型、上下文还是执行环境；
- 增加一条规则是否真的改善回归集，而非只修一个样例。

常见指标：

- 任务完成率；
- 可验证成功率；
- 无效工具调用率；
- 平均修复轮数；
- 人工介入率；
- 回滚率；
- 成本和端到端延迟；
- 安全违规和越权尝试。

## 常见低质量回答

### 低质量回答一

> Harness 就是 Agent 的操作系统或笼子。

问题：比喻可以帮助理解，但没有说明具体构成、边界和验证机制。

### 低质量回答二

> 除了模型权重以外的全部东西都是 Harness。

问题：范围过大，失去工程分析价值。应围绕 Agent 完成任务所需的环境、执行、反馈和治理系统来定义。

### 低质量回答三

> Prompt 不可靠，所以所有行为都写成 Workflow。

问题：Harness 的目标不是消灭模型自主性，而是在关键边界用确定性机制控制，在局部保留模型的探索和泛化能力。

### 低质量回答四

> 加一个 Reviewer Agent 就是 Evaluation Harness。

问题：Reviewer 仍可能共享模型偏差。可靠评估需要测试、业务断言、证据和人工标准。

## 可直接口述的回答

> Harness Engineering 是围绕模型设计一套可执行、可反馈、可约束和可验收的工作环境。模型负责理解任务和提出动作，Harness 负责构造上下文、暴露工具、维护状态、在沙箱中执行、反馈真实结果、限制权限，并通过测试或业务 Oracle 判断是否完成。
>
> Prompt、Context 和 Runtime 都是 Harness 的组成部分，但范围不同。Prompt 影响模型行为，Context 决定模型看见什么，Runtime 负责循环、状态和恢复；Harness 还包括仓库知识结构、工具契约、Guardrails、可观测、评估和持续治理。它不是某个固定框架，也没有唯一三层标准。生产级 Agent 的关键不是让模型多想，而是让环境对 Agent 可理解、规则可执行、结果可证明。

## 结合个人项目回答

> 我们内部的 Coding/CI/CD Agent，Harness 不只是 Claude Code 外面套一层服务。它应该包括会话和 Workspace 生命周期、OpenSandbox 隔离、Git/Jenkins/K8s 工具、按需加载的故障分析 Skill、日志裁剪、Checkpoint、权限审批、测试与部署验证、Trace 和成本统计。模型负责选择分析路径，但生产写操作、超时、幂等和验收必须由平台控制。长期来看，失败案例应优先沉淀成测试、脚本和结构化规则，而不是继续把提示词写长。

## 继续追问

1. Harness 与 Agent Platform 的边界是什么？
2. 如何通过消融实验判断某条 Harness 规则是否有效？
3. 长任务跨上下文窗口时，哪些状态必须持久化？
4. 为什么仓库“可被 Agent 理解”比单纯扩大 Context 更重要？
5. 如何防止 Harness 自身不断膨胀和过时？