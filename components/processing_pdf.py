from pypdf import PdfReader
import os
from openai import OpenAI
from dotenv import load_dotenv
import pandas as pd
from components import databse_csv
from io import BytesIO

load_dotenv()

openai_key = os.environ["OPENAI_API_KEY"]

def read_pdf(id,pdf_data):
  reader = PdfReader(pdf_data)
  text_data = []
  for page in reader.pages:
    text_data.append(page.extract_text())
  text_data = ", ".join(text_data)
  response = create_questions(text_data=text_data)
  text_csv = response.content
  text_csv = text_csv.replace("```","")
  pre_sentence = text_csv.split("問題;答え")[0]
  text_csv = text_csv[len(pre_sentence):]


  text_csv_buffer = BytesIO(text_csv.encode("utf-8"))
  questions_df = pd.read_csv(text_csv_buffer,sep=";")

  databse_csv.insert_df(id,questions_df)
  return text_data

def create_questions(text_data):
  text_data = text_data.replace(";",":")

  client = OpenAI(api_key=openai_key)
  completion = client.chat.completions.create(
    model="gpt-4o",
    temperature=0.1,
    messages=[
      {"role": "system", "content": """
      次のデータはPDF形式の講義資料からテキストデータを抽出したものです。
      テスト対策をしたいので、このテキストデータを元に幾つか問題と答えの組み合わせを作成して欲しいです！
      2問ほどお願いします!
      
      出力してもらった結果はPythonで読み込みたいので、「問題」「答え」の2つのカラムを持つ、";"区切りのCSVデータを変えして欲しいです!
      CSVデータだけを返すようにしてください!
      
      """},
      {"role": "user", "content": text_data}
    ]
  )
  response = completion.choices[0].message
  return response


