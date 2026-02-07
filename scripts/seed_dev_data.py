from __future__ import annotations

from datetime import datetime, timezone
import sqlite3

from sqlalchemy.orm import Session

from app.database import Base, SessionLocal, engine, DATA_DIR
from app.models.category import Category
from app.models.group import Group
from app.models.member import Member
from app.models.post import Post
from app.models.user import User


def _has_category_tags_column(db_path: str) -> bool:
    conn = sqlite3.connect(db_path)
    try:
        rows = conn.execute("PRAGMA table_info(categories);").fetchall()
        cols = {r[1] for r in rows}
        return "tags" in cols
    finally:
        conn.close()


def _ensure_schema() -> None:
    Base.metadata.create_all(bind=engine)


def _seed_users(db: Session) -> dict[str, int]:
    users = [
        {
            "username": "techcorp",
            "email": "techcorp@example.com",
            "display_name": "TechCorp",
            "role": "organizer",
            "password": "techcorp",  # 密码 = 用户名
        },
        {
            "username": "alice",
            "email": "alice@example.com",
            "display_name": "Alice",
            "role": "participant",
            "password": "alice",
        },
        {
            "username": "bob",
            "email": "bob@example.com",
            "display_name": "Bob",
            "role": "participant",
            "password": "bob",
        },
        {
            "username": "carol",
            "email": "carol@example.com",
            "display_name": "Carol",
            "role": "participant",
            "password": "carol",
        },
        {
            "username": "dave",
            "email": "dave@example.com",
            "display_name": "Dave",
            "role": "participant",
            "password": "dave",
        },
        {
            "username": "eve",
            "email": "eve@example.com",
            "display_name": "Eve",
            "role": "participant",
            "password": "eve",
        },
        {
            "username": "frank",
            "email": "frank@example.com",
            "display_name": "Frank",
            "role": "participant",
            "password": "frank",
        },
    ]

    ids: dict[str, int] = {}
    for u in users:
        existing = db.query(User).filter(User.username == u["username"]).first()
        if existing:
            ids[u["username"]] = existing.id
            continue
        obj = User(**u)
        db.add(obj)
        db.flush()
        ids[u["username"]] = obj.id
    db.commit()
    return ids


def _seed_categories(db: Session, creator_user_id: int) -> None:
    categories = [
        {
            "name": "AI 创新挑战赛 2024",
            "description": "探索人工智能的无限可能，用 AI 改变世界",
            "type": "competition",
            "status": "published",
            "tags": ["AI", "Machine Learning"],
            "participant_count": 128,
            "start_date": datetime(2024, 3, 1),
            "end_date": datetime(2024, 3, 30),
        },
        {
            "name": "Web3 黑客马拉松",
            "description": "围绕 Web3 与区块链的 2 周高强度协作开发",
            "type": "competition",
            "status": "published",
            "tags": ["Web3", "Blockchain"],
            "participant_count": 86,
            "start_date": datetime(2024, 4, 1),
            "end_date": datetime(2024, 4, 15),
        },
        {
            "name": "绿色科技创新大赛",
            "description": "用技术推动可持续发展，解决气候相关真实问题",
            "type": "competition",
            "status": "published",
            "tags": ["Climate", "Sustainability"],
            "participant_count": 64,
            "start_date": datetime(2024, 5, 1),
            "end_date": datetime(2024, 5, 31),
        },
        {
            "name": "开源社区贡献月",
            "description": "参与开源、完成任务、赢取奖励，和社区一起成长",
            "type": "operation",
            "status": "published",
            "tags": ["Open Source"],
            "participant_count": 256,
            "start_date": datetime(2024, 3, 1),
            "end_date": datetime(2024, 3, 31),
        },
        {
            "name": "移动应用创新赛",
            "description": "面向 iOS/Android 的移动应用创意与实现竞赛",
            "type": "competition",
            "status": "draft",
            "tags": ["Mobile", "iOS", "Android"],
            "participant_count": 0,
            "start_date": datetime(2024, 6, 1),
            "end_date": datetime(2024, 6, 30),
        },
        {
            "name": "2023 年度创新盛典",
            "description": "年度创新项目展示与颁奖盛典（已结束）",
            "type": "competition",
            "status": "closed",
            "tags": ["Innovation"],
            "participant_count": 512,
            "start_date": datetime(2023, 11, 1),
            "end_date": datetime(2023, 12, 15),
        },
    ]

    existing_names = {n for (n,) in db.query(Category.name).filter(Category.deleted_at.is_(None)).all()}
    inserted = 0
    for c in categories:
        if c["name"] in existing_names:
            continue
        db.add(Category(**c, created_by=creator_user_id))
        inserted += 1
    db.commit()
    print(f"Seeded categories: +{inserted}")


