from app.core.config import Settings


def test_cors_origins_supports_csv():
    s = Settings(cors_origins="http://localhost:3000,http://localhost:9080")
    assert s.cors_origins == ["http://localhost:3000", "http://localhost:9080"]


def test_cors_origins_supports_json_list():
    s = Settings(cors_origins='["http://a.test","http://b.test"]')
    assert s.cors_origins == ["http://a.test", "http://b.test"]

