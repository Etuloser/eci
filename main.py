import datetime

import uvicorn
from fastapi import FastAPI, Request
from pydantic import BaseModel

app = FastAPI()


class Resp(BaseModel):
    data: dict
    message: str
    code: int = 10020


@app.get("/", response_model=Resp)
def read_root() -> dict:
    return {
        "data": {},
        "message": "endpoint is '/'",
        "code": 10020,
    }


@app.post("/webhook")
async def webhook_endpoint(request: Request):
    # 获取 headers
    headers = dict(request.headers)

    # 获取 POST body
    try:
        body = await request.json()
    except Exception:
        # 如果不是 JSON，尝试获取原始 body
        body = await request.body()
        try:
            # 尝试解码为字符串
            body = body.decode("utf-8")
        except Exception:
            body = str(body)

    # 获取查询参数（如果有的话）
    query_params = dict(request.query_params)

    # 获取客户端信息
    client_host = request.client.host if request.client else None

    # 返回 headers 和 body
    return {
        "headers": headers,
        "body": body,
        "query_params": query_params,
        "client_host": client_host,
        "message": "Webhook received successfully",
        "timestamp": datetime.datetime.now().isoformat(),
        "method": request.method,
        "url": str(request.url),
    }


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=10862, log_level="info", reload=True)
