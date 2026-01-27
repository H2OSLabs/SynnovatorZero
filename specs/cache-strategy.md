# 缓存统计字段规范

本文档定义 Synnovator 平台中 post 缓存统计字段的维护策略和一致性模型。

> 数据类型定义详见 [docs/data-types.md](../docs/data-types.md)，CRUD 操作详见 [docs/crud-operations.md](../docs/crud-operations.md)。

---

## 缓存字段

以下字段为**只读缓存**，不支持手动 UPDATE，仅由系统在 `target:interaction` 关系变更时自动维护。

| 缓存字段 | 触发条件 | 计算逻辑 |
|---------|---------|---------|
| `like_count` | `target:interaction` 关系的 CREATE / DELETE（关联的 interaction type=like） | `COUNT(*)` 通过 `target:interaction` 关联的未删除 like interaction |
| `comment_count` | `target:interaction` 关系的 CREATE / DELETE（关联的 interaction type=comment） | `COUNT(*)` 通过 `target:interaction` 关联的未删除 comment interaction（含嵌套回复） |
| `average_rating` | `target:interaction` 关系的 CREATE / DELETE（关联的 interaction type=rating） | 通过 `target:interaction` 关联的所有未删除 rating interaction 的加权总分均值（权重来自 rule.scoring_criteria） |

---

## 一致性模型

- **最终一致性**：缓存字段在 interaction 变更后异步更新，短暂延迟可接受
- **全量重算**：每次触发时对该 post 的所有有效 interaction 重新计算，而非增量更新，确保数据准确
- **缓存重建**：提供管理员命令，可对指定 post 或全量 post 重建缓存统计
- **容错机制**：缓存更新失败时记录日志，不影响 interaction 本身的写入；下次触发时自动修正
