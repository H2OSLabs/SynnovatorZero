# Test Case Format Conventions

## File Naming

Files are numbered sequentially: `NN-module-name.md` (e.g., `01-user.md`, `08-relations.md`).

Next available number: check `ls specs/testcases/` for the highest existing number.

## File Structure

```markdown
# Module Name (Chinese)

> **格式约定：** 每条用例仅描述「场景」与「预期结果」，不包含测试方法和执行过程。

---

## N.1 Section Name

**TC-PREFIX-NNN：Test Case Title (Chinese)**
Description paragraph: scenario setup + expected result. Single paragraph, no bullet points
unless describing multiple cascading effects.

## N.M 负向/边界

**TC-PREFIX-900：Negative Case Title**
Description of the negative scenario and expected rejection/error.
```

## TC ID Conventions

Format: `TC-{PREFIX}-{NUMBER}`

### Existing Prefixes

| Prefix | Module | Number Ranges |
|--------|--------|---------------|
| USER | User | 001-020, 900-903 |
| CAT | Category | 001-020, 900-902 |
| RULE | Rule | 001-020, 100-109, 900-901 |
| GRP | Group | 001-020, 900-901 |
| POST | Post | 001-076, 900-903 |
| RES | Resource | 001-045, 900-903 |
| IACT | Interaction | 001-063, 900-905 |
| REL-CR | Relations (category:rule) | 001-003, 900 |
| REL-CP | Relations (category:post) | 001-004, 900-902 |
| REL-CG | Relations (category:group) | 001-003, 900-901 |
| REL-PP | Relations (post:post) | 001-005 |
| REL-PR | Relations (post:resource) | 001-005 |
| REL-GU | Relations (group:user) | 001, 900-902 |
| REL-TI | Relations (target:interaction) | 001-002 |
| DEL | Cascade Delete | 001-022 |
| PERM | Permissions | 001-025 |
| JOUR | User Journeys | 002-013 |
| TRANSFER | Resource Transfer | 001-004 |
| FRIEND | User Follow | 001-007, 900-902 |
| STAGE | Category Stages | 001-004 |
| TRACK | Category Tracks | 001-003 |
| PREREQ | Prerequisites | 001-004 |
| CATREL | Category Relations (negative) | 900-903 |
| ENTRY | Entry Rules | 001-031, 900-902 |
| CLOSE | Closure Rules | 001-040, 900-902 |
| ENGINE | Rule Engine | 001-061 |

### Number Range Convention

- **001-099**: Positive/happy-path test cases (CRUD, workflows)
- **100-199**: Feature-specific enforcement cases
- **900-999**: Negative/boundary test cases

## Writing Rules

1. **Chinese only** — All test case descriptions are in Chinese
2. **Scenario + Expected Result** — Each test case describes only the scenario and expected outcome
3. **No test method** — Do not include test implementation details or execution steps
4. **Single paragraph** — Each test case is typically one paragraph. Use bullet points only for cascading/multi-effect outcomes
5. **Bold title** — Use `**TC-XXX-NNN：Title**` format on its own line
6. **Section grouping** — Group related test cases under `## N.M Section Name`
7. **Negative section last** — Place negative/boundary tests at the end under `## N.M 负向/边界`
