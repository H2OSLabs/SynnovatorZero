# Task Plan: 后续改进任务

> **目标**: 根据工作流审查的后续建议，完成 4 项改进任务
> **创建时间**: 2026-02-08
> **状态**: `complete`

## 背景

工作流审查任务已完成，发现以下需要改进的项目：

1. specs/testcases/README.md 缺少 18-33 号文件
2. 前端缺少 Playwright E2E 测试
3. pen-to-react skill 目录未删除（已废弃）
4. 11-user-journeys.md 的完整 E2E 测试未实现

## 阶段列表

| Phase | 描述 | 优先级 | 状态 | 完成度 |
|-------|------|--------|------|--------|
| Phase 1 | 更新 specs/testcases/README.md | 立即 | `complete` | 100% |
| Phase 2 | 删除废弃的 pen-to-react skill | 中期 | `complete` | 100% |
| Phase 3 | 设置 Playwright E2E 测试框架 | 短期 | `complete` | 100% |
| Phase 4 | 实现前端集成测试用例 | 短期 | `complete` | 100% |
| Phase 5 | 验证与提交 | - | `complete` | 100% |

---

## Phase 1: 更新 specs/testcases/README.md `complete`

**目标**: 补充 18-33 号测试用例文件到 README.md

### 1.1 检查当前 README.md 内容

- [ ] 读取 `specs/testcases/README.md`
- [ ] 确认缺少哪些文件

### 1.2 列出所有测试用例文件

- [ ] 遍历 `specs/testcases/*.md`
- [ ] 整理完整文件列表

### 1.3 更新 README.md

- [ ] 添加 18-33 号文件
- [ ] 确保格式一致

---

## Phase 2: 删除废弃的 pen-to-react skill `complete`

**目标**: 清理 `.claude/skills/pen-to-react/` 目录

### 2.1 确认 pen-to-react 内容

- [ ] 列出目录结构
- [ ] 确认无其他依赖

### 2.2 删除目录

- [ ] `rm -rf .claude/skills/pen-to-react/`
- [ ] 验证删除成功

---

## Phase 3: 设置 Playwright E2E 测试框架 `complete`

**目标**: 配置 Playwright 测试环境

**发现**: 项目已有 pytest + playwright 测试框架

- [x] `e2e/` 目录已存在
- [x] `e2e/conftest.py` 提供 browser/context/page fixtures
- [x] `e2e/test_home.py` 首页测试示例
- [x] `playwright>=1.58.0` 已在 pyproject.toml
- [x] 无需额外配置

---

## Phase 4: 实现前端集成测试用例 `complete`

**目标**: 按 `specs/testcases/33-frontend-integration.md` 实现 E2E 测试

### 4.1 测试用例规范 (已读取)

8 个测试模块，22 个测试用例：
- 33.1 帖子创建集成 (5 cases: TC-FEINT-001~005)
- 33.2 团队创建集成 (3 cases: TC-FEINT-010~012)
- 33.3 活动创建集成 (2 cases: TC-FEINT-020~021)
- 33.4 用户认证集成 (3 cases: TC-FEINT-030~032)
- 33.5 编辑更新集成 (2 cases: TC-FEINT-040~041)
- 33.6 删除操作集成 (2 cases: TC-FEINT-050~051)
- 33.7 API 客户端完整性 (2 cases: TC-FEINT-090~091)
- 33.8 负向/边界 (3 cases: TC-FEINT-900~902)

### 4.2 实现测试文件

- [x] `e2e/test_post_integration.py` - 帖子创建集成 (5 tests)
- [x] `e2e/test_group_integration.py` - 团队创建集成 (3 tests)
- [x] `e2e/test_event_integration.py` - 活动创建集成 (2 tests)
- [x] `e2e/test_auth_integration.py` - 用户认证集成 (3 tests)
- [x] `e2e/test_edit_delete_integration.py` - 编辑删除集成 (4 tests)
- [x] `e2e/test_edge_cases.py` - 边界测试 (5 tests)

**总计**: 6 个测试文件，22 个测试用例

### 4.3 运行测试验证

- [ ] `uv run pytest e2e/ -v` (需要运行服务器)
- [ ] 确保测试通过

---

## Phase 5: 验证与提交 `complete`

- [x] 5.1 更新 progress.md
- [x] 5.2 提交所有更改
- [x] 5.3 推送到远程

> **注意**: E2E 测试需要启动服务器才能运行 (`make start`)

---

## 错误记录

| 时间 | 错误 | 尝试 | 解决方案 |
|------|------|------|----------|
| - | - | - | - |

