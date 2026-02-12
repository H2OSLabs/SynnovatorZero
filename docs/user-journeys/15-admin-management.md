# 15. 管理员行为与系统审计

- **角色：** 系统管理员 (Admin) / 运营人员
- **前置条件：** 拥有 Admin 角色权限
- **说明：** 涵盖内容治理、活动仲裁、团队管控、资源审计及系统安全等高级管理功能。

## 15.1 首页运营管理

| 用户旅程 | 说明 | 数据操作 |
|---------|------|---------|
| 首页置顶 | 管理员选择特定帖子固定在首页置顶栏，用于推广重要内容 | `UPDATE post` (is_pinned=true, pinned_at=timestamp) |
| 海报栏配置 | 管理员配置首页滚动海报栏的内容（图片、链接、顺序） | `UPDATE system_config` (carousel_items) |

## 15.2 内容与资产审计

| 用户旅程 | 说明 | 数据操作 |
|---------|------|---------|
| 违规内容干预 | 对被举报或系统识别的违规帖子、提案执行“软删除” | `UPDATE post` (status=deleted, deletion_reason=...) |
| 资源回收与管理 | 查看所有上传的 Resource，清理长时间未关联且已过期的孤立资源 | `DELETE resource` (条件：no_relations + expired) |
| 官方标识管理 | 为特定账号（如 AI 评论员、企业出题方）授予“官方”或“认证”标识 | `UPDATE user` (is_verified=true, verification_type=official/ai/enterprise) |

## 15.3 活动与星球仲裁 (Activity Arbitration)

| 用户旅程 | 说明 | 数据操作 |
|---------|------|---------|
| 规则临时调整 | 在特殊情况下（如不可抗力），修改进行中活动的 Rule 约束（如延长提交截止时间） | `UPDATE rule` (end_time, deadlines) |
| 评审异常处理 | 若发现评委评分异常（作弊/刷分），废弃特定 Rating 记录并重新计算平均分 | `UPDATE interaction` (status=voided) + `recalc_post_rating()` |
| 手动版本归档 | 对于纠纷导致无法正常结束的活动，强制执行“自动副本生成并归档”操作 | `trigger_event_closure_workflow(force=true)` |

## 15.4 团队与成员管控

| 用户旅程 | 说明 | 数据操作 |
|---------|------|---------|
| 纠纷强制裁决 | 若队长失联或违规，管理员执行“变更队长”或“强制解散团队” | `UPDATE group` (owner_id) / `DELETE group` |
| 成员变更豁免 | 在规则限制变更成员期间，因极端情况手动绕过约束增减成员 | `CREATE/DELETE group:user` (bypass_rules=true) |

## 15.5 奖励与结算审计

| 用户旅程 | 说明 | 数据操作 |
|---------|------|---------|
| 资产重发与撤回 | 修复系统故障导致的证书/勋章发放错误，撤回关系并重新发放 | `DELETE user:resource` + `CREATE user:resource` |
| 投票权池管理 | 监控“勋章投票”消耗，针对非法刷票行为进行票数作废处理 | `UPDATE interaction` (type=vote, status=voided) |

## 15.6 系统安全与反作弊

| 用户旅程 | 说明 | 数据操作 |
|---------|------|---------|
| 流量与访问控制 | 监控 Captcha 触发频率，手动锁定异常 IP 或账号 | `UPDATE user` (status=locked) / `BLOCK ip` |
| AI 算力池审计 | 监控“AI 评论员”算力消耗，调整不同角色的调用速率限制 | `UPDATE rate_limit_config` |

## 15.8 活动审核 (Activity Audit)

管理员对组织者提交的活动进行合规性审查，并确认资产冻结情况。

| 用户旅程 | 说明 | 数据操作 |
|---------|------|---------|
| 待审列表查看 | 筛选所有状态为 `pending_review` 的活动 | `READ event` (status=pending_review) |
| 审核通过 | 批准活动发布。系统自动触发 AssetPool 冻结检查，若成功则活动上线 | `UPDATE event` (status=published) + `AssetPool.freeze()` |
| 审核驳回 | 拒绝活动发布，需填写驳回原因。活动回退至草稿状态 | `UPDATE event` (status=draft, reject_reason=...) |

## 15.9 平台数据监控 (Platform Data Monitoring)

平台级宏观数据**仅管理员可见**，严禁对普通用户展示：

| 数据类型 | 指标示例 | 权限要求 |
|---------|---------|---------|
| **用户增长数据** | 平台总注册用户数、日活跃用户 (DAU)、新增注册趋势 | `READ system_stats` (role=admin) |
| **内容总量数据** | 平台总内容数 (Posts)、总资源数 (Resources)、总活动数 | `READ system_stats` (role=admin) |
| **系统运行指标** | API 调用总量、存储占用情况、服务器负载状态 | `READ system_health` (role=admin) |

> **注意：** 任何涉及平台整体规模、运营健康度的数据均为内部敏感信息。
