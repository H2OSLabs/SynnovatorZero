# 阶段 2.5-3: 种子数据设计与注入

> 从测试用例推导种子数据需求，通过 API 注入数据库。

## 阶段 2.5: 种子数据设计

### 使用 seed-designer Skill

```bash
# 从测试用例提取种子数据需求
uv run python .claude/skills/seed-designer/scripts/extract_requirements.py
```

### 数据来源

| 来源 | 位置 | 内容 |
|------|------|------|
| 测试用例前置条件 | `specs/testcases/*.md` | 每个测试用例的场景隐含的数据 |
| 用户旅程步骤 | `docs/user-journeys/*.md` | 旅程中预先存在的数据 |
| 领域模型文档 | `docs/data-types.md` | 字段定义和枚举值 |

### 输出

| 文件 | 描述 |
|------|------|
| `specs/seed-data-requirements.md` | 种子数据需求清单 |
| `scripts/seed_dev_data.py` | 种子脚本（带测试用例注释） |

### 种子脚本示例

```python
# scripts/seed_dev_data.py

def seed_users():
    """
    用户种子数据
    覆盖测试用例: TC-USER-*, TC-PERM-*, TC-POST-* (前置)
    """
    users = [
        # user_participant_1: 参赛者，用于帖子/报名测试
        {"username": "alice", "role": "participant"},
        # user_organizer_1: 组织者，用于活动/规则创建
        {"username": "organizer", "role": "organizer"},
        # user_admin_1: 管理员，用于权限测试
        {"username": "admin", "role": "admin"},
    ]
    # 注入逻辑...
```

## 阶段 3: 种子数据注入

### 通过 API 注入（推荐）

```bash
# 重置数据库并注入种子数据
make resetdb
make seed
```

> **为什么用 API 注入？** 确保数据通过业务校验规则，与生产环境一致。

### 验证

```bash
# 查看数据库数据
sqlite3 data/synnovator.db << EOF
SELECT COUNT(*) FROM users;
SELECT COUNT(*) FROM events;
SELECT COUNT(*) FROM posts;
EOF

# 运行后端 API 测试
uv run pytest app/tests/ -v
```

**重点验证：**
- 外键关系是否正确建立（TC-REL-*）
- 级联删除是否正常工作（TC-DEL-*）
- 缓存字段是否正确计算（TC-IACT 计数器测试）

## 验证覆盖度

- [ ] 每个 `specs/testcases/*.md` 的测试用例都有对应前置数据
- [ ] `specs/seed-data-requirements.md` 每条数据都有测试用例映射
- [ ] `scripts/seed_dev_data.py` 每个函数都有覆盖的测试用例注释
- [ ] 运行 `make seed` 后，测试用例不会因缺少数据而失败

## 下一步

完成种子数据后，进入 [阶段 4: UI 设计](05-ui-design.md)。
