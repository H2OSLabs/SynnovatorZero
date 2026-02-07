import re
from pathlib import Path


def test_stats_endpoint_exists(client):
    resp = client.get("/api/stats")
    assert resp.status_code == 200
    assert resp.json() == {"user_count": 0, "category_count": 0, "post_count": 0}


def test_nginx_api_proxy_pass_preserves_api_prefix():
    repo_root = Path(__file__).resolve().parents[2]
    conf_path = repo_root / "deploy" / "nginx.conf"
    conf = conf_path.read_text(encoding="utf-8")

    match = re.search(r"location\s+/api/\s*\{(?P<body>[\s\S]*?)\n\s*\}", conf)
    assert match, "deploy/nginx.conf 缺少 location /api/ 区块"
    block = match.group("body")

    assert re.search(r"\bproxy_pass\s+http://backend;\s*", block), (
        "deploy/nginx.conf 的 /api/ 反代必须使用 proxy_pass http://backend; "
        "以保持后端实际路由前缀 /api 不被剥离"
    )
    assert not re.search(r"\bproxy_pass\s+http://backend/;\s*", block), (
        "deploy/nginx.conf 检测到 proxy_pass http://backend/; "
        "它会把 /api/events 转发为 /events，导致后端 404"
    )

