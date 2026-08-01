# 字节跳动 Agent Engineer 面试题

## 方向

Agent 工程师 / 大模型应用工程师

---

# Q1: 如何设计一个 Agent 系统？

## 考察点

- Agent架构理解
- Runtime设计
- Tool调用
- 状态管理

## 基础回答

一个 Agent 系统通常包含：

```
User
 |
Agent Runtime
 |
LLM
 |
Tool
 |
Environment
```

Runtime负责：

- 管理任务状态
- 调度工具
- 控制循环
- 记录上下文

---

# Q2: Agent 为什么需要 Tool？

LLM本身只有语言能力，没有实时数据和执行能力。

Tool让Agent具备：

- 查询能力
- 操作能力
- 外部系统交互能力

例如：

Coding Agent 使用：

- git
- shell
- 文件系统
- 编译工具

---

# Q3: 如何解决 Agent Context 太长？

常见方案：

- 历史摘要
- 信息裁剪
- 检索相关内容
- 分阶段执行

生产环境需要 Context Engineering。

---

# Q4: 如何设计 Coding Agent？

核心模块：

- Repo理解
- Context管理
- 文件修改
- Tool执行
- 测试验证
- Diff审查

结合工程：

类似 Claude Code，需要 Sandbox、Runtime、工具管理和安全隔离。