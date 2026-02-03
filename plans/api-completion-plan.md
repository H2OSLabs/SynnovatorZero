# Synnovator API 补全与实现计划

> 根据 UI 设计规范 (`specs/ui/ui-design-spec.md`) 与现有 OpenAPI 规范 (`.synnovator/openapi.yaml`) 的差距分析生成
>
> 创建时间：2025-02-03
> 更新时间：2025-02-03 (补充完整待办项)

---

## 〇、当前状态总览

基于代码库检查，以下是各模块的实现状态：

| 模块 | 状态 | 说明 |
|------|------|------|
| **OpenAPI 规范** | ⚠️ 部分完成 | 缺失 Auth、User Relations、Category Association、Notifications 等端点 |
| **数据模型** | ⚠️ 部分完成 | user_user/category_category 已有，notifications 缺失 |
| **缓存字段** | ⚠️ 部分完成 | Post 缓存完整，User/Category 缓存字段缺失 |
| **权限校验** | 🔴 严重不足 | DELETE 端点无权限检查，Admin 端点未实现 |
| **数据库迁移** | 🔴 未执行 | alembic/versions/ 为空 |
| **前端组件** | 🔴 未开始 | 仅有占位符 |

---

## 一、缺失 API 清单

基于 UI 设计文档中标记为 "🚨 Not Implemented" 的接口：

### 1.1 认证系统 (Auth)

| API | 方法 | 对应 Journey | 优先级 |
|-----|------|-------------|--------|
| `/auth/login` | POST | J4 登录 | P0 |
| `/auth/logout` | POST | J4 登录 | P0 |
| `/auth/refresh` | POST | J4 Token 刷新 | P0 |
| `/oauth/authorize` | GET | J4 OAuth 登录 | P1 |
| `/oauth/token` | POST | J4 OAuth Token | P1 |
| `/oauth/callback` | GET | J4 OAuth 回调 | P1 |

### 1.2 用户关系 (User Relations - J14)

| API | 方法 | 说明 | 优先级 |
|-----|------|------|--------|
| `/users/{user_id}/follow` | POST | 关注用户 | P0 |
| `/users/{user_id}/follow` | DELETE | 取消关注 | P0 |
| `/users/{user_id}/followers` | GET | 粉丝列表 | P0 |
| `/users/{user_id}/following` | GET | 关注列表 | P0 |
| `/users/{user_id}/block` | POST | 拉黑用户 | P2 |
| `/users/{user_id}/block` | DELETE | 取消拉黑 | P2 |

### 1.3 活动关联 (Category Association - J15)

| API | 方法 | 说明 | 优先级 |
|-----|------|------|--------|
| `/categories/{category_id}/categories` | GET | 获取关联活动（赛段/赛道/前置） | P0 |
| `/categories/{category_id}/categories` | POST | 创建活动关联 | P0 |
| `/categories/{category_id}/categories/{target_id}` | DELETE | 删除活动关联 | P1 |

### 1.4 通知系统 (Notifications)

| API | 方法 | 说明 | 优先级 |
|-----|------|------|--------|
| `/notifications` | GET | 通知列表 | P1 |
| `/notifications/{id}` | PATCH | 标记已读 | P1 |
| `/notifications/read-all` | POST | 全部标记已读 | P2 |

### 1.5 辅助接口

| API | 方法 | 说明 | 优先级 |
|------|------|------|--------|
| `/stats` | GET | 平台统计数据 | P2 |
| `/search` | GET | 全局搜索（聚合） | P2 |

---

## 二、实施阶段

### Phase 0: shadcn/ui 组件安装与配置

**目标：** 安装并配置所有 UI 设计规范所需的 shadcn/ui 组件，为前端原型开发做准备

**前置条件：** Next.js 14 + Tailwind CSS v4 已配置

#### 0.1 初始化 shadcn/ui

```bash
cd frontend
npx shadcn@latest init
```

配置选项：
- Style: New York（或 Default）
- Base color: Neutral（适配 Neon Forge 主题）
- CSS variables: Yes

#### 0.2 安装核心组件

```bash
# 布局与导航
npx shadcn@latest add sidebar sheet navigation-menu breadcrumb pagination tabs

# 按钮与表单
npx shadcn@latest add button input textarea select checkbox radio-group

# 卡片与数据展示
npx shadcn@latest add card avatar badge skeleton separator scroll-area

# 交互与反馈
npx shadcn@latest add dialog alert-dialog dropdown-menu popover command tooltip sonner
```

#### 0.3 自定义主题配置

更新 `globals.css` 适配 Neon Forge 主题：

