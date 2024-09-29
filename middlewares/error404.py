from fastapi import Request
from fastapi.responses import RedirectResponse
from starlette.middleware.base import BaseHTTPMiddleware

class Error404Middleware(BaseHTTPMiddleware):
    async def dispatch(self, r: Request, call_next):
        response = await call_next(r)
        if response.status_code == 404:
            return RedirectResponse('/error404')
            
        return response
