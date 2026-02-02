# Ralph-Loop: Frontend Page Development (Phase 3-7)

> **Goal**: Complete frontend page development phases 3-7, ensuring all User Journeys pass E2E tests
> **Plan File**: task_plan.md
> **API Reference**: docs/frontend-api-mapping.md
> **E2E Report**: plans/e2e_test.md

---

## Prompt

You are a frontend developer working on Synnovator (协创者) Hackathon platform. Your task is to complete the remaining phases of frontend page development.

### Before Starting

1. Read `/planning-with-files` skill for progress tracking methodology
2. Read `task_plan.md` to understand current progress (Phase 1-2 complete)
3. Read `specs/ui/ui-design-spec.md` for UI design specifications
4. Read `docs/frontend-api-mapping.md` for API endpoint mapping
5. Read `docs/user-journeys.md` for User Journey test cases

### Phase 3: Create Page Route Structure

Create Next.js App Router pages according to task_plan.md section 3.2:

```
frontend/app/
├── page.tsx                    # / (update existing)
├── login/page.tsx              # /login
├── register/page.tsx           # /register
├── explore/page.tsx            # /explore
├── events/
│   ├── page.tsx                # /events
│   ├── [id]/page.tsx           # /events/[id]
│   └── create/page.tsx         # /events/create
├── posts/
│   ├── page.tsx                # /posts
│   ├── [id]/
│   │   ├── page.tsx            # /posts/[id]
│   │   └── edit/page.tsx       # /posts/[id]/edit
│   └── create/page.tsx         # /posts/create
├── groups/
│   ├── page.tsx                # /groups
│   ├── [id]/page.tsx           # /groups/[id]
│   └── create/page.tsx         # /groups/create
├── users/
│   └── [id]/page.tsx           # /users/[id]
└── settings/page.tsx           # /settings
```

**Priority Order**: P0 (core) → P1 (important) → P2 (extended)

**Acceptance Criteria**:
- [ ] All 16 route files created
- [ ] Each page exports default component
- [ ] Pages render without errors

### Phase 4: Implement Layout Components

Create layout components per ui-design-spec.md section 1.2:

| Component | File | Description |
|-----------|------|-------------|
| Header | `components/layout/Header.tsx` | 60px fixed top navigation |
| Sidebar | `components/layout/Sidebar.tsx` | 168px/60px collapsible sidebar |
| Panel | `components/layout/Panel.tsx` | 328px right panel |
| PageLayout | `components/layout/PageLayout.tsx` | 4 layout variants container |

**Layout Variants**:
```tsx
type LayoutVariant = 'full' | 'compact' | 'focus' | 'landing'

// Full: Sidebar expanded (168px) + Panel (328px)
// Compact: Sidebar collapsed (60px) + Panel
// Focus: No Sidebar + No Panel
// Landing: No Sidebar + No Panel (centered content)
```

**Acceptance Criteria**:
- [ ] All 4 layout components created
- [ ] PageLayout supports 4 variants
- [ ] Responsive at breakpoints (1440px, 1280px, 768px)

### Phase 5: Implement Card Components

Create card components per ui-design-spec.md section 8.2:

| Component | File | UI Design |
|-----------|------|-----------|
| CategoryCard | `components/cards/CategoryCard.tsx` | 8.2.1 活动卡片 |
| PostCard | `components/cards/PostCard.tsx` | 8.2.2 帖子卡片 |
| GroupCard | `components/cards/GroupCard.tsx` | 8.2.3 团队卡片 |
| UserCard | `components/cards/UserCard.tsx` | 8.2.4 用户卡片 |

**Acceptance Criteria**:
- [ ] All 4 card components created
- [ ] Cards match UI design wireframes
- [ ] Cards handle loading/error states
- [ ] Cards use shadcn/ui primitives (Card, Avatar, Badge)

### Phase 6: Implement Page Body Content

Implement page content by priority:

**P0 - Core Pages**:
1. `/` - Landing page with hero, stats, featured events
2. `/login` - Login form using existing LoginForm component
3. `/register` - Register form using existing RegisterForm component
4. `/explore` - Grid of events/posts with filters
5. `/events` - Event list with search/filter
6. `/events/[id]` - Event detail with tabs (overview, posts, teams, ranking)

