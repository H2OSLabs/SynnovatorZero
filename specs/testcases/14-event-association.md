# 活动关联（Event Association）

> **格式约定：** 每条用例仅描述「场景」与「预期结果」，不包含测试方法和执行过程。

> 活动关联功能基于新增的第 9 种关系 `event:event`（也称 `event_event`）实现。支持三种关联类型：赛段（stage）、赛道（track）、前置条件（prerequisite）。

---

## 14.1 赛段（Stage）

**TC-STAGE-001：创建连续赛段关联**
创建 3 个 event（A/B/C），创建 event:event 关系：A→B（relation_type=stage, stage_order=1），B→C（relation_type=stage, stage_order=2）。读取赛段链返回 A→B→C 的顺序关系。

**TC-STAGE-002：按 stage_order 排序读取赛段**
查询 event A 的所有 stage 类型 event:event 关系，返回结果按 stage_order 升序排列。

**TC-STAGE-003：赛段未完成时无法进入下一赛段**
活动 A（status=published，进行中），活动 B 为 A 的下一赛段（stage_order=2）。团队尝试报名活动 B（CREATE event:group）。系统拒绝操作，返回 "prerequisite stage not completed" 错误。

**TC-STAGE-004：赛段完成后可进入下一赛段**
将活动 A 更新为 status=closed。团队报名活动 B（CREATE event:group）。系统允许操作。

## 14.2 赛道（Track）

**TC-TRACK-001：创建并行赛道关联**
创建父活动 Main 和 2 个子活动（Track1/Track2）。创建 event:event 关系：Main→Track1（relation_type=track），Main→Track2（relation_type=track）。查询 Main 的赛道列表返回 Track1 和 Track2。

**TC-TRACK-002：团队可同时参加不同赛道**
Team A 报名 Track1（event:group）和 Track2（event:group）。两次报名均成功（不同赛道不受互斥约束，但同一赛道内的 Rule 约束仍然有效）。

**TC-TRACK-003：团队在同一赛道内受 Rule 约束**
Track1 关联了 max_submissions=1 的 Rule。团队已提交一次后再次提交被拒绝。不影响其在 Track2 的提交。

## 14.3 前置条件（Prerequisite）

**TC-PREREQ-001：悬赏活动作为前置条件关联到常规赛**
创建悬赏活动 Bounty（type=operation）和常规赛 Competition（type=competition）。创建 event:event（source_category_id=Bounty, target_category_id=Competition, relation_type=prerequisite）。关系创建成功。

**TC-PREREQ-002：前置活动完成后团队可报名目标活动**
Bounty 活动更新为 status=closed，团队在 Bounty 中有 accepted 的 event:group 记录。团队报名 Competition（CREATE event:group）。系统允许操作。

**TC-PREREQ-003：前置活动未完成时团队报名目标活动被拒绝**
Bounty 活动仍为 status=published（进行中）。团队尝试报名 Competition。系统拒绝操作，返回 "prerequisite not completed" 错误。

**TC-PREREQ-004：前置活动中组建的团队保持完整进入目标活动**
团队在 Bounty 活动中有 3 名 accepted 成员。报名 Competition 后，READ group:user 返回同样的 3 名成员（团队不因活动切换而变化）。

## 14.4 活动关联展示

**TC-CATREL-010：查看活动关联列表**
用户访问活动详情页，系统展示该活动的所有关联活动列表（包括 stage/track/prerequisite 类型）。

**TC-CATREL-011：从关联活动跳转**
用户点击关联活动列表中的条目，系统跳转到该关联活动的详情页。

**TC-CATREL-012：活动关联双向可见**
活动 A 关联活动 B 后，在活动 B 的详情页也能看到活动 A（双向可见）。

## 14.5 同一提案参加多个活动

**TC-CATREL-020：提案在多个关联活动中独立评审**
同一提案投递至多个关联活动后，在每个活动中可以被独立评审、打分，各活动的评分结果互不影响。

**TC-CATREL-021：提案在多个活动中独立获奖**
同一提案可以在多个关联活动中分别获奖，每个活动独立生成证书资源。

## 14.6 赛道类型标识

**TC-CATTRACK-010：常规赛道（X类型）标识展示**
常规赛道活动（competition 类型）在页面上显示"常规赛道"标识，提示参赛者提案相互可见。

**TC-CATTRACK-011：命题赛道（Y类型）标识展示**
企业命题和悬赏活动在页面上显示"命题赛道"标识，提示参赛者提案互不可见。

## 14.7 负向/边界

**TC-CATREL-900：重复创建同一活动关联被拒绝**
A→B（stage）关系已存在，再次创建相同的 event:event 关系。系统拒绝操作，返回唯一性冲突错误。唯一性约束：(source_category_id, target_category_id)。

**TC-CATREL-901：自引用被拒绝**
创建 event:event（source_category_id=A, target_category_id=A）。系统拒绝操作，返回 "cannot reference self" 错误。

**TC-CATREL-902：赛段循环依赖被拒绝**
A→B（stage），B→C（stage），尝试创建 C→A（stage）。系统拒绝操作，返回 "circular dependency detected" 错误。

**TC-CATREL-903：非法 relation_type 被拒绝**
创建 event:event 时 relation_type 为 "sponsor"。系统拒绝操作，返回枚举值无效错误（合法值为 stage | track | prerequisite）。

**TC-CATREL-904：已关闭活动无法添加关联**
组织者尝试为已 closed 状态的活动添加新的活动关联，系统拒绝操作。

**TC-CATREL-905：非关联活动无法共享提案**
用户尝试将提案投递至与原活动无任何关联关系的活动 C，系统拒绝（仅允许投递至已建立关联的活动）。
