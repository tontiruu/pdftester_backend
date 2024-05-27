import pandas as pd


database = {}

def fetch_questions(id):
  questions = database[id]
  response = []
  for Q,A in zip(questions["問題"],questions["答え"]):
    response.append({"Q":Q,"A":A})
  return response


def insert_df(id,questions_df):
  global database
  database[id] = questions_df
  