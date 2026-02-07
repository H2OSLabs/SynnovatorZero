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

## 8.4 测试用例映射

| 用户旅程 | 测试用例 | 测试文件 |
|---------|---------|---------|
| J-001 浏览内容 | TC-JOUR-001 | `browse.spec.ts` |
| J-002 创建活动 | TC-JOUR-002 | `create-event.spec.ts` |
| J-003 提交作品 | TC-JOUR-003 | `submit.spec.ts` |
| J-004 团队管理 | TC-JOUR-004 | `team.spec.ts` |
| ... | ... | ... |

## 下一步

完成 E2E 测试后，进入 [阶段 9: 最终集成验证](09-integration.md)。
