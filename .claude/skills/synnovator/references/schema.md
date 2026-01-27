# Synnovator Data Schema Reference

## Content Types

### category
| Field | Type | Required | Default | Notes |
|-------|------|----------|---------|-------|
| name | string | yes | — | Activity name |
| description | string | yes | — | Short description |
| type | enum | yes | — | `competition` \| `operation` |
| status | enum | no | `draft` | `draft` \| `published` \| `closed` |
| cover_image | string | no | — | Cover image URL |
| start_date | datetime | no | — | Start time |
| end_date | datetime | no | — | End time |
| id | string | auto | — | Unique ID |
| created_by | user_id | auto | — | Creator |
| created_at | datetime | auto | — | Creation time |
| updated_at | datetime | auto | — | Last update |
| deleted_at | datetime | auto | null | Soft delete timestamp |

### post
| Field | Type | Required | Default | Notes |
|-------|------|----------|---------|-------|
| title | string | yes | — | Post title |
| type | enum | no | `general` | `profile` \| `team` \| `category` \| `for_category` \| `certificate` \| `general` |
| tags | list[string] | no | [] | Tag list |
| status | enum | no | `draft` | `draft` \| `pending_review` \| `published` \| `rejected` |
| like_count | integer | cache | 0 | Auto-maintained |
| comment_count | integer | cache | 0 | Auto-maintained |
| average_rating | number | cache | null | Auto-maintained |
| id, created_by, created_at, updated_at, deleted_at | — | auto | — | Standard fields |

### resource
| Field | Type | Required | Default | Notes |
|-------|------|----------|---------|-------|
| filename | string | yes | — | Original filename |
| display_name | string | no | — | Display name |
| description | string | no | — | File description |
| mime_type | string | auto | — | MIME type |
| size | integer | auto | — | File size (bytes) |
| url | string | auto | — | Storage URL |
| id, created_by, created_at, updated_at, deleted_at | — | auto | — | Standard fields |

### rule
| Field | Type | Required | Default | Notes |
|-------|------|----------|---------|-------|
| name | string | yes | — | Rule name |
| description | string | yes | — | Rule description |
| allow_public | boolean | no | false | Allow public publishing |
| require_review | boolean | no | false | Require review |
| reviewers | list[user_id] | no | — | Reviewer list |
| submission_start | datetime | no | — | Submission start |
| submission_deadline | datetime | no | — | Submission deadline |
| submission_format | list[string] | no | — | Allowed formats |
| max_submissions | integer | no | — | Max submissions per user/team |
| min_team_size | integer | no | — | Min team size |
| max_team_size | integer | no | — | Max team size |
| scoring_criteria | list[object] | no | — | `[{name, weight, description}]` |
| id, created_by, created_at, updated_at, deleted_at | — | auto | — | Standard fields |

### user
| Field | Type | Required | Default | Notes |
|-------|------|----------|---------|-------|
| username | string | yes | — | Unique username |
| email | string | yes | — | Unique email |
| display_name | string | no | — | Display name |
| avatar_url | string | no | — | Avatar URL |
| bio | string | no | — | Bio |
| role | enum | no | `participant` | `participant` \| `organizer` \| `admin` |
| id, created_at, updated_at, deleted_at | — | auto | — | Standard fields |

### group
| Field | Type | Required | Default | Notes |
|-------|------|----------|---------|-------|
| name | string | yes | — | Group name |
| description | string | no | — | Description |
| visibility | enum | no | `public` | `public` \| `private` |
| max_members | integer | no | — | Max member count |
| require_approval | boolean | no | false | Require join approval |
| id, created_by, created_at, updated_at, deleted_at | — | auto | — | Standard fields |

### interaction
| Field | Type | Required | Default | Notes |
|-------|------|----------|---------|-------|
| type | enum | yes | — | `like` \| `comment` \| `rating` |
| target_type | enum | yes | — | `post` \| `category` \| `resource` |
| target_id | string | yes | — | Target object ID |
| value | string/object | no | — | Comment text or rating object |
| parent_id | interaction_id | no | — | Parent comment ID (nested replies) |
| id, created_by, created_at, updated_at, deleted_at | — | auto | — | Standard fields |

## Relation Types

### category_rule
`category_id` + `rule_id` + optional `priority` (integer, default 0)

### category_post
`category_id` + `post_id` + `relation_type` (`submission` \| `reference`) + auto `created_at`

### category_group
`category_id` + `group_id` + auto `registered_at`

### post_post
`source_post_id` + `target_post_id` + `relation_type` (`reference` \| `reply` \| `embed`) + optional `position`

### post_resource
`post_id` + `resource_id` + `display_type` (`attachment` \| `inline`) + optional `position`

### group_user
`group_id` + `user_id` + `role` (`owner` \| `admin` \| `member`) + `status` (`pending` \| `accepted` \| `rejected`) + auto `joined_at`, `status_changed_at`

### target_interaction
`target_type` + `target_id` + `interaction_id`

## Uniqueness Constraints
- user: `(username)`, `(email)`
- interaction (like): `(created_by, target_type, target_id)`
- category_rule: `(category_id, rule_id)`
- category_group: `(category_id, group_id)`
- group_user: `(group_id, user_id)`
