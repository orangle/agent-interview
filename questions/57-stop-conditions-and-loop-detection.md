# 手写停止条件与重复动作检测

- ID：Q057
- 难度：进阶 / 手撕设计
- 标签：Agent Loop、Stop Conditions、Loop Detection、Budget、Completion Verification

## 同义问法

- Agent 怎么知道什么时候停？
- 如何避免 Agent 死循环？
- 模型说“完成了”就能结束吗？
- 如何检测重复工具调用和无效探索？

## 一句话结论

**停止不是一个条件，而是三类机制共同决定：模型终止信号、代码层硬预算、任务完成验证。死循环检测则要同时观察动作重复、状态无进展和结果无新信息。**

## 一、为什么不能只依赖模型输出 Final

模型可能：

- 任务没完成但误判完成；
- 工具失败后编造成功；
- 反复调用同一工具；
- 在两个方案之间来回切换；
- 不断“再检查一下”；
- 因上下文污染忘记已经执行过什么。

因此 Runtime 必须拥有最终终止权。

## 二、终止条件分类

### 1. 成功终止

- 模型输出 final；
- 所有必需步骤完成；
- 验收器验证通过；
- 产物存在且满足 Schema；
- 无待处理审批、工具调用和未解决关键问题。

### 2. 可恢复暂停

- 等待人工审批；
- 等待异步工具结果；
- 等待用户补充信息；
- 主动暂停并保存 Checkpoint。

### 3. 失败终止

- 超过最大轮次；
- 超过 Token、时间或费用预算；
- 连续重复动作；
- 连续无进展；
- 不可恢复工具错误；
- 安全规则触发；
- 状态损坏或恢复冲突。

## 三、停止策略结构

```python
from dataclasses import dataclass
from typing import Literal

@dataclass
class StopDecision:
    should_stop: bool
    status: Literal["completed", "paused", "failed", "continue"]
    reason: str
    evidence: dict

class StopPolicy:
    def evaluate(self, state) -> StopDecision:
        if state.cancel_requested:
            return StopDecision(True, "failed", "cancelled", {})

        if state.waiting_approval:
            return StopDecision(True, "paused", "waiting_approval", {})

        if state.deadline_exceeded():
            return StopDecision(True, "failed", "deadline_exceeded", {})

        if state.budget_exceeded():
            return StopDecision(True, "failed", "budget_exceeded", {})

        loop = detect_loop(state)
        if loop.detected:
            return StopDecision(True, "failed", "loop_detected", loop.details)

        if state.model_proposed_final:
            verification = verify_completion(state)
            if verification.passed:
                return StopDecision(True, "completed", "verified", verification.evidence)
            state.add_feedback(verification.failures)

        return StopDecision(False, "continue", "", {})
```

## 四、动作指纹

对每次工具调用生成规范化指纹：

```python
import hashlib
import json

def action_fingerprint(tool_name, arguments):
    normalized = json.dumps(
        arguments,
        sort_keys=True,
        ensure_ascii=False,
        separators=(",", ":"),
    )
    raw = f"{tool_name}:{normalized}"
    return hashlib.sha256(raw.encode()).hexdigest()
```

注意：完全相同的参数只是最基础情况。还要做语义规范化：

- 时间范围统一；
- 默认参数补齐；
- 路径归一化；
- 无序列表排序；
- 忽略 request_id、时间戳等非业务字段。

## 五、重复不等于死循环

同一工具调用两次可能合理：

- 第一次失败，第二次重试；
- 状态可能随时间变化；
- 执行写操作后再次读取验证；
- 查询不同分页但参数被抽象后看似相同。

因此检测应结合：

```text
动作是否重复
+
结果是否重复
+
状态是否无进展
+
是否仍在允许重试窗口
```

## 六、进展度量

定义任务进展信号：

