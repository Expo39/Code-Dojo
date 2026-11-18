import copy


def backup_config(config):
    """Return a changed copy of config (a dict of lists) with "debug" appended to
    config["flags"]. The original must not change."""
    new = copy.deepcopy(config)
    new["flags"].append("debug")
    return new
