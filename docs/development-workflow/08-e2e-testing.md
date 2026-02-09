# 阶段 8: E2E 测试

> 必须步骤：E2E 测试覆盖核心用户旅程和前端-后端集成。

## 测试维度

1. **用户旅程测试**：验证完整业务流程（TC-JOUR-*）
2. **前端集成测试**：验证前端表单真正调用后端 API（TC-FEINT-*）

## 8.1 配置 Playwright

```bash
cd frontend

# 安装 Playwright
npm install -D @playwright/test

# 初始化配置
npx playwright install
```

**playwright.config.ts：**

```typescript
import { defineConfig } from '@playwright/test';

export default defineConfig({
  testDir: './tests/e2e',
  use: {
    baseURL: 'http://localhost:3000',
  },
  webServer: {
    command: 'npm run dev',
    port: 3000,
    reuseExistingServer: true,
  },
});
```

## 8.2 编写用户旅程测试

对照 `docs/user-journeys/*.md` 编写测试：

```typescript
// tests/e2e/user-journeys.spec.ts
import { test, expect } from '@playwright/test';

// J-002: 创建活动
test('organizer can create an event', async ({ page }) => {
  // 设置 Mock 用户（organizer）
  await page.addInitScript(() => {
    localStorage.setItem('mockUserId', 'user_organizer');
  });

  await page.goto('/events/new');
  await page.fill('[name="name"]', 'Test Hackathon');
  await page.fill('[name="description"]', 'A test event');
  await page.click('button[type="submit"]');

  await expect(page).toHaveURL(/\/events\/\w+/);
});

// J-003: 提交作品
test('participant can submit to event', async ({ page }) => {
  await page.addInitScript(() => {
    localStorage.setItem('mockUserId', 'user_participant');
  });

  await page.goto('/events/1');
  await page.click('text=提交作品');
  // ...
});
```

## 8.3 运行 E2E 测试

```bash
# 确保后端运行
make backend &

# 运行所有 E2E 测试
cd frontend && npx playwright test

# 运行指定测试
npx playwright test user-journeys

# 查看测试报告
npx playwright show-report
```

## 8.4 使用 Playwright Trace 调试

当 E2E 测试失败时，Trace 功能可以帮助快速定位问题。

### 启用 Trace

```bash
# 仅在测试失败时保存 trace
uv run pytest e2e/ -v --e2e-trace

# 所有测试都保存 trace（用于调试通过的测试）
uv run pytest e2e/ -v --e2e-trace-all
```

### 查看 Trace

```bash
# 打开 Trace Viewer（可视化界面）
npx playwright show-trace /tmp/e2e_traces/<test_name>.zip
```

Trace Viewer 提供：
- **时间线视图**：每个操作的截图和 DOM 快照
- **网络面板**：所有 HTTP 请求/响应
- **控制台日志**：console.log/error/warn
- **源代码定位**：点击操作跳转到测试代码

### 在测试中使用 traced_page

```python
from conftest import print_console_logs, assert_no_console_errors

def test_something(traced_page):
    """使用 traced_page fixture 自动捕获调试信息"""
    traced_page.goto("http://localhost:3000/explore")
    traced_page.wait_for_load_state("networkidle")

    # 访问捕获的日志
    print(traced_page.console_logs)    # 所有 console 输出
    print(traced_page.console_errors)  # console.error
    print(traced_page.network_errors)  # 失败的网络请求

    # 辅助函数
    print_console_logs(traced_page)       # 打印格式化日志
    assert_no_console_errors(traced_page) # 断言无 JS 错误
```

### Trace 文件内容

| 内容 | 说明 |
|------|------|
| 📸 Screenshots | 每个操作前后的截图 |
| 🌐 Network | 所有 HTTP 请求/响应（含 payload） |
| 📝 Console | 浏览器控制台日志 |
| 🔍 DOM Snapshots | 页面 DOM 快照（可检查元素） |
| 📍 Source Maps | 源代码映射，点击可定位 |

### 最佳实践

1. **CI 中始终启用 `--e2e-trace`**：失败时自动保存 trace
2. **本地调试用 `--e2e-trace-all`**：即使通过也保存，方便分析
3. **使用 `traced_page` fixture**：自动捕获 console 和 network 错误
4. **检查 network_errors**：API 调用失败会记录在这里

## 8.5 测试用例映射

| 用户旅程 | 测试用例 | 测试文件 |
|---------|---------|---------|
| J-001 浏览内容 | TC-JOUR-001 | `browse.spec.ts` |
| J-002 创建活动 | TC-JOUR-002 | `create-event.spec.ts` |
| J-003 提交作品 | TC-JOUR-003 | `submit.spec.ts` |
| J-004 团队管理 | TC-JOUR-004 | `team.spec.ts` |
| ... | ... | ... |

## 下一步

完成 E2E 测试后，进入 [阶段 9: 最终集成验证](09-integration.md)。
