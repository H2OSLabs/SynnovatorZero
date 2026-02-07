# Ralph Loop 提示词

## Phase 12: P2 Frontend Components

```
/ralph-loop:ralph-loop "/planning-with-files 规划并记录进度在 plans/api-completion-progress.md，完成 Phase 12: P2 Frontend Components

任务列表：
1. 创建 frontend/components/search/SearchModal.tsx - 实现全局搜索 Modal，使用 shadcn/ui Command 组件，支持 ⌘K 快捷键，可搜索用户/活动/作品
2. 创建 frontend/lib/search-api.ts - 实现搜索 API 调用函数
3. 创建 frontend/components/home/PlatformStats.tsx - 显示平台统计数据（用户数/活动数/作品数），使用 Card 组件展示
4. 在 backend 添加 GET /stats 端点返回平台统计数据
5. 执行 make start 启动服务，验证组件正常渲染
6. 更新 plans/api-completion-progress.md 标记 Phase 12 完成

完成上述任务后输出<promise>COMPLETE</promise>." --completion-promise "COMPLETE" --max-iterations 30
```

## Phase 13: Admin Batch Operations (可选)

```
/ralph-loop:ralph-loop "/planning-with-files 规划并记录进度在 plans/api-completion-progress.md，完成 Phase 13: Admin Batch Operations

任务列表：
1. 创建 app/schemas/admin.py - 定义批量操作的请求/响应 Schema (BatchDeleteRequest, BatchStatusUpdateRequest, BatchRoleUpdateRequest)
2. 更新 app/routers/admin.py 添加批量操作端点:
   - POST /admin/posts/batch-delete - 批量软删除作品
   - POST /admin/posts/batch-update-status - 批量更新作品状态 (draft/published/archived)
   - POST /admin/users/batch-update-roles - 批量更新用户角色
3. 添加 Admin 权限检查 (require_role('admin'))
4. 创建 app/tests/test_admin_batch.py - 测试批量操作功能 (权限验证/成功场景/边界情况)
5. 执行 uv run pytest app/tests/test_admin_batch.py -v 验证测试通过
6. 更新 .synnovator/openapi.yaml 添加批量操作端点定义
7. 更新 plans/api-completion-progress.md 标记 Phase 13 完成

完成上述任务后输出<promise>COMPLETE</promise>." --completion-promise "COMPLETE" --max-iterations 30
```

## 完整 API 补全流程（从 Phase 12 开始）

```
/ralph-loop:ralph-loop "/planning-with-files 规划并记录进度，依次完成以下任务：

**任务 1: Phase 12 - P2 Frontend Components**
根据 @docs/frontend-api-mapping.md 中的 API 映射，在 @frontend 中创建以下组件：
- 创建 frontend/components/search/SearchModal.tsx 全局搜索组件，使用 shadcn/ui Command 组件，支持 ⌘K 快捷键唤起，可搜索用户/活动/作品
- 创建 frontend/lib/search-api.ts 实现搜索 API 调用函数
- 创建 frontend/components/home/PlatformStats.tsx 平台统计组件，显示用户数/活动数/作品数
- 在 @app/routers 添加 GET /api/stats 端点返回平台统计数据

**任务 2: Phase 13 - Admin Batch Operations**
在 @app 后端实现管理员批量操作功能：
- 创建 app/schemas/admin.py 定义 BatchDeleteRequest, BatchStatusUpdateRequest, BatchRoleUpdateRequest Schema
- 更新 app/routers/admin.py 添加三个批量操作端点：POST /admin/posts/batch-delete, POST /admin/posts/batch-update-status, POST /admin/users/batch-update-roles
- 所有端点添加 Admin 角色权限检查 (require_role('admin'))
- 创建 app/tests/test_admin_batch.py 编写批量操作的单元测试

**任务 3: 单元测试验证**
执行 uv run pytest app/tests/ -v 确保所有后端单元测试通过，修复任何失败的测试

**任务 4: 前端测试更新**
根据新增的组件和 API 调用，更新 frontend 中的测试文件，确保测试覆盖新功能

**任务 5: 启动服务验证**
执行 make start 启动前后端服务器，手动验证：
- SearchModal 组件可通过 ⌘K 唤起
- PlatformStats 组件正确显示统计数据
- Demo 页面正常渲染所有新组件

**任务 6: E2E 测试验证**
根据 /tests-kit 中的业务测试用例，使用 /agent-browser 进行页面的点击和数据填写，验证以下场景：
- 搜索功能可正常搜索用户和作品
- 平台统计数据正确显示
- 管理员批量操作功能正常
将测试结果记录在 plans/e2e_test.md 中

**任务 7: 更新进度文档**
更新 plans/api-completion-progress.md，将 Phase 12 和 Phase 13 标记为完成，填写完成时间和测试结果

完成上述七项任务，且 task_plan.md 中的所有阶段都标注完成的时候，输出<promise>COMPLETE</promise>." --completion-promise "COMPLETE" --max-iterations 50
```
