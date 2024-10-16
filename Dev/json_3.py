"""
CA project
ce fichier est pour les tests de la librairie json
il prend clustering3.py et le convertit en json 
"""
import pandas as pd
import json

data = pd.read_csv('./clustering3.csv')
data_json = data.to_json(orient='records')
print(data_json)