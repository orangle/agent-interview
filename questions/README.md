# Agent 面试题库

面向中国大陆 Agent Engineer / 大模型应用工程师岗位的深度面试题库。

## 当前进度

- 原始题库问法：115
- 去重后的主问题：52
- 原理手撕扩展：11
- **已完成：63 / 63**

## 入口

- [完整题目索引](./BACKLOG.md)
- [Agent 设计原理与手撕专题](./PRINCIPLES.md)

## 推荐学习路线

### 第一阶段：建立 Agent 全局理解

1. [Q009 Agent 与大模型的本质区别](./09-agent-vs-model-and-components.md)
2. [Q001 Agent 与 Workflow](./01-agent-vs-workflow.md)
3. [Q002 ReAct 与 Agent Loop](./02-react-and-agent-loop.md)
4. [Q003 停止条件与循环控制](./03-agent-stop-and-loop-control.md)
5. [Q005 Context Engineering](./05-context-engineering.md)
6. [Q004 Tool Calling 可靠性](./04-reliable-tool-calling.md)

### 第二阶段：进入生产工程

1. [Q053 最小 Agent Runtime](./53-design-minimal-agent-runtime.md)
2. [Q055 Agent State 与消息协议](./55-agent-state-and-message-protocol.md)
3. [Q056 Context Builder 与 Token Budget](./56-context-builder-and-token-budget.md)
4. [Q058 Checkpoint、暂停、恢复与幂等](./58-checkpoint-pause-resume-idempotency.md)
5. [Q014 Agent 分层安全防御](./14-agent-layered-security-defense.md)
6. [Q007 Agent 评估体系](./07-agent-evaluation.md)

### 第三阶段：补齐专项能力

- RAG：Q008、Q020–Q030
- Tool Calling：Q031–Q035、Q054、Q059、Q060
- Memory：Q036–Q040
- Multi-Agent：Q006、Q041、Q042、Q061
- MCP / A2A / 网关：Q043–Q047
- Coding Agent：Q012、Q050、Q052、Q053–Q063

## 每道题怎么学

1. **先口述**：不看答案，用 2～5 分钟回答；
2. **再对照**：重点看为什么、失败模式和方案取舍；
3. **结合项目**：使用自己的 CI/CD Agent、Claude Code 平台和 OpenSandbox 经历重答；
4. **白板画图**：原理题画状态机、数据流和异常分支；
5. **写伪代码**：不依赖具体框架写核心循环和数据结构。

## 内容标准

- 宽泛题：定义、机制、工程、边界、项目经验；
- 精确题：直接原因、执行顺序、异常边界；
- 手撕题：状态、数据结构、伪代码、停止、恢复；
- 动态信息：标注整理日期，优先引用官方规范；
- 同义题：只保留一个主问题，在题内记录不同问法；
- 用户后续学习反馈：直接回写对应题目。