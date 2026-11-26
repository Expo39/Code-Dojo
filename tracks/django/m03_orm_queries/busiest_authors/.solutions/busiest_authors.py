from django.db.models import Count


def busiest_authors(Writer, min_novels, limit):
    if limit <= 0:
        return []
    rows = (
        Writer.objects.annotate(total=Count("novels"))
        .filter(total__gte=min_novels)
        .order_by("-total", "name")
        .values_list("name", "total")[:limit]
    )
    return list(rows)
