# Few-shot 与 Chain-of-Thought 在 Agent 中应该如何使用？

- ID：Q017
- 难度：基础 / 进阶
- 标签：Few-shot、Reasoning、Examples、Tool Calling、Prompt

## 核心结论

**Few-shot 用于展示任务边界和期望行为；推理提示用于帮助模型处理需要分解的问题。二者都不是越多越好。** Agent 的工具、状态和验证应由 Runtime 明确提供，不能依赖模型输出冗长“思维过程”来保证正确。

## 一、Few-shot 的主要用途

### 1. 边界示例

展示什么时候调用工具、什么时候直接回答、什么时候澄清或拒绝。

### 2. 结构示例

展示复杂 JSON、报告、引用和错误处理的正确格式。

### 3. 难例示例

选择容易混淆的 Hard Cases，而不是重复简单例子：

- 同名工具如何区分；
- 参数缺失时先问用户；
- 工具失败时不伪造结果；
- 证据不足时拒答。

### 4. 领域表达

展示组织术语、根因分析结构和 Review 标准。

## 二、示例选择

高质量 Few-shot 应：

- 与当前 Query 相似但不泄漏答案；
- 覆盖决策边界；
- 输出经过验证；
- 简短且信息密度高；
- 标明输入、动作、观察和最终结果；
- 随 Prompt / Tool 版本更新。

不是固定“2～5 个最好”。数量取决于模型、任务、Context Budget 和示例复杂度。

## 三、动态 Few-shot

从案例库检索相关示例：

```text
Current Task
→ Intent / Risk Filter
→ Example Retrieval
→ Diversity / Quality Filter
→ Token Budget
→ Prompt
```

必须避免：

- 检索到错误或过期案例；
- 示例中含其他用户数据；
- 多个相似例子挤占 Context；
- 示例让模型机械模仿不适用步骤。

动态示例库需要版本、来源和评测，不是把所有高分回答放向量库。

## 四、Chain-of-Thought 应怎么理解

面试中不要把 CoT 简化为“加一句一步步思考”。对于 Agent，更重要的是让系统得到**可执行的中间结构**：

- 计划；
- 子目标；
- 缺失信息；
- Tool Call；
- 证据；
- 验证结果；
- 下一步。

Runtime 不需要依赖或暴露模型私有推理文本。可以要求模型给出简洁的计划、结论依据和可验证状态，而不是无限输出长思维过程。

## 五、什么时候需要显式分解

适合：

- 多跳检索；
- 复杂约束；
- 工具依赖；
- 数学、代码和系统设计；
- 需要先规划再执行。

不适合：

- 简单查余额；
- 明确单工具查询；
- 低延迟高频请求；
- 确定性规则可直接完成。

简单任务强制规划会增加延迟、Token 和错误机会。

## 六、Agent 中更可靠的替代

相比要求模型长篇思考，更可靠的是：

- Structured Plan；
- Tool Schema；
- State Machine；
- Planner–Executor；
- External Verifier；
- 测试和规则；
- Evidence Binding；
- 最大步骤和预算。

## 七、Few-shot 与 Tool Calling

示例可以展示：

```text
User：查看 order-api 最近一次 beta 发布日志
Assistant Tool Call：get_latest_release(service="order-api", env="beta")
Tool Result：release_id=...
Assistant Tool Call：get_logs(release_id=...)
```

但示例不能替代参数 Schema、权限和错误校验。模型模仿正确 JSON 也可能生成不存在的服务或越权环境。

## 八、评估

做消融：

- 无示例；
- 固定示例；
- 动态示例；
- 显式计划；
- 直接 Tool Call。

指标：任务完成、工具准确、步骤、Token、延迟、格式错误和过度规划率。

## 常见错误回答

> Few-shot 放 3 个工具调用例子，CoT 用于复杂推理。

需要继续说明示例选择、动态检索、版本、边界和为什么不依赖私有思维过程。

## 面试口述版

> Few-shot 的价值是展示行为边界、结构和 Hard Case，而不是堆数量。我会优先放容易混淆的工具选择、缺参数澄清、失败和拒答例子，必要时从经过审核的案例库动态检索，并受 Token 和隐私约束。对于 CoT，我更关注可执行中间结构，例如计划、子目标、工具、证据和验证，不要求系统依赖或展示冗长思维文本。简单单工具任务直接执行，复杂多跳任务才使用结构化分解，并通过状态机、工具结果和外部验证保证可靠性。

## 结合个人项目

故障 Agent 的 Few-shot 应选“日志里有多个异常但根因是最早配置缺失”这样的难例；简单 Job 状态查询不需要 Planner。