def add_tag(tag, tags=None):
    """Return a list of tags with tag added. Without a list, start a new one."""
    if tags is None:
        tags = []
    tags.append(tag)
    return tags
