from backup_config import backup_config


def test_original_unchanged():
    config = {"flags": ["fast"], "name": "x"}
    new = backup_config(config)
    assert new["flags"] == ["fast", "debug"]
    assert config["flags"] == ["fast"]
