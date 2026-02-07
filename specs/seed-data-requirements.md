# 种子数据需求清单

> **本文档由阶段 2.5 (种子数据设计) 生成**
>
> 每条种子数据都必须映射到具体的测试用例，确保种子数据不是随意编造的，而是从测试用例前置条件系统性推导出来。

---

## 用户数据

| 标识 | 角色 | 用途 | 关联测试用例 |
|------|------|------|-------------|
| user_participant_1 | participant | 主要参赛者，用于帖子创建、活动报名 | TC-POST-001~076, TC-ENTRY-001~010 |
| user_participant_2 | participant | 次要参赛者，用于团队成员、关注测试 | TC-GRP-020~025, TC-FRIEND-001~010 |
| user_organizer_1 | organizer | 活动创建者，用于活动/规则管理 | TC-CAT-001~020, TC-RULE-001~020 |
| user_admin_1 | admin | 管理员，用于权限和管理操作测试 | TC-PERM-001~025 |

---

## 活动数据

| 标识 | 状态 | 规则 | 用途 | 关联测试用例 |
|------|------|------|------|-------------|
| cat_hackathon_1 | published | rule_entry_1, rule_submit_1 | 主要测试活动，开放报名/提交 | TC-ENTRY-*, TC-POST-050~076 |
| cat_draft_1 | draft | 无 | 草稿活动测试 | TC-CAT-002, TC-CAT-900 |
| cat_closed_1 | closed | rule_close_1 | 闭幕规则测试 | TC-CLOSE-001~040 |

---

## 规则数据

| 标识 | 类型 | 关联活动 | 关联测试用例 |
|------|------|---------|-------------|
| rule_entry_1 | entry | cat_hackathon_1 | TC-ENTRY-001~010, TC-ENGINE-001~020 |
| rule_submit_1 | submission | cat_hackathon_1 | TC-POST-050~076, TC-ENGINE-021~040 |
| rule_close_1 | closing | cat_closed_1 | TC-CLOSE-001~040 |

---

## 帖子数据

| 标识 | 类型 | 状态 | 所属活动 | 创建者 | 关联测试用例 |
|------|------|------|---------|--------|-------------|
| post_daily_1 | daily | published | 无 | user_participant_1 | TC-POST-001~010, TC-IACT-001~030 |
| post_daily_2 | daily | draft | 无 | user_participant_1 | TC-POST-002 |
| post_proposal_1 | proposal | published | cat_hackathon_1 | user_participant_1 | TC-POST-050~076 |

---

## 团队数据

| 标识 | 可见性 | 所有者 | 成员 | 关联测试用例 |
|------|-------|--------|------|-------------|
| group_public_1 | public | user_participant_1 | user_participant_2 (member) | TC-GRP-001~025, TC-REL-GU-* |
| group_private_1 | private | user_participant_2 | 无 | TC-GRP-010~015 |

---

## 交互数据

| 标识 | 类型 | 目标 | 创建者 | 关联测试用例 |
|------|------|------|--------|-------------|
| iact_like_1 | like | post_daily_1 | user_participant_2 | TC-IACT-001~010 |
| iact_comment_1 | comment | post_daily_1 | user_participant_2 | TC-IACT-011~020 |
| iact_rating_1 | rating | post_proposal_1 | user_organizer_1 | TC-IACT-021~030 |

---

## 关系数据

| 关系类型 | 源 | 目标 | 元数据 | 关联测试用例 |
|----------|-----|------|--------|-------------|
| group_user | group_public_1 | user_participant_1 | role=owner | TC-REL-GU-001~010 |
| group_user | group_public_1 | user_participant_2 | role=member | TC-REL-GU-011~020 |
| category_rule | cat_hackathon_1 | rule_entry_1 | - | TC-REL-CR-001~010 |
| category_rule | cat_hackathon_1 | rule_submit_1 | - | TC-REL-CR-001~010 |
| category_post | cat_hackathon_1 | post_proposal_1 | relation=submission | TC-REL-CP-001~020 |
| target_interaction | post_daily_1 | iact_like_1 | - | TC-REL-TI-001~010 |
| user_user | user_participant_1 | user_participant_2 | relation=follow | TC-FRIEND-001~010 |

---

## 维护说明

### 如何更新本文档

1. **添加新测试用例时**：检查测试用例的前置条件，如果需要新的种子数据，在本文档对应表格中添加
2. **修改测试用例时**：检查对应的种子数据是否仍然适用，必要时更新
3. **删除测试用例时**：检查对应的种子数据是否被其他测试用例使用，如果不再使用则删除

### 种子脚本同步

本文档的每条数据都应在 `scripts/seed_dev_data.py` 中有对应的注入代码：

```python
def seed_users():
    """
    用户种子数据
    数据来源: specs/seed-data-requirements.md > 用户数据
    """
    # user_participant_1: TC-POST-*, TC-ENTRY-*
    # user_participant_2: TC-GRP-020~025, TC-FRIEND-*
    # user_organizer_1: TC-CAT-*, TC-RULE-*
    # user_admin_1: TC-PERM-*
```
