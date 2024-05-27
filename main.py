from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from fastapi import APIRouter, Depends, HTTPException,UploadFile,File
from fastapi.middleware.cors import CORSMiddleware
from pypdf import PdfReader
from uuid import uuid4
from components import processing_pdf
from components import databse_csv
from openai import APIConnectionError
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

@app.post("/uploadfile")
async def create_upload_file(file: UploadFile = File(...)):
    try:
      contents = await file.read()
      filename = file.filename
      if filename.split(".")[-1] != "pdf":
        return {"id":0,"error":True,"error_message":"PDFファイルをアップロードしてください"}   
      id = uuid4()
      filename = f"{id}.pdf" 
      save_file = open(f"./input_pdf/{filename}","wb")
      save_file.write(contents)
      save_file.close()
      processing_pdf.read_pdf(id)
      return {"id": id, "error":False,"error_message":None}
    except APIConnectionError:
        print("a")
        return {"id":0,"error":True,"error_message":"通信エラーが発生しました。ネット接続を確認してください"}   
    except:
        return {"id":0,"error":True,"error_message":"不明なエラーが発生しました"}   

        # return {"id":0,"error":True,"error_message":"エラーが発生しました"}

@app.get("/fetch_questions")
async def fetch_questions(id):
    try:
        response = {"error":False}
        response["data"] = databse_csv.fetch_questions(id)
        return response
    except:
        return {"error":True,"data":None}



# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app, host="0.0.0.0", port=8001)
