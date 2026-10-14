"""FastAPI runtime — M0 hello. Full routes land in P-01..P-08 (Person B)."""
import os
from fastapi import FastAPI
from fastapi.responses import JSONResponse

app = FastAPI(title="sitewise-api")


@app.get("/health")
def health() -> JSONResponse:
    return JSONResponse({"service": "api", "ok": True})


@app.get("/")
def root() -> JSONResponse:
    return JSONResponse({"service": "api", "msg": "sitewise api up (M0 hello)"})


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv("PORT", "8000")))
