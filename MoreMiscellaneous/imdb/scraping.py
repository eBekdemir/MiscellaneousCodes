import requests
import pandas as pd
import json
from bs4 import BeautifulSoup as bs
import time
from html import unescape

'''
scraping from a list

türe göre filtreleme

seçilen filme göre öneriler
seçilen türe göre öneriler

seçilen filmin detayları

seçilen türe göre filmlerden alıntılar

seçilen türe göre film önerileri (movieRank a göre sıralı bir şekilde)



watchlist ve izlendi mekaniği ekle
kullanıcının oy vermesini sağla
kullanıcının izlediklerine ve oylarına göre öneri algoritması inşaa et
'''
start_time = time.time()

log_file = open('scraping_log.txt', 'a', encoding='utf-8')

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
    "Accept-Language": "en-US,en",
    "Accept-Encoding": "gzip, deflate, br, utf-8",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
}
session = requests.Session()

def movieDetail(movieTitle):
    try:
        movie_html = session.get('https://www.imdb.com/title/' + movieTitle, headers=headers)
        movie_soup = bs(movie_html.content, 'html.parser')
        next_script = movie_soup.find('script', {'id': '__NEXT_DATA__'})
        next_json = json.loads(next_script.text)
    except Exception as e:
        print(f'Error while getting movie page ({movieTitle}): \n\t{e}', flush=True, file=log_file)
        return None, None, None, None, None, None, None, None, None, None, None

    try:
        seconds = next_json['props']['pageProps']['aboveTheFoldData']['runtime']['seconds'] # .get('seconds') i didn't use that to see if it is not exist in log file
    except Exception as e:
        print(f'Error while getting seconds ({movieTitle}): \n\t{e}', flush=True, file=log_file)
        seconds = None

    try:
        release = next_json['props']['pageProps']['aboveTheFoldData']['releaseYear']['year'] # .get('year') i didn't use that to see if it is not exist in log file
    except Exception as e:
        print(f'Error while getting release year ({movieTitle}): \n\t{e}', flush=True, file=log_file)
        release = None

    try:
        countries = [country['text'] for country in next_json['props']['pageProps']['mainColumnData']['countriesOfOrigin']['countries']]
    except Exception as e:
        print(f'Error while getting countries ({movieTitle}): \n\t{e}', flush=True, file=log_file)
        countries = None

    try:
        directors = [director['name']['nameText']['text'] for directors in next_json['props']['pageProps']['aboveTheFoldData']['directorsPageTitle'] for director in directors['credits'] ]
    except Exception as e:
        print(f'Error while getting directors ({movieTitle}): \n\t{e}', flush=True, file=log_file)
        directors = None

    try:
        casts = [edge['node']['name']['nameText']['text'] for edge in next_json['props']['pageProps']['mainColumnData']['cast']['edges']]
    except Exception as e:
        print(f'Error while getting casts ({movieTitle}): \n\t{e}', flush=True, file=log_file)
        casts = None


    try:
        suggestions = [
            [edge['node']['titleText']['text'], edge['node']['id'], [genre['genre']['text'] for genre in edge['node']['titleGenres'].get('genres', [])]]
            for edge in next_json['props']['pageProps']['mainColumnData']['moreLikeThisTitles']['edges']
        ]
    except Exception as e:
        print(f'Error while getting suggestions ({movieTitle}): \n\t{e}', flush=True, file=log_file)
        suggestions = None
    
    try:
        keywords = [edge['node']['text'] for edge in next_json['props']['pageProps']['aboveTheFoldData']['keywords']['edges']]
    except Exception as e:
        print(f'Error while getting keywords ({movieTitle}): \n\t{e}', flush=True, file=log_file)
        keywords = None
    
    try:
        quotes = [quote['text'] for edge in next_json['props']['pageProps']['mainColumnData']['quotes']['edges'] for quote in edge['node']['lines']]        
    except Exception as e:
        print(f'Error while getting quotes ({movieTitle}): \n\t{e}', flush=True, file=log_file)
        quotes = None
    
    try:
        rating = next_json['props']['pageProps']['aboveTheFoldData']['ratingsSummary']['aggregateRating']
        rating_count = next_json['props']['pageProps']['aboveTheFoldData']['ratingsSummary']['voteCount']
    except Exception as e:
        print(f'Error while getting rating values ({movieTitle}): \n\t{e}', flush=True, file=log_file)
        rating = None
        rating_count = None
    
    try:
        description = next_json['props']['pageProps']['aboveTheFoldData']['plot']['plotText']['plainText']
    except Exception as e:
        print(f'Error while getting description ({movieTitle}): \n\t{e}', flush=True, file=log_file)
        description = None
    

    return seconds, release, countries, directors, casts, suggestions, keywords, quotes, rating, rating_count, description

