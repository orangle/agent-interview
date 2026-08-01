# Agent 工程面试知识库

面向中国大陆 **Agent Engineer / 大模型应用工程师 / AI 应用后端工程师** 岗位。不是堆八股，而是训练理解、原理、工程边界和项目表达。

<div class="stat-grid">
  <div><strong>63</strong><span>深度问题</span></div>
  <div><strong>11</strong><span>原理手撕题</span></div>
  <div><strong>8</strong><span>知识模块</span></div>
</div>

<div class="learning-panel">
  <div data-learning-progress></div>
  <div class="learning-actions">
    <a class="learning-button learning-button--primary" data-continue-learning href="09-agent-vs-model-and-components/">从 Q009 开始</a>
    <button class="learning-button" type="button" data-random-question>随机抽一题</button>
    <button class="learning-button" type="button" data-reset-progress>清空进度</button>
  </div>
</div>

!!! note "进度如何保存"
    每道题标题下都有“标记为已掌握”。学习进度只保存在当前浏览器，不上传服务器；更换设备后不会自动同步。

## 三条学习入口

<div class="card-grid" markdown>

<div class="study-card" markdown>

### 建立全局认知

先理解 Agent 与模型、Workflow、ReAct、Tool、Context 的关系，再进入具体框架。

[从 Q009 开始](09-agent-vs-model-and-components.md)

</div>

<div class="study-card" markdown>

### 原理手撕

训练状态机、数据结构、伪代码、异常恢复和生产边界，适合国内面试连续追问。

[进入原理专题](PRINCIPLES.md)

</div>

<div class="study-card" markdown>

### 完整题库

按 Agent、RAG、Tool、Memory、Multi-Agent、协议和系统设计分类查看全部 63 题。

[打开完整索引](BACKLOG.md)

</div>

</div>

## 推荐学习顺序

### 第一阶段：Agent 全局认知

1. [Q009 Agent 与大模型的本质区别](09-agent-vs-model-and-components.md)
2. [Q001 Agent 与 Workflow](01-agent-vs-workflow.md)
3. [Q002 ReAct 与 Agent Loop](02-react-and-agent-loop.md)
4. [Q003 停止条件与循环控制](03-agent-stop-and-loop-control.md)
5. [Q005 Context Engineering](05-context-engineering.md)
6. [Q004 Tool Calling 可靠性](04-reliable-tool-calling.md)

### 第二阶段：生产级 Runtime

1. [Q053 从零设计最小 Agent Runtime](53-design-minimal-agent-runtime.md)
2. [Q055 Agent State 与消息协议](55-agent-state-and-message-protocol.md)
3. [Q054 Function Calling 完整链路](54-function-calling-end-to-end.md)
4. [Q056 Context Builder 与 Token Budget](56-context-builder-and-token-budget.md)
5. [Q058 Checkpoint、恢复与幂等](58-checkpoint-pause-resume-idempotency.md)
6. [Q063 Trace、Replay 与故障归因](63-agent-trace-replay-failure-attribution.md)

### 第三阶段：按岗位补专项

- **Agent 应用开发**：Prompt、RAG、Tool Calling、评估、安全。
- **Agent 后端 / 平台**：Runtime、Checkpoint、异步工具、网关、多租户、可观测性。
- **Coding Agent**：代码修复闭环、沙箱、Harness、审批、Trace。
- **多 Agent 系统**：拓扑、状态、路由、A2A、错误放大与一致性。

## 每道题怎么学

1. **先口述 2～5 分钟**：不看答案，暴露自己真正不懂的地方。
2. **阅读核心结论**：确认概念和边界。
3. **看工程实现与失败模式**：重点理解为什么 Demo 方案不能直接上线。
4. **再口述一次**：只使用自己的语言。
5. **结合项目重答**：优先使用 CI/CD Agent、Claude Code 平台和 OpenSandbox 场景。

原理手撕题额外要求：

- 画状态机与数据流；
- 写核心数据结构；
- 写不依赖框架的伪代码；
- 主动补充超时、重试、幂等、恢复、权限和预算。

## 当前重点

现在不要平均用力。优先掌握：

```text
Q009 Agent 与模型
→ Q001 Agent 与 Workflow
→ Q002 Agent Loop
→ Q053 最小 Runtime
→ Q054 Function Calling
→ Q056 Context Builder
→ Q058 Checkpoint
→ Q063 Trace / Replay
```

这条路线最能把你的 DevOps / 平台工程经验转换成 Agent 工程岗位的面试优势。

<!-- pages-redeploy: 2026-08-01T19:40+08:00 -->
