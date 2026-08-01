# Agent 设计原理与手撕专题

这条专题面向国内面试常见的“不要只讲框架，现场把原理画出来、写出来”的考察方式。

目标不是背 LangChain、LangGraph 或某个 SDK 的 API，而是做到：

1. 不依赖框架画出 Agent 的状态流转；
2. 写出最小可运行的 Agent Loop；
3. 解释每个状态、数据结构和异常分支；
4. 从 Demo 逐步演进到可恢复、可审计、可控制的生产 Runtime；
5. 能说明框架只是这些原理的一种实现。

## 一、什么叫“手撕 Agent 原理”

面试官通常不会满足于：

> Agent = LLM + Tool + Memory + Planning。

他更可能继续问：

- LLM 返回什么结构，Runtime 怎么判断下一步？
- Tool call 是谁执行的？工具结果如何回填？
- Agent 状态存在哪里？服务重启后怎么继续？
- 如何识别死循环？重试工具还是重新规划？
- 并行工具如何保证依赖和副作用安全？
- Context 满了以后，哪些内容保留、压缩或外置？
- 如何证明任务完成，而不是模型自己说完成？

因此，一道原理题至少需要回答四层：

```text
抽象模型 → 状态与数据结构 → 核心算法/伪代码 → 生产异常路径
```

## 二、当前仓库已经覆盖的原理题

### 1. 控制循环

- [ReAct 与 Agent Loop 为什么有效，又有什么局限？](./02-react-and-agent-loop.md)
- [Agent 如何判断信息已经足够，并避免死循环？](./03-agent-stop-and-loop-control.md)
- [Agent 有哪些常见设计范式？复杂任务如何拆分与动态重规划？](./10-agent-patterns-task-decomposition-replanning.md)

需要掌握：

- Think / Act / Observe 的数据流；
- `final_output`、工具调用和 handoff 的分支；
- 最大轮次、Token、时间、重复动作等停止条件；
- Plan-and-Execute 的重规划触发条件。

### 2. Tool Calling

- [如何让 Tool Calling 在生产环境中可靠？](./04-reliable-tool-calling.md)
- [Skill、Tool、MCP Server 和 Workflow 的边界是什么？](./19-skill-tool-mcp-workflow-boundaries.md)

需要掌握：

- Tool Schema 如何进入模型上下文；
- 模型只是生成调用意图，Runtime 才负责执行；
- 参数校验、错误分类、超时、幂等、权限和审计；
- Tool Result 如何以结构化消息返回下一轮模型调用。

### 3. Context 与状态

- [Agent 的 Context Engineering 应该怎么做？](./05-context-engineering.md)
- [Agent 与大模型的本质区别是什么？一个 Agent 至少需要哪些组件？](./09-agent-vs-model-and-components.md)

需要掌握：

- Runtime State 与发给模型的 Context 不是同一个东西；
- Context Builder 如何选择当前目标、历史消息、工具结果、计划和记忆；
- 原始证据、结构化状态和压缩摘要应分开保存；
- Checkpoint 用于恢复执行，长期 Memory 用于跨任务复用。

### 4. Runtime 与 Harness

- [生产环境什么时候使用 Agent 框架，什么时候自己实现核心 Runtime？](./13-framework-vs-custom-runtime.md)
- [什么是 Harness Engineering？它与 Prompt、Context、Agent Runtime 有什么关系？](./52-harness-engineering.md)

需要掌握：

- Runtime 管理一次任务怎样运行；
- Harness 提供工具、权限、环境、反馈和验证；
- 框架封装的是 Loop、State、Tool、Checkpoint、Trace 等通用能力；
- 业务规则不应完全绑定到框架私有抽象中。

### 5. Multi-Agent 与评估

- [什么时候用单 Agent，什么时候用 Multi-Agent？](./06-single-vs-multi-agent.md)
- [如何建立 Agent 评估体系？](./07-agent-evaluation.md)

需要掌握：

- 多 Agent 本质是多个决策单元之间的任务与状态协调；
- Supervisor、handoff、agent-as-tool 的控制权不同；
- 不能只评估最终文本，还要评估轨迹、工具选择、参数、步数和成本。

## 三、需要新增的“手撕”题

