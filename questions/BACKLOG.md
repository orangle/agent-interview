# Agent Interview Question Index

原始题库中的 115 个问法已去重为 `Q001–Q052` 共 52 道主问题，并新增 `Q053–Q063` 共 11 道国内面试原理手撕题。

**当前状态：63 / 63 已完成。**

## A. Agent 基础、Runtime 与安全

- [Q001 Agent 和 Workflow 的本质区别](./01-agent-vs-workflow.md)
- [Q002 ReAct 与 Agent Loop](./02-react-and-agent-loop.md)
- [Q003 停止条件与死循环控制](./03-agent-stop-and-loop-control.md)
- [Q004 生产级 Tool Calling 可靠性](./04-reliable-tool-calling.md)
- [Q005 Context Engineering](./05-context-engineering.md)
- [Q006 单 Agent 与 Multi-Agent 选型](./06-single-vs-multi-agent.md)
- [Q007 Agent 评估体系](./07-agent-evaluation.md)
- [Q008 生产级 RAG 总体设计](./08-production-rag.md)
- [Q009 Agent 与大模型的本质区别](./09-agent-vs-model-and-components.md)
- [Q010 Agent 设计范式、任务拆分与重规划](./10-agent-patterns-task-decomposition-replanning.md)
- [Q011 Reflection、Reflexion 与 Evaluator-Optimizer](./11-reflection-reflexion-evaluator-optimizer.md)
- [Q012 Coding Agent 可验证修复闭环](./12-coding-agent-verifiable-repair-loop.md)
- [Q013 Agent 框架与自研 Runtime 的选型](./13-framework-vs-custom-runtime.md)
- [Q014 Agent 分层安全防御](./14-agent-layered-security-defense.md)
- [Q015 Badcase 归因与数据飞轮](./15-badcase-attribution-and-data-flywheel.md)

## B. Prompt、Context 与 Skill

- [Q016 Agent System Prompt 设计](./16-agent-system-prompt-design.md)
- [Q017 Few-shot 与推理提示在 Agent 中的使用](./17-few-shot-and-chain-of-thought-in-agents.md)
- [Q018 Agent Prompt 鲁棒性](./18-agent-prompt-robustness.md)
- [Q019 Skill、Tool、MCP Server 与 Workflow 的边界](./19-skill-tool-mcp-workflow-boundaries.md)

## C. RAG 与知识系统

- [Q020 RAG 分块与 Contextual Retrieval](./20-rag-chunking-and-contextual-retrieval.md)
- [Q021 Embedding 选型与微调](./21-embedding-model-selection-and-finetuning.md)
- [Q022 查询路由与查询重写](./22-rag-query-routing-and-rewriting.md)
- [Q023 FLAT、IVF、PQ、HNSW 索引选型](./23-vector-index-selection.md)
- [Q024 BM25 与向量混合召回](./24-hybrid-retrieval-and-rank-fusion.md)
- [Q025 Reranker、Bi-Encoder 与 Cross-Encoder](./25-reranker-bi-encoder-vs-cross-encoder.md)
- [Q026 RAG 分层评估](./26-rag-evaluation-system.md)
- [Q027 图片、表格、代码和复杂 PDF](./27-rag-complex-documents-and-multimodal.md)
- [Q028 长上下文与 RAG](./28-long-context-vs-rag.md)
- [Q029 Agent/RAG 幻觉检测与治理](./29-agent-rag-hallucination-detection-and-mitigation.md)
- [Q030 知识冲突、版本与更新](./30-knowledge-conflict-versioning-and-updates.md)

## D. Tool Calling 与执行系统

- [Q031 Function Calling 与 Tool Calling](./31-function-calling-vs-tool-calling.md)
- [Q032 大工具结果压缩与证据保留](./32-tool-result-compression-and-evidence-preservation.md)
- [Q033 异步长工具、回调与恢复](./33-async-long-running-tool-execution.md)
- [Q034 工具发现、路由与候选集控制](./34-tool-discovery-routing-and-candidate-control.md)
- [Q035 Parallel Tool Calling 一致性](./35-parallel-tool-calling-consistency.md)

## E. Memory

- [Q036 Memory 分层](./36-agent-memory-layering.md)
- [Q037 Memory 写入、读取、更新与遗忘](./37-memory-write-read-update-forgetting.md)
- [Q038 长对话短期记忆](./38-long-conversation-short-term-memory.md)
- [Q039 多租户 Memory 隔离与一致性](./39-multi-tenant-memory-isolation-and-consistency.md)
- [Q040 Memory 冷启动](./40-memory-cold-start.md)

## F. Multi-Agent、协议与平台

- [Q041 Multi-Agent 拓扑、通信、状态与路由](./41-multi-agent-topology-communication-state-routing.md)
- [Q042 Multi-Agent 错误放大](./42-multi-agent-error-amplification.md)
- [Q043 MCP 架构、原语与传输](./43-mcp-architecture-primitives-and-transports.md)
- [Q044 MCP、Function Calling 与直接 API](./44-mcp-vs-function-calling-and-direct-api.md)
- [Q045 SSE 与 WebSocket](./45-sse-vs-websocket-for-agent-frontend.md)
- [Q046 A2A：Agent Card、Task、Message 与 Artifact](./46-a2a-protocol-agent-card-task-message.md)
- [Q047 大模型网关](./47-llm-gateway-design.md)

## G. 系统设计、产品与框架

- [Q048 生产级智能客服 Agent](./48-production-customer-service-agent-design.md)
- [Q049 模型能力边界与路由](./49-model-capability-boundaries-and-routing.md)
- [Q050 Coding Agent 产品比较](./50-coding-agent-product-comparison.md)
- [Q051 Agent 框架选型](./51-agent-framework-selection.md)
- [Q052 Harness Engineering](./52-harness-engineering.md)

## H. 国内面试原理手撕专题

- [Q053 从零设计最小 Agent Runtime](./53-design-minimal-agent-runtime.md)
- [Q054 手写 Function Calling 完整链路](./54-function-calling-end-to-end.md)
- [Q055 手写 Agent State 与消息协议](./55-agent-state-and-message-protocol.md)
- [Q056 手写 Context Builder 与 Token Budget](./56-context-builder-and-token-budget.md)
- [Q057 手写停止条件与重复动作检测](./57-stop-conditions-and-loop-detection.md)
- [Q058 Checkpoint、暂停、恢复与幂等](./58-checkpoint-pause-resume-idempotency.md)
- [Q059 异步长工具状态机](./59-async-long-running-tools.md)
- [Q060 Parallel Tool Calling 依赖调度器](./60-parallel-tool-dependency-scheduler.md)
- [Q061 Planner–Executor–Replanner](./61-planner-executor-replanner.md)
- [Q062 Human-in-the-Loop 审批状态机](./62-human-in-the-loop-approval-state-machine.md)
- [Q063 Agent Trace、Replay 与故障归因](./63-agent-trace-replay-failure-attribution.md)

## 维护规则

- 同义问题合并到已有主问题；
- 动态产品和协议标注整理日期；
- 技术依据优先使用规范、论文和官方文档；
- 宽泛题回答定义、机制、工程、边界和项目经验；
- 手撕题回答状态、数据结构、伪代码、异常与恢复；
- 新的学习疑问直接回写对应题目。