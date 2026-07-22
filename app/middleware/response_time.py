import time
from starlette.middleware.base import BaseHTTPMiddleware


class ResponseTimeMiddleware(BaseHTTPMiddleware):

    async def dispatch(self, request, call_next):

        start_time = time.perf_counter()
        response = await call_next(request)
        end_time = time.perf_counter()

        response.headers["X-Response-Time"] = (
            f"{(end_time-start_time)*1000:.2f}ms"
        )

        return response