# Agent 设计原理与手撕专题

这条专题面向国内面试常见的“不要只讲框架，现场把原理画出来、写出来”的考察方式。

目标不是背 LangChain、LangGraph 或某个 SDK 的 API，而是做到：

1. 不依赖框架画出 Agent 的状态流转；
2. 写出最小可运行的 Agent Loop；
3. 解释每个状态、数据结构和异常分支；
4. 从 Demo 演进到可恢复、可审计、可控制的生产 Runtime；
5. 说明框架只是这些原理的一种实现。

## 一、什么叫“手撕 Agent 原理”

面试官不会满足于：

> Agent = LLM + Tool + Memory + Planning。

他通常会继续追问：

- LLM 返回什么结构，Runtime 如何决定下一步？
- Tool Call 是谁执行的？结果如何关联并回填？
- Agent 状态存在哪里？服务重启后怎么继续？
- 如何识别死循环？何时重试，何时重规划？
- 并行工具怎样处理依赖、冲突和副作用？
- Context 满了以后，哪些内容保留、压缩或外置？
- 模型说完成了，为什么业务上可能仍未完成？

一道原理题至少要回答：

```text
抽象模型
→ 状态与数据结构
→ 主流程和伪代码
→ 错误、停止与恢复路径
→ 从 Demo 到生产的演进
```

## 二、已完成的核心原理题

### A. 控制循环和运行时

1. [Q002 ReAct 与 Agent Loop 为什么有效，又有什么局限？](./02-react-and-agent-loop.md)
2. [Q003 Agent 如何判断信息已经足够，并避免死循环？](./03-agent-stop-and-loop-control.md)
3. [Q010 Agent 设计范式、任务拆分与动态重规划](./10-agent-patterns-task-decomposition-replanning.md)
4. [Q053 从零设计一个最小 Agent Runtime](./53-design-minimal-agent-runtime.md)
5. [Q057 手写停止条件与重复动作检测](./57-stop-conditions-and-loop-detection.md)

需要掌握：

- Think / Act / Observe 的状态流转；
- final、tool call、handoff、approval 的分支；
- 硬预算、完成验证和循环检测；
- 模型提议动作，Runtime 决定能否执行。

### B. Function Calling 与工具执行

1. [Q004 如何让 Tool Calling 在生产环境中可靠？](./04-reliable-tool-calling.md)
2. [Q019 Skill、Tool、MCP Server 和 Workflow 的边界](./19-skill-tool-mcp-workflow-boundaries.md)
3. [Q054 手写 Function Calling 完整链路](./54-function-calling-end-to-end.md)
4. [Q059 设计异步长工具状态机](./59-async-long-running-tools.md)
5. [Q060 设计 Parallel Tool Calling 依赖调度器](./60-parallel-tool-dependency-scheduler.md)

需要掌握：

- Tool Schema 如何进入模型上下文；
- 模型只生成调用意图，Runtime 执行；
- 参数与业务校验、权限、超时、错误分类、幂等；
- 长任务的提交、等待、回调、轮询、取消和恢复；
- 并行调用的 DAG、读写冲突和补偿。

### C. State、Context 与恢复

1. [Q005 Agent 的 Context Engineering 应该怎么做？](./05-context-engineering.md)
2. [Q009 Agent 与大模型的本质区别及核心组件](./09-agent-vs-model-and-components.md)
3. [Q055 手写 Agent State 与消息协议](./55-agent-state-and-message-protocol.md)
4. [Q056 手写 Context Builder 与 Token Budget](./56-context-builder-and-token-budget.md)
5. [Q058 设计 Checkpoint、暂停、恢复与幂等](./58-checkpoint-pause-resume-idempotency.md)

需要掌握：

- Runtime State、Event Log、Model Context 的区别；
- State Patch、版本号、Reducer 和消息关联 ID；
- Context 是从完整 State 中按预算生成的投影；
- 摘要不是无损压缩，原始证据必须可回溯；
- Checkpoint 保存可安全恢复的执行边界，而非仅保存 messages。

### D. 计划、审批与可观测性

1. [Q061 设计 Planner–Executor–Replanner](./61-planner-executor-replanner.md)
2. [Q062 设计 Human-in-the-Loop 审批状态机](./62-human-in-the-loop-approval-state-machine.md)
3. [Q063 设计 Agent Trace、Replay 与故障归因](./63-agent-trace-replay-failure-attribution.md)
4. [Q007 如何建立 Agent 评估体系？](./07-agent-evaluation.md)
5. [Q052 Harness Engineering 与 Runtime、Context 的关系](./52-harness-engineering.md)

