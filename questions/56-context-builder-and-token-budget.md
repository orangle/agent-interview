# 手写 Context Builder 与 Token Budget

- ID：Q056
- 难度：进阶 / 手撕设计
- 标签：Context Engineering、Token Budget、Memory、Tool Result、Compression

## 同义问法

- Agent 的上下文到底怎么拼？
- Context Window 快满时保留什么、删除什么？
- 如何设计 Context Builder，而不是把所有消息直接传给模型？
- 长任务如何避免上下文爆炸和摘要失真？

## 一句话结论

**Context Builder 是一个受预算约束的信息选择器，不是字符串拼接器。它需要从任务状态、近期事件、工具证据、长期记忆和规则中选择“当前决策最需要的信息”，并保留可回溯的原始证据引用。**

## 一、Context 和 State 不相等

```text
State：系统完整事实
Context：当前这一次模型调用可见的信息
```

State 可以很大，可以持久化在数据库、对象存储或事件日志中；Context 必须在模型窗口和成本预算内。

错误做法：

```python
messages.append(everything)
response = llm(messages)
```

问题：

- 工具结果不断累积；
- 早期错误信息长期污染后续决策；
- 关键规则被大量内容稀释；
- 成本和延迟线性增长；
- 摘要后无法定位原始证据；
- 模型“看见了”不等于“有效利用了”。

## 二、先定义预算，而不是超限后再截断

```python
from dataclasses import dataclass

@dataclass
class TokenBudget:
    model_window: int
    reserved_output: int
    reserved_tool_schema: int
    reserved_system: int
    safety_margin: int

    @property
    def available_context(self) -> int:
        return (
            self.model_window
            - self.reserved_output
            - self.reserved_tool_schema
            - self.reserved_system
            - self.safety_margin
        )
```

例如模型窗口为 `128K`，不代表能把 `128K` 全用于历史消息。还要预留：

- 模型输出；
- Tool Schema；
- 系统规则；
- 重试或结构化修复；
- Token 估算误差。

## 三、Context 分层

```text
P0：不可丢
- 系统安全规则
- 当前用户目标
- 当前步骤与完成条件
- 未解决约束

P1：高价值
- 最近关键动作与结果
- 当前计划
- 与当前步骤直接相关的证据
- 用户刚刚纠正的信息

P2：按需检索
- 长期记忆
- 历史相似任务
- 项目规范、Skill、文档

P3：可压缩或外置
- 原始长日志
- 已完成步骤的细节
- 重复工具输出
- 低相关历史对话
```

不是简单“越新越重要”。例如用户最早给出的安全限制，可能比最近十轮闲聊更重要。

## 四、Context Item 数据结构

```python
from dataclasses import dataclass
from typing import Literal

@dataclass
class ContextItem:
    item_id: str
    kind: Literal[
        "system", "goal", "constraint", "plan", "fact",
        "tool_observation", "memory", "conversation", "summary"
    ]
    content: str
    token_cost: int
    priority: int
    relevance: float
    freshness: float
    trust: float
    source_ref: str | None
    compressible: bool
    required: bool
```

可以定义一个粗略价值分数：

```python
value = (
    priority_weight * priority
    + relevance_weight * relevance
    + freshness_weight * freshness
    + trust_weight * trust
) / max(token_cost, 1)
```

这不是为了追求数学精确，而是强迫系统显式考虑“单位 Token 的信息价值”。

## 五、Context Builder 伪代码

```python
def build_context(state, event_store, memory_store, tools, budget):
    items = []

    items += build_required_system_items(state)
    items += build_current_goal_items(state)
    items += build_current_step_items(state)
    items += build_hard_constraints(state)

    recent_events = event_store.query_recent(state.run_id, limit=50)
    items += convert_events_to_context(recent_events)

    query = build_retrieval_query(state)
    memories = memory_store.search(
        tenant_id=state.tenant_id,
        user_id=state.user_id,
        query=query,
        top_k=8,
    )
    items += filter_memory(memories, state)

    items = deduplicate(items)
    items = resolve_conflicts(items)
    items = compress_large_items(items)

    selected = select_under_budget(
        items,
        max_tokens=budget.available_context,
    )

    return order_for_model(selected)
```

