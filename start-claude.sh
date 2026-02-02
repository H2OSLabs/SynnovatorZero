# 加载环境变量
set -a
source .env
set +a

claude --permission-mode bypassPermissions --mcp-config .claude/mcp.json