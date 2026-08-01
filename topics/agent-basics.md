# Agent 基础面试题

## 1. 什么是 Agent？

### 面试问题

什么是 Agent？它和普通 ChatBot 有什么区别？

### 核心回答

Agent 是由大模型驱动的任务执行系统，不只是生成文本，而是通过理解目标、规划步骤、调用工具、观察结果，持续完成任务。

核心闭环：

```
Goal
 ↓
Reasoning
 ↓
Action
 ↓
Observation
 ↓
Next Action
```

### ChatBot vs Agent

ChatBot：

用户输入 → LLM → 回复

Agent：

用户目标 → LLM决策 → Tool调用 → 环境反馈 → 完成任务

### 工程组成

- LLM
- Prompt / Context
- Tool
- Memory
- State Management
- Runtime

---

## 2. Agent 和 Workflow 有什么区别？

Workflow：固定流程编排。

Agent：动态决策。

实际企业系统通常结合：

```
Workflow 负责稳定流程
Agent 负责复杂决策
```

---

## 3. ReAct 是什么？

ReAct = Reasoning + Acting。

核心思想：让模型在思考和行动之间循环。

```
Thought
 ↓
Action
 ↓
Observation
 ↓
Thought
```

优点：

- 可以使用外部工具
- 可以根据结果调整方案
- 适合复杂任务

---

## 4. Agent 最大工程难点

不是调用 LLM，而是：

1. Context 管理
2. Tool 可靠性
3. 状态管理
4. 成本控制
5. 效果评估

---

## 结合个人项目

CICD 故障分析 Agent：

用户提出：发布失败原因是什么？

Agent：

- 查询 Jenkins
- 获取日志
- 分析异常
- 查询代码变更
- 输出根因和修复建议

LLM负责决策，工具负责获取真实信息。