**P1 - Important Pages**:
7. `/posts` - Post list with category filter
8. `/posts/[id]` - Post detail with comments
9. `/posts/create` - Create post form (Focus layout)
10. `/posts/[id]/edit` - Edit post form (Focus layout)
11. `/groups` - Group list
12. `/groups/[id]` - Group detail with members
13. `/users/[id]` - User profile with posts/follows

**P2 - Extended Pages**:
14. `/events/create` - Create event form (Focus layout)
15. `/groups/create` - Create group form (Focus layout)
16. `/settings` - User settings

**Acceptance Criteria**:
- [ ] All 16 pages have functional content
- [ ] Pages fetch data from API (docs/frontend-api-mapping.md)
- [ ] Loading/error states handled
- [ ] Navigation between pages works

### Phase 7: E2E Testing & Verification

Use `/agent-browser` skill to verify all User Journeys:

**Test Setup**:
```bash
# Start backend
make backend

# Start frontend
make frontend

# Wait for services
agent-browser wait --load networkidle
```

**User Journey Test Cases** (from docs/user-journeys.md):

| Journey | Test Case | Steps |
|---------|-----------|-------|
| J2 | Browse explore | Open /, click explore, verify events/posts visible |
| J3 | Register | Open /register, fill form, submit, verify redirect |
| J4 | Login | Open /login, fill form, submit, verify authenticated |
| J5 | Join group | Open /groups/[id], click join, verify membership |
| J6 | Create event | Open /events/create, fill form, submit, verify created |
| J7 | Join event | Open /events/[id], click join, verify registered |
| J8 | Create team | Open /groups/create, fill form, submit, verify created |
| J9 | Create post | Open /posts/create, fill form, submit, verify created |
| J10 | View ranking | Open /events/[id], click ranking tab, verify scores |
| J11 | Edit post | Open /posts/[id]/edit, modify, save, verify updated |
| J12 | Delete post | Open /posts/[id], click delete, confirm, verify deleted |
| J13 | Comment/like | Open /posts/[id], add comment, click like, verify counts |
| J14 | Follow user | Open /users/[id], click follow, verify following |
| J15 | Multi-stage event | Open /events/[id], navigate stages, verify UI |
| J16 | Asset transfer | Open /posts/[id]/edit, manage attachments, verify |

**E2E Test Script**:
```bash
# For each journey:
agent-browser open http://localhost:3000/<route>
agent-browser snapshot -i
agent-browser <actions based on journey>
agent-browser screenshot plans/screenshots/e2e-<journey>.png
# Verify expected state
```

**Acceptance Criteria**:
- [ ] All 16 User Journeys tested
- [ ] All tests pass
- [ ] Screenshots saved to plans/screenshots/
- [ ] Results documented in plans/e2e_test.md

---

## Workflow

1. **Before each phase**:
   - Read task_plan.md current state
   - Update phase status to `🔄 进行中`

2. **During each phase**:
   - Follow acceptance criteria
   - Commit after each significant milestone
   - Log errors in task_plan.md 错误记录 section

3. **After each phase**:
   - Update task_plan.md status to `✅ 完成`
   - Update findings.md with discoveries
   - Verify phase acceptance criteria met

4. **On error**:
   - Log error to task_plan.md
   - Try alternative approach (3-strike rule)
   - If blocked after 3 attempts, document and continue

---

## Completion Criteria

All phases complete when:
1. ✅ Phase 3: All 16 routes created
2. ✅ Phase 4: All 4 layout components working
3. ✅ Phase 5: All 4 card components working
4. ✅ Phase 6: All 16 pages have content
5. ✅ Phase 7: All 16 User Journeys pass E2E

When ALL criteria met, output:

```
<promise>COMPLETE</promise>
```

---

## Skills Reference

- `/planning-with-files` - Progress tracking with task_plan.md, findings.md
- `/agent-browser` - Browser automation for E2E testing
- `@playwright` - Alternative E2E testing framework

## Files Reference

| File | Purpose |
|------|---------|
| task_plan.md | Phase tracking and progress |
| findings.md | Research and discoveries |
| specs/ui/ui-design-spec.md | UI design specifications |
| docs/frontend-api-mapping.md | API endpoint mapping |
| docs/user-journeys.md | User Journey test cases |
| plans/e2e_test.md | E2E test results |
