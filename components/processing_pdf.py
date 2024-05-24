from pypdf import PdfReader
import os
from openai import OpenAI
from dotenv import load_dotenv
import pandas as pd
from components import databse_csv

load_dotenv()

openai_key = os.environ["OPENAI_API_KEY"]

def read_pdf(id):
  reader = PdfReader(f"input_pdf/{id}.pdf")
  os.remove(f"input_pdf/{id}.pdf")
  text_data = []
  for page in reader.pages:
    text_data.append(page.extract_text())
  text_data = ", ".join(text_data)
  response = create_questions(text_data=text_data)
  tmp_insert_questions_path = "database_csv/tmp_insert_questions.csv"
  file = open(tmp_insert_questions_path,"w")
  file.write(response.content)
  file.close()
  insert_questions = pd.read_csv(tmp_insert_questions_path,sep=";")
  databse_csv.insert_questions_to_database(id=id,df=insert_questions)


  return text_data

def create_questions(text_data):

  client = OpenAI(api_key=openai_key)
  completion = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
      {"role": "system", "content": """
      次のデータはPDF形式の講義資料からテキストデータを抽出したものです。
      テスト対策をしたいので、このテキストデータを元に幾つか問題と答えの組み合わせを作成して欲しいです！
      30問ほどお願いします!
      
      出力してもらった結果はPythonで読み込みたいので、「問題」「答え」の2つのカラムを持つ、";"区切りのCSVデータを変えして欲しいです!
      CSVデータだけを返すようにしてください!
      
      """},
      {"role": "user", "content": text_data}
    ]
  )
  response = completion.choices[0].message
  return response

