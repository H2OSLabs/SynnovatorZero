# 建议索引

本文档定义 Synnovator 平台的数据库索引建议，供开发实现参考。

> 数据类型定义详见 [docs/data-types.md](../docs/data-types.md)，关系定义详见 [docs/relationships.md](../docs/relationships.md)。

---

## 索引列表

| 索引 | 字段 | 用途 |
|------|-----|------|
| 内容列表查询 | `(type, status, deleted_at, created_at DESC)` | event/post 列表按状态和时间排序 |
| 用户内容查询 | `(created_by, deleted_at, created_at DESC)` | 查询某用户创建的所有内容 |
| 交互记录查询 | `target:interaction` 关系表 `(target_type, target_id)` + interaction `(type, deleted_at)` | 通过关系表查询目标的点赞/评论/评分 |
| 嵌套评论查询 | `(parent_id, deleted_at, created_at)` | 查询评论的子回复 |
| 分组成员查询 | `(group_id, status)` | 查询分组的有效成员 |
| 活动报名查询 | `(event_id)` on event:group | 查询活动的报名团队 |
| 用户关注查询 | `user:user` 关系表 `(source_user_id, relation_type)` | 查询用户的关注列表 |
| 用户粉丝查询 | `user:user` 关系表 `(target_user_id, relation_type)` | 查询用户的粉丝列表 |
| 活动赛段查询 | `event:event` 关系表 `(source_category_id, relation_type, stage_order)` | 查询活动的赛段/赛道/前置条件 |
| 软删除过滤 | `(deleted_at)` on 所有内容类型 | 加速 `deleted_at IS NULL` 过滤 |
