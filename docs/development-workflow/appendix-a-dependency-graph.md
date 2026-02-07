# 附录 A: 模块依赖图与开发顺序

> 核心原则：从零依赖的底层模块开始，逐层向上开发。每完成一层，立即测试该层对应的测试用例。

## 依赖关系图

```
┌─────────────── Layer 0: 零依赖基础 ───────────────┐
│   user (用户)          resource (资源)            │
│   零外部依赖            零外部依赖                 │
└──────────┬─────────────────┬──────────────────────┘
           │                 │
           ▼                 │
┌─────────────── Layer 1: 仅依赖 user ──────────────┐
│   rule (规则)   group (团队)   event (活动)       │
│   ← user        ← user        ← user              │
└──────────┬─────────┬──────────┬───────────────────┘
           │         │          │
           ▼         ▼          ▼
┌─────────────── Layer 2: 依赖 Layer 0-1 ───────────┐
│   post (帖子)          interaction (交互)         │
│   ← user, resource     ← user                     │
└──────────┬──────────────┬─────────────────────────┘
           │              │
           ▼              ▼
┌─────────────── Layer 3: 简单关系 ─────────────────┐
│   group_user     user_user      post_resource     │
│   post_post      (无规则引擎, 无复杂校验)         │
└──────────┬────────────────────────────────────────┘
           │
           ▼
┌─────────────── Layer 4: 复杂关系 ─────────────────┐
│   event_rule       target_interaction             │
│   event_post (含规则引擎校验)                     │
│   event_group (含前置条件检查)                    │
└──────────┬────────────────────────────────────────┘
           │
           ▼
┌─────────────── Layer 5: 高级图关系 ───────────────┐
│   event_event                                     │
│   (阶段/赛道/前置条件, 含环检测)                  │
└──────────┬────────────────────────────────────────┘
           │
           ▼
┌─────────────── Layer 6: 跨切面功能 ───────────────┐
│   软删除 + 级联删除      权限层                   │
│   声明式规则引擎          缓存字段维护            │
└──────────┬────────────────────────────────────────┘
           │
           ▼
┌─────────────── Layer 7: 集成验证 ─────────────────┐
│   13 个用户旅程端到端测试                         │
│   高级功能: 资源转移、评分排名、证书发放          │
└───────────────────────────────────────────────────┘
```

## 各层详细内容与测试映射

| Layer | 模块 | 依赖 | 测试用例 |
|-------|------|------|----------|
| **0** | user CRUD + 唯一性校验 | 无 | TC-USER-001~020, 900~903 |
| **0** | resource CRUD + 文件存储 | 无 | TC-RES-001~011, 900~901 |
| **1** | rule CRUD + scoring_criteria | user | TC-RULE-001~011, 900~901 |
| **1** | group CRUD + 成员角色定义 | user | TC-GRP-001~011, 900~901 |
| **1** | event CRUD + 状态机 | user | TC-CAT-001~011, 900~902 |
| **2** | post CRUD + 缓存字段 + 状态机 | user, resource | TC-POST-001~076, 900~903 |
| **2** | interaction CRUD | user | TC-IACT-001~063, 900~905 |
| **3** | group_user 关系 + 审批流程 | group, user | TC-REL-GU-*, TC-GRP-020~025 |
| **3** | user_user 关系 (关注/屏蔽) | user | TC-FRIEND-001~010, 900~902 |
| **3** | post_resource 关系 | post, resource | TC-REL-PR-* |
| **3** | post_post 关系 | post | TC-REL-PP-* |
| **4** | event_rule 关系 | event, rule | TC-REL-CR-* |
| **4** | target_interaction | interaction, post/event/resource | TC-REL-TI-* |
| **4** | event_post (含规则引擎校验) | event, post, rule | TC-REL-CP-*, TC-ENTRY-* |
| **4** | event_group (含前置条件) | event, group | TC-REL-CG-* |
| **5** | event_event (阶段/赛道/前置 + 环检测) | event | TC-STAGE-*, TC-TRACK-* |
| **6** | 软删除 + 级联删除 | 全部类型 | TC-DEL-001~022 |
| **6** | 权限层 + 可见性控制 | user, 全部类型 | TC-PERM-001~025 |
| **6** | 声明式规则引擎 | rule, event | TC-ENGINE-001~061 |
| **7** | 用户旅程集成测试 | 全部 | TC-JOUR-002~013 |
| **7** | 闭幕规则 | event, rule | TC-CLOSE-001~040 |
| **7** | 资源转移 | resource, post | TC-TRANSFER-001~004 |

## 开发节奏

```
每个 Layer 的开发循环:

  1. [planning-with-files] 更新 task_plan.md → 标记当前 Layer
  2. [api-builder 或手工] 开发该 Layer 的模块代码
  3. [tests-kit Guard] 运行该 Layer 对应的测试用例
  4. [planning-with-files] 更新 progress.md → 记录结果
  5. 如有失败 → 修复 → 重新测试 → 记录到 findings.md
  6. 全部通过 → 进入下一个 Layer
```
