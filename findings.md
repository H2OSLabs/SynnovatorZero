# Findings: 前端开发工作流双分支设计

> **更新时间**: 2026-02-08

## 1. AI UI 生成工具研究

### 工具对比

| 工具 | 文本输入 | API/MCP | pages.yaml 输出 | 成本 |
|------|---------|---------|-----------------|------|
| **v0.dev** | ✅ 自然语言 | REST API | ❌ 需转换 | $20+/月 |
| **shadcn MCP** | ✅ 对话式 | MCP (已配置) | ❌ 直接安装组件 | 免费 |
| **Magic UI MCP** | ✅ 自然语言 | MCP | ❌ React 组件 | 免费 |
| **Penpot** | ⚠️ 部分 | API + MCP (实验) | ❌ .penpot 格式 | 免费 |
| **Pixso** | ⚠️ 有限 | MCP (仅客户端) | ❌ HTML/图片 | 付费 |
| **Galileo AI** | ✅ 文本/图片 | ❌ 无公开 API | ❌ Figma 导出 | 订阅 |
| **Claude + shadcn** | ✅ 用户旅程 | 原生 | ✅ 可直接生成 | 已订阅 |

### 推荐方案

**Claude + shadcn/ui 混合方法**

优势：
1. **零额外成本** - 使用现有 Claude 订阅
2. **无缝集成** - 与现有 skills 和 MCP 兼容
3. **自定义输出** - 直接生成 `pages.yaml`
4. **主题合规** - 使用 Neon Forge 设计系统
5. **领域感知** - 使用项目上下文（CLAUDE.md、领域模型）

---

## 2. ai-ui-generator Skill 设计

### 架构

```
输入:
├── docs/user-journeys/*.md (用户旅程)
├── specs/testcases/*.md (测试用例)
├── specs/ui/*.pen (可选设计规格)
└── Design system tokens (Neon Forge)

处理:
├── 1. 解析用户旅程为页面需求
├── 2. 映射操作到 UI 模式
├── 3. 使用 shadcn MCP 匹配组件
├── 4. 应用 Neon Forge 主题
└── 5. 生成结构化规格

输出:
├── specs/design/pages.yaml
├── specs/ux/ (交互规格)
└── 组件安装命令
```

### 核心 References

需要创建以下参考文档：

| 文件 | 用途 |
|------|------|
| `component-catalog.md` | shadcn/ui 可用组件清单 |
| `layout-patterns.md` | 常见页面布局模式 |
| `interaction-patterns.md` | 交互模式库 |
| `neon-forge-tokens.md` | 设计系统 token 映射 |

---

## 3. 双分支工作流设计

### 检测逻辑

```python
def detect_design_source():
    # 检查 Figma 资源
    if exists("specs/design/figma/README.md"):
        return "figma"
    if has_figma_url_in_config():
        return "figma"

    # 无 Figma，使用 AI 生成
    return "ai-generated"
```

### 分支 A: 有 Figma

```
figma-resource-extractor
    ↓ specs/design/figma/
ui-spec-generator
    ↓ specs/design/pages.yaml
ux-spec-generator
    ↓ specs/ux/
frontend-prototype-builder
    ↓ React pages
```

### 分支 B: 无 Figma

```
ai-ui-generator
    ↓ 从 User Journey 生成
    ├── specs/design/pages.yaml
    └── specs/ux/
frontend-prototype-builder
    ↓ React pages
```

---

## 4. 已完成事项

- [x] 复制 Figma skills 到当前分支
- [x] 研究 AI UI 生成工具
- [x] 确定推荐方案 (Claude + shadcn/ui)

## 5. 待完成事项

- [ ] 创建 ai-ui-generator skill
- [ ] 创建参考文档 (component-catalog, patterns)
- [ ] 更新工作流文档（双分支）
- [ ] 集成测试
