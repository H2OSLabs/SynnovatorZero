# 6. 社交互动与反馈

- **角色：** 已登录用户（点赞/评论/关注）；评委/组织者（评分）
- **前置条件：** 已登录，目标内容对当前用户可见

## 6.1 点赞

| 用户旅程 | 说明 | 数据操作 |
|---------|------|---------|
| 点赞帖子 | 对喜欢的帖子点赞 | `CREATE interaction`（type: like, target_type: post） |
| 取消点赞 | 取消之前的点赞 | `DELETE interaction`（type: like） |
| 查看点赞数 | 查看帖子的点赞统计 | `READ post`（like_count 缓存字段） |

## 6.2 评论

| 用户旅程 | 说明 | 数据操作 |
|---------|------|---------|
| 发表评论 | 对帖子发表评论 | `CREATE interaction`（type: comment） |
| 回复评论 | 回复他人的评论 | `CREATE interaction`（type: comment, parent_id） |
| 删除评论 | 删除自己发表的评论 | `DELETE interaction`（软删除） |
| 查看评论列表 | 查看帖子下的所有评论 | `READ interaction`（type: comment, target_id） |

## 6.3 评分

| 用户旅程 | 说明 | 数据操作 |
|---------|------|---------|
| 评委打分 | 评委对参赛帖子进行打分 | `CREATE interaction`（type: rating） |
| 修改评分 | 评委修改之前的评分 | `UPDATE interaction`（type: rating） |
| 查看平均分 | 查看帖子的平均评分 | `READ post`（average_rating 缓存字段） |

**约束：**
- 只有被指定为活动评委的用户才能打分
- 每个评委对同一帖子只能打一次分（可修改）
- 评分值需在规则定义的范围内

## 6.4 缓存字段维护

以下缓存字段由系统自动维护：

| 字段 | 更新触发 | 说明 |
|------|---------|------|
| `like_count` | 点赞/取消点赞时 | 帖子的点赞总数 |
| `comment_count` | 评论/删除评论时 | 帖子的评论总数 |
| `average_rating` | 评分/修改评分时 | 帖子的平均评分 |
