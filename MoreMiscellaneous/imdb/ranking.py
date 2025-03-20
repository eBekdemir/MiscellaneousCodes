import pandas as pd
from collections import Counter
import ast


movies = pd.read_csv('movies_1.csv')

all_suggested = []
movies['rating'] = movies['rating'].fillna('null')
for vals in movies.loc[(movies['suggestions'].notnull()), ['rating', 'suggestions']].values.tolist():
    rates, suggested = vals
    if rates == None or rates == 'null': rates = 4
    all_suggested += [film[1] for film in ast.literal_eval(suggested)] * int(rates**1.25)

counts = Counter(all_suggested)

movies['movieRank'] = (movies['id'].map(counts).fillna(0).astype(int) * (movies['rating'].replace('null',4))).round(2)
movies['rating'] = movies['rating'].replace('null',None)

movies = movies.sort_values(by='movieRank', ascending=False)
movies.to_csv('movies_ranked.csv')