```css
:root {
  /* Neon Forge Dark Theme */
  --nf-lime: #BBFD3B;
  --nf-surface: #181818;
  --nf-dark: #222222;
  --nf-secondary: #333333;
  --nf-near-black: #0D0D0D;
  --nf-white: #FFFFFF;
  --nf-light-gray: #D9D9D9;
  --nf-muted: #8E8E8E;
  --nf-cyan: #00E5FF;
  --nf-pink: #FF6EC7;
  --nf-orange: #FF9800;
  --nf-error: #FF5252;
}

/* shadcn CSS variables mapping */
.dark {
  --background: 0 0% 9%;        /* #181818 */
  --foreground: 0 0% 100%;      /* #FFFFFF */
  --card: 0 0% 13%;             /* #222222 */
  --card-foreground: 0 0% 100%;
  --primary: 78 97% 61%;        /* #BBFD3B */
  --primary-foreground: 0 0% 5%;
  --secondary: 0 0% 20%;        /* #333333 */
  --secondary-foreground: 0 0% 100%;
  --muted: 0 0% 56%;            /* #8E8E8E */
  --muted-foreground: 0 0% 85%;
  --accent: 78 97% 61%;         /* #BBFD3B */
  --destructive: 0 72% 66%;     /* #FF5252 */
  --border: 0 0% 20%;
  --input: 0 0% 13%;
  --ring: 78 97% 61%;
}
```

#### 0.4 组件替代方案确认

根据用户确认，以下复杂组件使用简单替代方案：

| 原设计组件 | 替代方案 | 说明 |
|-----------|---------|------|
| Markdown 编辑器 | `textarea` | 纯文本编辑，后续可升级为富文本 |
| 文件拖拽上传 | `input[type=file]` | 原生文件选择器 |
| 多选标签输入 | `input` + `badge` | 输入框 + 回车添加 + badge 显示 |
| 富文本评论 | `textarea` | 纯文本评论 |

#### 0.5 验证清单

- [ ] `npx shadcn@latest init` 完成
- [ ] 所有核心组件安装成功
- [ ] Neon Forge 主题 CSS 变量配置
- [ ] 组件测试页面 `/test/components` 创建（可选）
- [ ] 构建无报错 `npm run build`

**交付物：**
- [ ] `frontend/components/ui/` 目录包含所有 shadcn 组件
- [ ] `frontend/app/globals.css` 包含 Neon Forge 主题变量
- [ ] `components.json` shadcn 配置文件

---

### Phase 1: OpenAPI 规范补全

**目标：** 在 `.synnovator/openapi.yaml` 中添加所有缺失的 API 定义

#### 1.1 添加 Auth 标签和端点

```yaml
# 新增 tag
- name: auth
  description: Authentication and authorization

# 新增 paths
/auth/login:
  post:
    summary: User login
    operationId: login
    tags: [auth]
    requestBody:
      required: true
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/LoginRequest'
    responses:
      '200':
        description: Login successful
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/LoginResponse'
      '401':
        $ref: '#/components/responses/Unauthorized'

/auth/logout:
  post:
    summary: User logout
    operationId: logout
    tags: [auth]
    security:
      - bearerAuth: []
    responses:
      '204':
        description: Logged out successfully

/auth/refresh:
  post:
    summary: Refresh access token
    operationId: refresh_token
    tags: [auth]
    requestBody:
      required: true
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/RefreshRequest'
    responses:
      '200':
        description: Token refreshed
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/LoginResponse'
```

#### 1.2 添加 User Relations 端点

```yaml
/users/{user_id}/follow:
  post:
    summary: Follow user
    operationId: follow_user
    tags: [users]
    parameters:
      - name: user_id
        in: path
        required: true
        schema:
          type: string
    responses:
      '201':
        description: Followed
      '409':
        description: Already following
  delete:
    summary: Unfollow user
    operationId: unfollow_user
    tags: [users]
    parameters:
      - name: user_id
        in: path
        required: true
        schema:
          type: string
    responses:
      '204':
        description: Unfollowed

/users/{user_id}/followers:
  get:
    summary: List user followers
    operationId: list_user_followers
    tags: [users]
    parameters:
      - name: user_id
        in: path
        required: true
        schema:
          type: string
      - $ref: '#/components/parameters/SkipParam'
      - $ref: '#/components/parameters/LimitParam'
    responses:
      '200':
        description: List of followers
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/PaginatedUserList'

/users/{user_id}/following:
  get:
    summary: List users that this user follows
    operationId: list_user_following
    tags: [users]
    parameters:
      - name: user_id
        in: path
        required: true
        schema:
          type: string
      - $ref: '#/components/parameters/SkipParam'
      - $ref: '#/components/parameters/LimitParam'
    responses:
      '200':
        description: List of users being followed
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/PaginatedUserList'
```

#### 1.3 添加 Category Association 端点

