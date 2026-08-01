from __future__ import annotations

from pathlib import Path
from textwrap import dedent

ROOT = Path(__file__).resolve().parents[1]
QUESTIONS = ROOT / "questions"
START = "<!-- mermaid-diagram:start -->"
END = "<!-- mermaid-diagram:end -->"

DIAGRAMS: dict[str, str] = {
    "01-agent-vs-workflow.md": """
flowchart LR
  R[业务需求] --> D{控制流程是否确定}
  D -->|确定| W[Workflow 编排]
  D -->|存在开放决策| A[受约束 Agent]
  W --> V[确定性校验与执行]
  A --> O[观察环境]
  O --> P[模型提出下一步]
  P --> G[Runtime 校验与执行]
  G --> O
  G --> V
""",
    "02-react-and-agent-loop.md": """
flowchart TD
  G[目标] --> T[Reason 思考]
  T --> A[Act 选择动作]
  A --> O[Observe 获取结果]
  O --> C{目标是否完成}
  C -->|否| T
  C -->|是| F[Final Answer]
  C -->|无进展或超预算| S[停止或升级人工]
""",
    "03-agent-stop-and-loop-control.md": """
flowchart TD
  I[每轮执行完成] --> H{硬预算是否耗尽}
  H -->|是| X[停止并记录原因]
  H -->|否| R{动作是否重复或无进展}
  R -->|是| P[重规划或人工接管]
  R -->|否| E{业务完成条件是否满足}
  E -->|是| V[独立验证]
  V -->|通过| D[成功结束]
  V -->|失败| P
  E -->|否| N[进入下一轮]
""",
    "04-reliable-tool-calling.md": """
sequenceDiagram
  participant M as Model
  participant R as Runtime
  participant A as Auth/Policy
  participant T as Tool
  M->>R: tool_call(name,args)
  R->>R: Schema 与业务校验
  R->>A: 权限与风险检查
  A-->>R: allow / approve / deny
  R->>T: 带幂等键执行
  T-->>R: 结构化结果或错误
  R->>R: 脱敏、截断、归一化
  R-->>M: tool_result(call_id,status,evidence)
""",
    "05-context-engineering.md": """
flowchart LR
  S[完整 Runtime State] --> F[相关性过滤]
  M[长期 Memory] --> F
  K[检索知识与工具结果] --> F
  F --> B[Token Budget 分配]
  B --> C[压缩与摘要]
  C --> A[Context Assembly]
  A --> L[LLM]
  L --> T[决策或工具调用]
  T --> S
""",
    "06-single-vs-multi-agent.md": """
flowchart TD
  Q[任务] --> C{是否存在清晰独立角色与上下文边界}
  C -->|否| S[单 Agent + 多工具]
  C -->|是| I{并行收益是否大于协调成本}
  I -->|否| S
  I -->|是| M[Multi-Agent]
  M --> P[Supervisor / Router]
  P --> A1[专业 Agent A]
  P --> A2[专业 Agent B]
  A1 --> J[共享状态与验收]
  A2 --> J
""",
    "07-agent-evaluation.md": """
flowchart TD
  D[真实任务与 Badcase] --> G[离线评测集]
  G --> L1[组件指标]
  G --> L2[轨迹指标]
  G --> L3[端到端任务成功率]
  L1 --> R[回归门禁]
  L2 --> R
  L3 --> R
  R --> O[线上灰度]
  O --> M[成功率 成本 延迟 安全]
  M --> D
""",
    "08-production-rag.md": """
flowchart LR
  subgraph Ingest[离线入库]
    D[文档] --> P[解析与清洗]
    P --> C[结构化分块]
    C --> E[Embedding]
    C --> B[关键词索引]
    E --> V[向量库]
    B --> X[倒排索引]
  end
  subgraph Query[在线查询]
    Q[用户问题] --> R[路由与改写]
    R --> V
    R --> X
    V --> F[融合召回]
    X --> F
    F --> K[Rerank]
    K --> G[带引用生成]
  end
""",
    "09-agent-vs-model-and-components.md": """
flowchart TD
  G[Goal 目标] --> C[Controller / Policy]
  S[State 状态] --> C
  O[Observation 观察] --> C
  C --> M[LLM 推理]
  M --> A[Action 候选动作]
  A --> R[Runtime 校验与执行]
  R --> E[Environment 环境]
  E --> O
  R --> S
  S --> T{Termination 终止条件}
""",
    "10-agent-patterns-task-decomposition-replanning.md": """
flowchart TD
  Q[复杂任务] --> D{任务是否可一次决定}
  D -->|是| R[ReAct 循环]
  D -->|否| P[Planner 生成可验收步骤]
  P --> E[Executor 执行当前步骤]
  E --> V{验证是否通过}
  V -->|通过| N{还有步骤吗}
  N -->|是| E
  N -->|否| F[完成]
  V -->|失败| RP[Replanner 生成最小 Plan Patch]
  RP --> E
""",
    "11-reflection-reflexion-evaluator-optimizer.md": """
flowchart LR
  A[初始输出或轨迹] --> E[Evaluator 评估]
  E --> D{是否达标}
  D -->|是| F[接受结果]
  D -->|否| R[Reflection 归因与建议]
  R --> O[Optimizer 重新生成或修正]
  O --> E
  R --> M[Reflexion 写入可复用经验]
""",
    "12-coding-agent-verifiable-repair-loop.md": """
flowchart TD
  B[Bug / 失败日志] --> R[复现与定位]
  R --> P[生成最小修改计划]
  P --> C[编辑代码]
  C --> T[运行针对性测试]
  T --> V{验证通过}
  V -->|否| A[分析新证据]
  A --> R
  V -->|是| D[Diff 审查与风险检查]
  D --> O[输出修复证据]
""",
    "13-framework-vs-custom-runtime.md": """
flowchart TD
  Q[系统需求] --> P{是否处于快速原型阶段}
  P -->|是| F[使用成熟框架]
  P -->|否| C{是否需要强控制 恢复 审计 多租户}
  C -->|否| F
  C -->|是| H[框架能力作为组件]
  H --> R[自研核心 Runtime]
  R --> S[状态机 权限 Checkpoint Trace]
""",
    "14-agent-layered-security-defense.md": """
flowchart TD
  U[用户输入与外部内容] --> L1[输入与指令边界]
  L1 --> L2[工具候选集最小化]
  L2 --> L3[参数 Schema 与业务校验]
  L3 --> L4[身份 权限 租户隔离]
  L4 --> L5[沙箱与网络资源限制]
  L5 --> L6[高风险动作审批]
  L6 --> L7[审计 Trace 与异常检测]
  L7 --> T[真实工具执行]
""",
    "15-badcase-attribution-and-data-flywheel.md": """
flowchart LR
  O[线上 Trace 与反馈] --> C[Badcase 聚类]
  C --> A[最早致错点归因]
  A --> T1[Prompt / Context 修复]
  A --> T2[Tool / Runtime 修复]
  A --> T3[模型或数据修复]
  T1 --> E[回归评测]
  T2 --> E
  T3 --> E
  E --> G[灰度上线]
  G --> O
""",
    "16-agent-system-prompt-design.md": """
flowchart TD
  P1[角色与目标] --> S[System Prompt]
  P2[行为边界] --> S
  P3[工具使用规则] --> S
  P4[输出契约] --> S
  P5[失败与升级策略] --> S
  S --> M[模型决策]
  M --> R[Runtime 强制权限 校验 幂等]
""",
    "17-few-shot-and-chain-of-thought-in-agents.md": """
flowchart TD
  Q[任务] --> E{是否存在稳定的行为范式}
  E -->|是| F[Few-shot 展示输入与正确动作]
  E -->|否| Z[零样本规则]
  F --> P[模型生成可观察的计划或结构化决策]
  Z --> P
  P --> R[Runtime 执行与验证]
  R --> T[保留结果与证据 不依赖隐藏思维链]
""",
    "18-agent-prompt-robustness.md": """
flowchart LR
  P[Prompt 版本] --> T[对抗与边界测试集]
  T --> V1[格式稳定性]
  T --> V2[工具选择稳定性]
  T --> V3[注入抵抗]
  T --> V4[长上下文稳定性]
  V1 --> G[回归门禁]
  V2 --> G
  V3 --> G
  V4 --> G
  G --> D[灰度发布]
""",
    "19-skill-tool-mcp-workflow-boundaries.md": """
flowchart TD
  U[用户目标] --> S[Skill 方法与领域知识]
  S --> A[Agent 决策]
  A --> W[Workflow 确定性编排]
  A --> T[Tool 原子能力]
  T --> M[MCP 标准化发现与调用]
  W --> R[Runtime 执行]
  M --> R
  R --> E[外部系统]
""",
    "20-rag-chunking-and-contextual-retrieval.md": """
flowchart LR
  D[原始文档] --> P[保留标题 章节 表格关系]
  P --> C[语义分块]
  C --> X[补充文档级上下文]
  X --> E[Embedding 与关键词索引]
  Q[查询] --> R[召回]
  E --> R
  R --> K[返回块 + 父级上下文]
""",
    "21-embedding-model-selection-and-finetuning.md": """
flowchart TD
  Q[业务检索任务] --> D[构建领域评测集]
  D --> B[比较候选 Embedding]
  B --> M[Recall@K MRR 延迟 成本]
  M --> G{通用模型是否达标}
  G -->|是| S[直接使用并监控漂移]
  G -->|否| F[领域数据微调或蒸馏]
  F --> M
""",
    "22-rag-query-routing-and-rewriting.md": """
flowchart TD
  Q[用户查询] --> C[意图 实体 时效性识别]
  C --> R{选择检索路径}
  R -->|关键词强| B[BM25]
  R -->|语义强| V[向量检索]
  R -->|结构化数据| S[SQL / API]
  R -->|需多步| M[分解查询]
  B --> F[融合与去重]
  V --> F
  S --> F
  M --> F
""",
    "23-vector-index-selection.md": """
flowchart TD
  N[向量规模与延迟目标] --> E{是否需要精确检索}
  E -->|是| F[FLAT]
  E -->|否| M{内存是否充足}
  M -->|是| H[HNSW]
  M -->|否| I[IVF]
  I --> P{是否需要进一步压缩}
  P -->|是| Q[PQ / IVF-PQ]
  P -->|否| I2[IVF-Flat]
  F --> B[在真实数据上 Benchmark]
  H --> B
  Q --> B
  I2 --> B
""",
    "24-hybrid-retrieval-and-rank-fusion.md": """
flowchart LR
  Q[查询] --> B[BM25 稀疏召回]
  Q --> V[向量稠密召回]
  B --> N[分数归一化或 RRF]
  V --> N
  N --> D[去重与权限过滤]
  D --> R[Cross-Encoder Rerank]
  R --> C[最终 Context]
""",
    "25-reranker-bi-encoder-vs-cross-encoder.md": """
flowchart LR
  Q[查询] --> B[Bi-Encoder 快速召回 Top-K]
  D[文档库] --> B
  B --> C[Cross-Encoder 联合编码 Query-Doc]
  C --> R[精排 Top-N]
  R --> G[生成或返回答案]
""",
    "26-rag-evaluation-system.md": """
flowchart TD
  Q[评测问题集] --> I[检索评估]
  I --> M1[Recall@K MRR nDCG]
  Q --> G[生成评估]
  G --> M2[Faithfulness 完整性 引用准确]
  I --> E[端到端评估]
  G --> E
  E --> M3[任务成功率 延迟 成本]
  M1 --> R[回归门禁]
  M2 --> R
  M3 --> R
""",
    "27-rag-complex-documents-and-multimodal.md": """
flowchart LR
  D[PDF / 图片 / 表格 / 代码] --> R[版面与对象识别]
  R --> T1[正文段落]
  R --> T2[表格结构]
  R --> T3[图片说明与坐标]
  R --> T4[代码块与符号]
  T1 --> C[多模态统一 Chunk]
  T2 --> C
  T3 --> C
  T4 --> C
  C --> I[索引 + 原页证据引用]
""",
    "28-long-context-vs-rag.md": """
flowchart TD
  Q[任务输入] --> S{内容规模与更新频率}
  S -->|小且一次性| L[直接长上下文]
  S -->|大或持续更新| R[RAG]
  S -->|既需全局又需精准证据| H[混合方案]
  H --> L2[摘要与核心材料进入长上下文]
  H --> R2[细节按需检索]
  L --> V[统一做引用与完成验证]
  R --> V
  L2 --> V
  R2 --> V
""",
    "29-agent-rag-hallucination-detection-and-mitigation.md": """
flowchart TD
  A[生成答案] --> C[拆分事实性 Claim]
  C --> E[匹配检索证据与工具结果]
  E --> V{证据是否支持}
  V -->|支持| K[保留并附引用]
  V -->|不足| R[继续检索或降低置信度]
  V -->|冲突| X[显式展示冲突与版本]
  R --> F[无法确认则拒答或升级]
""",
    "30-knowledge-conflict-versioning-and-updates.md": """
flowchart LR
  S[多来源知识] --> N[规范化实体与时间]
  N --> V[版本号 生效时间 来源优先级]
  V --> I[增量索引]
  Q[查询时间与场景] --> R[版本感知检索]
  I --> R
  R --> C{来源是否冲突}
  C -->|否| A[返回有效版本]
  C -->|是| X[展示冲突并保留证据]
""",
    "31-function-calling-vs-tool-calling.md": """
sequenceDiagram
  participant App as Application
  participant Model as Model
  participant Runtime as Runtime
  participant Tool as Tool/API
  App->>Model: Messages + Tool Schemas
  Model-->>Runtime: tool_call(name,args,call_id)
  Runtime->>Runtime: 校验 权限 幂等
  Runtime->>Tool: 执行真实能力
  Tool-->>Runtime: result / error
  Runtime-->>Model: tool_result(call_id,status,evidence)
  Model-->>App: 最终答案或下一次调用
""",
    "32-tool-result-compression-and-evidence-preservation.md": """
flowchart LR
  R[大体量 Tool Result] --> S[结构化解析]
  S --> F[错误与关键字段优先]
  F --> C[摘要 压缩 去重]
  C --> M[进入模型 Context]
  S --> O[原始结果对象存储]
  O --> E[Evidence Ref]
  E --> M
  M --> A[答案可回溯到原始证据]
""",
    "33-async-long-running-tool-execution.md": """
stateDiagram-v2
  [*] --> SUBMITTED
  SUBMITTED --> RUNNING: worker 接单
  RUNNING --> WAITING_EXTERNAL: 等待回调
  WAITING_EXTERNAL --> RUNNING: 收到事件
  RUNNING --> SUCCEEDED: 完成
  RUNNING --> FAILED: 不可恢复错误
  RUNNING --> RETRY_WAIT: 可重试错误
  RETRY_WAIT --> RUNNING
  SUBMITTED --> CANCELLED: 取消
  RUNNING --> CANCELLED: 取消
  SUCCEEDED --> [*]
  FAILED --> [*]
  CANCELLED --> [*]
""",
    "34-tool-discovery-routing-and-candidate-control.md": """
flowchart TD
  Q[当前任务与状态] --> R[语义 Tool Router]
  T[Tool Registry] --> R
  R --> F[权限 环境 风险过滤]
  F --> K[Top-K 候选工具]
  K --> M[模型选择具体工具]
  M --> V[Runtime 再次校验]
  V --> E[执行]
""",
    "35-parallel-tool-calling-consistency.md": """
flowchart LR
  P[模型提出多个 Tool Call] --> D[构建依赖 DAG]
  D --> C[读写集合与副作用冲突检测]
  C --> A[可并行批次]
  A --> T1[Tool A]
  A --> T2[Tool B]
  T1 --> J[结果 Join]
  T2 --> J
  J --> V[一致性验证与补偿]
""",
    "36-agent-memory-layering.md": """
flowchart TD
  S1[Runtime State 当前执行真相] --> C[Context Builder]
  S2[短期会话记忆] --> C
  S3[长期语义记忆] --> C
  S4[情节与经验记忆] --> C
  S5[用户事实与偏好] --> C
  C --> M[模型当前上下文]
  M --> W[受策略约束的 Memory Write]
  W --> S2
  W --> S3
  W --> S4
  W --> S5
""",
    "37-memory-write-read-update-forgetting.md": """
flowchart LR
  O[新观察或用户事实] --> E[抽取候选记忆]
  E --> V[真实性 敏感性 价值校验]
  V --> D{与旧记忆关系}
  D -->|新增| C[Create]
  D -->|修正| U[Update + Version]
  D -->|冲突| X[保留冲突与来源]
  C --> R[按任务检索]
  U --> R
  X --> R
  R --> F[衰减 淘汰 用户删除]
""",
    "38-long-conversation-short-term-memory.md": """
flowchart LR
  H[完整对话与事件流] --> W[滑动窗口保留最近轮次]
  H --> S[阶段摘要]
  H --> F[事实 决策 待办单独抽取]
  W --> C[Context Builder]
  S --> C
  F --> C
  C --> M[模型]
  M --> H
""",
    "39-multi-tenant-memory-isolation-and-consistency.md": """
flowchart TD
  R[Memory 请求] --> I[身份与租户解析]
  I --> K[tenant_id + user_id + namespace]
  K --> P[权限与数据分类策略]
  P --> S[分区存储与加密]
  S --> V[版本与并发控制]
  V --> A[审计日志]
  A --> Q[检索结果]
""",
    "40-memory-cold-start.md": """
flowchart TD
  N[新用户或新 Agent] --> D[显式偏好与初始配置]
  D --> B[安全默认行为]
  B --> O[观察少量高价值信号]
  O --> C[候选记忆需确认]
  C --> M[逐步个性化]
  M --> F[持续反馈与纠错]
""",
    "41-multi-agent-topology-communication-state-routing.md": """
flowchart TD
  U[用户任务] --> S[Supervisor / Router]
  S --> P[Planner Agent]
  S --> R[Research Agent]
  S --> E[Executor Agent]
  P --> B[共享 Blackboard / State]
  R --> B
  E --> B
  B --> V[Verifier Agent]
  V --> S
  S --> F[最终结果]
""",
    "42-multi-agent-error-amplification.md": """
flowchart LR
  E1[Agent A 错误假设] --> M1[消息传递]
  M1 --> E2[Agent B 基于错误继续推理]
  E2 --> M2[共享状态污染]
  M2 --> E3[Agent C 执行错误动作]
  E3 --> A[错误放大]
  G1[独立证据与置信度] -.抑制.-> M1
  G2[状态版本与验收门] -.抑制.-> M2
  G3[Verifier] -.抑制.-> E3
""",
    "43-mcp-architecture-primitives-and-transports.md": """
flowchart LR
  H[MCP Host / Agent] --> C[MCP Client]
  C <--> S[MCP Server]
  S --> T[Tools]
  S --> R[Resources]
  S --> P[Prompts]
  C -.stdio.-> S
  C -.Streamable HTTP.-> S
  H --> L[LLM 决策]
  L --> C
""",
    "44-mcp-vs-function-calling-and-direct-api.md": """
flowchart TD
  M[模型] --> F[Function Calling 调用意图]
  F --> R[Agent Runtime]
  R --> D{工具接入方式}
  D -->|进程内| L[本地函数]
  D -->|固定系统| A[直接 HTTP / gRPC API]
  D -->|标准化发现与互操作| C[MCP Client]
  C --> S[MCP Server]
  L --> E[真实能力]
  A --> E
  S --> E
""",
    "45-sse-vs-websocket-for-agent-frontend.md": """
flowchart TD
  U[Agent 前端需求] --> D{通信方向}
  D -->|服务端持续推送为主| S[SSE]
  D -->|高频双向交互| W[WebSocket]
  S --> E[Token Event Tool Status Trace]
  W --> B[实时控制 协作 终端]
  E --> R[断线重连 + Last-Event-ID]
  B --> H[心跳 顺序号 背压]
""",
    "46-a2a-protocol-agent-card-task-message.md": """
sequenceDiagram
  participant C as Client Agent
  participant D as Agent Card / Discovery
  participant S as Remote Agent
  C->>D: 查询能力与认证方式
  D-->>C: Agent Card
  C->>S: 创建 Task + Message
  S-->>C: Task 状态更新
  C->>S: 追加 Message / 输入
  S-->>C: Artifact
  S-->>C: completed / failed / input-required
""",
    "47-llm-gateway-design.md": """
flowchart LR
  A[Agent / Application] --> G[LLM Gateway]
  G --> I[统一协议与鉴权]
  I --> R[模型路由与降级]
  R --> P1[Provider A]
  R --> P2[Provider B]
  R --> P3[自建模型]
  G --> Q[限流 配额 成本]
  G --> O[日志 Trace 脱敏]
  P1 --> G
  P2 --> G
  P3 --> G
""",
    "48-production-customer-service-agent-design.md": """
flowchart TD
  U[用户请求] --> I[意图 风险 身份识别]
  I --> K[知识检索]
  I --> T[业务工具]
  K --> A[客服 Agent]
  T --> A
  A --> P{是否涉及高风险或低置信度}
  P -->|是| H[人工坐席接管]
  P -->|否| R[生成带证据回复]
  R --> F[质量监控与反馈]
""",
    "49-model-capability-boundaries-and-routing.md": """
flowchart TD
  Q[请求特征] --> C[能力分类]
  C --> R{模型路由}
  R -->|低复杂度| S[小模型]
  R -->|复杂推理| L[强模型]
  R -->|代码任务| K[代码模型]
  R -->|多模态| V[视觉模型]
  S --> G[质量门与降级]
  L --> G
  K --> G
  V --> G
  G --> O[成本 延迟 成功率监控]
""",
    "50-coding-agent-product-comparison.md": """
flowchart TD
  N[Coding Agent 产品] --> I[交互形态 IDE CLI 云端]
  N --> C[上下文与代码索引]
  N --> T[工具 沙箱 测试能力]
  N --> A[自主程度与审批]
  N --> E[评估 可观测性 成本]
  I --> D[按团队流程与风险选型]
  C --> D
  T --> D
  A --> D
  E --> D
""",
    "51-agent-framework-selection.md": """
flowchart TD
  R[需求] --> C{核心复杂度在哪里}
  C -->|简单工具调用| S[轻量 SDK]
  C -->|显式状态图与恢复| G[Graph / Workflow 框架]
  C -->|多 Agent 协作| M[Multi-Agent 框架]
  C -->|企业平台控制面| H[自研 Runtime + 选用组件]
  S --> E[PoC 与 Benchmark]
  G --> E
  M --> E
  H --> E
""",
    "52-harness-engineering.md": """
flowchart TD
  U[用户目标] --> H[Agent Harness]
  H --> C[Context Builder]
  H --> T[Tool Registry]
  H --> S[Sandbox / Workspace]
  H --> P[Policy / Approval]
  H --> O[Trace / Evaluation]
  C --> M[Model]
  M --> H
  T --> E[外部系统]
  S --> E
""",
    "53-design-minimal-agent-runtime.md": """
flowchart TD
  READY --> BUILD_CONTEXT
  BUILD_CONTEXT --> MODEL_INFERENCE
  MODEL_INFERENCE -->|tool_call| VALIDATE
  MODEL_INFERENCE -->|final| VERIFY_COMPLETION
  MODEL_INFERENCE -->|approval| WAITING_APPROVAL
  VALIDATE --> AUTHORIZE
  AUTHORIZE --> EXECUTE_TOOL
  EXECUTE_TOOL --> APPEND_EVENT
  APPEND_EVENT --> CHECKPOINT
  CHECKPOINT --> BUILD_CONTEXT
  VERIFY_COMPLETION -->|通过| SUCCEEDED
  VERIFY_COMPLETION -->|未通过| BUILD_CONTEXT
  WAITING_APPROVAL --> CHECKPOINT
""",
    "54-function-calling-end-to-end.md": """
sequenceDiagram
  participant U as User
  participant A as Agent Runtime
  participant M as Model
  participant T as Tool
  U->>A: 提交任务
  A->>M: Context + Tool Schema
  M-->>A: ToolCall
  A->>A: 校验 权限 审批 幂等
  A->>T: Execute
  T-->>A: ToolResult
  A->>A: Event + Checkpoint
  A->>M: ToolResult + Updated Context
  M-->>A: Final
  A-->>U: 验证后的结果
""",
    "55-agent-state-and-message-protocol.md": """
flowchart LR
  E[Event Log 不可变事件] --> R[Reducer]
  R --> S[RunState 当前真相]
  S --> C[Context Builder]
  C --> M[Model Messages 投影]
  M --> D[ModelDecision]
  D --> E2[新事件 ToolCall Result StatePatch]
  E2 --> E
  S --> K[Checkpoint]
""",
    "56-context-builder-and-token-budget.md": """
flowchart TD
  B[总 Token Budget] --> S1[System 与安全规则]
  B --> S2[当前目标与计划]
  B --> S3[最近对话]
  B --> S4[工具证据]
  B --> S5[检索知识与 Memory]
  S1 --> P[优先级裁剪]
  S2 --> P
  S3 --> P
  S4 --> P
  S5 --> P
  P --> C[压缩 去重 引用]
  C --> M[最终 Context]
""",
    "57-stop-conditions-and-loop-detection.md": """
flowchart TD
  S[当前 State] --> H[步数 时间 Token 成本硬限制]
  S --> R[重复动作与周期检测]
  S --> P[状态进展度检测]
  S --> V[业务完成验证]
  H --> D{Stop Policy}
  R --> D
  P --> D
  V --> D
  D -->|continue| N[下一轮]
  D -->|replan| RP[重规划]
  D -->|pause| A[人工或外部输入]
  D -->|terminal| T[成功或失败结束]
""",
    "58-checkpoint-pause-resume-idempotency.md": """
flowchart TD
  A[动作准备] --> P[记录 Pending Effect + 幂等键]
  P --> E[执行外部副作用]
  E --> R[记录 Effect Result]
  R --> C[保存 Checkpoint]
  C --> N[进入下一状态]
  X[服务重启] --> L[加载最新 Checkpoint]
  L --> Q{Effect 是否已有结果}
  Q -->|有| N
  Q -->|无| E
""",
    "59-async-long-running-tools.md": """
stateDiagram-v2
  [*] --> CREATED
  CREATED --> SUBMITTED
  SUBMITTED --> RUNNING
  RUNNING --> WAITING_CALLBACK
  WAITING_CALLBACK --> RUNNING: progress event
  RUNNING --> SUCCEEDED
  RUNNING --> FAILED
  RUNNING --> RETRY_WAIT
  RETRY_WAIT --> RUNNING
  CREATED --> CANCELLED
  SUBMITTED --> CANCELLED
  RUNNING --> CANCELLED
  SUCCEEDED --> [*]
  FAILED --> [*]
  CANCELLED --> [*]
""",
    "60-parallel-tool-dependency-scheduler.md": """
flowchart LR
  P[Tool Calls] --> D[依赖与读写集合分析]
  D --> A[批次 1]
  A --> T1[读取日志]
  A --> T2[读取发布记录]
  T1 --> J[Join Evidence]
  T2 --> J
  J --> B[批次 2]
  B --> T3[执行诊断]
  T3 --> V[验证与提交状态]
""",
    "61-planner-executor-replanner.md": """
flowchart TD
  G[Goal] --> P[Planner]
  P --> PL[Plan: 可执行 可验收步骤]
  PL --> E[Executor 执行当前步骤]
  E --> O[Observation]
  O --> V{验收通过}
  V -->|是| N{计划完成}
  N -->|否| E
  N -->|是| F[Final]
  V -->|否| R[Replanner]
  R --> PP[最小 Plan Patch]
  PP --> E
""",
    "62-human-in-the-loop-approval-state-machine.md": """
stateDiagram-v2
  [*] --> PROPOSED
  PROPOSED --> VALIDATED
  VALIDATED --> WAITING_APPROVAL: high risk
  VALIDATED --> EXECUTING: low risk
  WAITING_APPROVAL --> REJECTED: reject
  WAITING_APPROVAL --> REVALIDATING: approve
  REVALIDATING --> WAITING_APPROVAL: resource changed
  REVALIDATING --> EXECUTING: still valid
  EXECUTING --> SUCCEEDED
  EXECUTING --> FAILED
  REJECTED --> [*]
  SUCCEEDED --> [*]
  FAILED --> [*]
""",
    "63-agent-trace-replay-failure-attribution.md": """
flowchart LR
  R[一次 Agent Run] --> S1[Model Span]
  R --> S2[Tool Span]
  R --> S3[State Transition]
  R --> S4[Checkpoint / Approval]
  S1 --> T[统一 Trace]
  S2 --> T
  S3 --> T
  S4 --> T
  T --> P[Replay 重放]
  P --> C[与基线轨迹比较]
  C --> F[定位最早致错点]
  F --> E[修复并回归评测]
""",
}


