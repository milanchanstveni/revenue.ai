from fastapi import FastAPI
import uvicorn
from tortoise.contrib.fastapi import register_tortoise

from core.logging import LOG
from api.routers2 import API2
from db.utils import (
    create_database,
    get_db_config,
    load_priority_codes,
    delete_all_priority_records
)


APP = FastAPI(
    title="Revenue.AI",
    description='Second API service (Priority object)',
    version="1.0",
    docs_url="/docs",
)

register_tortoise(
    app=APP,
    config=get_db_config(),
    generate_schemas=True,
    add_exception_handlers=True,
)

APP.include_router(API2)

@APP.on_event("startup")
async def startup():
    await create_database()
    await delete_all_priority_records()
    await load_priority_codes()
    LOG.info("Server started.")


@APP.on_event("shutdown")
async def shutdown():
    LOG.info("Server stopped.")


if __name__ == "__main__":
    uvicorn.run(
        app="services.api2:APP",
        host="0.0.0.0",
        port=5001,
        reload=True
    )