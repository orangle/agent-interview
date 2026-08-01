# 长对话的短期记忆如何存储、压缩和淘汰？

- ID：Q038
- 难度：进阶 / 系统设计
- 标签：Short-term Memory、Conversation State、Summary、Compaction、Token Budget

## 核心结论

**长对话管理不是把最旧消息删掉，而是把会话拆成“可恢复的完整记录、结构化任务状态、可检索历史和当前模型上下文”。** 模型每轮只看到完成当前决策所需的信息，原始历史仍可回溯。

## 一、四份不同的数据

```text
1. Event Log：完整不可变消息与工具事件
2. Run State：目标、计划、槽位、事实、待办
3. Summary / Memory Blocks：压缩后的阶段信息
4. Model Context：本轮选择后的有限输入
```

只维护 `List[Message]` 会导致：

- 上下文无限增长；
- 服务重启难恢复真实任务状态；
- 摘要后无法审计；
- 旧工具结果重复占用 Token；
- 关键事实和闲聊权重相同。

## 二、存储层

### L1 进程内状态

当前正在执行 Run 的热状态，速度快但不可作为唯一来源。

### L2 Redis / 数据库

保存 Session 状态、Checkpoint、最近消息和锁，支持多实例和故障恢复。

### L3 对象存储 / 事件库

保存完整对话、工具大结果和审计 Trace，按需读取，不直接全部进入 Context。

这不是 GPU/CPU/磁盘的 KV Cache 分层。应用会话存储与模型推理 KV Cache 是不同层次。

## 三、压缩策略

### 1. 滑动窗口

保留最近若干消息。简单，但容易丢失早期目标、约束和承诺，只适合作为最外层兜底。

### 2. 滚动摘要

阶段性把旧消息压缩为摘要，再保留最近消息。

摘要应结构化：

```json
{
  "goal": "...",
  "confirmed_facts": [],
  "decisions": [],
  "user_constraints": [],
  "open_questions": [],
  "failed_attempts": [],
  "evidence_refs": []
}
```

比一段自由文本更容易更新和验证。

### 3. 实体与槽位抽取

把服务名、环境、时间范围、用户选择等关键字段放入显式 State，避免每轮从聊天历史重新推断。

### 4. 事件分段

按任务阶段、主题切换或子任务边界形成 Segment。当前 Context 加载当前 Segment，历史 Segment 按需检索。

### 5. 大结果外置

工具输出保存在 Artifact Store，消息中只保留摘要、统计和引用。

## 四、压缩触发条件

不应固定“每 N 轮”作为唯一条件，可综合：

- Token 使用达到预算比例；
- 子任务完成；
- 主题明显切换；
- 工具结果过大；
- Context Build 预计超限；
- Run 即将 Checkpoint 或暂停。

在任务边界压缩通常比任意轮数更不容易丢失语义。

## 五、哪些信息不能被普通摘要覆盖

- System / Policy；
- 用户明确约束；
- 高风险审批状态；
- 未完成任务；
- 关键实体和版本；
- 原始证据引用；
- 工具副作用结果；
- 幂等键和外部任务 ID。

这些应进入结构化 State 或 Pin 区，而不是寄希望摘要模型记住。

## 六、淘汰优先级

优先移除：

1. 已被结构化状态吸收的重复表达；
2. 已完成且无需后续依赖的中间过程；
3. 可通过引用重新加载的大工具结果；
4. 与当前任务无关的闲聊；
5. 低价值重复观察。

最后才考虑压缩关键历史。输出 Token 预留和安全规则永远不能被挤占。

## 七、摘要漂移

滚动摘要多次“摘要上一份摘要”会累积错误。缓解：

- 定期从原始事件重建；
- 摘要输出结构化字段；
- 关键字段与 State 做一致性校验；
- 保存 source_event_ids；
- 用户纠正时更新事实并使旧摘要失效；
- 高风险决策回到原始证据。

## 八、Context Builder

```python
def build_context(run, budget):
    parts = [policy, run.goal, run.structured_state]
    parts += select_recent_messages(run)
    parts += retrieve_relevant_segments(run)
    parts += select_evidence(run)
    return fit_to_budget(parts, reserve_output=True)
```

不同内容按优先级和独立预算选择，不能只按时间倒序塞满。

## 九、评估

- 长会话任务完成率；
- 关键约束保留率；
- 摘要事实错误率；
- 用户纠正后旧事实残留率；
- 平均输入 Token；
- 压缩调用成本；
- 从原始事件恢复的成功率；
- 不同对话长度下的质量曲线。

## 常见错误回答

> 保留最近 20 轮，旧内容用 LLM 摘要。

这是可用起点，不是完整设计。没有结构化状态、证据引用、任务边界和摘要漂移控制。

> LRU 淘汰记忆。

对话有顺序和依赖，普通缓存 LRU 不知道哪条信息是目标、权限或未完成任务。

## 面试口述版

> 我会分开保存完整 Event Log、结构化 Run State、阶段摘要和本轮 Model Context。短期热状态可在内存或 Redis，完整消息和大工具结果持久化，Context Builder 按目标、约束、当前计划、近期消息和相关历史分配 Token。压缩优先在子任务结束或预算超限时触发，摘要使用结构化字段并保留 source_event_ids。用户约束、审批状态、外部任务 ID 和证据引用进入显式 State，不能只靠摘要。这样服务可恢复、历史可审计，也能控制长对话 Token。

## 延伸阅读

- [Q056 Context Builder 与 Token Budget](./56-context-builder-and-token-budget.md)

## 结合个人项目

Claude Code 长会话中，代码文件和日志应外置；当前任务目标、已修改文件、未完成测试和用户限制进入结构化 State；已完成探索压缩为带文件引用的阶段摘要。