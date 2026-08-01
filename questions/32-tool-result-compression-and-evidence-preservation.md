# 工具返回结果过大时，如何裁剪、压缩并保留证据？

- ID：Q032
- 难度：进阶 / 手撕设计
- 标签：Tool Result、Context Compression、Evidence、Pagination、Artifact Store

## 同义问法

- 工具结果挤爆上下文怎么办？
- 日志返回几十 MB 怎么给 Agent？
- LLM 总结工具结果会不会丢证据？
- Tool 输出应该返回文本、结构化数据还是文件？
- 如何按需展开被裁剪内容？

## 来源

- 用户提供的二手题库：`5.3`

## 核心结论

**大结果处理不是简单截断，而是把“原始证据存储”和“模型工作上下文”分离。** 工具应返回小而结构化的观察、统计和证据引用；原始结果保存到 Artifact Store，模型需要时通过分页、过滤或 Drill-down 工具继续读取。

## 一、为什么不能直接全部塞入 Context

风险包括：

- 超出 Token Window；
- 关键错误被大量正常记录淹没；
- 输入成本和延迟上升；
- 重复结果在后续循环持续膨胀；
- 敏感字段泄露；
- 模型无法判断哪些内容被截断。

直接 `result[:10000]` 更危险：可能截掉异常结尾、JSON 右括号、表格表头或堆栈根因，而且模型不知道结果不完整。

## 二、分层结果模型

推荐工具返回：

```json
{
  "status": "success",
  "summary": "10:03 后错误率上升，主要异常为 connection timeout",
  "statistics": {
    "total_lines": 128430,
    "error_lines": 817,
    "unique_error_signatures": 6
  },
  "items": [
    {
      "signature": "upstream_timeout",
      "count": 642,
      "sample_refs": ["artifact://logs-88#L1201-L1240"]
    }
  ],
  "artifact_ref": "artifact://logs-88",
  "truncated": true,
  "next_actions": ["get_log_context", "list_error_signatures"]
}
```

这里有四层：

1. 模型立即可用的摘要；
2. 可比较的结构化统计；
3. 少量代表性样本；
4. 可回溯的原始 Artifact 引用。

## 三、优先在工具端减少数据

最有效的压缩不是让另一个 LLM 总结，而是让查询本身更精确：

- 时间范围；
- 租户、服务、环境；
- 字段 Projection；
- 错误级别；
- 聚合和 Group By；
- Pagination / Cursor；
- 只取变化内容；
- 最大行数和最大字节数。

例如日志工具不要只有：

```text
get_logs(service)
```

而应支持：

```text
get_logs(service, start, end, level, pattern, fields, cursor, limit)
```

但参数也不能无限复杂。可以提供“搜索、聚合、展开上下文”三个层次化工具。

## 四、结构化裁剪

对于 JSON：

- 只保留业务需要字段；
- 对大数组分页；
- 对嵌套对象保存 ID 和关键属性；
- 明确记录被移除字段；
- 保持 Schema 有效。

对于日志：

- 错误签名聚类；
- 保留首尾时间、频率和代表样本；
- 异常栈保留 `Caused by` 链与必要上下文；
- 相邻重复行压缩；
- 支持按证据引用回取原文。

对于搜索结果：

- 去重相同 URL / 文档；
- 每条保留标题、摘要、来源和时间；
- 正文延迟加载。

## 五、LLM 压缩的正确位置

LLM 适合把已经过滤后的中等结果压缩成任务相关摘要，不适合直接吞下无限原始数据。

压缩 Prompt 要求输出：

- 已确认事实；
- 异常和冲突；
- 仍缺信息；
- 原始 evidence_ref；
- 不得补充输入之外的结论。

摘要和原文必须分别保存。后续关键决策应能够回到原始证据验证，避免“摘要的摘要”不断累积误差。

## 六、渐进披露（Progressive Disclosure）

```text
Level 0：工具元数据和能力说明
Level 1：结果摘要与统计
Level 2：命中项和代表样本
Level 3：指定区间 / 指定记录详情
Level 4：完整 Artifact 下载或离线处理
```

Agent 每次只加载完成当前决策所需的最低层级。这个模式也适用于大型代码仓库和数据库结果。

## 七、Token Budget 分配

Context Builder 需要为 Tool Result 设置独立预算：

```text
总窗口
- System / Policy
- 当前目标与状态
- 最近交互
- 计划
- 证据预算
- 输出预留
```

工具返回超过预算时，按优先级保留：

1. 与当前子目标直接相关的事实；
2. 错误与冲突；
3. 最新观察；
4. 可回溯引用；
5. 代表性样本。

不是简单保留最近 N 条。

## 八、安全与隐私

压缩前执行：

- PII / Secret 脱敏；
- 行级权限过滤；
- 文件路径和内部 Token 清洗；
- Artifact 访问授权和过期时间；
- 审计谁读取了完整原文。

不能先把敏感原始结果交给模型，再在最终输出阶段脱敏。

## 九、失败语义

当结果被截断或摘要时必须显式告知模型：

```json
{
  "truncated": true,
  "coverage": "2026-08-01 10:00-10:05",
  "missing_reason": "byte_limit",
  "continuation_cursor": "cursor-19"
}
```

否则模型会把部分结果误当完整结果。

## 常见错误回答

> 只保留需要的字段，再让 LLM 总结。

没有说明“需要”由谁判断、原始证据如何保存、摘要如何验证以及如何继续展开。

> 超过长度直接截断。

截断破坏结构且隐藏覆盖范围，是最差兜底之一。

## 面试口述版

> 我会把原始工具结果和模型观察分开。工具端先通过时间、字段、过滤、聚合和分页减少数据，再返回结构化摘要、统计、代表样本、是否截断以及 artifact_ref。原始日志或文件放在受权限控制的 Artifact Store，Agent 可以用 Drill-down 工具按证据引用读取指定区间。LLM 压缩只处理已过滤结果，并且每条结论保留原始引用。这样既控制 Token，也不会让摘要成为无法验证的新事实源。

## 延伸阅读

- [Q056 手写 Context Builder 与 Token Budget](./56-context-builder-and-token-budget.md)

## 结合个人项目

Tomcat 或 Go 服务日志不应该整文件塞给模型。先由脚本识别启动阶段、异常签名、时间线和 `Caused by` 链，模型看到结构化证据；需要判断时再读取原始行区间。