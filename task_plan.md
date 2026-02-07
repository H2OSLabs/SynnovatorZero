# Task Plan: 完整 E2E 用户旅程测试

> **目标**: 实现 specs/testcases/11-user-journeys.md 定义的完整 E2E 测试
> **创建时间**: 2026-02-08
> **状态**: `complete`

## 背景

### 测试用例架构分析

项目采用分层测试策略：

| 层级 | 文件范围 | 测试类型 | 目的 |
|-----|---------|---------|------|
| 基础层 | 01-10 | 单元/CRUD | 验证基础数据操作和约束 |
| 桥接层 | 11 | 集成测试 | **用户旅程完整流程** |
| 高级层 | 12-17 | 功能测试 | 高级功能（转账、关注、规则引擎） |
| 场景层 | 18-33 | 端到端 | 按 User Journey 组织的细粒度场景 |

### 分散问题

- 11-user-journeys.md 定义 8 个核心旅程，但只是规范
- 18-33 按 User Journey 文档组织，与 11 存在重叠
- 现有 E2E 测试（e2e/test_*.py）侧重前端集成，非完整旅程

### 解决方案

实现 11-user-journeys.md 的 8 个核心旅程作为**完整 E2E 测试**：
- 涵盖多步骤、多角色、跨实体的业务流程
- 验证前后端集成 + 业务逻辑 + 数据一致性
- 与 18-33 细粒度测试互补，不重复

## 阶段列表

| Phase | 描述 | 用例 | 状态 | 完成度 |
|-------|------|------|------|--------|
| Phase 1 | 分析 11-user-journeys.md 8 个旅程 | - | `complete` | 100% |
| Phase 2 | 实现 TC-JOUR-002 匿名浏览 | 1 case | `complete` | 100% |
| Phase 3 | 实现 TC-JOUR-005 团队加入流程 | 1 case | `complete` | 100% |
| Phase 4 | 实现 TC-JOUR-007 团队报名活动 | 1 case | `complete` | 100% |
| Phase 5 | 实现 TC-JOUR-009 发送帖子 | 1 case | `complete` | 100% |
| Phase 6 | 实现 TC-JOUR-010 证书颁发流程 | 1 case | `complete` | 100% |
| Phase 7 | 实现 TC-JOUR-011 编辑帖子 | 2 cases | `complete` | 100% |
| Phase 8 | 实现 TC-JOUR-012 删除帖子级联 | 1 case | `complete` | 100% |
| Phase 9 | 实现 TC-JOUR-013 社区互动 | 1 case | `complete` | 100% |
| Phase 10 | 验证与提交 | - | `complete` | 100% |

---

## Phase 1: 分析 11-user-journeys.md `complete`

### 8 个核心旅程摘要

| 旅程 | 用例ID | 描述 | 涉及实体 |
|------|--------|------|---------|
| 匿名浏览 | TC-JOUR-002 | 未登录访客浏览公开内容 | event, post |
| 加入团队 | TC-JOUR-005 | 申请→审批→加入完整流程 | user, group, group_user |
| 团队报名 | TC-JOUR-007 | 团队报名活动+提交作品 | group, event, post, rule |
| 发送帖子 | TC-JOUR-009 | 日常帖子+参赛提案 | post, event, rule |
| 获取证书 | TC-JOUR-010 | 活动结束→证书颁发 | event, resource, post |
| 编辑帖子 | TC-JOUR-011 | 版本管理+副本机制 | post, post_post |
| 删除帖子 | TC-JOUR-012 | 级联删除验证 | post, interaction, relation |
| 社区互动 | TC-JOUR-013 | 点赞/评论/评分 | interaction, post |

### 测试策略

- 每个旅程一个测试类
- 使用 pytest + playwright (Python E2E)
- 需要真实后端服务 + 数据库
- 测试前清理/准备种子数据

---

## Phase 2: TC-JOUR-002 匿名浏览 `pending`

**文件**: `e2e/test_journey_anonymous.py`

**测试场景**:
1. 未登录访客访问首页
2. 浏览 published 活动列表
3. 浏览 published 帖子列表
4. 按 tag/type 筛选
5. 验证 draft 内容不可见

---

## Phase 3: TC-JOUR-005 团队加入流程 `pending`

**文件**: `e2e/test_journey_team_join.py`

**测试场景**:
1. Carol 申请加入需审批团队
2. 验证申请状态为 pending
3. Owner Alice 批准申请
4. 验证状态变为 accepted
5. Bob 申请被拒绝
6. Bob 再次申请
7. 验证团队成员列表

---

## Phase 4: TC-JOUR-007 团队报名活动 `pending`

**文件**: `e2e/test_journey_team_registration.py`

**测试场景**:
1. Alice 创建团队
2. Bob 加入团队
3. 团队报名活动
4. 创建参赛帖子
5. 验证规则约束检查
6. 验证报名列表
7. 验证成员列表

---

## Phase 5: TC-JOUR-009 发送帖子 `pending`

**文件**: `e2e/test_journey_post_creation.py`

**测试场景**:
1. 创建日常帖子（type=general）
2. 验证公开可见
3. 创建参赛提案（type=proposal）
4. 关联到活动
5. 验证规则约束
6. 验证审核流程（如适用）

---

## Phase 6: TC-JOUR-010 证书颁发 `pending`

**文件**: `e2e/test_journey_certificate.py`

**测试场景**:
1. 关闭活动
2. 创建证书资源
3. 关联到参赛帖子
4. 创建分享帖子
5. 验证可访问性

---

## Phase 7: TC-JOUR-011 编辑帖子 `pending`

**文件**: `e2e/test_journey_post_edit.py`

**测试场景**:
1. TC-JOUR-011-1: 编辑自己帖子（版本管理）
2. TC-JOUR-011-2: 编辑他人帖子（副本机制）

---

## Phase 8: TC-JOUR-012 删除帖子级联 `pending`

**文件**: `e2e/test_journey_post_delete.py`

**测试场景**:
1. 创建复杂关联帖子
2. 删除帖子
3. 验证物理删除
4. 验证关系解除
5. 验证 interaction 级联删除

---

## Phase 9: TC-JOUR-013 社区互动 `pending`

**文件**: `e2e/test_journey_community.py`

**测试场景**:
1. Dave 点赞帖子
2. Bob 发表评论
3. 评委进行评分
4. 验证重复点赞被拒绝
5. 验证计数器正确

---

## Phase 10: 验证与提交 `pending`

- [ ] 运行所有 E2E 测试
- [ ] 更新 progress.md
- [ ] 提交所有更改
- [ ] 推送到远程

---

## 与现有测试的关系

| 现有测试 | 新增测试 | 关系 |
|---------|---------|------|
| test_home.py | - | 保留，基础检查 |
| test_post_integration.py | test_journey_post_creation.py | 互补：前者验证 API 调用，后者验证完整业务流程 |
| test_group_integration.py | test_journey_team_*.py | 互补 |
| test_auth_integration.py | - | 保留，认证基础 |

---

## 错误记录

| 时间 | 错误 | 尝试 | 解决方案 |
|------|------|------|----------|
| - | - | - | - |