def _seed_posts(db: Session, author_user_ids: dict[str, int]) -> None:
    posts = [
        {
            "title": "基于大模型的智能教育平台",
            "type": "for_category",
            "status": "published",
            "visibility": "public",
            "tags": ["AI", "Education", "LLM"],
            "content": "我们开发了一个基于大语言模型的个性化学习平台，能够根据学生的学习进度自动调整教学内容。",
            "created_by": author_user_ids["alice"],
            "like_count": 128,
            "comment_count": 32,
        },
        {
            "title": "去中心化身份认证系统",
            "type": "for_category",
            "status": "published",
            "visibility": "public",
            "tags": ["Web3", "DID", "Privacy"],
            "content": "利用区块链技术构建的下一代身份认证系统，让用户真正掌控自己的数据。",
            "created_by": author_user_ids["bob"],
            "like_count": 96,
            "comment_count": 24,
        },
        {
            "title": "碳足迹追踪应用",
            "type": "general",
            "status": "published",
            "visibility": "public",
            "tags": ["Climate", "Mobile", "Gamification"],
            "content": "帮助用户记录和减少日常生活中的碳排放，通过游戏化机制激励环保行动。",
            "created_by": author_user_ids["alice"],
            "like_count": 72,
            "comment_count": 18,
        },
        {
            "title": "开源代码审查工具",
            "type": "general",
            "status": "published",
            "visibility": "public",
            "tags": ["DevTools", "AI", "Security"],
            "content": "AI 驱动的代码审查助手，帮助开发者发现潜在 bug 和安全漏洞。",
            "created_by": author_user_ids["bob"],
            "like_count": 156,
            "comment_count": 42,
        },
        {
            "title": "找队友：AI 方向",
            "type": "team",
            "status": "published",
            "visibility": "public",
            "tags": ["招募", "AI"],
            "content": "我们团队正在寻找 AI/ML 方向的伙伴，有兴趣的请联系。",
            "created_by": author_user_ids["eve"],
            "like_count": 45,
            "comment_count": 12,
        },
        {
            "title": "日常分享：参赛心得",
            "type": "general",
            "status": "published",
            "visibility": "public",
            "tags": ["心得", "分享"],
            "content": "参加了这次黑客马拉松，收获满满，欢迎交流参赛经验。",
            "created_by": author_user_ids["frank"],
            "like_count": 89,
            "comment_count": 28,
        },
    ]

    existing_titles = {t for (t,) in db.query(Post.title).filter(Post.deleted_at.is_(None)).all()}
    inserted = 0
    for p in posts:
        if p["title"] in existing_titles:
            continue
        db.add(Post(**p))
        inserted += 1
    db.commit()
    print(f"Seeded posts: +{inserted}")


def _seed_groups(db: Session, user_ids: dict[str, int]) -> dict[str, int]:
    groups = [
        {
            "name": "创新先锋队",
            "visibility": "public",
            "description": "热爱技术，热爱开源，我们是一群热情的创客！",
            "created_by": user_ids["alice"],
        },
        {
            "name": "AI 实验室",
            "visibility": "public",
            "description": "探索 AI 的无限可能，用技术改变世界",
            "created_by": user_ids["bob"],
        },
        {
            "name": "Web3 先锋",
            "visibility": "public",
            "description": "去中心化的未来由我们创造",
            "created_by": user_ids["carol"],
        },
        {
            "name": "设计创意组",
            "visibility": "public",
            "description": "用设计传递价值，用创意点亮生活",
            "created_by": user_ids["dave"],
        },
        {
            "name": "全栈开发团",
            "visibility": "public",
            "description": "从前端到后端，我们无所不能",
            "created_by": user_ids["eve"],
        },
        {
            "name": "数据科学家",
            "visibility": "private",
            "description": "用数据洞察一切",
            "created_by": user_ids["frank"],
        },
    ]

    existing = {n for (n,) in db.query(Group.name).filter(Group.deleted_at.is_(None)).all()}
    inserted = 0
    name_to_id: dict[str, int] = {}
    for g in groups:
        obj = db.query(Group).filter(Group.name == g["name"]).first()
        if obj:
            name_to_id[g["name"]] = obj.id
            continue
        if g["name"] in existing:
            continue
        obj = Group(**g)
        db.add(obj)
        db.flush()
        name_to_id[g["name"]] = obj.id
        inserted += 1
    db.commit()
    print(f"Seeded groups: +{inserted}")
    return name_to_id


def _seed_members(db: Session, group_ids: dict[str, int], user_ids: dict[str, int]) -> None:
    pairs = [
        ("创新先锋队", "alice", "owner"),
        ("创新先锋队", "bob", "member"),
        ("创新先锋队", "carol", "member"),
        ("AI 实验室", "bob", "owner"),
        ("AI 实验室", "alice", "admin"),
        ("AI 实验室", "dave", "member"),
        ("Web3 先锋", "carol", "owner"),
        ("Web3 先锋", "eve", "member"),
        ("设计创意组", "dave", "owner"),
        ("设计创意组", "frank", "member"),
        ("全栈开发团", "eve", "owner"),
        ("全栈开发团", "alice", "member"),
        ("数据科学家", "frank", "owner"),
    ]

    inserted = 0
    for group_name, username, role in pairs:
        gid = group_ids.get(group_name)
        uid = user_ids.get(username)
        if gid is None or uid is None:
            continue
        existing = db.query(Member).filter(Member.group_id == gid, Member.user_id == uid).first()
        if existing:
            continue
        db.add(
            Member(
                group_id=gid,
                user_id=uid,
                role=role,
                status="accepted",
                joined_at=datetime.now(timezone.utc),
                status_changed_at=datetime.now(timezone.utc),
            )
        )
        inserted += 1
    db.commit()
    print(f"Seeded members: +{inserted}")


def main() -> None:
    _ensure_schema()

    db_path = str(DATA_DIR / "synnovator.db")
    if not _has_category_tags_column(db_path):
        raise SystemExit(
            "当前数据库缺少 categories.tags 字段。请先运行 `make resetdb` 删除旧库后再执行 seed。"
        )

    with SessionLocal() as db:
        user_ids = _seed_users(db)
        _seed_categories(db, creator_user_id=user_ids["techcorp"])
        _seed_posts(db, author_user_ids=user_ids)
        group_ids = _seed_groups(db, user_ids=user_ids)
        _seed_members(db, group_ids=group_ids, user_ids=user_ids)
        print("Seed completed.")


if __name__ == "__main__":
    main()