```yaml
/categories/{category_id}/categories:
  get:
    summary: List category associations
    operationId: list_category_associations
    tags: [categories]
    parameters:
      - name: category_id
        in: path
        required: true
        schema:
          type: string
      - name: relation_type
        in: query
        schema:
          type: string
          enum: [stage, track, prerequisite]
    responses:
      '200':
        description: List of associated categories
        content:
          application/json:
            schema:
              type: array
              items:
                $ref: '#/components/schemas/CategoryAssociation'
  post:
    summary: Create category association
    operationId: create_category_association
    tags: [categories]
    parameters:
      - name: category_id
        in: path
        required: true
        schema:
          type: string
    requestBody:
      required: true
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/CategoryAssociationCreate'
    responses:
      '201':
        description: Association created
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/CategoryAssociation'
      '400':
        description: Invalid association (circular dependency, self-reference)
      '409':
        description: Association already exists

/categories/{category_id}/categories/{target_category_id}:
  delete:
    summary: Delete category association
    operationId: delete_category_association
    tags: [categories]
    parameters:
      - name: category_id
        in: path
        required: true
        schema:
          type: string
      - name: target_category_id
        in: path
        required: true
        schema:
          type: string
    responses:
      '204':
        description: Association deleted
      '404':
        $ref: '#/components/responses/NotFound'
```

#### 1.4 添加 Notifications 端点

```yaml
/notifications:
  get:
    summary: List notifications for current user
    operationId: list_notifications
    tags: [notifications]
    parameters:
      - $ref: '#/components/parameters/SkipParam'
      - $ref: '#/components/parameters/LimitParam'
      - name: is_read
        in: query
        schema:
          type: boolean
    responses:
      '200':
        description: List of notifications
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/PaginatedNotificationList'

/notifications/{notification_id}:
  patch:
    summary: Update notification (mark as read)
    operationId: update_notification
    tags: [notifications]
    parameters:
      - name: notification_id
        in: path
        required: true
        schema:
          type: string
    requestBody:
      required: true
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/NotificationUpdate'
    responses:
      '200':
        description: Notification updated
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/Notification'

/notifications/read-all:
  post:
    summary: Mark all notifications as read
    operationId: mark_all_notifications_read
    tags: [notifications]
    responses:
      '204':
        description: All notifications marked as read
```

#### 1.5 添加必要的 Schema

```yaml
# Auth Schemas
LoginRequest:
  type: object
  required: [email, password]
  properties:
    email:
      type: string
      format: email
    password:
      type: string
      format: password
      minLength: 8

LoginResponse:
  type: object
  required: [access_token, token_type, user]
  properties:
    access_token:
      type: string
    refresh_token:
      type: string
    token_type:
      type: string
      default: bearer
    expires_in:
      type: integer
      description: Token expiration time in seconds
    user:
      $ref: '#/components/schemas/User'

RefreshRequest:
  type: object
  required: [refresh_token]
  properties:
    refresh_token:
      type: string

# Category Association Schema
CategoryAssociationType:
  type: string
  enum: [stage, track, prerequisite]
  description: |
    - stage: Sequential stages (赛段), requires stage_order
    - track: Parallel tracks (赛道)
    - prerequisite: Prerequisite activity (前置条件)

CategoryAssociationCreate:
  type: object
  required: [target_category_id, relation_type]
  properties:
    target_category_id:
      type: string
    relation_type:
      $ref: '#/components/schemas/CategoryAssociationType'
    stage_order:
      type: integer
      description: Required for stage type, defines sequence order

CategoryAssociation:
  type: object
  required: [source_category_id, target_category_id, relation_type, created_at]
  properties:
    source_category_id:
      type: string
    target_category_id:
      type: string
    target_category:
      $ref: '#/components/schemas/Category'
    relation_type:
      $ref: '#/components/schemas/CategoryAssociationType'
    stage_order:
      type: integer
      description: Order for stage type associations
    created_at:
      type: string
      format: date-time

# Notification Schema
NotificationType:
  type: string
  enum: [award, comment, team_request, follow, mention, system]
  description: |
    - award: Competition award notification
    - comment: Comment on your post
    - team_request: Team join request
    - follow: Someone followed you
    - mention: Mentioned in a post/comment
    - system: System notification

Notification:
  type: object
  required: [id, type, content, is_read, created_at]
  properties:
    id:
      type: string
    type:
      $ref: '#/components/schemas/NotificationType'
    title:
      type: string
    content:
      type: string
    is_read:
      type: boolean
      default: false
    related_url:
      type: string
      description: URL to the related content
    actor:
      $ref: '#/components/schemas/User'
      description: The user who triggered the notification
    created_at:
      type: string
      format: date-time

NotificationUpdate:
  type: object
  properties:
    is_read:
      type: boolean

PaginatedNotificationList:
  type: object
  required: [items, total, skip, limit]
  properties:
    items:
      type: array
      items:
        $ref: '#/components/schemas/Notification'
    total:
      type: integer
    skip:
      type: integer
    limit:
      type: integer
    unread_count:
      type: integer
      description: Total count of unread notifications

# Stats Schema
PlatformStats:
  type: object
  properties:
    total_categories:
      type: integer
    total_posts:
      type: integer
    total_users:
      type: integer
    total_groups:
      type: integer
    active_categories:
      type: integer
      description: Categories with status=published
    recent_submissions:
      type: integer
      description: Posts created in last 7 days
```

**交付物：**
- [ ] 更新 `.synnovator/openapi.yaml`
- [ ] 运行 OpenAPI 验证确保无语法错误

