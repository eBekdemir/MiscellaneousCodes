import os
import sys
import requests
import pandas as pd
import json
from bs4 import BeautifulSoup as bs
import time
import logging
from html import unescape
import asyncio



if not os.path.exists("logs"):
    os.makedirs("logs")
if not os.path.exists("data"):
    os.makedirs("data")
    os.makedirs("data/cache")
elif not os.path.exists("data/cache"):
    os.makedirs("data/cache")

start_time = time.time()

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
    "Accept-Language": "en-US,en",
    "Accept-Encoding": "gzip, deflate, br, utf-8",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
}
session = requests.Session()

missingMovies = logging.getLogger("missingMovies")
missingMovies.setLevel(logging.WARNING)
logger = logging.getLogger("scraper")
logger.setLevel(logging.DEBUG)
if not os.path.exists(f"logs/scraping-{time.strftime('%Y-%m-%d')}.log"):
    file_handler = logging.FileHandler(f"logs/scraping-{time.strftime('%Y-%m-%d')}.log", mode="w")
else:
    file_handler = logging.FileHandler(f"logs/scraping-{time.strftime('%Y-%m-%d')}.log", mode="a")
if not os.path.exists(f"logs/missingMovies.log"):
    missing_handler = logging.FileHandler(f"logs/missingMovies.log", mode="w")
else:
    missing_handler = logging.FileHandler(f"logs/missingMovies.log", mode="a")
missing_handler.setLevel(logging.WARNING)
file_handler.setLevel(logging.INFO)
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s", "%Y-%m-%d %H:%M:%S")
missingFormatter = logging.Formatter("%(asctime)s ::: %(message)s", "%Y-%m-%d %H:%M:%S")
file_handler.setFormatter(formatter)
missing_handler.setFormatter(missingFormatter)
file_handler.flush = lambda: file_handler.stream.flush() # Force flush after every log message
missing_handler.flush = lambda: missing_handler.stream.flush() # Force flush after every log message
logger.addHandler(file_handler)
missingMovies.addHandler(missing_handler)


