# CI/CD 部署配置指南

## 架构概览

```
Push to main → GitHub Actions → Self-hosted Runner (部署服务器) → Docker Compose
```

- 代码推送到 `main` 分支自动触发构建部署
- Self-hosted Runner 直接在部署服务器上运行，无需传输镜像
- 部署失败自动回滚到上一个可用版本

## 一、服务器端安装 Self-hosted Runner

### 1. 在 GitHub 添加 Runner

进入仓库 → Settings → Actions → Runners → New self-hosted runner

选择 Linux x64，GitHub 会生成安装命令。

### 2. 在部署服务器执行

```bash
# 创建 runner 目录
mkdir -p /opt/actions-runner && cd /opt/actions-runner

# 下载（使用 GitHub 页面提供的最新版本 URL）
curl -o actions-runner-linux-x64.tar.gz -L https://github.com/actions/runner/releases/download/v2.xxx.x/actions-runner-linux-x64-2.xxx.x.tar.gz
tar xzf actions-runner-linux-x64.tar.gz

# 配置（使用 GitHub 页面提供的 token）
./config.sh --url https://github.com/H2OSLabs/SynnovatorZero --token YOUR_TOKEN

# 安装为 systemd 服务
sudo ./svc.sh install
sudo ./svc.sh start
sudo ./svc.sh status
```

### 3. 确保 Runner 用户有 Docker 权限

```bash
# 将 runner 用户加入 docker 组
sudo usermod -aG docker $(whoami)

# 验证
docker ps
docker compose version
```

### 4. 确保已安装必要工具

```bash
# 检查 docker compose v2
docker compose version

# 检查 curl（健康检查需要）
curl --version

# 检查 git
git --version
```

## 二、GitHub Secrets 配置

进入仓库 → Settings → Secrets and variables → Actions → New repository secret

| Secret 名称 | 必填 | 说明 |
|-------------|------|------|
| `POSTGRES_USER` | 否 | PostgreSQL 用户名，默认 `postgres` |
| `POSTGRES_PASSWORD` | 是 | PostgreSQL 密码 |
| `POSTGRES_DB` | 否 | 数据库名，默认 `synnovator_zero` |
| `DEPLOY_ENV` | 否 | 额外环境变量（每行一个 KEY=VALUE） |

## 三、工作流说明

### 自动触发

Push to `main` 分支自动触发，以下路径变更会被忽略：
- `*.md`（Markdown 文件）
- `docs/**`（文档目录）
- `.claude/**`（Claude 配置）

### 手动触发

GitHub Actions 页面 → Build & Deploy → Run workflow

可选参数：
- `force_rebuild`: 强制无缓存重建镜像

### 部署流程

```
1. Checkout 代码
2. 生成 .env 文件（从 Secrets）
3. Tag 当前镜像为 -prev（用于回滚）
4. docker compose build
5. docker compose up -d
6. 等待 10 秒稳定
7. 健康检查（最多 12 次，间隔 5 秒）
   ├── 成功 → 清理旧镜像 → 完成
   └── 失败 → 自动回滚到 -prev 镜像
```

### 并发控制

使用 `concurrency` 确保同一时间只有一个部署在执行，后续 Push 会排队等待。

## 四、手动部署

如需在服务器上手动执行：

```bash
cd /path/to/SynnovatorZero/deploy

# 交互模式（失败时会提示是否回滚）
./deploy.sh

# CI 模式（失败自动回滚）
./deploy.sh --ci
```

## 五、故障排查

### 查看 Runner 状态

```bash
sudo systemctl status actions.runner.*
sudo journalctl -u actions.runner.* -f
```

### 查看容器日志

```bash
cd /path/to/deploy
docker compose logs -f
docker compose logs backend --tail 50
docker compose logs frontend --tail 50
```

### 手动回滚

```bash
cd /path/to/deploy

# 查看可用的备份镜像
docker images | grep prev

# 恢复
docker tag synnovator-zero-frontend:latest-prev synnovator-zero-frontend:latest
docker tag synnovator-zero-backend:latest-prev synnovator-zero-backend:latest
docker compose up -d
```

### 查看 Workflow 执行记录

GitHub 仓库 → Actions → Build & Deploy → 查看具体运行日志
