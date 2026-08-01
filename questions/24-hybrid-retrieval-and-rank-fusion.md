# BM25 与向量检索如何做混合召回和结果融合？

- ID：Q024
- 难度：进阶 / 系统设计
- 标签：BM25、Dense Retrieval、Hybrid Search、RRF、加权融合

## 同义问法

- 关键词检索和向量检索为什么要一起用？
- 两路应该召回相同数量吗？
- BM25 分数和余弦相似度怎么合并？
- RRF 是什么？
- 如何动态调整两路召回比例？

## 来源

- 用户提供的二手题库：`3.10`、`3.11`
- Elasticsearch 官方 Hybrid Search 与 RRF 文档：
  - https://www.elastic.co/docs/solutions/search/hybrid-search
  - https://www.elastic.co/docs/reference/elasticsearch/rest-apis/reciprocal-rank-fusion

## 核心结论

**BM25 与向量检索不是互相替代，而是在捕获不同类型的相关性。** BM25 擅长精确 Token、稀有词、错误码和标识符；Dense Retrieval 擅长同义表达和语义意图。混合检索的难点不是“各取 Top-10”，而是候选预算、分数不可比、重复结果、过滤和最终排序。

## 一、两路检索分别擅长什么

### BM25 / 词法检索

优势：

- 错误码、订单号、类名、产品型号；
- 专有名词和稀有 Token；
- 关键词可解释；
- 新文档无需重新训练语义模型。

弱点：同义词、自然语言改写和跨语言能力有限。

### Dense Retrieval

优势：

- 同义表达；
- Query 与文档词面差异大；
- 意图和主题匹配；
- 自然语言问答。

弱点：精确标识符可能被语义“平均掉”，也容易召回主题相似但不能回答的内容。

## 二、为什么分数不能直接相加

BM25 分数没有固定上限，不同 Query 的分布也不同；余弦相似度或内积又是另一套尺度。直接：

```text
score = bm25_score + vector_score
```

会让某一路因数值范围更大而支配结果。

解决方案有两类。

## 三、融合方法

### 1. Reciprocal Rank Fusion（RRF）

RRF 不依赖原始分数，只看文档在各列表中的排名：

```text
RRF(d) = Σ 1 / (k + rank_i(d))
```

优势：

- 不需要校准两路分数；
- 对单路异常值不敏感；
- 实现简单，是很好的默认方案。

缺点：丢失了分数置信度信息；如果某一路本身质量很差，它仍会贡献排名分。

### 2. 分数归一化 + 加权融合

先对每路分数做 Min-Max、Z-score 或基于历史分布的校准，再加权：

```text
final = α * normalized_bm25 + (1-α) * normalized_dense
```

优势：可表达业务偏好和置信度。

缺点：归一化对 Query 分布敏感，权重需要通过评测或学习得到。

### 3. 学习排序或 Reranker

混合召回只负责扩大候选集，再由 Cross-Encoder 或 LLM Reranker 统一判断 Query–Document 相关性。这通常效果最好，但增加延迟和成本。

## 四、两路召回数量是否相同

不需要。候选数量应该由以下因素决定：

- Query 类型；
- 各路历史 Recall；
- Reranker 吞吐预算；
- 去重后有效候选数；
- 权限过滤后的剩余量。

可采用动态预算：

```text
含错误码/ID/类名
  → BM25 召回更多

自然语言解释、同义改写
  → Dense 召回更多

路由置信度低
  → 两路都扩大候选，但限制总预算
```

初始可以 1:1 作为基线，但最终必须通过 Query 分桶评测，而不是形成永久规则。

## 五、完整流程

```text
Original Query
   ├── BM25 Search ────── Top-N1
   └── Dense Search ───── Top-N2
                │
                ▼
        Permission Filter
                │
                ▼
        Deduplicate / Merge
                │
                ▼
          RRF or Weighted Fusion
                │
                ▼
             Reranker
                │
                ▼
          Diversity / Context Build
```

注意权限过滤的位置。如果数据库支持安全的 Pre-filter，应尽量在检索阶段限制租户和 ACL；不能先检索越权文档再依赖生成层隐藏。

## 六、去重与多样性

同一文档的相邻 Chunk 可能占满 Top-K。需要：

- 按 `document_id + section` 去重；
- 限制单文档最大块数；
- 合并相邻块；
- 使用 MMR 或业务规则增加结果多样性。

但多样性不能机械执行。对于一个需要完整异常栈的问题，同一来源的连续片段可能正是必要证据。

## 七、评估方式

分 Query 类型统计：

- BM25-only Recall@K；
- Dense-only Recall@K；
- Hybrid Recall@K；
- Rerank 后 NDCG / MRR；
- 候选重复率；
- P95 延迟；
- 端到端答案正确率。

必须保留单路结果用于故障归因，否则只看到最终答案错误，不知道是关键词、语义、融合还是重排出了问题。

## 常见错误回答

> 关键词和向量各召回 10 条，然后拼起来。

这只是候选并集，没有解决分数、重复、预算和排序。

> 向量检索更先进，可以完全替代 BM25。

在错误码、文件名、API 名和编号场景中，词法检索通常不可替代。

## 面试口述版

> BM25 捕获精确词法信号，Dense Retrieval 捕获语义信号，两者互补。由于原始分数不可直接比较，我会先各自召回、做权限过滤和去重，再用 RRF 作为稳定基线，必要时做分数校准或交给 Cross-Encoder 重排。两路数量不必相同，可以根据 Query 是否包含错误码、ID、专有名词动态分配，但总候选受 Reranker 延迟预算约束。评估时分别保留单路和融合结果，才能定位问题发生在哪层。

## 结合个人项目

CI/CD 日志中的 `NoSuchMethodError`、`dubbo.properties`、Pod 名和 Commit SHA 依赖精确匹配；“更换 JDK 后服务起不来”则适合语义检索。混合召回比单纯向量库更符合这个数据分布。