def movieDetail(movieID: str) -> dict:
    '''Get specified movie details from IMDB page'''
    try:
        movie_html = session.get('https://www.imdb.com/title/' + movieID, headers=headers)
        movie_soup = bs(movie_html.content, 'html.parser')
        next_script = movie_soup.find('script', {'id': '__NEXT_DATA__'})
        next_json = json.loads(unescape(next_script.text))
    except Exception as e:
        logger.warning(f"Getting movie html ({movieID}): {e}")
        missingMovies.warning(f"{movieID}")
        return None, None, None, None, None, None, None, None, None, None, None

    try:
        released = True if next_json['props']['pageProps']['aboveTheFoldData']['productionStatus']['currentProductionStage']['id'] == 'released' else False
    except Exception as e:
        logger.info(f"Getting release status ({movieID}): {e}")
        released = None

    try:
        movieTitle = next_json['props']['pageProps']['aboveTheFoldData']['titleText']['text']
    except Exception as e:
        logger.warning(f"Getting title ({movieID}): {e}")
        movieTitle = None

    try:
        seconds = next_json['props']['pageProps']['aboveTheFoldData']['runtime']['seconds'] # .get('seconds') i didn't use that to see if it is not exist in log file
    except Exception as e:
        logger.debug(f"Getting runtime ({movieID}: {movieTitle or '?'}): {e}")
        seconds = None
        
    try:
        duration = next_json['props']['pageProps']['aboveTheFoldData']['runtime']['displayableProperty']['value']['plainText']
    except Exception as e:
        logger.debug(f"Getting duration ({movieID}: {movieTitle or '?'}): {e}")
        if seconds:
            duration = f"{seconds//3600}h {seconds%3600//60}m"
        else: duration = None

    try:
        release = next_json['props']['pageProps']['aboveTheFoldData']['releaseYear']['year'] # .get('year') i didn't use that to see if it is not exist in log file
    except Exception as e:
        logger.debug(f"Getting release year ({movieID}: {movieTitle or '?'}): {e}")
        release = None

    try:
        countries = [country['text'] for country in next_json['props']['pageProps']['mainColumnData']['countriesOfOrigin']['countries']]
    except Exception as e:
        logger.debug(f"Getting countries of origin ({movieID}: {movieTitle or '?'}): {e}")
        countries = None

    try:
        directors = [director['name']['nameText']['text'] for directors in next_json['props']['pageProps']['aboveTheFoldData']['directorsPageTitle'] for director in directors['credits'] ]
    except Exception as e:
        logger.info(f"Getting directors ({movieID}: {movieTitle or '?'}): {e}")
        directors = None

    try:
        writers = [writer['name']['nameText']['text'] for writer in next_json['props']['pageProps']['mainColumnData']['writers'][0]['credits']]
    except Exception as e:
        logger.debug(f"Getting writers ({movieID}: {movieTitle or '?'}): {e}")
        writers = None

    try:
        cast = [edge['node']['name']['nameText']['text'] for edge in next_json['props']['pageProps']['mainColumnData']['cast']['edges']]
    except Exception as e:
        logger.info(f"Getting cast ({movieID}: {movieTitle or '?'}): {e}")
        cast = None

    try:
        suggestions = [
            [edge['node']['titleText']['text'], edge['node']['id']]
            for edge in next_json['props']['pageProps']['mainColumnData']['moreLikeThisTitles']['edges']
        ]
    except Exception as e:
        logger.info(f"Getting suggestions ({movieID}: {movieTitle or '?'}): {e}")
        suggestions = None
    
    try:
        keywords = [edge['node']['text'] for edge in next_json['props']['pageProps']['aboveTheFoldData']['keywords']['edges']]
    except Exception as e:
        logger.debug(f"Getting keywords ({movieID}: {movieTitle or '?'}): {e}")
        keywords = None
    
    try:
        quotes = list(filter(lambda x: x is not None, [quote['text'] for edge in next_json['props']['pageProps']['mainColumnData']['quotes']['edges'] for quote in edge['node']['lines']]))
    except Exception as e:
        logger.debug(f"Getting quotes ({movieID}: {movieTitle or '?'}): {e}")
        quotes = None
    
    try:
        rating = next_json['props']['pageProps']['aboveTheFoldData']['ratingsSummary']['aggregateRating']
        rating_count = next_json['props']['pageProps']['aboveTheFoldData']['ratingsSummary']['voteCount']
    except Exception as e:
        logger.debug(f"Getting rating ({movieID}: {movieTitle or '?'}): {e}")
        rating = None
        rating_count = None
    
    try:
        description = next_json['props']['pageProps']['aboveTheFoldData']['plot']['plotText']['plainText']
    except Exception as e:
        logger.info(f"Getting description ({movieID}: {movieTitle or '?'}): {e}")
        description = None
    try:
        genres = [gn['text'] for genre in [next_json['props']['pageProps']['aboveTheFoldData']['genres']['genres']] for gn in genre]
    except Exception as e: 
        logger.info(f"Getting genres ({movieID}: {movieTitle or '?'}): {e}")
        genres = None
    
    try:
        image = next_json['props']['pageProps']['aboveTheFoldData']['primaryImage']['url']
    except Exception as e:
        image = None
        logger.debug(f"Getting image ({movieID}: {movieTitle or '?'}): {e}")

    try:
        typ = next_json['props']['pageProps']['aboveTheFoldData']['titleType']['id']
    except Exception as e:
        logger.debug(f"Getting type ({movieID}: {movieTitle or '?'}): {e}")
        typ = None

    return {
        "title": movieTitle,
        "releaseStatus": released,
        "type": typ,
        "runtimeSeconds": seconds,
        "duration": duration,
        "releaseYear": release,
        "countriesOfOrigin": countries,
        "directors": directors,
        "writers": writers,
        "cast": cast,
        "suggestions": suggestions,
        "keywords": keywords,
        "quotes": quotes,
        "rating": rating,
        "ratingCount": rating_count,
        "description": description,
        "genres": genres,
        "imageUrl": image
    }



