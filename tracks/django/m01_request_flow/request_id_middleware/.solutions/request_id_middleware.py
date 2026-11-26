import re
import uuid

VALID = re.compile(r"[A-Za-z0-9_-]{1,64}")


class RequestIDMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        incoming = request.META.get("HTTP_X_REQUEST_ID", "").strip()
        request_id = incoming if VALID.fullmatch(incoming) else uuid.uuid4().hex
        request.request_id = request_id
        response = self.get_response(request)
        response["X-Request-ID"] = request_id
        return response
