import os

import uvicorn
from fastapi import FastAPI, Response
from starlette.requests import Request

import constants
from logger import customLogger as logger
from middlewares.middleware import LoggingMiddleware, addCorsMiddleware
from routes import cvrp

if not os.path.exists('./logs'):
    os.makedirs('./logs')

logger.info("Loading application ... ")


app = FastAPI(
    title="CVRP SERVICE",
    description="This is a webservices for CVRP services",
)

async def catch_exceptions_middleware(request: Request, call_next):
    try:
        return await call_next(request)
    except Exception as error:
        # you probably want some kind of logging here
        logger.error(error, exc_info=True)
        return Response("Internal server error", status_code=500)

app.middleware('http')(catch_exceptions_middleware)
app.add_middleware(LoggingMiddleware)
addCorsMiddleware(app)


app.include_router(cvrp.router, prefix="/cvrp")

if __name__ == "__main__":
    # uvicorn.run("app:app", host=constants.APP_HOST, port=constants.APP_PORT, reload=constants.APP_RELOAD)
    uvicorn.run("app:app" , host=constants.APP_HOST ,port=constants.APP_PORT, reload=constants.APP_RELOAD)
