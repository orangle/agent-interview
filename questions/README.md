# 题库索引与整理规范

## 当前可学习题目

### 第一组：Agent 的本质与控制闭环

1. [Agent 和 Workflow 的本质区别是什么？](./01-agent-vs-workflow.md)
2. [ReAct 与 Agent Loop 为什么有效，又有什么局限？](./02-react-and-agent-loop.md)
3. [Agent 如何判断信息已经足够，并避免死循环？](./03-agent-stop-and-loop-control.md)
4. [Agent 与大模型的本质区别是什么？一个 Agent 至少需要哪些组件？](./09-agent-vs-model-and-components.md)
5. [Agent 有哪些常见设计范式？复杂任务如何拆分与动态重规划？](./10-agent-patterns-task-decomposition-replanning.md)
6. [Reflection、Reflexion 和 Evaluator-Optimizer 有什么区别？](./11-reflection-reflexion-evaluator-optimizer.md)

### 第二组：工程实现与生产边界

7. [如何让 Tool Calling 在生产环境中可靠？](./04-reliable-tool-calling.md)
8. [Agent 的 Context Engineering 应该怎么做？](./05-context-engineering.md)
9. [什么时候用单 Agent，什么时候用 Multi-Agent？](./06-single-vs-multi-agent.md)
10. [如何建立 Agent 评估体系？](./07-agent-evaluation.md)
11. [生产环境什么时候使用 Agent 框架，什么时候自己实现核心 Runtime？](./13-framework-vs-custom-runtime.md)
12. [Agent 的 System Prompt 应该怎么写？与普通 Chat Prompt 有什么不同？](./16-agent-system-prompt-design.md)
13. [Skill、Tool、MCP Server 和 Workflow 的边界是什么？](./19-skill-tool-mcp-workflow-boundaries.md)
14. [什么是 Harness Engineering？它与 Prompt、Context、Agent Runtime 有什么关系？](./52-harness-engineering.md)

### 第三组：RAG

15. [如何设计一个生产可用的 RAG 系统？](./08-production-rag.md)

## 待回答题目

用户提供的 115 个原始问法已合并为 52 道主问题：

- [Canonical Question Backlog](./BACKLOG.md)
- [原始题库导入记录](../intake/2026-08-01-agent-developer-question-bank.md)

## 推荐学习方式

每道题分三遍：

1. **先口述**：不看答案，用 2～5 分钟回答；
2. **再对照**：重点看机制、边界、失败模式和项目表达；
3. **最后重答**：只保留自己的语言，不机械背诵全文。

学习后的疑问、不同意见和实际案例，直接反馈到对应题目。后续修改优先补充：

- 为什么；
- 什么情况下不成立；
- 如何用真实系统验证；
- 如何结合个人项目回答。

## 去重规则

新增问题前，先判断它是否只是已有问题的另一种问法。

例如以下问法归入同一道题：

- Agent 和 Workflow 有什么区别？
- 什么时候应该用 Agent，而不是固定工作流？
- LangChain Chain 和自主 Agent 如何选择？
- 为什么不把所有流程都交给 Agent？

只有当新问题需要一套明显不同的推理框架时，才单独建题。

## 来源记录规则

每道题的“来源”至少说明：

- 公司或岗位（来源可确认时）；
- 面试轮次或日期（来源包含时）；
- 原始问法；
- 原始链接。

如果来源只是题库文章而非第一手面经，需要明确标记为“二手题目整理”，不能伪装成某家公司真实原题。

技术答案的证据优先级：

1. 协议规范、论文、官方文档；
2. 可复现的开源实现和实验；
3. 有上下文的工程案例；
4. 社区文章和个人经验。

## 回答质量标准

### 宽泛题

宽泛题需要回答五层：

1. **定义层**：概念是什么；
2. **机制层**：为什么能够工作；
3. **工程层**：系统如何实现；
4. **边界层**：什么时候不适用、哪里会失败；
5. **经验层**：如何结合真实项目说明判断与取舍。

### 精确题

精确题重点回答：

- 直接原因；
- 可执行方案；
- 方案顺序；
- 异常与边界。

避免为了“有深度”而偏离题目。

## 自检清单

提交前检查：

- [ ] 是否解释了“为什么”，而不是只列名词？
- [ ] 是否区分 Demo 方案和生产方案？
- [ ] 是否写出了方案代价和失败模式？
- [ ] 是否存在一句话就能反驳的绝对结论？
- [ ] 是否给出了可直接口述的回答？
- [ ] 来源是否真实、可追溯？
- [ ] 是否与已有题目重复？
- [ ] 动态变化的产品、模型和协议是否标注了回答日期？

## 难度标记

- `基础`：理解 Agent 必须掌握；
- `进阶`：需要具备工程实践和方案取舍能力；
- `系统设计`：需要从目标、约束、架构、可靠性和评估完整展开。

题目的标签不是岗位级别。基础题也可能被面试官连续追问到很深。