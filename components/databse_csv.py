import pandas as pd

def insert_questions_to_database(id,df):
  df["id"] = id

  questions_database_path = "database_csv/questions.csv"
  questions_database = pd.read_csv(questions_database_path,sep=";")
  questions_database = pd.concat([questions_database,df],ignore_index=True)
  questions_database.to_csv(questions_database_path)