# Agent Interview

面向中国大陆 **Agent Engineer / 大模型应用工程师 / AI 应用后端工程师** 岗位的深度面试知识库。

## 在线学习

**GitHub Pages：<https://orangle.github.io/agent-interview/>**

站点使用 MkDocs Material 构建，支持：

- 手机、平板和 PC 响应式阅读；
- 左侧题目导航和页内目录；
- 中文全文搜索；
- 深色 / 浅色模式；
- 代码块复制；
- 每次推送到 `main` 后自动部署。

## 当前进度

- 原始题库问法：115
- 去重后的主问题：52
- 国内面试原理手撕题：11
- **已完成：63 / 63**

入口：

- [完整题目索引](./questions/BACKLOG.md)
- [Agent 原理与手撕专题](./questions/PRINCIPLES.md)
- [学习路线](./questions/README.md)

## 内容原则

### 精度优先于数量

不堆只有几行答案的八股。每道宽泛题回答定义、机制、工程实现、失败边界、方案取舍和项目经验。

### 同义问题只保留一次

不同公司和面经出现的同义题合并为一个主问题，在题内记录来源和不同问法。

### 小白能够理解，面试深度不降低

先建立直觉，再进入状态、数据结构、算法、生产异常和 Trade-off。目标是能够继续应对追问，而不是背名词。

### 原理题能够现场手写

手撕专题要求脱离 LangChain、LangGraph 等框架，画出：

- Agent 状态机；
- Function Calling 链路；
- Context Builder；
- Checkpoint 和恢复；
- 异步与并行工具调度；
- Planner–Executor–Replanner；
- HITL 审批；
- Trace、Replay 和故障归因。

## 目录

```text
.
├── README.md
├── mkdocs.yml
├── requirements-docs.txt
├── .github/workflows/pages.yml
├── questions/
│   ├── index.md
│   ├── BACKLOG.md
│   ├── PRINCIPLES.md
│   ├── 01-...md
│   └── 63-...md
├── projects/
│   └── personal-experience-map.md
└── intake/
    └── 原始题库导入记录
```

## 学习方式

1. 不看答案，先口述 2～5 分钟；
2. 对照核心机制、失败模式和取舍；
3. 用自己的 CI/CD Agent、Coding Agent 平台或 OpenSandbox 项目重答；
4. 原理题画状态机和数据流；
5. 不依赖具体框架写伪代码；
6. 学习后的疑问和反例继续回写对应题目。

## 本地预览

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements-docs.txt
mkdocs serve
```

访问 `http://127.0.0.1:8000`。

## 来源规则

1. 面经用于证明问题真实出现过；
2. 协议规范、论文和官方工程文档用于校验技术答案；
3. 动态产品和协议标注整理日期；
4. 无法确认的数字、榜单和经验结论不写成确定事实。