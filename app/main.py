import uvicorn
from fastapi import FastAPI, HTTPException
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.instrumentation.sqlalchemy import SQLAlchemyInstrumentor
from opentelemetry.instrumentation.sqlite3 import SQLite3Instrumentor

from app.api.v1.routers import all_routers


app = FastAPI(title="Basic Template for Fast API + DB")

FastAPIInstrumentor.instrument_app(app)
SQLAlchemyInstrumentor().instrument()
SQLite3Instrumentor().instrument()


for router in all_routers:
    app.include_router(router)


@app.get("/", include_in_schema=False)
@app.get("/api/", include_in_schema=False)
@app.get("/api/v1", include_in_schema=False)
async def not_found():
    """
    Return a 404 for / and /api and /api/v1.
    """
    raise HTTPException(status_code=404, detail="Not Found")


@app.get("/ping", include_in_schema=False)
async def ping():
    """
    Return a 200 for /ping.
    """
    return {"pong": "pong"}


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8002, reload=True)
