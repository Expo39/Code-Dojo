from django.db import models


class Book(models.Model):
    title = models.CharField(max_length=200)
    isbn = models.CharField(max_length=13, unique=True)
    pages = models.PositiveIntegerField()
    published = models.DateField(null=True, blank=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)

    class Meta:
        app_label = "dojo"
        ordering = ["title"]
        constraints = [
            models.CheckConstraint(condition=models.Q(pages__gte=1), name="book_pages_at_least_one"),
        ]

    def __str__(self):
        return f"{self.title} ({self.isbn})"

    def is_long(self):
        return self.pages >= 500
