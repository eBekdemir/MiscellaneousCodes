import pandas as pd
import numpy as np
import json
import time

with open('data/ranking_settings.json') as f:
    S = json.load(f)

def calculateRatingScore(movies: pd.DataFrame):
    scores = movies[['id']].copy()

    movies['rating'] = pd.to_numeric(movies['rating'], errors='coerce')
    movies['ratingCount'] = pd.to_numeric(movies['ratingCount'], errors='coerce')
    movies['rating'] = movies['rating'].fillna(0)
    movies['ratingCount'] = movies['ratingCount'].fillna(0)
    movies['userRate'] = pd.to_numeric(movies['userRate'], errors='coerce')

    conditionsPower = [
        movies['ratingCount'] < 500,
        (movies['ratingCount'] >= 500) & (movies['ratingCount'] < 1000),
        (movies['ratingCount'] >= 1000) & (movies['ratingCount'] < 2000),
        (movies['ratingCount'] >= 2000) & (movies['ratingCount'] < 5000),
        (movies['ratingCount'] >= 5000) & (movies['ratingCount'] < 10000),
        (movies['ratingCount'] >= 10000) & (movies['ratingCount'] < 20000),
        (movies['ratingCount'] >= 20000) & (movies['ratingCount'] < 40000),
        (movies['ratingCount'] >= 40000) & (movies['ratingCount'] < 80000),
        (movies['ratingCount'] >= 80000) & (movies['ratingCount'] < 125000),
        (movies['ratingCount'] >= 125000) & (movies['ratingCount'] < 200000),
        (movies['ratingCount'] >= 200000) & (movies['ratingCount'] < 500000),
        (movies['ratingCount'] >= 500000) & (movies['ratingCount'] < 1000000),
        movies['ratingCount'] >= 1000000
    ]

    choicesPower = [
        S['imdbRatingPower'],
        S['imdbRatingPower'] + 0.15,
        S['imdbRatingPower'] + 0.25,
        S['imdbRatingPower'] + 0.275,
        S['imdbRatingPower'] + 0.3,
        S['imdbRatingPower'] + 0.325,
        S['imdbRatingPower'] + 0.35,
        S['imdbRatingPower'] + 0.375,
        S['imdbRatingPower'] + 0.4,
        S['imdbRatingPower'] + 0.425,
        S['imdbRatingPower'] + 0.45,
        S['imdbRatingPower'] + 0.475,
        S['imdbRatingPower'] + 0.5
    ]

    movies['imdbRatingPower'] = np.select(conditionsPower, choicesPower, default=1.0)


    # If both rating and userRate are NaN, assign a default score
    movies['adjustedRating'] = np.select(
        [
            (movies['rating'].isna() & movies['userRate'].isna()),  # Both are NaN
            (movies['rating'].isna()),  # Only rating is NaN
            (movies['ratingCount'] == 0),  # If ratingCount is 0, prevent errors
            movies['userRate'].isna()  # Only userRate is NaN
        ],
        [
            2,  # Default score when both are missing
            2,  # Default score if only rating is missing
            2,  # Assign a fallback score if ratingCount is 0
            movies['rating'] ** movies['imdbRatingPower'] - 5 ** movies['imdbRatingPower']
        ],
        default=(movies['rating'] ** movies['imdbRatingPower'] - 5 ** movies['imdbRatingPower'] + 
                movies['userRate'] ** S['userRatingPower'] - 6 ** S['userRatingPower'])
    )

    scores['ratingScore'] = ((movies['adjustedRating'] * movies['ratingCount']) / (movies['ratingCount'] + S['minRatingCount']))*S['ratingWeight']
    return scores


def genreScore(movies):
    scores = movies[['id']].copy()
    movies['genres'] = movies['genres'].str.split(':,:')
    
    calculate = lambda x: sum([S['genreWeights'][genre] for genre in x if genre in S['genreWeights']])
    
    movies['genreScore'] = movies['genres'].apply(calculate)
    movies['genreScore'] = (movies['genreScore'] / movies['genres'].apply(len)) * S['genreWeight']
    
    scores['genreScore'] = movies['genreScore']
    return scores

def main() -> None:

    movies = pd.read_parquet('data/movies.parquet')

    ratings = calculateRatingScore(movies)
    genres = genreScore(movies)
    scores = pd.merge(ratings, genres, on='id')
    scores['totalScore'] = scores['ratingScore'] + scores['genreScore']
    scores.to_parquet('data/initial_scores2.parquet')


if __name__=='__main__':
    start = time.time()
    main()
    print(f'Execution time: {time.time() - start} seconds')