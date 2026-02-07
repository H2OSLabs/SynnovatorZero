# 前后端集成测试

> **格式约定：** 每条用例仅描述「场景」与「预期结果」，不包含测试方法和执行过程。
>
> **本文档特殊说明：** 本文档测试前端页面与后端 API 的集成，验证"用户操作 → API 调用 → 数据持久化 → UI 反馈"的完整链路。与业务逻辑测试（验证 API 本身）互补，确保前端表单真正调用了后端 API。

---

## 33.1 帖子创建集成

**TC-FEINT-001：前端创建日常帖子调用后端 API**
用户在 `/posts/create` 页面填写标题和内容，点击"发布"按钮，系统调用 `POST /api/posts` 创建帖子，成功后跳转到帖子详情页 `/posts/{id}`，新帖子在数据库中可查询到。

**TC-FEINT-002：前端保存帖子草稿调用后端 API**
用户在 `/posts/create` 页面填写内容，点击"保存草稿"按钮，系统调用 `POST /api/posts` 创建 status=draft 的帖子，成功后跳转到帖子详情页。

**TC-FEINT-003：前端创建提案调用后端 API**
用户在 `/posts/create?type=proposal` 页面创建提案，点击"发布"按钮，系统调用 `POST /api/posts` 创建 type=proposal 的帖子，成功后跳转到提案详情页。

**TC-FEINT-004：前端创建帖子失败显示错误**
用户在 `/posts/create` 页面未填写标题直接点击"发布"，系统显示错误提示"请输入帖子标题"，不调用后端 API。

**TC-FEINT-005：前端创建帖子时 API 返回错误**
用户在 `/posts/create` 页面填写内容并发布，后端 API 返回错误（如 401 未登录），前端显示 toast 错误消息，不跳转页面。

## 33.2 团队创建集成

**TC-FEINT-010：前端创建团队调用后端 API**
用户在 `/groups/create` 页面填写团队名称和简介，点击"创建"按钮，系统调用 `POST /api/groups` 创建团队，成功后跳转到团队详情页 `/groups/{id}`，新团队在数据库中可查询到，创建者自动成为 owner。

**TC-FEINT-011：前端创建团队失败显示错误**
用户在 `/groups/create` 页面未填写团队名称直接点击"创建"，系统显示错误提示"请输入团队名称"，不调用后端 API。

**TC-FEINT-012：前端创建私有团队调用后端 API**
用户在 `/groups/create` 页面选择"私密"可见性，点击"创建"，系统调用 `POST /api/groups` 创建 visibility=private 的团队。

## 33.3 活动创建集成

**TC-FEINT-020：前端创建活动调用后端 API**
组织者在 `/events/create` 页面填写活动信息，点击"创建"按钮，系统调用 `POST /api/categories` 创建活动，成功后跳转到活动详情页。

**TC-FEINT-021：非组织者无法访问活动创建页**
参赛者角色用户访问 `/events/create`，系统重定向或显示权限不足提示。

## 33.4 用户认证集成

**TC-FEINT-030：前端登录调用后端 API**
用户在 `/login` 页面输入用户名和密码，点击登录，系统调用 `POST /api/auth/login`，成功后存储用户信息并跳转到首页。

**TC-FEINT-031：前端注册调用后端 API**
用户在 `/register` 页面填写注册信息，点击注册，系统调用 `POST /api/auth/register`，成功后自动登录并跳转。

**TC-FEINT-032：前端登录失败显示错误**
用户在 `/login` 页面输入错误密码，后端返回 401，前端显示错误提示"用户名或密码错误"。

## 33.5 编辑更新集成

**TC-FEINT-040：前端编辑帖子调用后端 API**
用户在 `/posts/{id}/edit` 页面修改帖子内容，点击"保存"，系统调用 `PATCH /api/posts/{id}` 更新帖子，成功后跳转到帖子详情页。

**TC-FEINT-041：前端编辑团队信息调用后端 API**
团队 owner 在团队编辑页面修改团队简介，点击"保存"，系统调用 `PATCH /api/groups/{id}` 更新团队信息。

## 33.6 删除操作集成

**TC-FEINT-050：前端删除帖子调用后端 API**
用户点击帖子删除按钮并确认，系统调用 `DELETE /api/posts/{id}` 软删除帖子，成功后跳转到帖子列表页。

**TC-FEINT-051：前端删除团队调用后端 API**
团队 owner 点击团队删除按钮并确认，系统调用 `DELETE /api/groups/{id}` 软删除团队。

## 33.7 API 客户端完整性

**TC-FEINT-090：api-client.ts 包含所有 CRUD 方法**
前端 `lib/api-client.ts` 文件必须包含每个数据类型的创建（create）、读取（get/list）、更新（update）、删除（delete）方法，不能只有 GET 方法而缺少 POST/PATCH/DELETE。

**TC-FEINT-091：前端创建页面无 TODO 遗留**
所有前端创建页面（`/posts/create`, `/groups/create`, `/events/create` 等）的表单提交函数不能包含 `// TODO:` 注释占位，必须实现真实的 API 调用。

## 33.8 负向/边界

**TC-FEINT-900：未登录用户创建帖子被拦截**
未登录用户访问 `/posts/create` 或点击发布按钮，系统拦截并重定向到登录页。

**TC-FEINT-901：API 客户端网络错误处理**
用户在创建页面提交时网络中断，系统显示"网络错误，请重试"提示，不丢失用户输入的内容。

**TC-FEINT-902：重复提交防护**
用户快速多次点击"发布"按钮，系统只发送一次 API 请求（按钮在提交期间禁用）。