def render_block(diagram: str) -> str:
    body = dedent(diagram).strip()
    return f"{START}\n\n## 可视化图解\n\n```mermaid\n{body}\n```\n\n{END}"


def upsert(content: str, block: str) -> str:
    if START in content and END in content:
        before, rest = content.split(START, 1)
        _, after = rest.split(END, 1)
        return before.rstrip() + "\n\n" + block + after

    anchors = ["\n## 核心结论", "\n## 先建立直觉", "\n## 一、", "\n## 完整链路"]
    positions = [content.find(anchor) for anchor in anchors if content.find(anchor) >= 0]
    if positions:
        pos = min(positions)
        return content[:pos].rstrip() + "\n\n" + block + "\n\n" + content[pos:].lstrip()

    lines = content.splitlines()
    insert_at = 1
    while insert_at < len(lines) and not lines[insert_at].startswith("## "):
        insert_at += 1
    lines[insert_at:insert_at] = ["", block, ""]
    return "\n".join(lines).rstrip() + "\n"


def ensure_mkdocs_config() -> bool:
    path = ROOT / "mkdocs.yml"
    text = path.read_text(encoding="utf-8")
    old = "  - pymdownx.superfences\n"
    new = dedent(
        """
          - pymdownx.superfences:
              custom_fences:
                - name: mermaid
                  class: mermaid
                  format: !!python/name:pymdownx.superfences.fence_code_format
        """
    )
    if "custom_fences:" not in text:
        if old not in text:
            raise RuntimeError("pymdownx.superfences entry not found in mkdocs.yml")
        text = text.replace(old, new, 1)
        path.write_text(text, encoding="utf-8")
        return True
    return False


