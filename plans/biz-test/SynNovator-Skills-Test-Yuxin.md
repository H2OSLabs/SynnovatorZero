# Synnovator Skill 自动化测试指令集 (Claude Code 专用)

## 0. 准备工作：同步规范
> **指令：** "请阅读并理解项目中的 `command.md` 和 `user-journey.md`。接下来的所有操作必须严格遵守这些文档中定义的 Schema、枚举值及业务逻辑规则。"

---

## 1. 基础数据模型测试 (CRUD)

### 任务：测试创建活动 (category)
> **指令：** "请创建一个 `type: competition` 的 `category`。
> - 状态设为 `published`。
> - YAML 必须包含 `name`, `description`, `start_date`。
> - 验证：检查返回的对象是否自动生成了 UUID 格式的 `id`。"

### 任务：测试创建用户和团队 (user/group)
> **指令：** "执行以下流程：
> 1. 创建一个新 `user`。
> 2. 以该用户身份创建一个 `group`，设置 `require_approval: true`。
> 3. 验证：`group:user` 关系的 `role` 应为 `owner`，`status` 应为 `accepted`。"

### 任务：测试创建资源 (resource)
> **指令：** "创建一个 `resource` 实体。
> - 设置 `filename: 'demo.mp4'`, `mime_type: 'video/mp4'`。
> - 验证：读取该资源，确保 `url` 字段非空且格式正确。"

---

## 2. 核心业务逻辑测试 (Logic & Rules)

### 任务：测试报名规则 (Not create Only Select)
> **指令：** "模拟活动报名：
> 1. 创建一个 `rule`，内容设定为 `Not create Only Select`。
> 2. 将此 Rule 关联至一个活动。
> 3. 模拟用户尝试通过『新建 Post』进行报名：验证系统是否根据 `rule.jpg` 的逻辑拦截新建操作，并改为『选择已有 Post』。
> 4. 验证：选定的 Post 是否被正确打上 `#for_<category>` 标签。"

### 任务：测试创建提案 (post type=for_category)
> **指令：** "为指定活动创建一个参赛提案 `post`。
> - 设置 `type: for_category`。
> - 验证：此 Post 的 `status` 初始值应根据 Rule 设定（如 `pending_review` 或 `published`）。"

### 任务：测试编辑逻辑与版本管理
> **指令：** "编辑一个现有的 Post。
> - 验证：系统是否按照 `user-journey.md` 逻辑『创建新版本并编辑』，即生成一个新的 `id` 但保留原有的关联关系。"

---

## 3. 关系与统计验证

### 任务：测试是否正确列出提交给某个活动的提案
> **指令：** "执行 `READ category:post`。
> - 过滤条件：`relation_type: submission`。
> - 验证：输出列表是否仅包含该活动的参赛提案，不包含其他引用的帖子。"

### 任务：测试社区互动与缓存更新
> **指令：** "对一个 Post 执行点赞和评论：
> 1. `CREATE interaction (type: like)`。
> 2. `CREATE interaction (type: comment)`。
> 3. 验证：检查该 Post 对象的 `like_count` 和 `comment_count` 是否已自动更新（最终一致性）。"

---

## 4. 异常与清理测试

### 任务：删除功能验证
> **指令：** "删除一个测试用的 `post`。
> - 验证：执行软删除策略，检查 `deleted_at` 字段是否已被赋值。
> - 验证：确保关联的 `target:interaction`（点赞/评论）也无法被普通 READ 检索到。"