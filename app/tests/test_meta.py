from app.schemas.enums import PostType


def test_get_post_types(client):
    resp = client.get("/api/meta/post-types")
    assert resp.status_code == 200
    data = resp.json()
    assert data["default"] == PostType.general.value
    assert set(data["items"]) == {t.value for t in PostType}