---

### Phase 2: 数据模型补全

**目标：** 补全缺失的数据模型和缓存字段

#### 2.1 新增 Notification 模型

**当前状态：** 🔴 不存在

**文件：** `app/models/notification.py`

```python
from sqlalchemy import Column, String, Boolean, ForeignKey, Text
from sqlalchemy.orm import relationship
from app.models.base import BaseModel

class Notification(BaseModel):
    __tablename__ = "notifications"

    user_id = Column(String(26), ForeignKey("users.id"), nullable=False, index=True)
    type = Column(String(20), nullable=False)  # award|comment|team_request|follow|mention|system
    title = Column(String(200), nullable=True)
    content = Column(Text, nullable=False)
    is_read = Column(Boolean, default=False, nullable=False)
    related_url = Column(String(500), nullable=True)
    actor_id = Column(String(26), ForeignKey("users.id"), nullable=True, index=True)

    # Relationships
    user = relationship("User", foreign_keys=[user_id], back_populates="notifications")
    actor = relationship("User", foreign_keys=[actor_id])
```

#### 2.2 User 模型添加缓存字段

**当前状态：** 🔴 缺失 follower_count / following_count

**文件：** `app/models/user.py`

```python
# 添加以下字段
follower_count = Column(Integer, nullable=False, default=0)
following_count = Column(Integer, nullable=False, default=0)

# 添加 notifications 关系
notifications = relationship("Notification", back_populates="user", foreign_keys="Notification.user_id")
```

#### 2.3 Category 模型添加缓存字段

**当前状态：** 🔴 缺失 participant_count

**文件：** `app/models/category.py`

```python
# 添加以下字段
participant_count = Column(Integer, nullable=False, default=0)
```

#### 2.4 更新 Schema

**User Schema (`app/schemas/user.py`):**
```python
class UserBase(BaseModel):
    # ... existing fields
    follower_count: int = 0
    following_count: int = 0
```

**Category Schema (`app/schemas/category.py`):**
```python
class CategoryBase(BaseModel):
    # ... existing fields
    participant_count: int = 0
```

**交付物：**
- [ ] 创建 `app/models/notification.py`
- [ ] 更新 `app/models/user.py` 添加缓存字段
- [ ] 更新 `app/models/category.py` 添加缓存字段
- [ ] 创建 `app/schemas/notification.py`
- [ ] 更新 `app/schemas/user.py`
- [ ] 更新 `app/schemas/category.py`
- [ ] 更新 `app/models/__init__.py` 导出新模型

---

### Phase 3: 缓存策略实现

**目标：** 实现缺失的缓存更新触发器

#### 3.1 User 缓存更新函数

**当前状态：** 🔴 完全缺失

**文件：** `app/services/cache_update.py` (新建) 或 `app/routers/users.py`

```python
def _update_user_follow_cache(db: Session, user_id: int) -> None:
    """更新用户的 follower_count 和 following_count 缓存"""
    from app import crud

    user = crud.users.get(db, id=user_id)
    if user is None:
        return

    # 计算粉丝数 (被多少人关注)
    user.follower_count = crud.user_users.count_followers(db, user_id=user_id)

    # 计算关注数 (关注了多少人)
    user.following_count = crud.user_users.count_following(db, user_id=user_id)

    db.add(user)
    db.commit()
```

**调用位置：**
- `POST /users/{id}/follow` - 关注后更新双方计数
- `DELETE /users/{id}/follow` - 取关后更新双方计数
- `app/services/cascade_delete.py` - 用户删除时清理

#### 3.2 Category 缓存更新函数

**当前状态：** 🔴 完全缺失

```python
def _update_category_participant_cache(db: Session, category_id: int) -> None:
    """更新活动的 participant_count 缓存"""
    from app import crud

    category = crud.categories.get(db, id=category_id)
    if category is None:
        return

    # 计算参与团队数
    category.participant_count = crud.category_groups.count_by_category(db, category_id=category_id)

    db.add(category)
    db.commit()
```

**调用位置：**
- `POST /categories/{id}/groups` - 团队报名后
- `DELETE /categories/{id}/groups/{group_id}` - 取消报名后
- `app/services/cascade_delete.py` - 团队删除时

#### 3.3 CRUD 补充

**文件：** `app/crud/user_users.py`

```python
def count_followers(self, db: Session, user_id: int) -> int:
    """统计粉丝数"""
    return db.query(UserUser).filter(
        UserUser.target_user_id == user_id,
        UserUser.relation_type == "follow"
    ).count()

def count_following(self, db: Session, user_id: int) -> int:
    """统计关注数"""
    return db.query(UserUser).filter(
        UserUser.source_user_id == user_id,
        UserUser.relation_type == "follow"
    ).count()
```

**文件：** `app/crud/category_groups.py`

```python
def count_by_category(self, db: Session, category_id: int) -> int:
    """统计活动参与团队数"""
    return db.query(CategoryGroup).filter(
        CategoryGroup.category_id == category_id
    ).count()
```

