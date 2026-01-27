# 测试Synnovator Skill创建提案（post）

## 1   测试用例

### 1.1   A1. 基础可用性

**TC-POST-001：最小字段创建（general, draft）**

- 前置：已登录用户（participant）
    
- 输入：仅包含 `title` + 正文 Markdown（不写 type/tags/status）
    
- 期望：创建成功；type 视为 general；status= draft（默认）
    
    
    
- 额外检查：READ post 能查到该帖
    

**TC-POST-002：显式发布（general, published）**

- 前置：已登录用户
    
- 输入：`title` + `status: published` + 正文
    
- 期望：创建成功；READ post（公开视角）可读到已发布贴（“已发布: 任何人；草稿: 作者/Admin”）
    
    
    

**TC-POST-003：带 tags 创建（tag 作为检索/运营入口）**

- 输入：`tags: ["提案","找队友"]` 或你们真实运营 tag
    
- 期望：READ post 支持按 tag 筛选命中（文档明确“支持按 tag/type 筛选”）
    
    
    

---

### 1.2   A2. type 语义覆盖

**TC-POST-010：type=team（团队卡片内容）**

- 输入：`type: team` + 正文包含成员列表
    
- 期望：创建成功；后续可被嵌入到其它帖子（post:post embed）
    
    
    

**TC-POST-011：type=profile（个人资料卡片）**

- 输入：`type: profile`
    
- 期望：创建成功；后续能作为用户主页/卡片渲染的数据源（这里先不测渲染，只测数据可用）
    

**TC-POST-012：type=for_category（参赛提交/提案）**

- 输入：`type: for_category` + 正文包含“项目简介/技术方案/演示链接”
    
- 期望：创建成功；并能被关联到某个活动（category:post relation_type=submission）
    
    
    
- 注：这条与任务 3 强相关，但在任务 1 里至少要确认“这种 post 能创建出来且字段合理”
    
    
    

**TC-POST-013：type=certificate（证书分享帖）**

- 输入：`type: certificate` + 正文包含证书说明
    
- 期望：创建成功；后续能挂 resource（证书文件）作为附件/内联（会在任务 2/组合测试里验证）
    

---

### 1.3   A3. 关系驱动的可用性


**TC-POST-020：提案帖嵌入团队卡片（post:post embed）**

- 步骤：先创建 team post，再创建提案 post，然后 CREATE post:post（embed, position=1）
    
    
    
- 期望：READ post:post 能查询到 embed 关系；position 正确
    

**TC-POST-021：提案帖引用另一帖（post:post reference）**

- 例如“找队友贴”引用“提案贴”
    
    
    
- 期望：引用关系可查询；用于后续“证据链/关联阅读”
    



### 1.4   A4. 负向/边界


**TC-POST-900：缺少 title**

- 输入：无 title
    
- 期望：创建失败；错误明确指出必填字段缺失（title）
    
    
    

**TC-POST-901：非法 type / status**

- 输入：`type: foo` 或 `status: archived`
    
- 期望：创建失败；错误明确指出枚举可选范围（type/status）
    
    
    

**TC-POST-902：未登录用户创建 post**

- 依据权限表：CREATE post = 已登录用户
    
    
    
- 期望：拒绝；错误说明需要认证

## 2   Mock data

### 2.1   B1. 用户（user）

- `user_alice`：participant（提案作者）
    
- `user_bob`：participant（队友/被邀请者）
    
- `user_org_01`：organizer（用于后续活动/规则）
    

（user schema 见文档：username/email 必填；role 默认 participant）



### 2.2   B2. 活动与规则（category + rule）

> 虽然任务 1 不要求一定关联活动，但为了你后面任务 3，建议一次性准备好。

- `cat_ai_hackathon_2025`：type=competition, status=published（活动）
    
    
    
- `rule_submission_01`：allow_public=true, require_review=true（规则）
    
    
    
- 关系：`cat_ai_hackathon_2025` : `rule_submission_01`（priority=1）
    
    
    

### 2.3   B3. 团队（group）

- `grp_team_synnovator`：public, require_approval=true
    
    
    
- 关系：group:user
    
    - Alice = owner
        
    - Bob = member 
        
        
        

### 2.4   B4. 帖子（post）样本（可直接拷贝使用）

#### 1) 找队友贴（general）