def top250():
    """
    it creates a csv file with imdb top 250 movies
    the csv file includes those:
        ,id,name,rating,ratingCount,movieRank,genres,duration,seconds,description,releaseYear,countries,directors,casts,suggestions,keywords,quotes

    """
    try:
        url = "https://www.imdb.com/chart/top/"
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
                'name': item['item'].get('alternateName', item['item']['name']),
                'userRate':None,
                'rating': item['item']['aggregateRating']['ratingValue'],
                'ratingCount': item['item']['aggregateRating']['ratingCount'],
                'movieRank': 0,
                'genres': item['item']['genre'].split(', '),
                'duration': item['item']['duration'][2:],
                'seconds': None,
                'description': item['item']['description']
            }
            for item in jsn['itemListElement']
        ], index=range(1, 251))

    except Exception as e:
        print(f'Error while getting top 250: \n\t{e}', flush=True, file=log_file)
        return


    seconds = [None for _ in range(250)] 
    release = [None for _ in range(250)]
    countries = [None for _ in range(250)]
    directors = [None for _ in range(250)]
    casts = [None for _ in range(250)]
    suggestions = [None for _ in range(250)] 
    keywords = [None for _ in range(250)]
    quotes = [None for _ in range(250)]


    for ind in range(250):
        try:
            seconds[ind], release[ind], countries[ind], directors[ind], casts[ind], suggestions[ind], keywords[ind], quotes[ind], _, _, _ = movieDetail(df.loc[ind+1, 'id'])
            print(ind+1, df.loc[ind+1, 'name'], time.time()-start_time)
        except Exception as e:
            print(f"Error while getting movie details ({df.loc[ind+1, 'name']}): \n\t{e}", flush=True, file=log_file)


    df['seconds'] = seconds
    df['releaseYear'] = release
    df['countries'] = countries
    df['directors'] = directors
    df['casts'] = casts
    df['suggestions'] = suggestions
    df['keywords'] = keywords
    df['quotes'] = quotes
    
    suggested = pd.DataFrame(columns=[
    "id", "name", "userRate", "rating", "ratingCount", "movieRank", "genres", 
    "duration", "seconds", "description", "releaseYear", "countries", 
    "directors", "casts", "suggestions", "keywords", "quotes"
    ])

    for film_list in suggestions:
        if film_list == [None] or film_list == [] or film_list == None: continue
        for film in film_list:
            if not df['name'].isin([film[0]]).any() and not suggested['name'].isin([film[0]]).any():
                try:
                    print(film[0], time.time()-start_time)
                    seconds, release, countries, directors, casts, suggestions, keywords, quotes, rating, rating_count, description = movieDetail(film[1])
                    data = {
                        'id':film[1], "userRate":None, "name": film[0], "rating":rating, "ratingCount":rating_count, "movieRank":0, 
                        "genres":film[2], "duration":None, "seconds":seconds, "description":description, 
                        "releaseYear":release, "countries":countries, 
                        "directors":directors, "casts":casts, "suggestions":suggestions, "keywords":keywords, "quotes":quotes}
                    new_film = pd.DataFrame([data])
                    suggested = pd.concat([suggested, new_film], ignore_index=True)

                except Exception as e:
                    print(f'Error while getting and adding suggested movie details ({film}): \n\t{e}', flush=True, file=log_file)

    try:
        columns_to_unescape = ['name', 'description', 'suggestions', 'keywords', 'quotes', 'casts', 'directors']
        for column in columns_to_unescape:
            df[column] = df[column].astype(str).apply(unescape)
            suggested[column] = suggested[column].astype(str).apply(unescape)
    except Exception as e:
        print(f'Error while unescape html: \n\t{e}', flush=True, file=log_file)
        
    try:
        df.to_csv('top250_1.csv')
        suggested.to_csv('suggested_by250_1.csv')
    except Exception as e:
        print(f'Error while saving data to csv: \n\t{e}', flush=True, file=log_file)
    try:
        movies = pd.concat([df, suggested])
        movies = movies.set_index('id')
        movies.to_csv('movies_1.csv')
    except Exception as e:
        print(f'Error while saving data to movies: \n\t{e}', flush=True, file=log_file)
    print(f'\n\n{time.time()-start_time}\n')


def from_list(url):
    try:
        htmlurl = f"https://www.imdb.com/list/{url}/"
        htmll = session.get(url, headers=headers)
        soup = bs(htmll.content, 'lxml')
        script = soup.find('script', {'type':'application/ld+json'})
        jsn = json.loads(script.text)


    except Exception as e:
        print(f'Error while getting top 250: \n\t{e}', flush=True, file=log_file)
        return
    
    while True:
        try:
            next_script = soup.find('script', {'id': '__NEXT_DATA__'})
            next_json = json.loads(next_script.text)
            break
        except Exception as e:
            print(f'Error while getting next page: \n\t{e}', flush=True, file=log_file)
        
        
        if 
        df = pd.DataFrame(
        #     [
        #     {
        #         'id': item['item']['url'].split('/')[-2],
        #         'name': item['item'].get('alternateName', item['item']['name']),
        #         'userRate':None,
        #         'rating': item['item']['aggregateRating']['ratingValue'],
        #         'ratingCount': item['item']['aggregateRating']['ratingCount'],
        #         'movieRank': 0,
        #         'genres': item['item']['genre'].split(', '),
        #         'duration': item['item']['duration'][2:],
        #         'seconds': None,
        #         'description': item['item']['description']
        #     }
        #     for item in jsn['itemListElement']
        # ], index=range(1, 251)
        )
        
        
        
    
if __name__ == '__main__':
    # top250()
    from_list()

log_file.close()