需要掌握：

- 计划步骤必须可执行、可验收、可局部重试；
- 重规划应输出最小 Plan Patch，而非每次推翻重做；
- 审批冻结精确动作和参数，审批后必须重新校验；
- Trace 记录 Context Manifest、动作、证据、状态和验证；
- Replay 的目标是对比和定位最早致错点。

## 三、现场答题模板

### 第一步：确认目标和边界

先问清楚：

- 单 Agent 还是多 Agent；
- 是否调用有副作用的工具；
- 是否需要跨进程恢复；
- 是同步请求还是长任务；
- 如何定义任务完成；
- 延迟、成本、安全和并发约束是什么。

### 第二步：画核心状态机

```text
READY
  ↓
BUILD_CONTEXT
  ↓
MODEL_INFERENCE
  ├── FINAL ─────────────→ VERIFY_COMPLETION → SUCCEEDED / CONTINUE
  ├── TOOL_CALL ─────────→ VALIDATE → AUTHORIZE → EXECUTE
  ├── NEED_APPROVAL ─────→ WAITING_APPROVAL
  ├── WAIT_EXTERNAL ─────→ CHECKPOINT → RESUME
  └── INVALID_OUTPUT ────→ REPAIR / FAILED

EXECUTE
  → NORMALIZE_RESULT
  → APPEND_EVENT
  → CHECKPOINT
  → BUILD_CONTEXT
```

### 第三步：定义核心数据结构

至少说清楚：

- `RunState`：任务真实状态；
- `MessageEnvelope`：结构化消息；
- `ModelDecision`：final、tool calls、handoff 等决策；
- `ToolCall` / `ToolResult`：调用与结果；
- `Checkpoint`：可恢复快照；
- `EffectRecord`：副作用与幂等；
- `Trace` / `Span`：可观测链路。

### 第四步：写主循环

```python
while not state.is_terminal():
    stop = stop_policy.evaluate(state)
    if stop.should_stop:
        transition_to_terminal_or_pause(state, stop)
        break

    context = context_builder.build(state)
    decision = model.generate(context, candidate_tools(state))
    validate_decision(decision)

    events = runtime.execute_decision(state, decision)
    state = reducer.apply(state, events)
    checkpoint_store.save(state)
```

### 第五步：主动补生产异常

至少主动说明：

- 模型超时和输出非法；
- 参数错误、瞬时错误、业务错误和未知错误；
- 有副作用工具的审批与幂等；
- 工具成功但状态未落盘；
- 重复调用、周期振荡和无进展；
- Context 超限和摘要漂移；
- 服务重启和断点恢复；
- 重复回调和乱序事件；
- Token、时间、费用和并发预算；
- Trace、Replay 和故障归因。

## 四、判断是否真正理解

能回答以下问题，才算掌握：

- 为什么 Runtime State 不能只保存为对话消息？
- 为什么工具错误不应全部交给 LLM 决定是否重试？
- 为什么“模型输出 Final”不等于任务完成？
- 为什么 Checkpoint 与长期 Memory 不是一回事？
- 为什么并行 Tool Calling 不是简单 `asyncio.gather`？
- 工具成功但 Checkpoint 失败时，恢复系统应该怎么做？
- 为什么审批通过后还要重新校验外部资源版本？
- 为什么 Replay 不一定能字节级复现模型输出？
- 为什么一个 200 行 Agent Loop 仍可能无法进入生产？

## 五、推荐学习顺序

```text
Q009 Agent 与模型
→ Q002 ReAct / Agent Loop
→ Q053 最小 Runtime
→ Q055 State 与消息协议
→ Q054 Function Calling
→ Q057 停止与循环检测
→ Q056 Context Builder
→ Q058 Checkpoint 与恢复
→ Q059 异步长工具
→ Q060 并行调度
→ Q061 Planner / Replanner
→ Q062 人工审批
→ Q063 Trace / Replay
→ Q052 Harness Engineering
```

每学完一题，至少完成：

1. 口述 3～5 分钟；
2. 白板画状态机和数据流；
3. 不依赖框架写出核心数据结构与伪代码；
4. 用自己的 CI/CD Agent、Claude Code 平台或 OpenSandbox 场景重新回答。

## 六、下一阶段可继续增加的系统设计题

- 设计 Tool Registry 与语义 Tool Router；
- 设计多租户 Agent 的会话隔离和资源配额；
- 设计 Coding Agent Runtime；
- 设计 CI/CD 故障诊断 Agent；
- 设计支持 MCP 的企业 Tool Gateway；
- 设计 Multi-Agent Supervisor 与状态一致性机制。
