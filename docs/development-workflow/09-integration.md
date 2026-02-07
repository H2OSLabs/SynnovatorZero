# 阶段 9: 最终集成验证

> 前面各阶段已完成模块级增量测试，本阶段聚焦于全栈端到端集成验证。

## 9.1 tests-kit 最终 Guard 检查

```bash
uv run python .claude/skills/tests-kit/scripts/check_testcases.py
```

确保所有测试模块覆盖：
- 01-07: 内容类型 CRUD
- 08: 关系操作
- 09: 级联删除
- 10: 权限控制
- 11: 用户旅程
- 12-17: 高级功能

## 9.2 后端完整测试

```bash
# 运行所有后端测试
uv run pytest app/tests/ -v

# 测试覆盖率
uv run pytest app/tests/ --cov=app --cov-report=html
```

## 9.3 验证前端-后端连通性 ⭐

> 在运行 E2E 测试前，先验证 Next.js rewrites 代理正常工作。

```bash
# 启动服务
make start

# 确保种子数据已注入
make seed

# 验证后端 API 直接访问
curl http://localhost:8000/api/users | head -c 200

# 验证前端代理转发（关键！）
curl http://localhost:3000/api/users | head -c 200
# 应返回相同的用户列表 JSON

# 验证关键 API 端点
curl -s http://localhost:3000/api/posts | python3 -c \
  "import sys,json; d=json.load(sys.stdin); print(f'Posts: {len(d[\"items\"])} items')"
curl -s http://localhost:3000/api/events | python3 -c \
  "import sys,json; d=json.load(sys.stdin); print(f'Events: {len(d[\"items\"])} items')"
curl -s http://localhost:3000/api/groups | python3 -c \
  "import sys,json; d=json.load(sys.stdin); print(f'Groups: {len(d[\"items\"])} items')"
```

**常见问题排查：**

| 症状 | 原因 | 解决方案 |
|------|------|---------|
| 前端 `/api/*` 返回 404 | `next.config.js` 缺少 rewrites | 添加 rewrites 配置（见 [06-frontend-setup.md](06-frontend-setup.md)） |
| 前端请求超时 | 后端未启动 | 运行 `make backend` |
| 数据返回空 | 种子数据未注入 | 运行 `make resetdb && make seed` |

## 9.4 全栈集成测试

```bash
# 运行 E2E 测试
cd frontend && npx playwright test

# 手动验证
open http://localhost:3000
open http://localhost:8000/docs
```

## 9.5 测试结果汇总

| 测试层 | 命令 | 预期结果 |
|-------|------|---------|
| 后端单元测试 | `uv run pytest app/tests/` | 390+ passed |
| 前端单元测试 | `cd frontend && npm test` | 43+ passed |
| 前端→后端代理 | `curl localhost:3000/api/users` | 返回用户列表 JSON |
| E2E 测试 | `npx playwright test` | 核心用户流程通过 |

## 9.6 完成会话记录

```bash
# 更新 progress.md，标记所有阶段完成
# 运行完成检查脚本
bash .claude/skills/planning-with-files/scripts/check-complete.sh
```

## 完成

恭喜！开发工作流全部完成。

如需更新数据模型，参见 [附录 B: 数据模型更新流程](appendix-b-update-flows.md)。
