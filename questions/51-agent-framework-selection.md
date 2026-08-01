# LangChain、LangGraph、LangSmith 及主流 Agent 框架如何选型？

- ID：Q051
- 难度：进阶 / 系统设计
- 标签：LangChain、LangGraph、LangSmith、AutoGen、CrewAI、ADK、Framework Selection
- 时效性：框架变化快，整理日期为 2026-08-01

## 核心结论

**框架选型不是比较功能清单，而是确定你需要哪一层抽象：模型与工具集成、Agent Loop、持久化 Runtime、多 Agent 通信，还是可观测和部署平台。**

先画自己的状态机、错误恢复和部署约束，再选择最薄的合适框架；不要从框架名反推系统架构。

## 一、LangChain 生态的层次

根据当前官方文档：

- **LangChain**：高层 Agent Framework，提供模型、工具、消息、Middleware 和常见 Agent Loop 抽象；
- **LangGraph**：低层编排与 Runtime，侧重显式状态、Durable Execution、Streaming、HITL 和持久化；
- **LangSmith**：Tracing、Evaluation、Prompt、Deployment 和运行平台；
- **Deep Agents**：建立在 LangGraph 上的更完整 Harness，包含规划、Subagent、文件系统和 Context 管理。

官方资料：

- https://docs.langchain.com/oss/python/concepts/products
- https://docs.langchain.com/oss/python/langgraph/overview

### 什么时候用 LangChain

- 快速构建标准 Tool-calling Agent；
- 团队需要统一模型和工具接口；
- 编排不复杂；
- 希望使用成熟 Middleware 和集成。

### 什么时候直接用 LangGraph

- 需要显式 State 与状态转移；
- 长任务、暂停恢复；
- 确定 Workflow 与 Agent 决策混合；
- HITL；
- 复杂错误和重试；
- 希望控制每个节点。

### LangSmith 的位置

LangSmith 不是 LangGraph 的替代品，而是开发、Trace、评测和部署治理平台。也可观测其他框架。

## 二、AutoGen

当前 AutoGen 分为：

- **AgentChat**：高层单/多 Agent API 和预置 Team Pattern；
- **Core**：事件驱动、消息与 Runtime 基础，适合更灵活或分布式多 Agent；
- **Extensions**：模型、MCP、Docker Code Executor、gRPC Runtime 等集成。

官方资料：

- https://microsoft.github.io/autogen/
- https://microsoft.github.io/autogen/stable/user-guide/agentchat-user-guide/index.html

适合：

- 对话式多 Agent 研究和原型；
- 需要自定义消息协议和事件驱动 Runtime；
- 分布式 Agent 实验。

需要重点评估 Context 增长、终止条件、状态持久化和生产部署，而不是只使用 Group Chat Demo。

## 三、CrewAI

CrewAI 提供：

- Crews：角色化 Agent 团队；
- Tasks / Processes：顺序、层级等协作；
- Flows：事件和状态驱动的确定编排；
- Memory、Knowledge、Guardrails 和 Observability。

官方资料：

- https://docs.crewai.com/

适合：

- 业务团队快速构建角色协作；
- 内容研究、流程自动化；
- 希望较高层表达 Crews + Flow。

需要验证高并发、复杂状态、版本升级和底层可控性是否符合你的场景。

## 四、Google ADK 等

Google ADK、OpenAI Agents SDK、LlamaIndex 等也提供 Agent、Tool、Session、Runner 或多 Agent 抽象。选型方法相同：看你的模型生态、部署环境、协议、可观测性和 Runtime 需求，而不是枚举所有框架。

## 五、选型矩阵

| 需求 | 优先考虑 |
|---|---|
| 快速标准 Agent | 高层 Agent Framework |
| 复杂状态机和恢复 | LangGraph / Durable Runtime |
| 对话式多 Agent | AutoGen AgentChat / Core |
| 角色化业务自动化 | CrewAI Crews + Flows |
| RAG 数据框架 | LlamaIndex / LangChain 相关组件 |
| 统一 Trace 与 Eval | LangSmith 或 OpenTelemetry 体系 |
| 强企业平台控制 | 自研薄 Runtime + 选用底层组件 |

这个表只是方向，最终仍需要 POC。

## 六、选型时必须验证

### 控制与恢复

- State 是否显式；
- Checkpoint；
- 幂等；
- 暂停、恢复和取消；
- 异步长工具；
- 部分失败。

### 扩展和锁定

- Model / Tool 是否可替换；
- 是否依赖私有消息结构；
- 业务逻辑能否脱离框架测试；
- 升级兼容性；
- 数据格式能否导出。

### 生产属性

- 并发与资源；
- 多租户；
- 权限和审计；
- Trace；
- 部署方式；
- 维护活跃度；
- 语言与团队能力。

## 七、框架与自研的边界

推荐：

- 自己定义业务 State、Tool Contract、错误分类和领域模型；
- 框架提供模型适配、图执行、Checkpoint 或 Trace；
- 用 Adapter 隔离框架；
- 核心业务测试不依赖在线模型；
- 先做最小 POC，再决定长期绑定。

不要为“避免依赖”重写所有通用能力，也不要把业务规则深埋进框架对象。

## 八、POC 任务

同一真实任务分别实现：

- 正常路径；
- 工具超时；
- 中途审批；
- 服务重启恢复；
- Context 超限；
- 多 Agent 分歧；
- Trace 回放；
- 框架升级。

比较代码复杂度、可解释性、故障恢复、运行成本和维护成本。

## 常见错误回答

> LangGraph 适合 Workflow，CrewAI 适合 Multi-Agent，AutoGen 适合聊天。

过度标签化。它们的能力都在扩展，应按抽象层和生产要求判断。

> 生产环境框架都不可靠，核心 Loop 必须手写。

自研也会引入大量持久化和恢复问题。应判断框架是否可控、可测试和可替换，而不是一概拒绝。

## 面试口述版

> 我先区分 Framework、Runtime、Harness 和 Observability。LangChain 偏高层 Agent 抽象，LangGraph 偏显式状态和 Durable Runtime，LangSmith负责 Trace、Eval 和部署；AutoGen 更强调消息和多 Agent Runtime；CrewAI 用 Crews 与 Flows 表达角色协作和确定流程。选型前我会画业务状态机，列出恢复、HITL、多租户、权限和部署要求，再用真实异常路径 POC。业务 State、Tool Contract 和错误语义由自己定义，框架通过 Adapter 接入，避免既重复造轮子又被私有抽象锁死。

## 结合个人项目

统一 Agent 平台底层可使用 OpenSandbox 管环境，自研 Go Control Plane 管 Session、Workspace 和任务状态；上层允许 LangGraph、Claude Code 或其他 Runtime 通过 Adapter 接入，而不是强制全公司使用一个框架。