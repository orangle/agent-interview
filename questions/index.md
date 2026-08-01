# Agent 工程面试知识库

这是一套面向中国大陆 Agent Engineer / 大模型应用工程师岗位的深度面试题库。

<div class="stat-grid">
  <div><strong>63</strong><span>深度问题</span></div>
  <div><strong>11</strong><span>原理手撕题</span></div>
  <div><strong>8</strong><span>知识模块</span></div>
</div>

## 从这里开始

<div class="card-grid" markdown>

<div class="study-card" markdown>

### 基础认知

从 Agent、Workflow、ReAct、Context 和 Tool Calling 建立全局理解。

[开始学习 Q009](09-agent-vs-model-and-components.md)

</div>

<div class="study-card" markdown>

### 原理手撕

训练状态机、数据结构、伪代码、异常恢复和生产边界。

[进入手撕专题](PRINCIPLES.md)

</div>

<div class="study-card" markdown>

### 完整题库

查看 Q001–Q063 的分类索引和全部答案。

[打开完整索引](BACKLOG.md)

</div>

</div>

## 推荐路线

### 1. 先建立 Agent 全局认知

1. [Q009 Agent 与大模型的本质区别](09-agent-vs-model-and-components.md)
2. [Q001 Agent 与 Workflow](01-agent-vs-workflow.md)
3. [Q002 ReAct 与 Agent Loop](02-react-and-agent-loop.md)
4. [Q003 停止条件与循环控制](03-agent-stop-and-loop-control.md)
5. [Q005 Context Engineering](05-context-engineering.md)
6. [Q004 Tool Calling 可靠性](04-reliable-tool-calling.md)

### 2. 再学习生产级 Runtime

1. [Q053 从零设计最小 Agent Runtime](53-design-minimal-agent-runtime.md)
2. [Q055 Agent State 与消息协议](55-agent-state-and-message-protocol.md)
3. [Q056 Context Builder 与 Token Budget](56-context-builder-and-token-budget.md)
4. [Q058 Checkpoint、暂停、恢复与幂等](58-checkpoint-pause-resume-idempotency.md)
5. [Q014 Agent 分层安全防御](14-agent-layered-security-defense.md)
6. [Q007 Agent 评估体系](07-agent-evaluation.md)

### 3. 按岗位补专项

| 方向 | 重点题目 |
|---|---|
| RAG / 知识库 | Q008、Q020–Q030 |
| Tool Calling | Q031–Q035、Q054、Q059、Q060 |
| Memory | Q036–Q040 |
| Multi-Agent | Q006、Q041、Q042、Q061 |
| MCP / A2A / 网关 | Q043–Q047 |
| Coding Agent | Q012、Q050、Q052–Q063 |

## 学习方法

每道题按五步练习：

1. **先口述**：不看答案回答 2～5 分钟；
2. **看机制**：理解为什么有效，而不是背名词；
3. **看边界**：重点理解失败模式和 Trade-off；
4. **结合项目**：用 CI/CD Agent、Claude Code 平台和 OpenSandbox 经历重答；
5. **手写原理**：画状态机并写不依赖框架的伪代码。

!!! tip "不要机械背答案"
    面试官会继续追问。真正目标是能从目标、约束、状态、工具、失败和验证重新推导方案。

## 内容维护原则

- 同义题只保留一个主问题；
- 宽泛题充分展开，精确题直接回答；
- 动态产品和协议标注整理日期；
- 技术依据优先采用规范、论文和官方文档；
- 后续学习中的疑问和反例直接回写对应题目。