## 六、选择算法

最简单可以使用：

1. 先放所有 `required=True`；
2. 按类别保底，例如规则、目标、计划、证据各至少一部分；
3. 剩余项按价值密度排序；
4. 超大项先压缩，不直接截断；
5. 最后校验 Token；
6. 超限时从最低价值项开始删除。

```python
def select_under_budget(items, max_tokens):
    selected = []
    used = 0

    for item in [x for x in items if x.required]:
        selected.append(item)
        used += item.token_cost

    candidates = sorted(
        [x for x in items if not x.required],
        key=context_value_density,
        reverse=True,
    )

    for item in candidates:
        if used + item.token_cost <= max_tokens:
            selected.append(item)
            used += item.token_cost

    return selected
```

真实系统还需要按类别配额，避免某一种内容占满整个窗口。

## 七、工具结果如何压缩

工具应该返回三层：

```text
Level 1：结构化结论
Level 2：可读摘要
Level 3：原始证据引用
```

例如日志工具：

```json
{
  "summary": "启动失败的第一个稳定异常是 ClassNotFoundException",
  "facts": {
    "class": "com.demo.OrderService",
    "first_seen": "2026-08-01T10:21:03Z",
    "repeated": 17
  },
  "evidence_refs": [
    "log://run-88/startup.log#L842-L901"
  ],
  "truncated": true
}
```

模型先看到摘要，需要核对时再调用证据读取工具。

## 八、摘要不是无损压缩

滚动摘要的风险：

- 摘要模型遗漏约束；
- 早期误解被固化；
- 多轮摘要产生“摘要漂移”；
- 细节被删除后无法恢复；
- 把假设写成事实。

因此摘要必须：

- 区分事实、假设、决定和未解决问题；
- 保存源事件范围；
- 有版本号；
- 原始内容不删除，只从在线 Context 外置；
- 对关键字段使用结构化抽取，而不是只写自然语言摘要。

示例：

```json
{
  "facts": ["生产环境使用 JDK 17"],
  "decisions": ["先排除配置缺失，再检查依赖冲突"],
  "hypotheses": ["可能存在旧包残留"],
  "open_questions": ["beta 与 prod 的配置是否一致"],
  "source_event_range": [101, 166]
}
```

## 九、冲突处理

如果长期记忆说“用户偏好 Java”，当前会话说“这次用 Go”，不能简单拼接后让模型自己判断。

建议优先级：

```text
当前明确指令
> 当前任务约束
> 已确认最新事实
> 用户长期偏好
> 历史推断
```

冲突应在进入模型前显式标记：

```json
{
  "conflict": true,
  "old": "默认使用 Java",
  "new": "本次任务使用 Go",
  "resolution": "current_task_override"
}
```

## 十、何时触发压缩

不要只在“已经超限”时处理。可以设置软阈值：

- 预计输入超过窗口 70%：压缩已完成步骤；
- 工具结果超过单项上限：立即摘要并外置；
- 连续多轮没有引用某段内容：降权；
- 计划阶段切换：生成阶段性摘要；
- 模型输出质量开始下降：检查上下文噪声，而不只换更大窗口。

## 十一、Context Builder 的可观测性

每次调用记录：

- 候选项数量；
- 选中/丢弃项；
- 每类 Token 占比；
- 压缩前后 Token；
- 每项来源；
- 检索分数和最终选择理由；
- 是否发生冲突和覆盖。

否则出现 badcase 时，只知道模型答错，不知道模型当时看到了什么。

## 十二、面试口述版

> 我不会把 Agent 的所有 messages 直接传给模型，而会设计一个 Context Builder。它先根据模型窗口预留输出、工具 Schema、系统规则和安全余量，得到本轮可用预算；然后从当前目标、步骤、约束、近期事件、工具证据和长期记忆中构造 Context Item。不可丢的信息先放入，其余按相关性、可信度、新鲜度和单位 Token 价值选择，并设置类别配额。大工具结果返回结构化结论、摘要和原始证据引用，原始内容外置。摘要必须区分事实、假设、决定和未解决问题，并保留来源，避免摘要漂移。最后记录每轮选择了什么、丢弃了什么，才能在 badcase 中还原模型当时真正看见的上下文。