def ensure_css() -> bool:
    path = QUESTIONS / "stylesheets" / "extra.css"
    text = path.read_text(encoding="utf-8")
    marker = "/* Mermaid diagrams */"
    if marker in text:
        return False
    addition = dedent(
        """

        /* Mermaid diagrams */
        .md-typeset .mermaid {
          margin: 1.4rem 0;
          text-align: center;
          overflow-x: auto;
        }

        .md-typeset .mermaid svg {
          display: inline-block;
          max-width: 100%;
          height: auto;
        }

        @media screen and (max-width: 600px) {
          .md-typeset .mermaid {
            margin-left: -0.35rem;
            margin-right: -0.35rem;
          }
        }
        """
    )
    path.write_text(text.rstrip() + addition + "\n", encoding="utf-8")
    return True


def main() -> None:
    changed: list[str] = []
    for filename, diagram in DIAGRAMS.items():
        path = QUESTIONS / filename
        if not path.exists():
            raise FileNotFoundError(path)
        original = path.read_text(encoding="utf-8")
        updated = upsert(original, render_block(diagram))
        if updated != original:
            path.write_text(updated, encoding="utf-8")
            changed.append(str(path.relative_to(ROOT)))

    if ensure_mkdocs_config():
        changed.append("mkdocs.yml")
    if ensure_css():
        changed.append("questions/stylesheets/extra.css")

    print(f"Updated {len(changed)} files")
    for item in changed:
        print(item)


if __name__ == "__main__":
    main()