- 完成步骤数量增加；
- 未解决问题减少；
- 新事实数量增加；
- 验收失败项减少；
- 新产物生成；
- 工具错误从未知变成已定位；
- 置信度或证据覆盖提高。

```python
@dataclass
class ProgressSnapshot:
    completed_steps: int
    unresolved_count: int
    verified_facts: int
    artifact_count: int
    validation_failures: int


def progress_delta(before, after):
    return (
        (after.completed_steps - before.completed_steps)
        + (before.unresolved_count - after.unresolved_count)
        + (after.verified_facts - before.verified_facts)
        + (after.artifact_count - before.artifact_count)
        + (before.validation_failures - after.validation_failures)
    )
```

连续 N 轮 `progress_delta <= 0`，可认为陷入无进展状态。

## 七、循环类型

### 1. 精确重复

```text
search_logs(service=A)
search_logs(service=A)
search_logs(service=A)
```

### 2. 参数抖动

```text
limit=100 → 101 → 100 → 101
```

### 3. 双状态振荡

```text
方案 A → 方案 B → 方案 A → 方案 B
```

### 4. 工具间循环

```text
查日志 → 查代码 → 查日志 → 查代码
```

### 5. 语言重复但动作不同

模型不断说“需要更多信息”，但每次查询都没有增加证据。

## 八、检测算法

```python
def detect_loop(state):
    recent = state.steps[-8:]

    if exact_action_repeated(recent, threshold=3):
        return Loop(True, "exact_action_repeat")

    if action_result_pair_repeated(recent, threshold=2):
        return Loop(True, "same_action_same_result")

    if detect_periodic_pattern(recent, max_period=3, repeats=3):
        return Loop(True, "periodic_oscillation")

    if no_progress_for_turns(state.progress_history, turns=4):
        return Loop(True, "no_progress")

    return Loop(False, None)
```

周期检测可以对最近动作指纹序列检查长度 1～3 的重复子序列。

## 九、触发循环后不一定直接失败

可按层次处理：

```text
第一次检测
→ 给模型结构化反馈：哪些动作重复、为什么无进展

第二次检测
→ 强制重新规划，禁止最近动作

第三次检测
→ 降级模型、转人工或失败终止
```

反馈示例：

```json
{
  "runtime_feedback": "loop_detected",
  "pattern": ["search_logs", "search_code"],
  "repeats": 3,
  "new_information": false,
  "required_action": "replan_or_stop",
  "forbidden_fingerprints": ["...", "..."]
}
```

## 十、完成验证

不能问模型“你完成了吗”，而要定义验收器：

```python
class CompletionVerifier:
    def verify(self, state):
        checks = [
            required_artifacts_exist(state),
            output_schema_valid(state),
            mandatory_steps_succeeded(state),
            evidence_coverage_sufficient(state),
            no_pending_side_effects(state),
            domain_tests_passed(state),
        ]
        return VerificationResult.from_checks(checks)
```

例如 Coding Agent：

- Diff 已生成；
- 文件能解析；
- 指定测试通过；
- 没有修改禁止目录；
- 变更范围符合任务；
- 最终说明引用真实测试结果。

## 十一、预算应多维控制

```text
max_turns
max_total_tokens
max_wall_clock_time
max_tool_calls
max_cost
max_consecutive_failures
max_same_tool_calls
```

只限制轮次不够：某一轮可能并行调用几十个工具，或一次塞入大量 Token。

## 十二、面试口述版

> 我会把停止条件分为成功、暂停和失败三类。模型输出 final 只是成功候选，Runtime 还要通过产物、步骤、证据和领域测试做完成验证。失败侧设置轮次、Token、时间、费用、工具次数和连续错误等硬预算。死循环检测不能只看同一工具调用几次，而要结合规范化动作指纹、工具结果、状态进展和允许重试次数；同时检测精确重复、参数抖动、周期振荡和连续无进展。发现循环后先反馈并强制重规划，再失败或转人工。最终终止权必须在 Runtime，不在模型。