`--- title: "【找队友】AI Hackathon 2025 一起组队做开发者工具" type: general tags: ["找队友", "提案"] status: published ---  我们计划做一个“AI 代码审查助手”，欢迎前端/后端/LLM 应用同学加入。 你可以直接评论或私信。`

#### 2) 团队卡片（team）

`--- title: "Team Synnovator" type: team tags: ["全栈", "AI"] status: published ---  ## 团队介绍 我们是一支专注于 AI 应用开发的全栈团队。  ## 成员 - Alice — 后端 / 分布式 - Bob — 前端 / React - Carol — AI / LLM 应用`

#### 3) 提案/参赛提交（for_category）

> 参考你文档里的示例结构（type=for_category, status=published）
> 
> 

`--- title: "AI 代码审查助手 — CodeReview Copilot" type: for_category tags: ["AI", "开发者工具", "代码审查"] status: published ---  ## 项目简介 CodeReview Copilot 是一款基于大语言模型的智能代码审查工具，能自动识别问题并给出改进建议。  ## 技术方案 - AST 解析 + LLM 理解的双层分析 - 支持 Python / JavaScript / Go  ## 演示 [Demo 视频](https://example.com/demo.mp4)`

#### 5) 关系样本（用于 TC-POST-020/021）

- embed 团队卡片到提案贴：
    
    
    

`source_post_id: "post_codereview_copilot" target_post_id: "post_team_synnovator" relation_type: embed position: 1`

- reference 找队友贴引用提案贴：
    
    
    

`source_post_id: "post_looking_for_teammates" target_post_id: "post_codereview_copilot" relation_type: reference position: 0`

# 测试Synnovator Skill创建资源（resource）

## 1   测试用例

### 1.1   A1. 基础可用性

**TC-RES-001：最小字段上传（只带 filename）**

- 前置：已登录用户（任意角色）
    
- 操作：CREATE resource，仅提供 `filename` 
    
    
    
- 期望：创建成功；自动生成字段存在（id/mime_type/size/url/uploaded_by/created_at）
    
    
    
- 额外检查：READ resource 可获取下载/读取信息（在资源可见的前提下）
    
    
    

**TC-RES-002：带 display_name + description 上传**

- 操作：CREATE resource，提供 filename + display_name + description 
    
    
    
- 期望：创建成功；display_name 覆盖默认展示名（不填则使用 filename）
    
    
    

---

### 1.2   A2. 与帖子关联的可用性

**TC-RES-010：资源作为“附件 attachment”挂到帖子**

- 前置：已存在一个 post（建议用你任务 1 的提案帖或找队友贴）
    
- 步骤：
    
    1. CREATE resource
        
    2. CREATE post:resource，display_type=attachment，position=0 
        
        
        
- 期望：
    
    - READ post:resource 能查到该资源
        
    - display_type=attachment，position 正确 
        
        
        
    - READ resource 在“帖子可见”情况下可读（文档描述：关联帖子可见则可读）
        
        
        

**TC-RES-011：资源作为“内联 inline”挂到帖子**

- 步骤同上，只是 display_type=inline，position=0/1
    
- 期望：READ post:resource 返回 display_type=inline；position 可用于排序 
    
    
    
- 价值：确认“同一个资源”在不同展示方式下都能稳定工作（skill 的关系属性可用）
    

**TC-RES-012：同一帖子挂多个资源，position 排序生效**

- 步骤：对同一 post 连续 CREATE 两个 post:resource 关系：position=0/1
    
- 期望：READ post:resource 返回结果可排序且 position 信息完整 
    
    
    

---

### 1.3   A3. 权限与可见性

**TC-RES-020：资源可读性继承帖子可见性**

- 前置：准备两种帖子：
    
    - post A：published（任何人可读）
        
    - post B：draft（只有作者/Admin 可读）
        
        
        
- 步骤：
    
    - 将同一个 resource 关联到 post A（或分别关联两个资源到 A/B）
        
    - 以“未登录/普通访客”执行 READ resource
        
- 期望：
    
    - 关联到 published post 的资源可读
        
    - 关联到 draft post 的资源不可读或被拒绝（因为“关联帖子可见则可读”）
        
        
        

---

### 1.4   A4. 更新与删除

**TC-RES-030：UPDATE resource 元信息**

- 操作：UPDATE resource 修改 display_name/description
    
- 期望：更新成功；READ resource 返回新元信息 
    
    
    
