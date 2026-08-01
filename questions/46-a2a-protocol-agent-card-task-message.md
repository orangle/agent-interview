# A2A 协议解决什么问题？Agent Card、Task、Message 如何工作？

- ID：Q046
- 难度：基础 / 进阶 / 协议
- 标签：A2A、Agent Card、Task、Message、Artifact、Agent Interoperability
- 时效性：基于 A2A `1.0.0` 规范，整理日期为 2026-08-01

## 核心结论

**A2A 用于独立、可能不透明的 Agent 系统之间发现能力、发起有状态任务并交换消息与产物。** 它关注 Agent-to-Agent 协作，不要求对方暴露内部 Prompt、工具和推理实现。

官方规范：

- https://github.com/a2aproject/A2A/blob/main/docs/specification.md

## 一、MCP 与 A2A 的关注点不同

```text
MCP：Agent / Host 如何连接工具和上下文 Server
A2A：一个 Agent 系统如何把任务委派给另一个 Agent 系统
```

两者可以组合：远程 Agent 通过 A2A 接收任务，它内部再通过 MCP 使用工具。

## 二、Agent Card

Agent Card 是远程 Agent 的能力和连接元数据，描述：

- 身份和说明；
- Service Endpoint；
- 协议接口和版本；
- 支持的输入输出 Modality；
- Skills；
- Streaming、Push Notification 等 Capability；
- Authentication / Security Scheme；
- 扩展。

公开 Card 可以通过：

```text
https://host/.well-known/agent-card.json
```

发现。敏感能力可以通过鉴权后的 Extended Agent Card 暴露。

Card 是能力声明，不是可信证明。客户端仍需验证来源、签名、TLS、权限和业务准入。

## 三、Message、Part、Artifact

### Message

一次交互消息，包含发送角色和一个或多个 Part，用于：

- 发起任务；
- 补充信息；
- 澄清；
- 状态说明；
- 多轮交互。

### Part

最小内容单元，可承载文本、结构化数据、文件引用等不同类型。

### Artifact

任务产生的正式输出，例如报告、代码、文件或结构化结果。

规范强调 Message 与 Artifact 的职责不同：消息用于沟通，稳定任务输出应放在 Artifact 中，不能只依赖瞬时流消息。

## 四、Task

Task 是 A2A 的有状态工作单元：

```json
{
  "id": "task-123",
  "contextId": "ctx-8",
  "status": {"state": "TASK_STATE_WORKING"},
  "artifacts": [],
  "history": []
}
```

Task 有生命周期和终态，适合长时间任务、异步结果和 Human-in-the-Loop。客户端可以获取、列出、取消或订阅任务。

`contextId` 用于关联相关任务和消息；`taskId` 标识一个具体工作单元，不能混为会话 ID。

## 五、核心操作

A2A 1.0 定义与传输 Binding 无关的操作，包括：

- Send Message；
- Send Streaming Message；
- Get Task；
- List Tasks；
- Cancel Task；
- Agent Card 获取；
- Push Notification 配置等。

简单交互可以直接返回 Message；复杂交互返回 Task，后台继续运行并产生状态或 Artifact 更新。

## 六、异步优先

长任务可使用：

- Streaming 获取实时 `TaskStatusUpdateEvent` 和 `TaskArtifactUpdateEvent`；
- Polling 获取 Task；
- Push Notification 在客户端离线后通知；
- 重新 Get Task 获取权威状态与产物。

Streaming 消息不应作为关键结果唯一载体，因为断线后未必完整重放；Task 和 Artifact 才是持久状态。

## 七、多轮交互

远程 Agent 可进入需要输入状态，发送 Message 请求补充信息；客户端携带 `contextId` 和已有 `taskId` 继续交互。

必须定义：

- 哪些终态不能继续写消息；
- 超时和清理；
- 重复 `messageId` 的幂等；
- Task 访问权限；
- History 保留策略。

## 八、传输与 Binding

A2A 1.0 规范将数据模型和操作与具体 Binding 分开，并描述 JSON-RPC、gRPC 和 HTTP+JSON/REST 等 Binding。不要把 A2A 简化成“固定 HTTP+SSE”。

## 九、安全

- Agent Card 不放凭证；
- 验证 Agent 身份和 Endpoint；
- 每个 Task 做认证授权；
- 文件和结构化 Part 做内容安全检查；
- 防 SSRF 和恶意 Artifact；
- 限制任务、消息、文件和运行预算；
- 不把远程 Agent 输出自动写入全局确认状态；
- 高风险动作仍由本地 Policy 和人工审批控制。

## 十、A2A 不解决什么

- 如何选择正确 Agent；
- 远程 Agent 是否可靠；
- 内部工具权限；
- 任务结果是否真实；
- 跨 Agent 业务事务；
- 多 Agent 的全局规划和状态合并。

这些由本地 Orchestrator、Registry、Evaluation 和业务系统负责。

## 常见错误回答

> Agent Card 在 `/.well-known/agent.json`。

当前 1.0 规范使用 `/.well-known/agent-card.json`。

> A2A 通过 HTTP+SSE 通信。

当前规范有独立数据模型与操作，并支持多种 Binding；Streaming 只是交互方式之一。

## 面试口述版

> A2A 面向独立 Agent 系统互操作。远程 Agent 通过 Agent Card 声明身份、Endpoint、Skills、输入输出类型、安全方案和可选能力。客户端发送 Message，简单任务可直接得到 Message，复杂任务返回有生命周期的 Task；沟通过程使用 Message 和 Part，正式结果放在 Artifact。长任务可 Streaming、Polling 或 Push Notification，但权威状态仍从 Task 获取。A2A 不暴露 Agent 内部实现，也不自动保证结果可信，本地 Orchestrator 仍需做 Agent 选择、权限、证据校验和高风险审批。

## 结合个人项目

统一 Agent 平台可以把“代码分析 Agent”“发布诊断 Agent”作为 A2A 服务对外声明能力。会话平台通过 Card 发现和委派任务，但最终写代码或发布仍受本地 Workspace、Tool Gateway 和审批系统控制。