# 题库索引与整理规范

## 编号说明

题号是全局稳定 ID，不会因为答案尚未完成而重新排序。

- `Q001–Q052`：由用户提供的 115 个原始问法去重后形成的 52 道主问题；
- `Q020–Q051`：已经分类并保存在 [BACKLOG.md](./BACKLOG.md)，目前部分仍待撰写或核验；
- `Q052`：Harness Engineering，已经先行完成；
- `Q053–Q063`：为国内面试“手撕 Agent 原理”新增的独立设计题。

因此，索引中从 `Q019` 跳到 `Q052`，不代表中间题目丢失，只代表当前页面优先展示已经完成、可以直接学习的答案。

## 专题入口

- [Agent 设计原理与手撕专题](./PRINCIPLES.md)
- [全部主问题与完成状态](./BACKLOG.md)
- [原始题库导入记录](../intake/2026-08-01-agent-developer-question-bank.md)

## 当前可学习题目

### 一、Agent 本质与控制闭环

- [Q001 Agent 和 Workflow 的本质区别是什么？](./01-agent-vs-workflow.md)
- [Q002 ReAct 与 Agent Loop 为什么有效，又有什么局限？](./02-react-and-agent-loop.md)
- [Q003 Agent 如何判断信息已经足够，并避免死循环？](./03-agent-stop-and-loop-control.md)
- [Q009 Agent 与大模型的本质区别是什么？一个 Agent 至少需要哪些组件？](./09-agent-vs-model-and-components.md)
- [Q010 Agent 有哪些常见设计范式？复杂任务如何拆分与动态重规划？](./10-agent-patterns-task-decomposition-replanning.md)
- [Q011 Reflection、Reflexion 和 Evaluator-Optimizer 有什么区别？](./11-reflection-reflexion-evaluator-optimizer.md)

### 二、工程实现与生产边界

- [Q004 如何让 Tool Calling 在生产环境中可靠？](./04-reliable-tool-calling.md)
- [Q005 Agent 的 Context Engineering 应该怎么做？](./05-context-engineering.md)
- [Q006 什么时候用单 Agent，什么时候用 Multi-Agent？](./06-single-vs-multi-agent.md)
- [Q007 如何建立 Agent 评估体系？](./07-agent-evaluation.md)
- [Q008 如何设计一个生产可用的 RAG 系统？](./08-production-rag.md)
- [Q013 生产环境什么时候使用 Agent 框架，什么时候自己实现核心 Runtime？](./13-framework-vs-custom-runtime.md)
- [Q016 Agent 的 System Prompt 应该怎么写？](./16-agent-system-prompt-design.md)
- [Q019 Skill、Tool、MCP Server 和 Workflow 的边界是什么？](./19-skill-tool-mcp-workflow-boundaries.md)
- [Q052 什么是 Harness Engineering？](./52-harness-engineering.md)

### 三、Agent 原理手撕专题

- [Q053 从零设计一个最小 Agent Runtime](./53-design-minimal-agent-runtime.md)
- [Q054 手写 Function Calling 完整链路](./54-function-calling-end-to-end.md)
- [Q055 手写 Agent State 与消息协议](./55-agent-state-and-message-protocol.md)
- [Q056 手写 Context Builder 与 Token Budget](./56-context-builder-and-token-budget.md)
- [Q057 手写停止条件与重复动作检测](./57-stop-conditions-and-loop-detection.md)
- [Q058 设计 Checkpoint、暂停、恢复与幂等](./58-checkpoint-pause-resume-idempotency.md)
- [Q059 设计异步长工具状态机](./59-async-long-running-tools.md)
- [Q060 设计 Parallel Tool Calling 依赖调度器](./60-parallel-tool-dependency-scheduler.md)
- [Q061 设计 Planner–Executor–Replanner](./61-planner-executor-replanner.md)
- [Q062 设计 Human-in-the-Loop 审批状态机](./62-human-in-the-loop-approval-state-machine.md)
- [Q063 设计 Agent Trace、Replay 与故障归因](./63-agent-trace-replay-failure-attribution.md)

## 推荐学习方式

每道普通题分三遍：

1. **先口述**：不看答案，用 2～5 分钟回答；
2. **再对照**：重点看机制、边界、失败模式和项目表达；
3. **最后重答**：只保留自己的语言，不机械背诵全文。

原理手撕题增加两步：

4. **白板画图**：画状态、数据流和异常分支；
5. **写伪代码**：不依赖 LangChain、LangGraph 等框架写核心结构与主循环。

## 去重规则

新增问题前，先判断它是否只是已有问题的另一种问法。

例如以下问法归入同一道题：

- Agent 和 Workflow 有什么区别？
- 什么时候应该用 Agent，而不是固定工作流？
- LangChain Chain 和自主 Agent 如何选择？
- 为什么不把所有流程都交给 Agent？

只有当新问题需要明显不同的推理框架、状态模型或评价指标时，才单独建题。

## 来源记录规则

每道题的“来源”尽可能说明：

- 公司或岗位（来源可确认时）；
- 面试轮次或日期（来源包含时）；
- 原始问法；
- 原始链接。

如果来源只是题库文章而非第一手面经，明确标记为“二手题目整理”，不能伪装成某家公司真实原题。

技术答案证据优先级：

1. 协议规范、论文、官方文档；
2. 可复现的开源实现和实验；
3. 有上下文的工程案例；
4. 社区文章和个人经验。

## 回答质量标准

### 宽泛题

至少回答五层：

1. 定义层：概念是什么；
2. 机制层：为什么能够工作；
3. 工程层：系统如何实现；
4. 边界层：什么时候不适用、哪里会失败；
5. 经验层：如何结合真实项目说明判断与取舍。

### 精确题

重点回答：

- 直接原因；
- 可执行方案；
- 方案顺序；
- 异常与边界。

避免为了“显得有深度”而偏离题目。

### 原理手撕题

至少包含：

- 抽象模型；
- 核心状态与数据结构；
- 主流程和伪代码；
- 停止条件；
- 错误与恢复路径；
- 从 Demo 到生产的演进。

## 自检清单

- [ ] 是否解释了“为什么”，而不是只列名词？
- [ ] 是否区分 Demo 方案和生产方案？
- [ ] 是否写出方案代价和失败模式？
- [ ] 是否存在一句话即可反驳的绝对结论？
- [ ] 是否提供可直接口述的回答？
- [ ] 来源是否真实、可追溯？
- [ ] 是否与已有题目重复？
- [ ] 动态产品、模型和协议是否标注回答日期？
- [ ] 原理题是否能脱离具体框架画图并写伪代码？
