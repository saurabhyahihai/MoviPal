import pytest
import numpy as np
import pandas as pd

from project import convert_string_to_list, fetch_by_title, fetch_by_genre, fetch_by_year, fetch_by_lang

def test_convert_string_to_list():
    assert convert_string_to_list("['Comedy', 'Romance']") == ['Comedy', 'Romance']
    assert convert_string_to_list("['Drama']") == ['Drama']
    assert convert_string_to_list("['DC Films', 'Warner Bros. Pictures']") == ['DC Films', 'Warner Bros. Pictures']


def test_fetch_by_title():
    df1 = pd.DataFrame({'title': {604605: 'Hello World', 745376: 'Hello, Goodbye, and Everything in Between'}, 'release_date': {604605: '2019-09-20', 745376: '2022-07-06'}, 'genres': {604605: "['Animation', 'Romance', 'Science Fiction']", 745376: "['Romance', 'Drama']"}, 'original_language': {604605: 'Japanese', 745376: 'English'}, 'vote_average': {604605: 7.3, 745376: 6.3}, 'vote_count': {604605: 282, 745376: 184}, 'popularity': {604605: 23.936, 745376: 22.393}, 'overview': {604605: 'A shy high schooler in Kyoto meets a man claiming to be his future self, who tells him he’s hacked into the past to save their first love.',  745376: 'Clare and Aidan, after making a pact that they would break up before college, find themselves retracing the steps of their relationship on their last evening as a couple. The epic date leads them to familiar landmarks, unexpected places, and causes them to question whether high school love is meant to last.'}, 'budget': {604605: 0, 745376: 0}, 'production_companies': {604605: "['Graphinica']",  745376: "['ACE Entertainment']"}, 'revenue': {604605: 0, 745376: 0}, 'runtime': {604605: 98, 745376: 83}, 'tagline': {604605: 'This world is overturned in its last one second.',  745376: 'Every ending is a new beginning.'}})
    df1['release_date'] = pd.to_datetime(df1["release_date"])
    assert fetch_by_title("Hello").to_dict() == df1.to_dict()
    assert fetch_by_title("Nothing will be the result") == False


def test_fetch_by_genre():
    df2 = pd.DataFrame({'title': {}, 'release_date': {}, 'genres': {}, 'original_language': {}, 'vote_average': {}, 'vote_count': {}, 'popularity': {}, 'overview': {}, 'budget': {}, 'production_companies': {}, 'revenue': {}, 'runtime': {}, 'tagline': {}})
    assert fetch_by_genre("Nothing will be the result").to_dict() == df2.to_dict()

    df3 = pd.DataFrame({'title': {10253: 'Dragon Wars: D-War'}, 'release_date': {10253: '2007-08-01'}, 'genres': {10253: "['Fantasy', 'Drama', 'Horror', 'Action', 'Thriller', 'Science Fiction']"}, 'original_language': {10253: 'Korean'}, 'vote_average': {10253: 4.4}, 'vote_count': {10253: 342}, 'popularity': {10253: 14.345}, 'overview': {10253: 'Based on the Korean legend, unknown creatures will return and devastate the planet. Reporter Ethan Kendrick is called in to investigate the matter.'}, 'budget': {10253: 32000000}, 'production_companies': {10253: "['Younggu-Art Movies', 'Showbox']"}, 'revenue': {10253: 75108998}, 'runtime': {10253: 90}, 'tagline': {10253: "They've made our world their battleground."}})
    df3["release_date"] = pd.to_datetime(df3["release_date"])
    assert fetch_by_genre(['Action', 'Horror', 'Thriller', 'Drama', 'Fantasy']).to_dict() == df3.to_dict()


def test_fetch_by_year():
    df4 = pd.DataFrame({'title': {143: 'All Quiet on the Western Front'}, 'release_date': {143: '1930-04-29'}, 'genres': {143: "['Drama', 'War']"}, 'original_language': {143: 'English'}, 'vote_average': {143: 7.8}, 'vote_count': {143: 653}, 'popularity': {143: 18.622}, 'overview': {143: 'A young soldier faces profound disillusionment in the soul-destroying horror of World War I. Together with several other young German soldiers, he experiences the horrors of war, such evil of which he had not conceived of when signing up to fight. They eventually become sad, tormented, and confused of their purpose.'}, 'budget': {143: 1448864}, 'production_companies': {143: "['Universal Pictures']"}, 'revenue': {143: 3270000}, 'runtime': {143: 133}, 'tagline': {143: 'They left for war as boys never to return as men.'}})
    df4["release_date"] = pd.to_datetime(df4["release_date"])
    assert fetch_by_year(1930).to_dict() == df4.to_dict()

    df5 = pd.DataFrame({'title': {}, 'release_date': {}, 'genres': {}, 'original_language': {}, 'vote_average': {}, 'vote_count': {}, 'popularity': {}, 'overview': {}, 'budget': {}, 'production_companies': {}, 'revenue': {}, 'runtime': {}, 'tagline': {}})
    assert fetch_by_genre("1900").to_dict() == df5.to_dict()


def test_fetch_by_lang():
    assert len(fetch_by_lang("korean")) == 395

    df7 = pd.DataFrame({'title': {}, 'release_date': {}, 'genres': {}, 'original_language': {}, 'vote_average': {}, 'vote_count': {}, 'popularity': {}, 'overview': {}, 'budget': {}, 'production_companies': {}, 'revenue': {}, 'runtime': {}, 'tagline': {}})
    assert fetch_by_lang("no language").to_dict() == df7.to_dict()