- 权限：上传者/Admin（文档写明）
    
    
    

**TC-RES-031：DELETE resource 级联解除 post:resource**

- 操作：
    
    1. 创建 resource 并关联到 post
        
    2. DELETE resource
        
- 期望：资源被删除；post:resource 关系解除（文档写了级联影响：解除所有 post:resource 关系）
    
    
    

---

### 1.5   A5. 负向/边界

**TC-RES-900：缺少 filename**

- 操作：CREATE resource 不提供 filename
    
- 期望：失败；错误明确指出必填字段 filename 缺失 
    
    
    

**TC-RES-901：未登录用户 CREATE resource**

- 依据权限：CREATE resource = 已登录用户 
    
    
    
- 期望：拒绝；错误提示需要认证
    

**TC-RES-902：创建 post:resource 时引用不存在的 post_id/resource_id**

- 操作：CREATE post:resource 使用不存在 id
    
- 期望：失败；错误能明确是哪个 id 不存在（这是可用性关键：LLM/Agent 才能自修复）

## 2   Mock data

### 2.1   B1. 资源样本（resource）

**RES-MOCK-001：演示视频（mp4）**

`filename: "project-demo.mp4" display_name: "项目演示视频" description: "3 分钟 demo，用于提案展示"`

**RES-MOCK-002：提交包（zip）**

`filename: "source-code.zip" display_name: "源代码提交包" description: "包含核心代码与README"`

**RES-MOCK-003：项目说明书（pdf）**

`filename: "project-report.pdf" display_name: "项目说明书" description: "PDF 版技术报告"`

**RES-MOCK-004：封面图（png）**

`filename: "cover.png" display_name: "封面图" description: "活动/提案用封面"`

> 这些样本覆盖你们 rule 里常见 submission_format（markdown/pdf/zip 等），便于后续组合测试（即便你现在还没强校验 submission_format）
> 
> 
> 
> 。

---

### 2.2   B2. 关联目标帖子（post_id）占位

你任务 2 里需要一个“可关联的 post”。直接沿用任务 1 的 mock：

- `post_codereview_copilot`（提案/参赛提交帖）
    
- `post_looking_for_teammates`（找队友贴）
    

（post 的创建与类型在任务 1 已覆盖；这里不重复写正文。）

---

### 2.3   B3. 关系样本（post:resource）

**REL-MOCK-001：附件 attachment（position=0）** 



`post_id: "post_codereview_copilot" resource_id: "res_project_demo_mp4" display_type: attachment position: 0`

**REL-MOCK-002：内联 inline（position=0）** 



`post_id: "post_codereview_copilot" resource_id: "res_project_demo_mp4" display_type: inline position: 0`

**REL-MOCK-003：同帖多资源排序（position=0/1）** 



`# 0: 视频内联 post_id: "post_codereview_copilot" resource_id: "res_project_demo_mp4" display_type: inline position: 0`

`# 1: zip 作为附件 post_id: "post_codereview_copilot" resource_id: "res_source_code_zip" display_type: attachment position: 1`

# 测试是否正确列出提交给某个活动的提案

## 1   测试用例

### 1.1   A1. 基础可用性

**TC-LIST-001：活动下只列出 submission（单条）**

- 前置：
    
    - 有一个已发布活动 category（公开可读）
        
        
        
    - 该活动下存在 1 条 `category:post` 关系，`relation_type=submission` 指向某个提案帖 
        
        
        
- 操作：`READ category:post`，filter `relation_type=submission` 
    
    
    
- 期望：返回列表仅包含该提案帖（post_id 命中），不包含任何 reference 类型帖子
    
    
    

**TC-LIST-002：活动下 submission 多条，全部被列出**

- 前置：同一活动下挂 3 条 submission
    
- 操作：同上
    
- 期望：返回 3 条且数量准确；每条都能 READ post 详情（已发布任何人可读）
    
    
    

---

### 1.2   A2. 过滤正确性

**TC-LIST-010：混合关联（submission + reference），过滤只出 submission**

- 前置：
    
    - 同一 category 下同时存在：
        
        - `relation_type=submission` 的提案帖
            
        - `relation_type=reference` 的展示/引用帖 
            
            
            
- 操作：`READ category:post (relation_type=submission)`
    
    
    
- 期望：结果集中 **完全不出现** reference 帖
    