**交付物：**
- [ ] 创建 `app/services/cache_update.py`
- [ ] 实现 `_update_user_follow_cache()`
- [ ] 实现 `_update_category_participant_cache()`
- [ ] 更新 `app/crud/user_users.py` 添加计数方法
- [ ] 更新 `app/crud/category_groups.py` 添加计数方法
- [ ] 在相关路由中调用缓存更新函数
- [ ] 更新 `app/services/cascade_delete.py` 添加缓存清理

---

### Phase 4: 权限校验修复

**目标：** 修复权限系统的严重漏洞

#### 4.1 所有 DELETE 端点添加所有权检查 (🔴 严重)

**当前状态：** 任何用户都可删除任何资源！

**需要修复的端点：**

| 端点 | 所需权限 |
|------|---------|
| `DELETE /posts/{id}` | 作者 or Admin |
| `DELETE /groups/{id}` | Owner or Admin |
| `DELETE /resources/{id}` | 创建者 or Admin |
| `DELETE /users/{id}` | 本人 or Admin |
| `DELETE /rules/{id}` | 创建者 or Admin |
| `DELETE /categories/{id}` | 创建者 or Admin |

**实现模式：**

```python
# app/deps.py - 添加通用所有权检查依赖
def require_ownership(resource_type: str):
    """Factory: 检查当前用户是否为资源所有者或 Admin"""
    def _check_ownership(
        resource_id: str,
        x_user_id: Optional[int] = Header(None),
        db: Session = Depends(get_db),
    ) -> int:
        if x_user_id is None:
            raise HTTPException(status_code=401, detail="Authentication required")

        from app import crud
        user = crud.users.get(db, id=x_user_id)
        if user is None:
            raise HTTPException(status_code=401, detail="User not found")

        # Admin 可以操作任何资源
        if user.role == "admin":
            return x_user_id

        # 检查资源所有权
        resource = getattr(crud, resource_type).get(db, id=resource_id)
        if resource is None:
            raise HTTPException(status_code=404, detail="Resource not found")

        if resource.created_by != x_user_id:
            raise HTTPException(status_code=403, detail="Not the resource owner")

        return x_user_id
    return _check_ownership
```

**路由修改示例 (`app/routers/posts.py`):**

```python
@router.delete("/posts/{post_id}", status_code=204)
def delete_post(
    post_id: str,
    user_id: int = Depends(require_current_user_id),  # 添加
    db: Session = Depends(get_db),
):
    post = _crud.posts.get(db, id=post_id)
    if post is None:
        raise HTTPException(status_code=404, detail="Post not found")

    # 添加所有权检查
    user = _crud.users.get(db, id=user_id)
    if user.role != "admin" and post.created_by != user_id:
        raise HTTPException(status_code=403, detail="Not the post owner")

    _crud.posts.remove(db, id=post_id)
```

#### 4.2 PATCH 端点添加所有权检查

**需要修复的端点：**

| 端点 | 当前状态 | 所需权限 |
|------|---------|---------|
| `PATCH /posts/{id}` | ❌ 无检查 | 作者 or Admin |
| `PATCH /groups/{id}` | ❌ 无检查 | Owner/Admin member or Admin |
| `PATCH /resources/{id}` | ❌ 无检查 | 创建者 or Admin |
| `PATCH /users/{id}` | ❌ 无检查 | 本人 or Admin |
| `PATCH /rules/{id}` | ❌ 无检查 | 创建者 or Admin |
| `PATCH /categories/{id}` | ✅ 已有 | (保持现状) |

#### 4.3 Admin 批操作实现

**当前状态：** 🔴 3 个端点全部为 TODO

**文件：** `app/routers/admin.py`

```python
@router.delete("/admin/posts", response_model=schemas.BatchResult, tags=["admin"])
def batch_delete_posts(
    body: schemas.BatchIds,
    user_id: int = Depends(require_role("admin")),  # 添加权限检查
    db: Session = Depends(get_db),
):
    success_count = 0
    failed_count = 0
    failed_ids = []
    errors = {}

    for post_id in body.ids:
        try:
            post = _crud.posts.get(db, id=post_id)
            if post:
                _crud.posts.remove(db, id=post_id)
                success_count += 1
            else:
                failed_count += 1
                failed_ids.append(post_id)
                errors[post_id] = "Not found"
        except Exception as e:
            failed_count += 1
            failed_ids.append(post_id)
            errors[post_id] = str(e)

    return {
        "success_count": success_count,
        "failed_count": failed_count,
        "failed_ids": failed_ids,
        "errors": errors,
    }

# 同样实现 batch_update_post_status 和 batch_update_user_roles
```

#### 4.4 JWT 认证替换 Header 认证 (P1)

**当前状态：** 使用 `X-User-Id` Header（临时方案，不安全）

**目标架构：**
```
┌─────────────┐      ┌─────────────┐      ┌─────────────┐
│   Client    │ ──── │ JWT Bearer  │ ──── │   FastAPI   │
│             │      │   Token     │      │   verify    │
└─────────────┘      └─────────────┘      └─────────────┘
```

