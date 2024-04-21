
import os

from fastapi import FastAPI

from starlette.requests import Request
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.responses import Response
from fastapi.middleware.cors import CORSMiddleware

from logger import customLogger
import uuid
class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        req_id = uuid.uuid4()
        customLogger.info(f'REQUEST  {str(req_id)}: {request.method} - {request.url}')
        response = await call_next(request)
        customLogger.info(f'RESPONSE {str(req_id)}: {response.status_code}')
        return response


def addCorsMiddleware(app: FastAPI):
    origins = ["*"]
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )