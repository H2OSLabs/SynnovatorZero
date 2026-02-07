# 阶段 0: 项目初始化

## 0.1 创建项目结构

```
SynnovatorZero/
├── app/                  # FastAPI 后端（由 api-builder 生成）
├── frontend/             # Next.js 前端
├── .synnovator/          # 文件数据存储 + OpenAPI spec
├── .claude/skills/       # Claude Code skills
├── docs/                 # 功能说明文档
│   ├── data-types.md     #   7 种内容类型字段定义
│   ├── relationships.md  #   9 种关系类型定义
│   ├── crud-operations.md #  CRUD 操作与权限矩阵
│   ├── user-journeys/    #   用户旅程（目录）
│   ├── rule-engine.md    #   声明式规则引擎规范
│   └── development-workflow/  # 本工作流文档（目录）
├── specs/                # 开发规范文档
│   ├── data-integrity.md #   数据完整性约束
│   ├── testcases/        #   测试用例
│   └── ui/               #   Neon Forge 设计系统
├── deploy/               # Docker & 部署配置
├── pyproject.toml        # Python 依赖
├── uv.toml               # UV 包管理器配置
└── Makefile              # 构建命令
```

> **为什么是 `app/` 而不是 `backend/`？**
> api-builder 的 Jinja2 模板硬编码了 `from app.xxx` 导入路径。使用 `app/` 可以零修改地使用生成代码。

## 0.2 配置开发环境

```bash
# 安装 Python 依赖管理工具（如未安装）
# curl -LsSf https://astral.sh/uv/install.sh | sh

# 安装 Node.js (使用 nvm)
nvm install 18
nvm use 18

# 同步所有 Python 依赖
uv sync

# 安装前端依赖
cd frontend && npm install
```

**已安装的 Python 依赖：**
- fastapi, uvicorn, sqlalchemy (后端核心)
- pyyaml, jinja2 (skill 脚本依赖)
- alembic (数据库迁移)
- pytest, httpx (测试)

## 0.3 初始化开发规划

> 每次开始新的开发会话时执行，确保进度不会丢失。

使用 **planning-with-files** skill 创建规划文件：

```bash
bash .claude/skills/planning-with-files/scripts/init-session.sh SynnovatorZero
```

生成三个文件：

| 文件 | 用途 | 更新时机 |
|------|------|----------|
| `task_plan.md` | 阶段规划与进度追踪 | 每个阶段开始/结束时 |
| `findings.md` | 研究发现与技术决策记录 | 每次有新发现时 |
| `progress.md` | 会话执行日志 | 每完成一个操作时 |

**会话恢复（中断后继续）：**

```bash
# 检查上次会话状态
python3 .claude/skills/planning-with-files/scripts/session-catchup.py "$(pwd)"

# 查看 git 变更
git diff --stat

# 读取规划文件，继续执行
cat task_plan.md progress.md
```

## 下一步

完成项目初始化后，进入 [阶段 0.5: 领域建模](01-domain-modeling.md)。
