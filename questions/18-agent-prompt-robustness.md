# Agent Prompt 为什么会失效？如何提高鲁棒性？

- ID：Q018
- 难度：进阶
- 标签：Prompt Robustness、Instruction Conflict、Long Context、Tool Schema、Evaluation

## 核心结论

**Prompt 失效往往不是措辞不够“强”，而是指令冲突、上下文噪音、模型能力、工具契约和 Runtime 边界共同造成。** 鲁棒性来自减少 Prompt 承担的职责，把确定规则下沉到代码，并用评测验证不同输入和长任务下的行为。

## 一、主要失效原因

### 1. 指令冲突

System、Developer、Skill、历史消息和用户输入可能给出相互矛盾要求。长 Prompt 中同一规则重复但细节不同，会让模型无法判断优先级。

### 2. 规则过多且不可执行

把权限、重试、业务流程和所有异常情况都写入 Prompt，模型需要同时记忆大量条件，遵循率自然下降。

### 3. Context 噪音和位置效应

长历史、工具大结果、重复文档和旧计划稀释当前目标。所谓 Lost in the Middle 是风险之一，但不能靠“所有重要规则放最后”解决全部问题。

### 4. Tool Contract 不清

工具名称重叠、参数说明缺失、错误返回是自由文本，导致模型即使理解目标也无法稳定行动。

### 5. 任务缺少状态

Prompt 只包含聊天记录，没有明确当前计划、已确认事实、未完成事项和停止条件，模型每轮重新推断状态。

### 6. 模型边界

模型可能不支持所需 Context、Schema、语言、复杂推理或稳定 Tool Calling。Prompt 无法无限弥补能力差距。

### 7. 概率性与解码

温度和采样会影响稳定性，但把温度设为 0 也不保证完全确定；Provider、模型版本和并发执行也可能产生变化。

### 8. 对抗输入

用户、网页和文档可能包含 Prompt Injection。只靠在 Prompt 中追加“禁止泄露”无法建立安全边界。

## 二、Prompt 应承担什么

适合放：

- 角色和任务目标；
- 能力边界；
- 决策原则；
- 输出 Contract；
- 少量关键示例；
- 当前任务上下文。

不适合只靠 Prompt 保证：

- 权限；
- 幂等；
- 超时和重试；
- 业务金额计算；
- 数据隔离；
- Sandbox；
- 最终完成验证。

## 三、结构化 Prompt

推荐稳定区块：

```text
[Policy] 不随会话变化的规则
[Role & Goal]
[Capabilities] 当前候选工具
[Run State] 当前计划、事实、待办
[Evidence] 有来源的观察
[User Request]
[Output Contract]
```

不要把所有历史原样混在一起。不同区块标明来源和可信级别。

## 四、减少冲突

- 单一规则源；
- Policy 和 Skill 版本化；
- 禁止相同规则多处复制；
- 构建时检测重复与矛盾；
- Runtime 根据任务动态加载必要规则；
- 旧计划和过期工具结果不进入当前 Context。

## 五、把行为变成状态机

例如“最多追问两次后转人工”应由状态计数执行：

```python
if clarification_count >= 2:
    transition("HUMAN_HANDOFF")
```

而不是只在 Prompt 中提醒模型。Prompt 可以说明原因，Runtime 保证执行。

## 六、工具鲁棒性

- 工具描述互斥且明确；
- 参数 Schema；
- 候选工具控制；
- 错误结构化；
- 缺参时允许澄清；
- Tool Result 标注完整性和证据；
- Runtime 做权限和业务校验。

很多“Prompt 选错工具”其实是工具产品设计问题。

## 七、长上下文处理

- 当前目标和 State 固定高优先级；
- 历史分段和按需检索；
- 大结果外置；
- 摘要保留 source_event_ids；
- 给输出预留 Token；
- Context 超限时显式降级；
- 定期从原始事件重建摘要。

## 八、Prompt Injection

- 外部内容明确标为不可信数据；
- 不允许外部文本改变 Tool 权限；
- Secret 在进入模型前隔离；
- Tool Gateway 最小权限；
- 高风险动作审批；
- 输出和网络目的地控制。

核心不是让模型永远识别注入，而是注入成功时也无法突破系统边界。

## 九、评测方法

建立 Prompt Eval：

- 正常输入；
- 模糊输入；
- 指令冲突；
- 长上下文；
- 工具失败；
- 缺参数；
- Prompt Injection；
- 无答案；
- 多轮纠正；
- 模型升级。

指标：指令遵循、工具选择、格式、拒答、步骤、Token、延迟和安全违规。每次 Prompt 变更需要版本和回归。

## 十、修复顺序

```text
先确认任务和 Rubric
→ 定位是 Context、Tool、State 还是模型问题
→ 删除冲突和无效内容
→ 下沉确定性规则到 Runtime
→ 补结构和 Hard Case 示例
→ 必要时换模型或拆任务
→ 回归评测
```

不要无限追加新的“务必、严格、绝对”。

## 常见错误回答

> 指令写明确，重要规则放首尾，温度调低，加 Few-shot。

这些有帮助，但没有解决状态、工具、代码边界和评测。

## 面试口述版

> Agent Prompt 失效通常来自指令冲突、上下文噪音、工具描述、缺少显式 State 和模型能力，而不只是措辞问题。我会把 Prompt 分成 Policy、目标、当前能力、Run State、证据和输出 Contract，动态加载必要内容；权限、重试、追问次数、幂等和完成条件下沉到 Runtime。工具使用明确 Schema 和结构化错误，长历史通过状态、分段和 Artifact 引用管理。最后用冲突、长上下文、工具失败、注入和模型升级样本做回归，而不是靠不断追加更强硬的文字。

## 结合个人项目

巨长 CI/CD Prompt 应拆成 Router、Skills、Tool Contract 和 Case Retrieval；主 Prompt 只保留目标、决策原则和当前状态，具体故障知识按需加载。