**依赖包：**
```toml
passlib = { extras = ["bcrypt"], version = "^1.7.4" }
python-jose = { extras = ["cryptography"], version = "^3.3.0" }
```

**实现步骤：**
1. 创建 `app/core/security.py` - Token 生成/验证
2. 更新 `app/deps.py` - 替换 Header 认证为 JWT 认证
3. 添加 Token 黑名单支持（可选 Redis）

**交付物：**
- [ ] 修复所有 DELETE 端点权限
- [ ] 修复所有 PATCH 端点权限
- [ ] 实现 Admin 批操作
- [ ] 实现 JWT 认证（P1）

---

### Phase 5: 数据库迁移

**目标：** 生成并执行数据库迁移

**当前状态：** 🔴 `alembic/versions/` 为空，未生成任何迁移

#### 5.1 生成初始迁移

```bash
cd /Users/allenwoods/Sync/2-engineering/SynnovatorZero-Daiming

# 确保所有模型已导入
# 编辑 app/models/__init__.py 确保导出所有模型

# 生成迁移脚本
uv run alembic revision --autogenerate -m "initial_schema"

# 检查生成的迁移脚本
cat app/alembic/versions/*.py

# 执行迁移
uv run alembic upgrade head
```

#### 5.2 迁移内容预览

将创建以下表：
- `users` - 用户表（含新增 follower_count, following_count）
- `categories` - 活动表（含新增 participant_count）
- `posts` - 帖子表
- `resources` - 资源表
- `rules` - 规则表
- `groups` - 团队表
- `interactions` - 互动表
- `comments` - 评论表
- `ratings` - 评分表
- `user_users` - 用户关系表
- `category_categories` - 活动关联表
- `category_groups` - 活动-团队关系表
- `category_posts` - 活动-帖子关系表
- `category_rules` - 活动-规则关系表
- `post_posts` - 帖子关系表
- `post_resources` - 帖子-资源关系表
- `members` - 团队成员表
- `target_interactions` - 目标-互动关系表
- `notifications` - 通知表 (新增)

**交付物：**
- [ ] 生成初始迁移脚本
- [ ] 验证迁移脚本正确性
- [ ] 执行迁移
- [ ] 验证表结构

---

### Phase 6: 业务逻辑实现

**目标：** 实现各端点的具体业务逻辑

#### 6.1 Auth 模块 (P0)

- [ ] 实现密码哈希和验证 (passlib + bcrypt)
- [ ] 实现 JWT Token 生成和验证 (python-jose)
- [ ] 实现登录端点 `/auth/login`
  - 验证邮箱+密码
  - 生成 access_token 和 refresh_token
  - 返回用户信息
- [ ] 实现登出端点 `/auth/logout`
  - Token 加入黑名单 (Redis 或内存)
- [ ] 实现 Token 刷新 `/auth/refresh`
- [ ] 集成 OAuth2 (Google/GitHub) - 可使用 `oneauth-oauth2` skill (P1)

#### 6.2 用户关系模块 (P0)

- [ ] 实现关注 `POST /users/{id}/follow`
  - 检查是否已关注
  - 检查不能关注自己
  - 创建 user_user 记录 (relation_type=follow)
  - 创建通知给被关注者
  - **更新双方的 follower_count / following_count 缓存**
- [ ] 实现取关 `DELETE /users/{id}/follow`
  - 删除 user_user 记录
  - **更新双方缓存计数**
- [ ] 实现关注列表查询 `GET /users/{id}/following`
  - 分页返回关注的用户列表
- [ ] 实现粉丝列表查询 `GET /users/{id}/followers`
  - 分页返回粉丝用户列表

#### 6.3 活动关联模块 (P0)

参考测试用例：`specs/testcases/14-category-association.md`

- [ ] 实现创建关联 `POST /categories/{id}/categories`
  - 检查自引用 (TC-CATREL-901)
  - 检查重复创建 (TC-CATREL-900)
  - 检查循环依赖 (TC-CATREL-902，仅 stage 类型)
  - 验证 relation_type 枚举值 (TC-CATREL-903)
- [ ] 实现查询关联 `GET /categories/{id}/categories`
  - 支持按 relation_type 筛选
  - stage 类型按 stage_order 排序
- [ ] 实现删除关联 `DELETE /categories/{id}/categories/{target_id}`
- [ ] 更新报名逻辑，增加前置条件校验
  - TC-PREREQ-002/003: 检查前置活动是否完成
  - TC-STAGE-003/004: 检查前一赛段是否完成

循环依赖检测算法：
```python
def detect_cycle(source_id: str, target_id: str, relation_type: str) -> bool:
    """检测添加 source->target 后是否形成循环"""
    if relation_type != "stage":
        return False

    # BFS 从 target 出发，检查是否能回到 source
    visited = set()
    queue = [target_id]
    while queue:
        current = queue.pop(0)
        if current == source_id:
            return True  # 发现循环
        if current in visited:
            continue
        visited.add(current)
        successors = get_stage_successors(current)
        queue.extend(successors)
    return False
```

