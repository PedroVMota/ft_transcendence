# backend/middleware.py
from django.utils.deprecation import MiddlewareMixin
from Auth.models import serverLogs


class LoggingMiddleware(MiddlewareMixin):
    def process_response(self, request, response):
        print("LoggingMiddleware process_response called")  # Add this line
        if request.user.is_authenticated:
            print("REQUEST USER IS AUTHENTICATED")  # Add this line
            serverLogs.objects.create(
                user=request.user,
                mehod=request.method,
                path=request.path,
                status=response.status_code
            )
        else:
            serverLogs.objects.create(
                user=None,
                mehod=request.method,
                path=request.path,
                status=response.status_code
            )
        return response