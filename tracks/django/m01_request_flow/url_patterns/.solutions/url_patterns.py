from django.http import HttpResponse
from django.urls import path


def home(request):
    return HttpResponse("home")


def article_detail(request, pk):
    return HttpResponse(f"article {pk}")


def archive(request, year, slug):
    return HttpResponse(f"archive {year} {slug}")


urlpatterns = [
    path("", home, name="home"),
    path("articles/<int:pk>/", article_detail, name="article-detail"),
    path("archive/<int:year>/<slug:slug>/", archive, name="archive"),
]