以下题目是已有题库中相对薄弱、但很适合现场手写或白板设计的部分。

### P0：必须掌握

1. [从零设计一个最小 Agent Runtime](./53-design-minimal-agent-runtime.md)
2. 手写 Function Calling 的完整执行链路
3. 设计 Agent State、Message、ToolCall、Observation 的数据结构
4. 手写停止条件与重复动作检测器
5. 设计 Context Builder：窗口、摘要、证据和 Token Budget
6. 设计 Tool Registry 与 Tool Router
7. 设计 Checkpoint、暂停、恢复和幂等执行

### P1：进阶

8. 设计异步长工具的任务状态机
9. 设计 Parallel Tool Calling 的依赖图和调度器
10. 设计 Planner-Executor-Replanner
11. 设计 Human-in-the-Loop 审批状态机
12. 设计多租户 Agent 的会话隔离与资源配额
13. 设计 Agent Trace、Replay 与故障归因系统

### P2：系统设计

14. 设计一个 Coding Agent Runtime
15. 设计一个 CI/CD 故障诊断 Agent
16. 设计一个支持 MCP 的企业 Tool Gateway
17. 设计一个可恢复的长任务 Agent 平台
18. 设计 Multi-Agent Supervisor 与状态一致性机制

## 四、现场答题模板

遇到“手写一个 Agent”时，不要直接开始写 `while True`。建议按以下顺序回答。

### 第一步：确认目标和边界

先问清楚：

- 单 Agent 还是多 Agent；
- 是否调用有副作用的工具；
- 是否需要跨进程恢复；
- 是同步请求还是长任务；
- 如何定义任务完成。

### 第二步：画核心状态机

```text
READY
  ↓
BUILD_CONTEXT
  ↓
MODEL_INFERENCE
  ├── FINAL ─────────────→ SUCCEEDED
  ├── TOOL_CALL ─────────→ VALIDATE_TOOL
  ├── NEED_CONFIRMATION ─→ WAITING_APPROVAL
  └── INVALID_OUTPUT ────→ REPAIR / FAILED

VALIDATE_TOOL
  ├── PASS → EXECUTE_TOOL → APPEND_OBSERVATION → CHECKPOINT → BUILD_CONTEXT
  └── FAIL → APPEND_ERROR ─────────────────────────────────→ BUILD_CONTEXT
```

### 第三步：定义核心数据结构

至少说清楚：

- `RunState`：任务级状态；
- `Message`：模型可见消息；
- `ToolCall`：调用意图与参数；
- `ToolResult`：成功、失败和错误语义；
- `Checkpoint`：可恢复快照；
- `TraceEvent`：可观测事件。

### 第四步：写主循环

主循环只负责控制，不应把所有业务细节塞进去：

```text
load state
while budget remains:
    context = build_context(state)
    decision = call_model(context, candidate_tools)
    transition(state, decision)
    checkpoint(state)
return terminal_result
```

### 第五步：补异常和生产边界

至少主动补充：

- 模型超时与重试；
- 工具参数错误和不可恢复错误；
- 有副作用工具的幂等键；
- 重复调用和无进展检测；
- Context 超限；
- 服务重启和断点恢复；
- 权限审批与审计；
- Token、时间和调用次数预算。

## 五、判断是否真正理解

能回答以下问题，才算掌握，而不是背名词：

- 为什么 Runtime State 不能只保存为对话消息？
- 为什么工具错误不应该全部交给 LLM 决定是否重试？
- 为什么“模型输出 Final”不等于业务任务完成？
- 为什么 Checkpoint 和长期 Memory 不能混为一谈？
- 为什么并行 Tool Calling 不是简单 `asyncio.gather`？
- 为什么一个 200 行 Agent Loop 仍可能无法进入生产？
- 为什么状态机比无限 `while` 循环更容易测试和恢复？

## 六、学习顺序

```text
Agent 与模型
→ Agent Loop
→ State 与消息协议
→ Tool Calling
→ 停止与错误处理
→ Context Builder
→ Checkpoint 与恢复
→ Harness 与安全
→ Multi-Agent
→ 平台化
```

每学完一题，至少完成两次输出：

1. 口述 3～5 分钟；
2. 不依赖框架写出伪代码或数据结构。