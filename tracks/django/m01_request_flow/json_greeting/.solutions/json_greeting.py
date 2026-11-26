from django.http import JsonResponse
from django.views.decorators.http import require_GET


@require_GET
def greeting(request):
    name = request.GET.get("name", "").strip() or "world"
    return JsonResponse({"message": f"Hello, {name}!"})
