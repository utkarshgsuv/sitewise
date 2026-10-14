"""MCP server — M0 hello (FastAPI stub). Person A swaps in FastMCP + envelope verify in M-01."""
import os
from fastapi import FastAPI
from fastapi.responses import JSONResponse

app = FastAPI(title="sitewise-mcp")


@app.get("/health")
def health() -> JSONResponse:
    return JSONResponse({"service": "mcp", "ok": True})


@app.get("/")
def root() -> JSONResponse:
    return JSONResponse({"service": "mcp", "msg": "sitewise mcp up (M0 hello, FastMCP lands in M-01)"})


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv("PORT", "8001")))
