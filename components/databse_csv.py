import pandas as pd

def fetch_questions(id):
  questions =pd.read_csv(f"database_csv/{id}.csv",sep=";")
  response = []
  for Q,A in zip(questions["問題"],questions["答え"]):
    response.append({"Q":Q,"A":A})
  return response

  