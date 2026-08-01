# MCP 的架构、原语、会话和传输机制是什么？

- ID：Q043
- 难度：基础 / 进阶 / 协议
- 标签：MCP、Host、Client、Server、Resources、Prompts、Tools、JSON-RPC
- 时效性：基于 MCP `2025-11-25` 规范，整理日期为 2026-08-01

## 核心结论

**MCP 是 LLM 应用与外部能力之间的标准化上下文与工具协议。** 它解决的是 Host 如何发现、协商并调用不同 Server 提供的能力，而不是替 Agent 决定业务流程，也不自动保证权限和安全。

官方规范：

- https://modelcontextprotocol.io/specification/2025-11-25

## 一、Host–Client–Server 架构

```text
MCP Host（Claude Desktop、IDE、Agent 应用）
  ├── MCP Client A ── 1:1 ── MCP Server A
  ├── MCP Client B ── 1:1 ── MCP Server B
  └── LLM / Context / Consent / Policy
```

### Host

负责：

- 创建和管理 Client；
- 聚合上下文；
- 控制用户授权与安全策略；
- 连接 LLM；
- 隔离不同 Server；
- 决定哪些结果进入模型上下文。

### Client

Host 内的协议连接器，一个 Client 与一个 Server 建立有状态会话，处理初始化、能力协商、消息路由、订阅和通知。

### Server

暴露专注的上下文或能力。可以是本地子进程，也可以是远程服务。Server 通常不应看到 Host 的完整会话，只接收完成请求需要的信息。

## 二、核心原语

### 1. Resources

由 Server 暴露的上下文数据，使用 URI 标识，例如文件、数据库 Schema、Git 历史。通常由应用或用户选择如何加入 Context。

### 2. Prompts

可复用的提示模板或交互入口，通常偏用户控制，例如菜单操作、Slash Command。

### 3. Tools

可执行能力，模型可提出调用，例如查数据库、调用 API 或写文件。Host 负责同意、执行链路和安全控制。

2025-11-25 规范还定义 Client 可提供的能力，包括 Sampling、Roots 和 Elicitation。不能把 MCP 简化为只有 Tool Calling。

## 三、Base Protocol

MCP 消息使用 JSON-RPC 2.0，包含：

- Request；
- Response；
- Notification；
- 错误对象。

连接初始化时双方进行版本与 Capability Negotiation。只有声明支持的功能才能在会话中使用。

```text
Client → initialize
Server → protocolVersion + capabilities
Client → initialized notification
随后进行 tools/list、resources/read、tools/call 等交互
```

## 四、传输方式

### stdio

Host 启动 Server 子进程，通过标准输入输出传输 JSON-RPC。

适合：

- 本地 IDE；
- 命令行工具；
- 单用户桌面应用；
- 低部署成本集成。

Host 管理进程生命周期，Server 日志应输出到 stderr，不能污染协议 stdout。

### Streamable HTTP

远程 Server 通过 HTTP 提供 MCP 端点，支持普通响应、流式返回、会话管理、恢复和重投递相关机制。

适合：

- 企业共享 Server；
- 跨网络部署；
- 统一授权、扩缩容和治理。

旧版 HTTP+SSE 已被 Streamable HTTP 取代，不能再把当前 MCP 远程传输概括成两个固定端点的 HTTP+SSE。

规范传输说明：

- https://modelcontextprotocol.io/specification/2025-11-25/basic/transports

## 五、MCP 是有状态协议，但业务状态另算

MCP 会话状态包括：

- 协议版本；
- 双方 Capability；
- Session；
- 订阅和通知；
- 进行中的请求。

它不等于 Agent 的任务状态、用户 Memory 或业务事务。Agent Run 仍需要自己的 Checkpoint 和 Durable Execution。

## 六、安全边界

MCP 标准化连接，不等于可信。Host 必须：

- 验证 Server 身份和来源；
- 做用户同意与最小权限；
- 过滤工具候选；
- 校验参数和结果；
- 防止 Token / Secret 泄露；
- 对远程 Server 使用授权；
- 将 Server 描述和 Tool Annotation 视为不完全可信；
- 保留审计日志。

工具说明写“只读”不能替代真实权限控制。

## 七、动态发现

Client 可以 `tools/list`、`resources/list`、`prompts/list` 获取能力，并接收列表变化通知。但 Host 不应把发现到的全部能力直接暴露给模型，还需根据用户、任务、风险和 Token 预算构造候选集。

## 八、MCP 不解决什么

- Agent 的规划算法；
- Tool 选择正确率；
- 业务事务；
- 多 Agent 协作；
- 任务完成验证；
- Server 内部实现质量；
- 权限策略本身。

它类似连接标准，而不是完整 Agent Framework。

## 常见错误回答

> MCP 是 Agent 调工具的 USB-C。

这个比喻适合入门，但面试要继续说明 Host/Client/Server、Capability Negotiation、Resources/Prompts/Tools、JSON-RPC 和安全边界。

> MCP 的传输是 stdio 和 HTTP+SSE。

这是旧规范表述。当前标准远程传输是 Streamable HTTP。

## 面试口述版

> MCP 采用 Host–Client–Server 架构。Host 是包含 LLM、用户同意和安全策略的应用，每个 Client 与一个 Server 建立有状态会话，通过 JSON-RPC 完成初始化和能力协商。Server 可以暴露 Resources、Prompts 和 Tools，Client 侧还可能支持 Sampling、Roots 和 Elicitation。标准传输是本地 stdio 和远程 Streamable HTTP。MCP 只标准化发现与通信，Host 仍要负责权限、候选工具、参数校验、审计和 Agent 任务状态，不能把协议连接等同于安全执行。

## 结合个人项目

企业 Agent 平台可以把日志、Jenkins、Git 和 Kubernetes 封装为 MCP Server，但 Host 仍应根据项目和环境做权限过滤，并通过自己的 Tool Gateway 统一审计，而不是让每个会话直接连接任意 Server。