def top250(typ: str = 'movies'):
    """
    it creates a csv file with imdb top 250 movies
    the csv file includes those:
        ,id,name,rating,ratingCount,movieRank,genres,duration,seconds,description,releaseYear,countries,directors,casts,suggestions,keywords,quotes

    """
    try:
        if typ == 'movies':
            url = "https://www.imdb.com/chart/top/"
        elif typ == 'tvshows': 
            url = "https://www.imdb.com/chart/toptv/"
        htmll = session.get(url, headers=headers)
        soup = bs(htmll.content, 'lxml')
        
        # The code below returns only first 25 item:
        # ul = soup.find_all('ul', class_='ipc-metadata-list')[0]
        # print(*[li.find('h3').text for li in ul.find_all('li')], sep='\n')


        # I found a script which includes all items in it:
        script = soup.find('script', {'type':'application/ld+json'})
        jsn = json.loads(script.text)
        
        df = pd.DataFrame([
            {
                'id': item['item']['url'].split('/')[-2],
                'title': str(unescape(item['item'].get('alternateName', item['item']['name']))),
                'releaseStatus': True,
                'type': 'movie',
                'runtimeSeconds': None,
                'rating': item['item']['aggregateRating']['ratingValue'],
                'ratingCount': item['item']['aggregateRating']['ratingCount'],
                'genres': ':,:'.join(item['item']['genre'].split(', ')),
                'description': str(unescape(item['item']['description']))
            }
            for item in jsn['itemListElement']
        ], index=range(1, 251))

    except Exception as e:
        logger.error(f"Getting top 250 movies: {e}")
        return

    for ind in range(1,251):
        try:
            theMovie = movieDetail(df.loc[ind, 'id'])
            df.at[ind, 'runtimeSeconds'] = theMovie.get('runtimeSeconds', 0)
            df.at[ind, 'duration'] = theMovie.get('duration', 0)
            df.at[ind, 'releaseYear'] = theMovie.get('releaseYear')
            df.at[ind, 'countriesOfOrigin'] = ':,:'.join(theMovie.get('countriesOfOrigin', [])) if isinstance(theMovie.get('countriesOfOrigin'), list) else theMovie.get('countriesOfOrigin', "Unknown")
            df.at[ind, 'directors'] = ':,:'.join(theMovie.get('directors', [])) if isinstance(theMovie.get('directors'), list) else theMovie.get('directors')
            df.at[ind, 'writers'] = ':,:'.join(theMovie.get('writers', [])) if isinstance(theMovie.get('writers'), list) else theMovie.get('writers')
            df.at[ind, 'cast'] = ':,:'.join(theMovie.get('cast', [])) if isinstance(theMovie.get('cast'), list) else theMovie.get('cast')
            df.at[ind, 'suggestionsID'] = ':,:'.join([sug[1] for sug in theMovie.get('suggestions', [])]) if isinstance(theMovie.get('suggestions'), list) else theMovie.get('suggestions')
            df.at[ind, 'suggestionsTitle'] = ':,:'.join([sug[0] for sug in theMovie.get('suggestions', [])]) if isinstance(theMovie.get('suggestions'), list) else theMovie.get('suggestions')
            df.at[ind, 'keywords'] = ':,:'.join(theMovie.get('keywords', [])) if isinstance(theMovie.get('keywords'), list) else theMovie.get('keywords')
            df.at[ind, 'quotes'] = ':,:'.join(theMovie.get('quotes', [])) if isinstance(theMovie.get('quotes'), list) else theMovie.get('quotes')
            df.at[ind, 'imageUrl'] = theMovie.get('imageUrl')

            print(ind, df.loc[ind, 'title'], time.time()-start_time)
            
        except Exception as e:
            logger.warning(f"Getting movie details ({df.loc[ind+1, 'id']}: {df.loc[ind+1, 'title']}): {e}")
            missingMovies.warning(f"{df.loc[ind+1, 'id']}")
            

    df.to_parquet(f'data/top250{typ}.parquet')
    df.to_csv(f'data/top250{typ}.csv') # to show structure of the data


