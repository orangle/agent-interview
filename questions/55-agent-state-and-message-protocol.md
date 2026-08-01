# 手写 Agent State 与消息协议

- ID：Q055
- 难度：进阶 / 手撕设计
- 标签：Agent State、Message Protocol、Event Sourcing、Checkpoint、Reducer

## 同义问法

- Agent 的状态到底存什么？
- Messages 和 State 有什么区别？
- 如何设计可恢复、可审计的 Agent 数据结构？
- 多 Agent 如何共享状态而不互相污染？

## 一句话结论

**Messages 是给模型看的上下文载体，State 是 Runtime 的真实执行状态，Event 是状态变化的事实记录。生产系统不要把三者混成一个不断增长的消息数组。**

## 一、为什么只存 messages 不够

很多 Demo 只有：

```python
messages = [
    {"role": "user", "content": "..."},
    {"role": "assistant", "tool_calls": [...]},
    {"role": "tool", "content": "..."},
]
```

它能跑，但有几个根本问题：

- 无法快速知道当前处于规划、执行、等待审批还是失败状态；
- 业务字段只能塞进自然语言，难以校验；
- 原始日志、摘要、计划、预算和审批信息混在一起；
- 恢复执行时不知道哪些副作用已经发生；
- 多 Agent 共享完整对话，容易上下文污染；
- 压缩历史时可能误删恢复所需的事实。

## 二、建议拆成四层

```text
Run Metadata
  运行身份、租户、用户、版本、时间

Structured State
  目标、计划、步骤、预算、审批、工具结果索引

Event Log
  每次状态变化的不可变事实

Model Context
  从 State + Events + Memory 中动态投影出的有限消息
```

## 三、核心状态结构

```python
from dataclasses import dataclass, field
from typing import Any, Literal

RunStatus = Literal[
    "created", "running", "waiting_tool", "waiting_approval",
    "paused", "completed", "failed", "cancelled"
]

StepStatus = Literal[
    "pending", "running", "succeeded", "failed", "skipped"
]

@dataclass
class Budget:
    max_turns: int
    max_tokens: int
    deadline_ms: int
    max_tool_calls: int
    used_turns: int = 0
    used_tokens: int = 0
    used_tool_calls: int = 0

@dataclass
class PlanStep:
    step_id: str
    description: str
    dependencies: list[str]
    status: StepStatus
    output_refs: list[str] = field(default_factory=list)

@dataclass
class Approval:
    approval_id: str
    tool_call_id: str
    status: Literal["pending", "approved", "rejected", "expired"]
    requested_at: int
    decided_at: int | None = None
    decided_by: str | None = None

@dataclass
class RunState:
    run_id: str
    tenant_id: str
    user_id: str
    task: str
    status: RunStatus
    version: int
    current_agent: str
    current_step_id: str | None
    plan: list[PlanStep]
    facts: dict[str, Any]
    unresolved_questions: list[str]
    approvals: list[Approval]
    artifact_refs: list[str]
    budget: Budget
    last_error: dict[str, Any] | None
```

## 四、消息协议不要只用 role + content

建议定义统一 Envelope：

```python
@dataclass
class MessageEnvelope:
    message_id: str
    run_id: str
    sender: str
    receiver: str
    type: Literal[
        "user_input", "model_decision", "tool_call", "tool_result",
        "handoff", "approval_request", "approval_result",
        "state_patch", "final_output", "error"
    ]
    payload: dict[str, Any]
    created_at: int
    correlation_id: str | None
    causation_id: str | None
    sequence: int
```

三个 ID 的作用：

- `message_id`：当前消息唯一标识；
- `correlation_id`：把同一业务链路串起来，例如一次工具调用及其结果；
- `causation_id`：说明当前事件由哪个事件触发，便于故障归因。

## 五、状态更新采用 Patch，而不是任意覆盖

多个节点并发写 State 时，最危险的是“最后写入覆盖前面结果”。

可以让节点只返回 Patch：

```python
@dataclass
class StatePatch:
    expected_version: int
    set_fields: dict[str, Any]
    append_events: list[dict[str, Any]]
    add_artifact_refs: list[str]
```

写入时执行乐观锁：

```python
def apply_patch(state, patch):
    if state.version != patch.expected_version:
        raise StateConflict()

    validate_transition(state, patch)
    new_state = reduce_patch(state, patch)
    new_state.version += 1
    return new_state
```

## 六、状态机约束

状态不能随意跳转：

```text
created → running
running → waiting_tool | waiting_approval | paused | completed | failed
waiting_tool → running | failed
waiting_approval → running | cancelled | failed
paused → running | cancelled
completed / failed / cancelled → 终态
```

例如：

- `completed` 后不能再执行工具；
- 未审批的高危工具不能从 `waiting_approval` 直接变成 `running`；
- 恢复任务必须校验 Checkpoint 版本和工具执行记录。

## 七、Event Sourcing 的价值

事件示例：

```json
{
  "event_id": "evt-102",
  "run_id": "run-1",
  "type": "tool_execution_succeeded",
  "payload": {
    "tool_call_id": "call-7",
    "artifact_ref": "obs://run-1/call-7/result.json"
  },
  "causation_id": "evt-101",
  "sequence": 102
}
```

事件日志可以用于：

- 重建某一时刻状态；
- Replay 故障路径；
- 判断工具是否已执行；
- 对比模型或 Prompt 版本；
- 生成模型上下文之外的审计证据。

但不必所有系统都完整采用 Event Sourcing。至少要保存关键状态迁移和副作用事件。

## 八、Context 是 State 的投影

```python
def build_model_context(state, events, memory, token_budget):
    return [
        system_rules(state.current_agent),
        task_summary(state.task),
        current_plan_view(state.plan),
        known_facts(state.facts),
        unresolved_questions(state.unresolved_questions),
        recent_relevant_events(events),
        retrieve_relevant_memory(memory, state.task),
    ]
```

不是所有 State 都发给模型：

- 租户 ID、内部版本、幂等键通常不需要；
- 密钥和权限数据绝不能进入模型；
- 原始大结果只传摘要和引用；
- 审批状态可以结构化表达，但不暴露内部策略。

## 九、多 Agent 状态隔离

建议：

```text
Global Run State
  目标、共享事实、全局计划、最终产物

Agent Local State
  本 Agent 的局部假设、草稿、临时工具结果

Message Bus
  只传递结构化结论和证据引用
```

不要让所有 Agent 直接修改同一大字典。应通过：

- 明确字段所有权；
- Reducer 合并；
- 乐观锁或单写者模型；
- Append-only 消息；
- 冲突检测和仲裁节点。

## 十、面试口述版

> 我会把 Agent 的数据分成 Runtime State、事件日志和 Model Context 三层。State 保存任务状态、计划、预算、审批和产物引用，是系统真相；Event 记录每次状态变化和副作用，便于恢复、Replay 和审计；Context 则是从 State、事件和长期记忆中按 Token 预算动态投影出来的模型输入。消息协议不能只有 role 和 content，至少要有消息类型、call_id、correlation_id、causation_id 和 sequence。状态更新采用受控 Patch 和版本号，防止并发覆盖；多 Agent 则区分全局共享状态和局部状态，通过结构化消息及 Reducer 合并，而不是共享整段对话。