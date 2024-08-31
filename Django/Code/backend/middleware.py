# backend/middleware.py
from django.utils.deprecation import MiddlewareMixin
from Auth.models import serverLogs
from django.middleware.csrf import CsrfViewMiddleware


class LoggingMiddleware(MiddlewareMixin):
    def process_response(self, request, response):
        serverLogs.objects.create(
            user=None,
            mehod=request.method,
            path=request.path,
            status=response.status_code
        )
        return response


class AllowAllCsrfMiddleware(CsrfViewMiddleware):
    def _accept(self, request):
        # Aceita qualquer origem
        return None