def suggestedMovies(unique_movies: set, filename: str = 'suggested'):
    '''Get suggested movies' details for specified movies'''

    suggested = pd.DataFrame(columns=[
        "id", "title", "releaseStatus", "type", "runtimeSeconds", "duration", "rating", "ratingCount", 
        "genres", "description", "releaseYear", "countriesOfOrigin", 
        "directors", "writers", "cast", "suggestionsID", "suggestionsTitle", "keywords", "quotes", "imageUrl"
    ])

    c = 0
    for movieID in unique_movies:
        c += 1
        print(filename, c, movieID, time.time()-start_time)
        try:
            movieID = movieID.strip()
            theMovie = movieDetail(movieID)
            new_row = pd.DataFrame([{
                "id": movieID,
                "title": theMovie.get('title'),
                "releaseStatus": theMovie.get('releaseStatus'), 
                "type": theMovie.get('type'),
                'releaseYear': theMovie.get('releaseYear'),
                "rating": theMovie.get('rating', None),
                "ratingCount": theMovie.get('ratingCount', None),
                "runtimeSeconds": theMovie.get('runtimeSeconds', 0),
                "duration": theMovie.get('duration', 0),
                "genres": ':,:'.join(theMovie.get('genres', [])) if isinstance(theMovie.get('genres'), list) else theMovie.get('genres'),
                "description": theMovie.get('description', None),
                "countriesOfOrigin": ':,:'.join(theMovie.get('countriesOfOrigin', [])) if isinstance(theMovie.get('countriesOfOrigin'), list) else theMovie.get('countriesOfOrigin', "Unknown"),
                "directors": ':,:'.join(theMovie.get('directors', [])) if isinstance(theMovie.get('directors'), list) else theMovie.get('directors'),
                "writers": ':,:'.join(theMovie.get('writers', [])) if isinstance(theMovie.get('writers'), list) else theMovie.get('writers'),
                "cast": ':,:'.join(theMovie.get('cast', [])) if isinstance(theMovie.get('cast'), list) else theMovie.get('cast'),
                "suggestionsID": ':,:'.join([sug[1] for sug in theMovie.get('suggestions', [])]) if isinstance(theMovie.get('suggestions'), list) else theMovie.get('suggestions'),
                "suggestionsTitle": ':,:'.join([sug[0] for sug in theMovie.get('suggestions', [])]) if isinstance(theMovie.get('suggestions'), list) else theMovie.get('suggestions'),
                "keywords": ':,:'.join(theMovie.get('keywords', [])) if isinstance(theMovie.get('keywords'), list) else theMovie.get('keywords'),
                "quotes": ':,:'.join(theMovie.get('quotes', [])) if isinstance(theMovie.get('quotes'), list) else theMovie.get('quotes'),
                "imageUrl": theMovie.get('imageUrl')
            }])
            suggested = pd.concat([suggested, new_row], ignore_index=True)

        except Exception as e:
            logger.warning(f"Getting movie details ({movieID}): {e}")
            missingMovies.warning(f"{movieID}")
        if c % 100 == 0:
            suggested.to_parquet(f'data/cache/{filename}_{c//100}.parquet')
    suggested.to_parquet(f'data/{filename}.parquet')
    for c in range(100, len(unique_movies)+100, 100):
        if os.path.exists(f'data/cache/{filename}_{c//100}.parquet'):
            os.remove(f'data/cache/{filename}_{c//100}.parquet')

    return '200'

def uniqueSuggestions(df: pd.DataFrame, excepts: set = set()) -> set:
    suggestions = df["suggestionsID"].str.split(':,:').dropna()
    unique_suggests = set([id for sublist in [lst for lst in suggestions] for id in sublist])
    return set(unique_suggests - excepts)


async def main(num_scrape: int = 5, level: str = '1'):

    movies = pd.read_parquet('data/movies.parquet')
    suggested = list(uniqueSuggestions(movies, set(movies['id'])))
    length = len(suggested)
    
    tasks = []
    for i in range(num_scrape):
        start_idx = i * (length // num_scrape)
        end_idx = (i + 1) * (length // num_scrape) if i != (num_scrape - 1) else length
        task = asyncio.to_thread(suggestedMovies, suggested[start_idx:end_idx], f'suggested_{level}_{i+1}')
        tasks.append(task)
    
    start = time.time()

    results = await asyncio.gather(*tasks)

    print(f"Time: {time.time()-start:.2f}\n{length} movies are scraped")
    frames = [pd.read_parquet(f'data/suggested_{level}_{i+1}.parquet') for i in range(num_scrape)]
    suggesteddf = pd.concat(frames)
    suggesteddf.to_parquet(f'data/suggested_{level}.parquet')
    for i in range(num_scrape):
        if os.path.exists(f'data/suggested_{level}_{i+1}.parquet'):
            os.remove(f'data/suggested_{level}_{i+1}.parquet')
    
    pd.concat([movies, suggesteddf]).to_parquet('data/movies.parquet')
    print("All done in {:.2f} seconds".format(time.time()-start_time))

async def top250both():
    res = await asyncio.gather(asyncio.to_thread(top250, 'movies'), asyncio.to_thread(top250, 'tvshows'))
    
if __name__ == "__main__":
    if len(sys.argv) < 2:
        asyncio.run(main())
    elif len(sys.argv) < 3 and sys.argv[1] == 'top250':
        asyncio.run(top250both())
    else:
        asyncio.run(main(int(sys.argv[1]), sys.argv[2]))