#### 6.4 通知模块 (P1)

- [ ] 实现通知 CRUD
  - `GET /notifications` - 列表（分页、筛选已读/未读）
  - `PATCH /notifications/{id}` - 标记已读
  - `POST /notifications/read-all` - 全部已读
- [ ] 实现通知触发器
  - 评论时通知帖子作者
  - 点赞时通知帖子作者（可配置阈值）
  - 关注时通知被关注者
  - 团队申请时通知团队管理员
  - 获奖时通知团队成员
- [ ] 返回未读计数 `unread_count`

**交付物：**
- [ ] `app/routers/auth.py` - Auth 路由
- [ ] `app/routers/notifications.py` - 通知路由
- [ ] 更新 `app/routers/users.py` - 关注相关端点
- [ ] 更新 `app/routers/categories.py` - 活动关联端点
- [ ] `app/services/notification_triggers.py` - 通知触发器

---

### Phase 7: 前端组件实现

**目标：** 实现 UI 设计文档中定义的前端组件

**当前状态：** 🔴 仅有占位符，无组件实现

#### 7.1 P0 优先级组件

| 组件 | 依赖 API | 文件路径 |
|------|---------|---------|
| `LoginForm` | `/auth/login` | `frontend/components/auth/LoginForm.tsx` |
| `RegisterForm` | `POST /users` | `frontend/components/auth/RegisterForm.tsx` |
| `UserFollowButton` | `/users/{id}/follow` | `frontend/components/user/UserFollowButton.tsx` |
| `CategoryStageView` | `/categories/{id}/categories` | `frontend/components/category/CategoryStageView.tsx` |

#### 7.2 P1 优先级组件

| 组件 | 依赖 API | 文件路径 |
|------|---------|---------|
| `NotificationDropdown` | `/notifications` | `frontend/components/notification/NotificationDropdown.tsx` |
| `FollowersList` | `/users/{id}/followers` | `frontend/components/user/FollowersList.tsx` |
| `FollowingList` | `/users/{id}/following` | `frontend/components/user/FollowingList.tsx` |
| `CategoryTrackView` | `/categories/{id}/categories` | `frontend/components/category/CategoryTrackView.tsx` |

#### 7.3 P2 优先级组件

| 组件 | 依赖 API | 文件路径 |
|------|---------|---------|
| `SearchModal` | `/search` | `frontend/components/search/SearchModal.tsx` |
| `PlatformStats` | `/stats` | `frontend/components/home/PlatformStats.tsx` |

#### 7.4 实现方式

使用 `pen-to-react` skill 或 `openapi-to-components` skill：

```bash
# 从 OpenAPI 生成 TypeScript 类型和 API 客户端
# 然后手动或使用 skill 实现组件
```

**交付物：**
- [ ] `frontend/components/auth/LoginForm.tsx`
- [ ] `frontend/components/auth/RegisterForm.tsx`
- [ ] `frontend/components/user/UserFollowButton.tsx`
- [ ] `frontend/components/user/FollowersList.tsx`
- [ ] `frontend/components/user/FollowingList.tsx`
- [ ] `frontend/components/category/CategoryStageView.tsx`
- [ ] `frontend/components/category/CategoryTrackView.tsx`
- [ ] `frontend/components/notification/NotificationDropdown.tsx`
- [ ] `frontend/components/search/SearchModal.tsx`
- [ ] `frontend/components/home/PlatformStats.tsx`

---

### Phase 8: 测试与文档

#### 8.1 单元测试

- [ ] Auth 模块测试
  - 登录成功/失败
  - Token 验证
  - Token 刷新
  - 登出后 Token 失效
- [ ] 用户关系模块测试
  - 参考 `specs/testcases/13-user-follow.md`
  - TC-FOLLOW-001 ~ TC-FOLLOW-010
- [ ] 活动关联模块测试
  - 参考 `specs/testcases/14-category-association.md`
  - TC-STAGE-001 ~ TC-CATREL-903
- [ ] 通知模块测试
  - 创建/查询/标记已读
- [ ] **权限测试**
  - 所有 DELETE 端点的所有权检查
  - 所有 PATCH 端点的所有权检查
  - Admin 批操作权限

#### 8.2 集成测试

- [ ] 端到端登录流程测试
- [ ] OAuth 集成测试
- [ ] 多阶段活动报名流程测试
- [ ] 通知触发流程测试

#### 8.3 API 文档

- [ ] 更新 Swagger UI
- [ ] 生成 TypeScript 客户端类型（使用 `openapi-to-components` skill）

---

## 三、数据索引

根据 `specs/data-indexing.md`，需要添加的索引：

### 3.1 已有索引 (在模型中定义)

