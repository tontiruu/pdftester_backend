from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from fastapi import APIRouter, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware

# API configuration
app = FastAPI()
# another_slack_backend.include_router(api_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],  # 全てのHTTPメソッドを許可
    allow_headers=["*"],
)


# @app.get("/get_main_messages")
# async def test():
#     return get_main_message("ミニ運営")





if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
