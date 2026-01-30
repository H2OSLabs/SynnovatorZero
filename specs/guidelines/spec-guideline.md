# 如何为高性能编程智能体进行结构设计、规划和迭代

**TL;DR: 目标是编写一份清晰的规约，涵盖恰到好处的细节（可能包括结构、风格、测试、边界）来引导 AI，但不要让它不堪重负。将大任务分解为小任务，而不是将所有内容都放在一个大的提示词中。先在只读模式下进行规划，然后持续执行和迭代。**

>   *「我听过很多关于为 [AI 智能体](https://zhida.zhihu.com/search?content_id=269519553&content_type=Article&match_order=1&q=AI+智能体&zd_token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJ6aGlkYV9zZXJ2ZXIiLCJleHAiOjE3Njk2Njk2NDAsInEiOiJBSSDmmbrog73kvZMiLCJ6aGlkYV9zb3VyY2UiOiJlbnRpdHkiLCJjb250ZW50X2lkIjoyNjk1MTk1NTMsImNvbnRlbnRfdHlwZSI6IkFydGljbGUiLCJtYXRjaF9vcmRlciI6MSwiemRfdG9rZW4iOm51bGx9.4n3CLNqaBKpSPrUavounMjZW1KwpWDaOp4PNPLdpaEY&zhida_source=entity) (AI agents) 编写优秀规约的说法，但还没有找到一个可靠的框架。我可以写出一份堪比 RFC 的规约，但到了一定程度，上下文就太大了，模型就会崩溃。」*

许多开发者都有这种挫败感。简单地向一个 AI 智能体扔一份庞大的规约是行不通的——[上下文窗口](https://zhida.zhihu.com/search?content_id=269519553&content_type=Article&match_order=1&q=上下文窗口&zd_token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJ6aGlkYV9zZXJ2ZXIiLCJleHAiOjE3Njk2Njk2NDAsInEiOiLkuIrkuIvmlofnqpflj6MiLCJ6aGlkYV9zb3VyY2UiOiJlbnRpdHkiLCJjb250ZW50X2lkIjoyNjk1MTk1NTMsImNvbnRlbnRfdHlwZSI6IkFydGljbGUiLCJtYXRjaF9vcmRlciI6MSwiemRfdG9rZW4iOm51bGx9.n1GCtkz2vB56fxW8bDpm3i5B3ZwL8OyXut_n9s-7csk&zhida_source=entity)的限制和模型的「[注意力预算](https://zhida.zhihu.com/search?content_id=269519553&content_type=Article&match_order=1&q=注意力预算&zd_token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJ6aGlkYV9zZXJ2ZXIiLCJleHAiOjE3Njk2Njk2NDAsInEiOiLms6jmhI_lipvpooTnrpciLCJ6aGlkYV9zb3VyY2UiOiJlbnRpdHkiLCJjb250ZW50X2lkIjoyNjk1MTk1NTMsImNvbnRlbnRfdHlwZSI6IkFydGljbGUiLCJtYXRjaF9vcmRlciI6MSwiemRfdG9rZW4iOm51bGx9.2x4Db7nbuUy7Hf0sqI1NYdrAFZ_6Pad9lcv6N3TF_5E&zhida_source=entity)」会成为障碍。关键在于编写巧妙的规约：能够清晰引导智能体、保持在实际上下文大小范围内，并随项目演进的文档。本指南将我使用 [Claude Code](https://zhida.zhihu.com/search?content_id=269519553&content_type=Article&match_order=1&q=Claude+Code&zd_token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJ6aGlkYV9zZXJ2ZXIiLCJleHAiOjE3Njk2Njk2NDAsInEiOiJDbGF1ZGUgQ29kZSIsInpoaWRhX3NvdXJjZSI6ImVudGl0eSIsImNvbnRlbnRfaWQiOjI2OTUxOTU1MywiY29udGVudF90eXBlIjoiQXJ0aWNsZSIsIm1hdGNoX29yZGVyIjoxLCJ6ZF90b2tlbiI6bnVsbH0.4arWwYGLSRFrpq6B64k7E1WQwgXSdbdxNgCePOWVOh8&zhida_source=entity) 和 Gemini CLI 等编程智能体的最佳实践提炼成一个规约编写框架，以保持你的 AI 智能体专注和高效。

我们将介绍编写优秀 AI 智能体规约的五个原则。

## **1. 从一个高层次的愿景开始，让 AI 起草细节**

**用一份简洁的高层次规约启动你的项目，然后让 AI 将其扩展成详细的计划。**

与其一开始就过度设计，不如从一个明确的目标陈述和几个核心需求开始。把这看作一个「产品简报」，让智能体据此生成一个更详尽的规约。这利用了 AI 在阐述细节方面的优势，同时你保持对方向的控制。除非你已经觉得有非常具体的技术要求必须从一开始就满足，否则这种方法很有效。

**为什么这会有用：** 基于 [LLM](https://zhida.zhihu.com/search?content_id=269519553&content_type=Article&match_order=1&q=LLM&zd_token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJ6aGlkYV9zZXJ2ZXIiLCJleHAiOjE3Njk2Njk2NDAsInEiOiJMTE0iLCJ6aGlkYV9zb3VyY2UiOiJlbnRpdHkiLCJjb250ZW50X2lkIjoyNjk1MTk1NTMsImNvbnRlbnRfdHlwZSI6IkFydGljbGUiLCJtYXRjaF9vcmRlciI6MSwiemRfdG9rZW4iOm51bGx9.vWKidZrxZJ-eThpLi2JQNHG2F7NSyKKkFXzMXvnx-ew&zhida_source=entity) (大语言模型) 的智能体在给定一个坚实的高层次指令时，非常擅长充实细节，但它们需要一个明确的任务来避免偏离轨道。通过提供一个简短的大纲或目标描述，并要求 AI 生成一个完整的规约（例如一个 spec.md 文件），你就为智能体创建了一个持久的参考。对于智能体来说，提前规划更为重要——你可以先迭代计划，然后把它交给智能体来编写代码。这份规约成为你和 AI 共同构建的第一个产物。

**实践方法：** 通过以下提示词开始一个新的编程会话：

>   「你是一名 AI 软件工程师。为 [项目 X] 起草一份详细的规约，涵盖目标、功能、约束和一个分步计划。」
>   保持你最初的提示词是高层次的——例如，「构建一个 web 应用，用户可以在其中跟踪任务（待办事项列表），包含用户账户、一个数据库和一个简单的 UI」。

智能体可能会响应一个结构化的规约草案：一个概述、功能列表、技术栈建议、数据模型等等。这份规约随后成为你和智能体都可以回顾的「事实来源」。GitHub 的 AI 团队提倡[规约驱动开发 (spec-driven development)](https://link.zhihu.com/?target=https%3A//github.blog/ai-and-ml/generative-ai/spec-driven-development-with-ai-get-started-with-a-new-open-source-toolkit/)，其中「规约成为共享的事实来源……是与项目一同演进的、活的、可执行的产物」。在编写任何代码之前，审查并完善 AI 的规约。确保它与你的愿景一致，并纠正任何幻觉或偏离目标的细节。

**使用规划模式 (Plan Mode) 强制规划优先：**像 Claude Code 这样的工具提供了[规划模式 (Plan Mode)](https://link.zhihu.com/?target=https%3A//code.claude.com/docs/en/common-workflows)，它将智能体的操作限制为只读——它可以分析你的代码库并创建详细的计划，但在你准备好之前不会编写任何代码。这对于规划阶段是理想的：在规划模式下开始（在 Claude Code 中是 Shift+Tab），描述你想要构建什么，让智能体在探索你现有代码的同时起草一份规约。要求它通过向你提问关于计划的问题来澄清模糊之处。让它审查计划的架构、最佳实践、安全风险和测试策略。目标是完善计划，直到没有误解的余地。只有那时，你才退出规划模式，让智能体执行。这个工作流可以防止在规约稳固之前就直接跳入代码生成的常见陷阱。

**将规约用作上下文：** 一旦批准，保存这份规约（例如，保存为 SPEC.md），并根据需要将相关部分提供给智能体。许多使用强大模型的开发者正是这样做的——规约文件在会话之间保持持久，每当项目工作恢复时，它就能锚定 AI。这减轻了当对话历史过长或当你必须重启智能体时可能发生的遗忘。这类似于在团队中使用产品需求文档 (Product Requirements Document, PRD) 的方式：一个所有成员（无论是人还是 AI）都可以查阅以保持同步的参考。正如一位工程师所观察到的，经验丰富的人通常会「[先写好文档](https://link.zhihu.com/?target=https%3A//simonwillison.net/2025/Oct/7/vibe-engineering/)，模型可能仅凭这些输入就能构建出匹配的实现」。规约就是那个文档。

**保持目标导向：** 为 AI 智能体编写的高层次规约应侧重于「做什么 (what)」和「为什么 (why)」，而不是琐碎的「如何做 (how)」（至少在初期是这样）。把它想象成用户故事和验收标准：用户是谁？他们需要什么？成功的标准是什么？（例如，「用户可以添加、编辑、完成任务；数据被持久化保存；应用响应迅速且安全」）。这使得 AI 的详细规约始终以用户需求和结果为基础，而不仅仅是技术上的待办事项。正如 [GitHub Spec Kit 文档](https://link.zhihu.com/?target=https%3A//github.blog/ai-and-ml/generative-ai/spec-driven-development-with-ai-get-started-with-a-new-open-source-toolkit/)所说，提供一个关于你正在构建什么及其原因的高层次描述，然后让编程智能体生成一个关注用户体验和成功标准的详细规约。从这个宏观愿景开始，可以防止智能体在后来进入编程阶段时只见树木不见森林。

## **2. 采用专业的 PRD (或 SRS) 的结构化框架**

**将你的 AI 规约视为一份结构化文档 (PRD)，包含清晰的章节，而不是一堆松散的笔记。**

许多开发者对待智能体的规约，就像对待传统的产品需求文档 (PRDs) 或系统设计文档一样——全面、组织良好，并且易于一个「字面思维」的 AI 解析。这种正式的方法为智能体提供了一个遵循的蓝图，并减少了模糊性。

**六个核心领域：** GitHub 对[超过 2,500 个智能体配置文件](https://link.zhihu.com/?target=https%3A//github.blog/ai-and-ml/github-copilot/how-to-write-a-great-agents-md-lessons-from-over-2500-repositories/)的分析揭示了一个清晰的模式：最有效的规约涵盖了六个领域。以此作为完整性的检查清单：

**1. 命令 (Commands):** 尽早放入可执行命令——不仅仅是工具名称，而是带有标志的完整命令：`npm test`、`pytest -v`、`npm run build`。智能体将不断参考这些命令。

**2. 测试 (Testing):** 如何运行测试，你使用什么框架，测试文件在哪里，以及覆盖率期望是什么。

**3. 项目结构 (Project structure):** 源代码在哪里，测试放在哪里，文档属于哪里。要明确：「`src/` 用于应用代码，`tests/` 用于单元测试，`docs/` 用于文档。」

**4. 代码风格 (Code style):** 一个展示你风格的真实代码片段胜过三段描述它的文字。包括命名约定、格式化规则和良好输出的示例。

**5. Git 工作流 (Git workflow):** 分支命名、提交信息格式、PR 要求。如果你明确说明，智能体可以遵循这些。

**6. 边界限制 (Boundaries):** 智能体永远不应该触碰的东西——密钥文件、供应商目录、生产配置、特定文件夹。「绝不提交密钥」是 GitHub 研究中单个最常见的有用约束。

**具体说明你的技术栈：** 说「React 18 与 TypeScript、Vite 和 Tailwind CSS」，而不是「React 项目」。包括版本和关键依赖项。模糊的规约产生模糊的代码。

**使用一致的格式：** 清晰度是王道。许多开发者在规约中使用 Markdown 标题甚至类似 XML 的标签来划分章节，因为 AI 模型处理结构良好的文本比处理自由形式的散文更好。例如，你可以这样构建规约：

```text
# 项目规约：我团队的任务应用

## 目标
- 构建一个供小团队管理任务的 web 应用...

## 技术栈
- React 18+, TypeScript, Vite, Tailwind CSS
- Node.js/Express 后端, PostgreSQL, Prisma ORM

## 命令
- 构建: `npm run build` (编译 TypeScript, 输出到 dist/)
- 测试: `npm test` (运行 Jest, 提交前必须通过)
- 代码检查: `npm run lint --fix` (自动修复 ESLint 错误)

## 项目结构
- `src/` – 应用源代码
- `tests/` – 单元和集成测试
- `docs/` – 文档

## 边界
- ✅ 总是: 提交前运行测试, 遵循命名约定
- ⚠️ 先询问: 数据库模式变更, 添加依赖项
- 🚫 绝不: 提交密钥, 编辑 node_modules/, 修改 CI 配置
```

这种组织水平不仅有助于你清晰地思考，也有助于 AI 找到信息。Anthropic 的工程师建议[将提示词组织成不同的部分](https://link.zhihu.com/?target=https%3A//www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)（如 <background>, <instructions>, <tools>, <output_format> 等），正是出于这个原因——它给了模型关于哪部分信息是什么的强烈线索。并且记住，「精简不等于简短」——如果规约中的细节很重要，不要回避，但要保持专注。

**将规约集成到你的工具链中：** 将规约视为与版本控制和 CI/CD 绑定的「可执行产物」。[GitHub Spec Kit](https://link.zhihu.com/?target=https%3A//github.blog/ai-and-ml/generative-ai/spec-driven-development-with-ai-get-started-with-a-new-open-source-toolkit/) 使用一个四阶段、门控式的工作流，使你的规约成为工程流程的中心。规约不是写完就放在一边，而是驱动实现、检查清单和任务分解。你的主要角色是引导；编程智能体则完成大部分的编写工作。每个阶段都有一个特定的任务，在当前任务完全验证之前，你不会进入下一个阶段：

![img](https://pic3.zhimg.com/v2-4c01d977dc0e09bd1d07056a992c45c8_1440w.jpg)

**1. 明确需求 (Specify):** 你提供一个关于你正在构建什么及其原因的高层次描述，编程智能体则生成一份详细的规约。这无关技术栈或应用设计——它关乎用户旅程、体验以及成功的标准。谁会使用它？它解决了什么问题？他们将如何与它互动？把它想象成绘制你想要创造的用户体验地图，然后让编程智能体充实细节。这成为一个随着你了解更多而演进的活产物。

**2. 计划 (Plan):** 进入技术层面。你提供你想要的技术栈、架构和约束，编程智能体则生成一个全面的技术计划。如果你的公司有标准化的技术，就在这里说明。如果你需要与遗留系统集成或有合规性要求，所有这些都放在这里。你可以要求多种计划变体来比较方法。如果你提供了内部文档，智能体可以将你的架构模式直接集成到计划中。

**3. 任务 (Tasks):** 编程智能体接受规约和计划，并将它们分解为实际的工作——小的、可审查的块，每个块解决难题的一个特定部分。每个任务都应该是你可以独立实现和测试的东西，几乎就像是为你的 AI 智能体进行测试驱动开发。你得到的不是「构建认证功能」，而是具体的任务，如「创建一个用户注册端点，验证电子邮件格式」。

**4. 实施 (Implement):** 你的编程智能体逐个（或并行地）处理任务。你审查的是解决特定问题的专注变更，而不是上千行的代码转储。智能体知道要构建什么（规约）、如何构建（计划）以及要做什么（任务）。关键是，你的角色是在每个阶段进行验证：规约是否捕捉到了你想要的东西？计划是否考虑了约束？AI 是否遗漏了边缘情况？这个过程为你内置了检查点，以便在进入下一步之前进行批判、发现差距和纠正方向。

这种门控式的工作流可以防止 Willison 所说的「纸牌屋代码」——那些在审查下会崩溃的脆弱 AI 输出。Anthropic 的 Skills 系统提供了类似的模式，让你定义可重用的、基于 Markdown 的行为，智能体可以调用这些行为。通过将你的规约嵌入到这些工作流中，你确保智能体在规约得到验证之前无法继续，并且变更会自动传播到任务分解和测试中。

**考虑为专门的角色使用 agents.md：**对于像 [GitHub Copilot](https://zhida.zhihu.com/search?content_id=269519553&content_type=Article&match_order=1&q=GitHub+Copilot&zd_token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJ6aGlkYV9zZXJ2ZXIiLCJleHAiOjE3Njk2Njk2NDAsInEiOiJHaXRIdWIgQ29waWxvdCIsInpoaWRhX3NvdXJjZSI6ImVudGl0eSIsImNvbnRlbnRfaWQiOjI2OTUxOTU1MywiY29udGVudF90eXBlIjoiQXJ0aWNsZSIsIm1hdGNoX29yZGVyIjoxLCJ6ZF90b2tlbiI6bnVsbH0.o77uqKh8gSTI1fdPJ8nzcg7Ak4h_uSPZEifOxytkAUI&zhida_source=entity) 这样的工具，你可以创建 [agents.md 文件](https://link.zhihu.com/?target=https%3A//github.blog/ai-and-ml/github-copilot/how-to-write-a-great-agents-md-lessons-from-over-2500-repositories/)来定义专门的智能体角色——一个用于技术写作的 @docs-agent，一个用于 QA 的 @test-agent，一个用于代码审查的 @security-agent。每个文件都作为该角色行为、命令和边界的专注规约。当你希望为不同任务使用不同智能体，而不是一个通用助手时，这尤其有用。

**为智能体体验 (Agent Experience, AX) 而设计：** 正如我们为开发者体验 (Developer Experience, DX) 设计 API 一样，考虑为「智能体体验」设计规约。这意味着使用干净、可解析的格式：智能体将消费的任何 API 的 OpenAPI 模式，为 LLM 消费而总结文档的 llms.txt 文件，以及明确的类型定义。Agentic AI Foundation (AAIF) 正在标准化像 [MCP](https://zhida.zhihu.com/search?content_id=269519553&content_type=Article&match_order=1&q=MCP&zd_token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJ6aGlkYV9zZXJ2ZXIiLCJleHAiOjE3Njk2Njk2NDAsInEiOiJNQ1AiLCJ6aGlkYV9zb3VyY2UiOiJlbnRpdHkiLCJjb250ZW50X2lkIjoyNjk1MTk1NTMsImNvbnRlbnRfdHlwZSI6IkFydGljbGUiLCJtYXRjaF9vcmRlciI6MSwiemRfdG9rZW4iOm51bGx9.dr7LdASykNwKqpgCxfYhevoJRt63HvGszg3S2ESNdyo&zhida_source=entity) (Model Context Protocol) 这样的协议用于工具集成——遵循这些模式的规约更容易被智能体消费并可靠地执行。

**PRD vs SRS 心态：** 借鉴已建立的文档实践是有帮助的。对于 AI 智能体规约，你通常会将两者融合到一个文档中（如上所示），但涵盖这两个角度对你有利。像 PRD 一样编写它，确保你包含以用户为中心的上下文（「每个功能背后的原因」），这样 AI 就不会为错误的事情进行优化。像 SRS 一样扩展它，确保你确定了 AI 实际生成正确代码所需的具体细节（比如使用哪个数据库或 API）。开发者们发现，这种额外的前期努力通过大幅减少以后与智能体的沟通不畅而得到回报。

**让规约成为一份「活文档」：** 不要写完就忘了。随着你和智能体做出决策或发现新信息，更新规约。如果 AI 必须更改数据模型，或者你决定砍掉一个功能，将这些反映在规约中，使其保持为基准事实。把它想象成版本控制的文档。在[规约驱动的工作流](https://link.zhihu.com/?target=https%3A//github.blog/ai-and-ml/generative-ai/spec-driven-development-with-ai-get-started-with-a-new-open-source-toolkit/)中，规约驱动实现、测试和任务分解，在规约验证之前你不会进入编码阶段。这个习惯能保持项目的一致性，特别是当你或智能体离开一段时间后再回来时。记住，规约不仅仅是为 AI 准备的——它也帮助作为开发者的你保持监督，并确保 AI 的工作满足真实需求。

## **3. 将任务分解为模块化的提示词和上下文，而不是一个单一的提示词**

**分而治之：一次给 AI 一个专注的任务，而不是一个包含所有内容的大而全的提示词。**

经验丰富的 AI 工程师已经认识到，试图将整个项目（所有需求、所有代码、所有指令）塞进一个单一的提示词或智能体消息中，是导致混乱的根源。你不仅可能触及 Token 限制，还可能因为「[指令诅咒 (curse of instructions)](https://link.zhihu.com/?target=https%3A//maxpool.dev/research-papers/curse_of_instructions_report.html)」而导致模型失去焦点——过多的指令导致它无法很好地遵循任何一个。解决方案是以模块化的方式设计你的规约和工作流，一次处理一个部分，并且只引入该部分所需的上下文。

![img](https://pica.zhimg.com/v2-2d387edc68c53ae37e856635fc8c43a8_1440w.jpg)

**过多上下文/指令的诅咒：** 研究已经证实了许多开发者凭经验观察到的现象：当你向提示词中堆砌更多指令或数据时，模型遵守每一条指令的性能会[显著下降](https://link.zhihu.com/?target=https%3A//openreview.net/pdf/848f1332e941771aa491f036f6350af2effe0513.pdf)。一项研究将此称为「指令诅咒」，表明即使是 GPT-4 和 Claude，在被要求同时满足许多要求时也会遇到困难。实际上，如果你给出 10 个详细规则的要点，AI 可能会遵守前几个，然后开始忽略其他的。更好的策略是迭代式专注。[行业指南](https://link.zhihu.com/?target=https%3A//maxpool.dev/research-papers/curse_of_instructions_report.html)建议将复杂需求分解为顺序的、简单的指令作为最佳实践。让 AI 一次专注于一个子问题，完成它，然后再继续下一个。这能保持高质量并使错误可控。

**将规约划分为阶段或组件：** 如果你的规约文档很长或涵盖范围很广，考虑将其拆分为几个部分（可以是物理上独立的文件，也可以是明确分开的章节）。例如，你可能有一个「后端 API 规约」部分和另一个「前端 UI 规约」部分。当 AI 在处理后端时，你不需要总是给它提供前端规约，反之亦然。许多使用多智能体设置的开发者甚至为每个部分创建独立的智能体或子流程——例如，一个智能体负责数据库/模式，另一个负责 API 逻辑，另一个负责前端——每个都只拥有规约的相关部分。即使你使用单个智能体，也可以通过仅将相关规约部分复制到该任务的提示词中来模拟这一点。避免上下文过载：不要一次性将认证任务与数据库模式更改混合在一起，正如 [DigitalOcean AI 指南](https://link.zhihu.com/?target=https%3A//docs.digitalocean.com/products/gradient-ai-platform/concepts/context-management/)所警告的。保持每个提示词都紧密围绕当前目标。

**大型规约的扩展目录/摘要：** 一个聪明的技巧是让智能体为规约构建一个带有摘要的扩展目录。这本质上是一个「规约摘要」，将每个部分浓缩为几个关键点或关键词，并引用可以找到详细信息的位置。例如，如果你的完整规约中有一个长达 500 字的「安全要求」部分，你可以让智能体将其总结为：「安全：使用 HTTPS，保护 API 密钥，实施输入验证（见完整规约 §4.2）」。通过在规划阶段创建一个层次化的摘要，你可以得到一个可以保留在提示词中的鸟瞰图，而细节则在需要时才加载。这个扩展目录就像一个索引：智能体可以查阅它并说「啊哈，有一个我应该看看的安全部分」，然后你就可以按需提供该部分。这类似于人类开发者在处理特定部分时，会先浏览大纲，然后翻到规约文档的相关页面。

要实现这一点，你可以在编写规约后提示智能体：「将上述规约总结成一个非常简洁的大纲，包含每个部分的关键点和一个参考标签。」结果可能是一个章节列表，每个章节都有一到两句的摘要。该摘要可以保存在系统或助手消息中，以引导智能体的注意力，而不会占用太多 Token。这种[层次化摘要方法](https://link.zhihu.com/?target=https%3A//addyo.substack.com/p/context-engineering-bringing-engineering)已知可以通过关注高层结构来帮助 LLM 维持长期上下文。智能体携带了一份规约的「心智地图」。

**为不同规约部分利用子智能体或「技能」：** 另一个高级方法是使用多个专门的智能体（Anthropic 称之为子智能体，或者你可以称之为「技能」）。每个子智能体都针对特定专业领域进行配置，并被赋予与该领域相关的规约部分。例如，你可能有一个数据库设计器子智能体，它只知道规约的数据模型部分，还有一个 API 编码器子智能体，它知道 API 端点规约。主智能体（或一个协调器）可以自动将任务路由到适当的子智能体。好处是每个智能体需要处理的上下文窗口更小，角色更专注，这可以[提高准确性并允许在独立任务上并行工作](https://link.zhihu.com/?target=https%3A//10xdevelopers.dev/structured/claude-code-with-subagents/)。Anthropic 的 Claude Code 通过让你定义拥有自己系统提示词和工具的子智能体来支持这一点。「每个子智能体都有一个特定的目的和专业领域，使用自己独立于主对话的上下文窗口，并有一个自定义的系统提示词来指导其行为」，正如他们的文档所述。当出现与子智能体领域相匹配的任务时，Claude 可以将该任务委托给它，子智能体则独立返回结果。

**并行智能体以提高吞吐量：** 同时运行多个智能体正成为开发者生产力的「下一个大事件」。与其等待一个智能体完成任务后再开始另一个，你可以为不重叠的工作启动并行的智能体。Willison 将此描述为「[拥抱并行编程智能体](https://link.zhihu.com/?target=https%3A//simonwillison.net/2025/Oct/7/vibe-engineering/)」，并指出这「出奇地有效，尽管在精神上很累人」。关键是划分任务范围，使智能体不会互相干扰——一个智能体编码一个功能，而另一个编写测试，或者不同的组件被同时构建。像 LangGraph 或 OpenAI Swarm 这样的协调框架可以帮助协调这些智能体，而通过[向量数据库](https://zhida.zhihu.com/search?content_id=269519553&content_type=Article&match_order=1&q=向量数据库&zd_token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJ6aGlkYV9zZXJ2ZXIiLCJleHAiOjE3Njk2Njk2NDAsInEiOiLlkJHph4_mlbDmja7lupMiLCJ6aGlkYV9zb3VyY2UiOiJlbnRpdHkiLCJjb250ZW50X2lkIjoyNjk1MTk1NTMsImNvbnRlbnRfdHlwZSI6IkFydGljbGUiLCJtYXRjaF9vcmRlciI6MSwiemRfdG9rZW4iOm51bGx9.yzdRlgLADXvrfagGXHe4M1Yk416_PCTPqLIZvO7xHzo&zhida_source=entity)（如 Chroma）的共享内存可以让它们访问公共上下文而无需冗余的提示。

**单智能体 vs. 多智能体：何时使用**

| 方面     | 单智能体                                             | 并行/多智能体                                              |
| -------- | ---------------------------------------------------- | ---------------------------------------------------------- |
| 优势     | 设置更简单；开销更低；易于调试和跟踪                 | 吞吐量更高；能处理复杂的相互依赖关系；各领域有专家         |
| 挑战     | 大型项目中上下文过载；迭代速度较慢；存在单点故障风险 | 协调开销；潜在冲突；需要共享内存（如向量数据库）           |
| 适用场景 | 独立模块；中小型项目；早期原型设计                   | 大型代码库；一人编码+一人测试+一人审查；独立功能开发       |
| 技巧     | 使用规范摘要；每个任务刷新上下文；经常开启新会话     | 初始限制在2-3个智能体；使用MCP进行工具共享；定义清晰的边界 |

在实践中，使用子智能体或特定技能的提示词可能看起来像这样：你维护多个规约文件（或提示词模板）——例如 SPEC_backend.md、SPEC_frontend.md——然后你告诉 AI，「对于后端任务，参考 SPEC_backend；对于前端任务，参考 SPEC_frontend。」或者在像 Cursor/Claude 这样的工具中，你实际上为每个任务启动一个子智能体。这设置起来肯定比单个智能体循环要复杂，但它模仿了人类开发者的做法——我们会在脑海中将一个大的规约 compartmentalize 成相关的块（你不会一次性把整个 50 页的规约都记在脑子里；你会回忆起当前任务所需的部分，并对整体架构有一个大概的了解）。正如所指出的，挑战在于管理相互依赖性：子智能体之间仍必须协调（前端需要知道后端规约中的 API 契约等）。一个中央概览（或一个「架构师」智能体）可以通过引用子规约并确保一致性来提供帮助。

**每个提示词专注于一个任务/部分：** 即使没有花哨的多智能体设置，你也可以手动强制模块化。例如，在规约写好之后，你的下一步可能是：「第一步：实现数据库模式。」你只向智能体提供规约的数据库部分，外加规约中的任何全局约束（如技术栈）。智能体就此工作。然后对于第二步，「现在实现认证功能」，你提供规约的认证部分，如果需要的话，可能还有模式的相关部分。通过为每个主要任务刷新上下文，你确保模型不会携带大量可能分散其注意力的陈旧或不相关信息。正如一个指南所建议的：「[重新开始：在切换主要功能时开始新的会话](https://link.zhihu.com/?target=https%3A//docs.digitalocean.com/products/gradient-ai-platform/concepts/context-management/)以清除上下文」。你可以每次都提醒智能体关键的全局规则（来自规约的约束部分），但如果不是全部需要，就不要把整个规约都塞进去。

**使用内联指令和代码 TODO：** 另一个模块化的技巧是，将你的代码或规约作为对话的活跃部分。例如，用 `// TODO` 注释来构建你的代码框架，描述需要做什么，然后让智能体逐一填充它们。每个 TODO 实际上都充当了一个小任务的迷你规约。这让 AI 保持高度专注（「根据这段规约片段实现这个特定函数」），你可以在一个紧密的循环中进行迭代。这类似于给 AI 一个要完成的清单项目，而不是一次性给整个清单。

底线是：小的、专注的上下文胜过一个巨大的提示词。这能提高质量，并防止 AI 因一次性处理太多而「不堪重负」。正如一套最佳实践所总结的，向模型提供「单一任务焦点」和「仅相关信息」，避免到处倾倒所有东西。通过将工作构建成模块——并使用像规约摘要或子规约智能体这样的策略——你将绕过上下文大小限制和 AI 的短期记忆上限。记住，一个被良好喂养的 AI 就像一个被良好喂养的函数：只给它[当前工作所需的输入](https://link.zhihu.com/?target=https%3A//addyo.substack.com/p/context-engineering-bringing-engineering)。

## **4. 构建自我检查、约束机制并融入人类专业知识**

**让你的规约不仅是智能体的待办事项列表，也是质量控制的指南——并且不要害怕注入你自己的专业知识。**

一份好的 AI 智能体规约会预见 AI 可能出错的地方并设置护栏。它还会利用你所知道的（领域知识、边缘情况、「陷阱」），这样 AI 就不会在真空中操作。把规约想象成 AI 的教练和裁判：它应该鼓励正确的方法并指出犯规。

**使用三层边界：** [GitHub 对 2,500 多个智能体文件的分析](https://link.zhihu.com/?target=https%3A//github.blog/ai-and-ml/github-copilot/how-to-write-a-great-agents-md-lessons-from-over-2500-repositories/)发现，最有效的规约使用三层边界系统，而不是一个简单的「不要做」列表。这为智能体提供了更清晰的指导，关于何时继续、何时暂停和何时停止：

![img](https://pic1.zhimg.com/v2-babcfa34abc9b23c94cdd9145b600522_1440w.jpg)

**✅ 始终执行 (Always do):** 智能体应该无需询问就采取的行动。「总是在提交前运行测试。」「总是遵循风格指南中的命名约定。」「总是将错误记录到监控服务。」

**⚠️ 事先确认 (Ask first):** 需要人类批准的行动。「在修改数据库模式前询问。」「在添加新依赖项前询问。」「在更改 CI/CD 配置前询问。」这一层捕捉了那些可能没问题但需要人类检查的高影响变更。

**🚫 绝对禁止 (Never do):** 硬性停止。「绝不提交密钥或 API keys。」「绝不编辑 node_modules/ 或 vendor/。」「未经明确批准，绝不移除一个失败的测试。」「绝不提交秘密」是该研究中单个最常见的有用约束。

这种三层方法比一个扁平的规则列表更加细致。它承认某些行为总是安全的，某些需要监督，而某些则是绝对禁止的。智能体可以在「总是做」的项目上自信地前进，为「先询问」的项目标记以供审查，并在「绝不做」的项目上硬性停止。

**鼓励自我验证：**一个强大的模式是让智能体自动根据规约验证其工作。如果你的工具允许，你可以集成单元测试或代码检查等检查项，让 AI 在生成代码后运行。但即使在规约/提示词层面，你也可以指示 AI 进行复核：例如，「实现后，将结果与规约进行比较，并确认所有要求都已满足。列出任何未解决的规约项。」这促使 LLM 反思其输出与规约的关系，从而发现遗漏。这是一种内置于流程中的自我审计形式。

例如，你可以在提示词后附加：「（写完函数后，回顾上述需求列表并确保每项都得到满足，标记任何缺失的项）。」然后模型（理想情况下）会输出代码，后面跟着一个简短的检查清单，指明它是否满足了每个要求。这减少了在你运行测试之前它忘记某些东西的可能性。这并非万无一失，但很有帮助。

**使用 LLM-as-a-Judge 进行主观检查：** 对于那些难以自动测试的标准——如代码风格、可读性、对架构模式的遵守——可以考虑使用「LLM-as-a-Judge」。这意味着让第二个智能体（或一个独立的提示词）根据你的规约质量指南来审查第一个智能体的输出。Anthropic 和其他公司发现这种方法对于主观评估很有效。你可能会提示：「审查此代码是否遵守我们的风格指南。标记任何违规行为。」评判智能体返回的反馈要么被采纳，要么触发一次修订。这在语法检查之外增加了一层语义评估。

**一致性测试:** Willison 提倡构建一致性套件——即任何实现都必须通过的、与语言无关的测试（通常基于 YAML）。这些测试充当一种契约：如果你正在构建一个 API，一致性套件会指定预期的输入/输出，而智能体的代码必须满足所有情况。这比临时的单元测试更严格，因为它直接源于规约，并且可以在不同实现中重用。在规约的「成功」部分包含一致性标准（例如，「必须通过 conformance/api-tests.yaml 中的所有测试用例」）。

**在规约中利用测试：** 如果可能，在你的规约和提示词流中加入测试计划甚至实际的测试。在传统开发中，我们使用 TDD 或编写测试用例来澄清需求——你也可以对 AI 做同样的事情。例如，在规约的「成功标准」中，你可能会说「这些示例输入应该产生这些输出……」或「以下单元测试应该通过」。可以提示智能体在脑海中运行这些用例，或者如果它有能力的话，实际执行它们。Simon Willison 指出，拥有一个[健壮的测试套件](https://link.zhihu.com/?target=https%3A//simonwillison.net/2025/Oct/7/vibe-engineering/)就像给了智能体超能力——当测试失败时，它们可以快速验证和迭代。在 AI 编程的上下文中，在规约中为测试或预期结果编写一些伪代码可以指导智能体的实现。此外，你可以在子智能体设置中使用一个专门的「[测试智能体](https://link.zhihu.com/?target=https%3A//10xdevelopers.dev/structured/claude-code-with-subagents/)」，它接受规约的标准并持续验证「代码智能体」的输出。

**运用你的领域知识：** 你的规约应该反映出只有经验丰富的开发者或有上下文的人才知道的见解。例如，如果你正在构建一个电子商务智能体，并且你知道「产品」和「类别」是多对多关系，就要明确说明（不要假设 AI 会推断出来——它可能不会）。如果某个库是出了名的棘手，请提及要避免的陷阱。本质上，将你的指导倾注到规约中。规约可以包含诸如「如果使用库 X，请注意版本 Y 中的内存泄漏问题（应用变通方法 Z）」之类的建议。这种程度的细节是将一个普通的 AI 输出转变为真正健壮的解决方案的关键，因为你已经引导 AI 避开了常见的陷阱。

此外，如果你有偏好或风格指南（比如说，「在 React 中使用函数组件而不是类组件」），请在规约中明确规定。AI 随后会模仿你的风格。许多工程师甚至在规约中包含一些小例子，例如，「所有 API 响应都应为 JSON。例如，错误时为 `{"error": "message"}`。」通过给出一个快速的例子，你将 AI 锚定在你想要的确切格式上。

**简单任务的极简主义：** 虽然我们提倡详尽的规约，但专业知识的一部分是知道何时应保持简单。对于相对简单、孤立的任务，一个过于冗长的规约实际上可能会比帮助更添乱。如果你要求智能体做一些直接的事情（比如「在页面上居中一个 div」），你可能只需要说，「确保解决方案简洁，不要添加无关的标记或样式。」那里就不需要一个完整的 PRD。相反，对于复杂的任务（比如「实现一个带有 Token 刷新和错误处理的 OAuth 流程」），那你就需要拿出详细的规约了。一个好的经验法则是：根据任务的复杂性调整规约的详细程度。不要对一个难题规约不足（智能体会手足无措或偏离轨道），但也不要对一个琐碎的问题过度规约（智能体可能会被纠缠或在不必要的指令上耗尽上下文）。

**如果需要，保持 AI 的「人设」：** 有时，你的规约的一部分是定义智能体应该如何行为或响应，特别是如果智能体与用户互动。例如，如果构建一个客户支持智能体，你的规约可能包括诸如「使用友好和专业的语气」，「如果你不知道答案，请求澄清或表示会跟进，而不是猜测」之类的准则。这类规则（通常包含在系统提示词中）有助于保持 AI 的输出与期望一致。它们本质上是 AI 行为的规约项。保持它们的一致性，并在长时间的会话中如果需要的话提醒模型（如果不加约束，LLM 的风格会随着时间的推移而「漂移」）。

**你仍然是循环中的决策者：** 规约赋予了智能体权力，但你仍然是最终的质量过滤器。如果智能体产生的东西技术上符合规约但感觉不对，请相信你的判断。要么完善规约，要么直接调整输出。AI 智能体的好处是它们不会被冒犯——如果它们交付的设计不合意，你可以说，「实际上，这不是我想要的，我们来澄清一下规约，然后重做。」规约是与 AI 合作中的一个活产物，而不是你不能改变的一次性合同。

Simon Willison 幽默地将与 AI 智能体合作比作「一种非常奇怪的管理形式」，甚至「从编程智能体那里获得好结果感觉[与管理一名人类实习生非常相似](https://link.zhihu.com/?target=https%3A//simonwillison.net/2025/Oct/7/vibe-engineering/)」。你需要提供清晰的指令（规约），确保它们有必要的上下文（规约和相关数据），并给出可操作的反馈。规约设定了舞台，但在执行过程中的监控和反馈是关键。如果一个 AI 是一个「奇怪的数字实习生，如果你给他们机会，他们绝对会作弊」，那么你编写的规约和约束就是你防止作弊并让他们专注于任务的方式。

回报是：一份好的规约不仅告诉 AI 要构建什么，还帮助它自我纠正并保持在安全边界内。通过内置验证步骤、约束和你的宝贵知识，你大大增加了智能体第一次输出就正确的几率（或者至少更接近正确）。这减少了迭代次数和那些「它到底为什么会那么做？」的时刻。

## **5. 测试、迭代和演进规约（并使用正确的工具）**

**将规约编写和智能体构建看作一个迭代循环：尽早测试，收集反馈，完善规约，并利用工具来自动化检查。**

最初的规约不是终点——它是一个循环的开始。最好的结果来自于你持续根据规约验证智能体的工作并相应地进行调整。此外，现代 AI 开发者使用各种工具来支持这个过程（从 CI 管道到上下文管理实用程序）。

![img](https://picx.zhimg.com/v2-9de03dc08e8db94d70fd4a209698f807_1440w.jpg)

**持续测试：** 不要等到最后才看智能体是否满足了规约。在每个主要里程碑之后，甚至每个函数之后，运行测试或至少进行快速的手动检查。如果出现问题，在继续之前更新规约或提示词。例如，如果规约说「密码必须用 bcrypt 哈希」，而你看到智能体的代码存储了明文——停下来纠正它（并提醒规约或提示词关于这个规则）。自动化测试在这里大放异彩：如果你提供了测试（或者边做边写），让智能体运行它们。在许多编程智能体设置中，你可以让智能体在完成任务后运行 `npm test` 或类似的命令。结果（失败）可以反馈到下一个提示词中，有效地告诉智能体「你的输出在 X、Y、Z 方面不符合规约——修复它。」这种智能体循环（编码 -> 测试 -> 修复 -> 重复）非常强大，也是像 Claude Code 或 Copilot Labs 这样的工具如何演进以处理更大任务的方式。始终定义「完成」意味着什么（通过测试或标准），并检查它。

**迭代规约本身：** 如果你发现规约不完整或不清晰（也许智能体误解了什么，或者你意识到你遗漏了一个要求），更新规约文档。然后明确地将智能体与新的规约重新同步：「我已经更新了规约如下……鉴于更新后的规约，相应地调整计划或重构代码。」这样，规约就仍然是单一的事实来源。这类似于我们在正常开发中处理需求变更的方式——但在这种情况下，你也是你的 AI 智能体的产品经理。如果可能的话，保留版本历史（即使只是通过提交信息或笔记），这样你就知道什么变了以及为什么变。

**利用上下文管理和记忆工具：** 有一个不断增长的工具生态系统来帮助管理 AI 智能体的上下文和知识。例如，检索增强生成 (Retrieval-Augmented Generation, RAG) 是一种模式，智能体可以动态地从知识库（如向量数据库）中提取相关数据块。如果你的规约非常庞大，你可以嵌入它的部分内容，让智能体在需要时检索最相关的部分，而不是总是提供全部内容。还有一些框架实现了模型上下文协议 (Model Context Protocol, MCP)，它可以根据当前任务自动为模型提供正确的上下文。一个例子是 [Context7](https://link.zhihu.com/?target=https%3A//docs.digitalocean.com/products/gradient-ai-platform/concepts/context-management/) (context7.com)，它可以根据你正在处理的内容自动从文档中获取相关的上下文片段。在实践中，这可能意味着智能体注意到你正在处理「支付处理」，然后它会将你的规约或文档的「支付」部分拉入提示词中。考虑利用这类工具或建立一个初步的版本（即使只是在你的规约文档中进行简单的搜索）。

**谨慎地并行化：** 一些开发者在不同任务上并行运行多个智能体实例（如前文提到的子智能体）。这可以加快开发速度——例如，一个智能体生成代码，而另一个同时编写测试，或者两个功能被同时构建。如果你走这条路，确保任务是真正独立的或清晰分开的，以避免冲突（规约应注明任何依赖关系）。例如，不要让两个智能体同时写入同一个文件。一个工作流是让一个智能体生成代码，另一个并行审查它，或者构建独立的组件，稍后集成。这是高级用法，管理起来可能会精神上很累（正如 Willison 承认的，运行多个智能体是「[出奇地有效，尽管在精神上很累人](https://link.zhihu.com/?target=https%3A//simonwillison.net/2025/Oct/7/vibe-engineering/)！」）。开始时最多使用 2-3 个智能体，以保持事情的可管理性。

**版本控制和规约锁定：** 使用 Git 或你选择的版本控制来跟踪智能体的行为。有了 AI 的辅助，[良好的版本控制习惯](https://link.zhihu.com/?target=https%3A//simonwillison.net/2025/Oct/7/vibe-engineering/)变得更加重要。将规约文件本身提交到仓库中。这不仅保留了历史，智能体甚至可以使用 `git diff` 或 `blame` 来理解变更（LLM 非常擅长阅读 diffs）。一些高级的智能体设置让智能体查询 VCS 历史以查看某项内容是何时引入的——令人惊讶的是，模型在 Git 方面可以「非常能干」。通过将你的规约保存在仓库中，你允许你和 AI 都能跟踪演变。有些工具（如前面提到的 GitHub Spec Kit）将规约驱动开发集成到 git 工作流中——例如，基于更新的规约来门控合并，或从规约项生成检查清单。虽然你不需要那些工具也能成功，但要点是像对待代码一样对待规约——勤奋地维护它。

**成本和速度的考虑：** 使用大型模型和长上下文可能会又慢又贵。一个实用的技巧是巧妙地进行模型选择和批处理。也许可以使用更便宜/更快的模型进行初步草稿或重复性工作，并将最强大（也最昂贵）的模型留给最终输出或复杂推理。一些开发者使用 GPT-4 或 Claude 进行规划和关键步骤，但将更简单的扩展或重构工作交给本地模型或更小的 API 模型。如果使用多个智能体，也许不是所有都需要是顶级的；一个运行测试的智能体或一个代码检查智能体可以是较小的模型。还要考虑节流上下文大小：如果 5k Token 就够了，就不要喂 20k。正如我们讨论的，[更多的 Token 可能意味着收益递减](https://link.zhihu.com/?target=https%3A//www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)。

**全面监控和记录日志：** 在复杂的智能体工作流中，记录智能体的行为和输出至关重要。检查日志，看智能体是否偏离轨道或遇到错误。许多框架提供跟踪日志或允许打印智能体的思维链 （特别是如果你提示它逐步思考）。审查这些日志可以突出规约或指令可能被误解的地方。这与调试程序并无不同——只是这里的「程序」是对话/提示链。如果发生奇怪的事情，回到规约/指令，看看是否存在模糊之处。

**学习和改进：** 最后，将每个项目都视为一个学习机会，以完善你的规约编写技巧。也许你会发现某种措辞总是让 AI 感到困惑，或者以某种方式组织规约章节会带来更好的遵守度。将这些教训融入到下一个规约中。AI 智能体领域正在迅速发展，所以新的最佳实践（和工具）不断涌现。通过博客（如 Simon Willison、Andrej Karpathy 等人的博客）保持更新，并且不要犹豫去试验。

为 AI 智能体编写的规约不是「写一次就完事了」。它是一个持续的指导、验证和完善循环的一部分。这种勤奋的回报是巨大的：通过及早发现问题并使智能体保持一致，你可以避免以后代价高昂的重写或失败。正如一位 AI 工程师打趣说，使用这些实践感觉就像有「一支实习生大军」为你工作，但你必须管理好他们。一份好的、持续维护的规约，就是你的管理工具。

## **避免常见陷阱**

在结束之前，有必要指出一些可能会破坏即使是善意的规约驱动工作流的反模式。[GitHub 对 2,500 多个智能体文件的研究](https://link.zhihu.com/?target=https%3A//github.blog/ai-and-ml/github-copilot/how-to-write-a-great-agents-md-lessons-from-over-2500-repositories/)揭示了一个鲜明的对比：「大多数智能体文件失败是因为它们太模糊了。」以下是要避免的错误：

**模糊的提示词：**「给我构建一些酷的东西」或「让它工作得更好」没有给智能体任何可以锚定的东西。正如 Baptiste Studer 所说：「模糊的提示词意味着错误的结果。」要具体说明输入、输出和约束。「你是一个有用的编程助手」是行不通的。「你是一名测试工程师，为 React 组件编写测试，遵循这些示例，并且从不修改源代码」则可以。

**没有摘要的过长上下文：** 将 50 页的文档倾倒到一个提示词中，并希望模型能自己搞清楚，这很少奏效。使用层次化摘要（如原则 3 中讨论的）或 RAG 来只呈现相关内容。上下文长度不能替代上下文质量。

**跳过人工审查：** Willison 有一个个人原则：「我不会提交我无法向别人解释的代码。」仅仅因为智能体产生的东西通过了测试，并不意味着它是正确的、安全的或可维护的。务必审查关键的代码路径。「纸牌屋」的比喻同样适用：AI 生成的代码可能看起来很坚固，但在你没有测试到的边缘情况下会崩溃。

**混淆氛围编程与生产工程：** 使用 AI 进行快速原型设计（vibe coding) 对于探索和一次性项目来说非常棒。但是，将这些代码未经严格的规约、测试和审查就发布到生产环境，是在自找麻烦。我区分「氛围编程」和「AI 辅助工程」——后者需要本指南所描述的纪律。要清楚自己处于哪种模式。

**忽视「致命三要素」：** Willison 警告说，有三个特性使 AI 智能体变得危险：速度（它们工作得比你审查得快）、非确定性（相同的输入，不同的输出）和成本（鼓励在验证上偷工减料）。你的规约和审查过程必须考虑到这三点。不要让速度超过你的验证能力。

**遗漏六个核心领域：** 如果你的规约没有涵盖命令、测试、项目结构、代码风格、git 工作流和边界，你很可能遗漏了智能体需要的东西。在交给智能体之前，使用第 2 节的六领域检查清单作为健全性检查。

## **结论**

为 AI 编程智能体编写一份有效的规约，需要将坚实的软件工程原则与对 LLM 怪癖的适应相结合。从明确的目标开始，让 AI 帮助扩展计划。像一份严肃的设计文档一样构建规约——涵盖六个核心领域，并将其集成到你的工具链中，使其成为可执行的产物，而不仅仅是文字。通过一次只给智能体一块拼图来保持其专注（并考虑使用像摘要目录、子智能体或并行协调等巧妙策略来处理大型规约）。通过包含三层边界（总是/先询问/绝不）、自检和一致性测试来预见陷阱——本质上，是教 AI 如何不失败。并将整个过程视为迭代的：使用测试和反馈来持续完善规约和代码。

遵循这些准则，你的 AI 智能体在处理大型上下文时「崩溃」或偏离到无意义方向的可能性将大大降低。

祝你编写规约顺利！