| 表 | 索引 | 状态 |
|----|------|------|
| user_users | source_user_id, target_user_id, UniqueConstraint | ✅ |
| category_categories | source_category_id, target_category_id, UniqueConstraint | ✅ |
| 其他关系表 | 外键索引 + UniqueConstraint | ✅ |

### 3.2 需要补充的索引 (notifications 表)

```sql
-- notifications
CREATE INDEX idx_notification_user ON notifications(user_id, is_read, created_at DESC);
CREATE INDEX idx_notification_unread ON notifications(user_id) WHERE is_read = FALSE;
```

---

## 四、执行顺序

```
Phase 0: shadcn/ui 组件安装与配置
    ├── 0.1 初始化 shadcn/ui
    ├── 0.2 安装核心组件
    ├── 0.3 自定义 Neon Forge 主题
    ├── 0.4 确认替代方案
    └── 0.5 验证构建

Phase 1: OpenAPI 规范补全
    ├── 1.1 添加 Auth 端点
    ├── 1.2 添加 User Relations 端点
    ├── 1.3 添加 Category Association 端点
    ├── 1.4 添加 Notifications 端点
    └── 1.5 添加所有 Schema

Phase 2: 数据模型补全
    ├── 2.1 创建 Notification 模型
    ├── 2.2 User 模型添加缓存字段
    ├── 2.3 Category 模型添加缓存字段
    └── 2.4 更新 Schema

Phase 3: 缓存策略实现
    ├── 3.1 User 缓存更新函数
    ├── 3.2 Category 缓存更新函数
    └── 3.3 CRUD 补充

Phase 4: 权限校验修复 (🔴 优先)
    ├── 4.1 DELETE 端点所有权检查
    ├── 4.2 PATCH 端点所有权检查
    ├── 4.3 Admin 批操作实现
    └── 4.4 JWT 认证 (P1)

Phase 5: 数据库迁移
    ├── 5.1 生成迁移脚本
    └── 5.2 执行迁移

Phase 6: 业务逻辑实现
    ├── 6.1 Auth 模块 (P0)
    ├── 6.2 User Relations 模块 (P0)
    ├── 6.3 Category Association 模块 (P0)
    └── 6.4 Notifications 模块 (P1)

Phase 7: 前端组件实现
    ├── 7.1 P0 组件 (Login, Register, Follow, Stage)
    ├── 7.2 P1 组件 (Notification, Followers, Following, Track)
    └── 7.3 P2 组件 (Search, Stats)

Phase 8: 测试与文档
    ├── 8.1 单元测试
    ├── 8.2 集成测试
    └── 8.3 API 文档
```

---

## 五、风险与依赖

### 5.1 技术风险

| 风险 | 影响 | 缓解措施 |
|------|------|---------|
| **权限漏洞** | 🔴 数据泄露/篡改 | **Phase 4 优先执行** |
| OAuth 集成复杂度 | 延迟上线 | 可先实现密码登录，OAuth 作为 P1 |
| 循环依赖检测性能 | 大量关联时变慢 | 限制关联深度（如最多 10 级） |
| 通知实时推送 | 需要 WebSocket | 先用轮询，后续升级 SSE/WebSocket |
| Token 黑名单存储 | 需要 Redis | 可先用内存存储，生产环境切换 Redis |

### 5.2 外部依赖

- Redis（Token 黑名单、实时计数）- 可选，有内存 fallback
- OneAuth 服务（如使用 OAuth）- P1 优先级
- 前端联调配合

---

## 六、验收标准

### 6.1 功能验收

- [ ] 用户可以通过邮箱+密码登录
- [ ] 用户可以关注/取关其他用户
- [ ] 用户可以查看自己的粉丝和关注列表
- [ ] 组织者可以创建多阶段/多赛道活动
- [ ] 参赛者完成前置活动后可报名目标活动
- [ ] 用户可以收到并查看通知
- [ ] **非所有者无法删除/修改他人资源**
- [ ] **Admin 可执行批量操作**

### 6.2 测试覆盖

- [ ] 所有新增 API 有单元测试
- [ ] `specs/testcases/14-category-association.md` 中的场景全部通过
- [ ] `specs/testcases/13-user-follow.md` 中的场景全部通过
- [ ] **所有权限检查场景有测试**
- [ ] 测试覆盖率 > 80%

### 6.3 文档完整

- [ ] OpenAPI 规范更新并验证通过
- [ ] Swagger UI 可正常访问所有新端点
- [ ] TypeScript 客户端类型生成
- [ ] README 更新新功能说明

---

## 七、相关文档

- UI 设计规范: `specs/ui/ui-design-spec.md`
- 用户旅程: `docs/user-journeys.md`
- 数据类型定义: `docs/data-types.md`
- 关系定义: `docs/relationships.md`
- 缓存策略: `specs/cache-strategy.md`
- 数据索引: `specs/data-indexing.md`
- 测试用例 - 活动关联: `specs/testcases/14-category-association.md`
- 测试用例 - 用户关注: `specs/testcases/13-user-follow.md`
- 现有 OpenAPI: `.synnovator/openapi.yaml`