**TC-LIST-011：不带 filter 读取 category:post，返回包含 submission+reference（对比用）**

- 操作：`READ category:post` 不传 relation_type filter（如果你们实现允许）
    
    
    
- 期望：结果包含两类；并可用于证明“过滤逻辑确实生效”
    

---

### 1.3   A3. 权限与可见性

> READ 权限中写了：公开活动任何人可读；草稿活动仅创建者/Admin。
> 
> 
> 
>   
> 帖子已发布任何人可读；草稿仅作者/Admin。
> 
> 

**TC-LIST-020：活动 published + submission post draft：列表是否“安全”**

- 前置：
    
    - category 是 published（访客可读）
        
        
        
    - 有一条 submission 指向 **draft** 的 post（作者自己能读，访客不能）
        
        
        
- 操作：以“未登录访客”执行 `READ category:post (submission)`
    
- 期望（你们需要二选一，并通过测试暴露选择）：
    
    - **方案 A（推荐）**：该 submission 不出现在列表（避免泄露草稿存在）
        
    - **方案 B**：返回但对该 post 做脱敏/不可展开（会显著增加产品/agent复杂度）
        

> 这个用例的价值在于：它会逼你们明确“列表层”到底遵循 category 权限还是 post 权限优先。

---

### 1.4   A4. 一致性与健壮性

**TC-LIST-030：关联指向不存在的 post_id（脏数据）**

- 前置：造一条 `category:post` 关系，post_id 不存在
    
- 操作：`READ category:post (submission)`
    
- 期望：
    
    - 不崩；返回结果中跳过该条或明确标记 broken reference
        
    - 错误/告警信息能让调用方（agent）知道哪条关系坏了  
        （关系字段定义见 category:post 的必填键）
        
        
        

**TC-LIST-031：同一 post 被重复 submission 关联（重复提交/误操作）**

- 前置：同一个 post_id 被同一 category 关联两次 relation_type=submission
    
- 操作：读取 submission 列表
    
- 期望：你们需要决定：
    
    - 去重（更像产品行为）
        
    - 还是保留两条（更像数据库行为）
        

> 这条测试的目标是帮助你决定：skill 是否要承担“产品语义去重”。
## 2   Mock data

### 2.1   B1. Category（活动）

用于被查询的活动：

`# category: cat_ai_hackathon_2025 name: "2025 AI Hackathon" description: "面向全球开发者的 AI 创新大赛" type: competition status: published`

category 的 schema/状态字段见定义。



---

### 2.2   B2. Posts（提案/非提案混合）

准备 4 个帖子：2 个 submission，1 个 reference，1 个 draft submission（用来测权限）。

**POST-SUB-001（published 提案）**

`--- title: "CodeReview Copilot" type: for_category tags: ["AI","开发者工具"] status: published --- ## 项目简介 ...`

post 的 type/status 定义见 schema。



**POST-SUB-002（published 提案）**

`--- title: "Data Labeling Agent" type: for_category tags: ["AI","数据"] status: published --- ## 项目简介 ...`

**POST-REF-001（reference 展示/引用帖）**

`--- title: "优秀作品展示合集" type: general tags: ["展示"] status: published --- 这里引用了多个作品链接。`

**POST-SUB-003（draft 提案，用于权限测试）**

`--- title: "Stealth Project Draft" type: for_category tags: ["AI"] status: draft --- 未发布草稿作品。`

已发布/草稿可读权限差异见 READ post。



---

### 2.3   B3. Relations：category:post（关键）

category:post 关系字段与 relation_type 枚举在示例里写得很明确。



把这些关系建起来：

**REL-CATPOST-001（submission）**

`category_id: "cat_ai_hackathon_2025" post_id: "post_codereview_copilot"      # 映射到 POST-SUB-001 relation_type: submission`

**REL-CATPOST-002（submission）**

`category_id: "cat_ai_hackathon_2025" post_id: "post_data_labeling_agent"     # 映射到 POST-SUB-002 relation_type: submission`

**REL-CATPOST-003（reference）**

`category_id: "cat_ai_hackathon_2025" post_id: "post_showcase_collection"     # 映射到 POST-REF-001 relation_type: reference`

**REL-CATPOST-004（submission + draft post，用于 TC-LIST-020）**

`category_id: "cat_ai_hackathon_2025" post_id: "post_stealth_draft"           # 映射到 POST-SUB-003 relation_type: submission`