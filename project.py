import numpy as np
import pandas as pd
import pyfiglet
import webbrowser
import datetime

data = pd.read_csv("popular_10000_movies_tmdb.csv")

# This sets the id column as the primary index
data = data.set_index('id')

# This converts the release_date column items to pandas date object format
data['release_date'] = pd.to_datetime(data["release_date"])

# The data contains cn as the original_language column entry at many places, which means Chinese
# This converts cn to Chinese
data.loc[data["original_language"] == "cn", "original_language"] = "Chinese"


def convert_string_to_list(st):
    '''
    The lists in the genres and the production_companies columns are designed like lists, but actually are strings.
    This function converts the value into an actual list and returns it.
    '''
    st = st[1:-1]
    elements = st.split(",")
    res = []
    for each in elements:
        res.append(each.strip()[1:-1])
    return res


def fetch_by_title(name, dat=data.copy()):
    '''
    This function returns the results for queries based on the title of the movies.
    The default dataset is the primary one, but a subset can be used when required.
    '''
    res = dat.loc[data["title"].str.contains(name, case = False)].sort_values("popularity", ascending = False)
    if res.empty:
        return False
    else:
        return res


def fetch_by_genre(query, dat=data.copy()):
    '''
    Returns the result of a search query based on genres.
    By default, the dataset is the primary one, but in-case we require to search within a subset, we can do so
    by putting it as one of the parameters.
    '''
    res = dat
    for q in query:
        res = res.loc[res["genres"].str.contains(q, case = False)].sort_values("popularity", ascending = False)
    return res


def fetch_by_year(yr, dat=data.copy()):
    '''
    This function returns the search results based on the year the movies were published in from the
    specified dataset (primary dataset is the default one).
    '''
    res = dat.loc[dat["release_date"].dt.year == yr].sort_values("popularity", ascending = False)
    return res


def fetch_by_lang(lang, dat=data.copy()):
    '''
    This function returns the search results based on the language the movies were originally released in
    from the specified dataset (primary dataset is the default one).
    '''
    lang = lang.strip().lower().title()
    res = dat.loc[dat["original_language"] == lang].sort_values("popularity", ascending = False)
    return res


def frame_presenter(frame):
    '''
    This function is used by all search functions to present the obtained dataframe in a formatted manner,
    and also to conduct various operations like pagination.
    '''
    try:
        page = 0
        print()
        print("Total results:", len(frame))
        print()
        print("Search results:")
        print()
        while page < len(frame):
            num = 1
            curr = frame.iloc[page:page+6]
            for i, item in curr.iterrows():
                print(num, item["title"], end = " ")

                if str(item["tagline"]) != "nan":
                    print("-", item["tagline"])
                else:
                    print()

                print("Release year:", str(item["release_date"])[:4], end = "    ")
                genr_list = convert_string_to_list(item["genres"])
                genr = ""
                for i in genr_list:
                    genr = genr + i + ", "
                genr = genr.strip()[:-1]
                print("Genres:", genr)
                print()
                num += 1
                if num > 6:
                    break
            page += 6
            while True:
                try:
                    opt = int(input("Enter the choice or 0 to navigate to the next page: "))
                    print()
                    if opt == 0:
                        print("-"*50)
                        break
                    elif opt > 0 and opt < 7:
                        return curr[opt-1:opt]
                    else:
                        print("Enter a valid choice.")
                except:
                    print("Enter a valid choice.")
    except:
        return False


def search_by_name(d=data, t=True):
    '''
    This function searches the dataset for movies via their name/title.
    First a dataset is obtained using fetch_by_title function, then the results are printed.
    The user gets to choose an option from there.
    '''
    ser = input("Enter a name to search for: ")

    df = pd.DataFrame()
    df = fetch_by_title(ser, d)

    if t == True:
        return frame_presenter(df)
    else:
        return df


def search_by_genre(d=data, t=True):
    '''
    This function filters out movies based on the genres.
    It fetches the search results from the fetch_by_genre function.
    '''

    ent = []
    while True:
        try:
            ent = input("Enter the genres separated by a comma: ").strip().split(",")
            for n in range(len(ent)):
                ent[n] = ent[n].strip().title()
            break
        except:
            print("Please enter the genres in the valid format.")

    df = pd.DataFrame()
    df = fetch_by_genre(ent, d)

    if t == True:
        return frame_presenter(df)
    else:
        return df


def search_by_year(d=data, t=True):
    '''
    This function searches for movies filtered according to the year they were released in.
    It fetches the search data from the fetch_by_year function.
    '''
    while True:
        year = input("Enter a year: ")
        try:
            year = int(year)
        except:
            year = datetime.datetime.now().year
            print(f"The input wasn't valid. So the current year {year} was chosen.")
        break

    df = pd.DataFrame()
    df = fetch_by_year(year, d)

    if t == True:
        return frame_presenter(df)
    else:
        return df


def search_by_lang(d=data, t=True):
    '''
    This function searches for movies filtered according to the language they were originally released in.
    It fetches the search data from the fetch_by_lang function.
    '''
    while True:
        try:
            langu = input("Enter a language: ")
            break
        except:
            print("Enter a valid language.")

    df = pd.DataFrame()
    df = fetch_by_lang(langu, d)

    if t == True:
        return frame_presenter(df)
    else:
        return df


def adv_search():
    '''
    This function utilises all search functions together to serve even more filtered results.
    '''
    print()
    print("Please enter the following details in order to get advanced search results.")
    print("You can leave an entry empty if you don't have any specific idea of what to enter.")
    print()
    try:
        new_df = data.copy()
        new_df = search_by_name(new_df, False)
        new_df = search_by_genre(new_df, False)
        new_df = search_by_year(new_df, False)
        new_df = search_by_lang(new_df, False)
    except:
        print()
        print("No movies exist with the provided information in the dataset.")
        new_df = pd.DataFrame()

    return frame_presenter(new_df)



# the main function starts from here
def main():
    print(pyfiglet.figlet_format("        MoviPal"))
    print("Welcome to Movipal. Here you can search for popular movies.")

    while True:
        print()
        print("Following are the search categories:")
        print("1. By name              2. By genres")
        print("3. By release year      4. By language")
        print("5. Advanced Search")

        while True:
            try:
                ch = int(input("Enter your choice (number): "))
                if ch > 0 and ch < 6:
                    break
            except:
                print("Enter a valid choice.")

        resp = False
        if ch == 1:
            resp = search_by_name()
        elif ch == 2:
            resp = search_by_genre()
        elif ch == 3:
            resp = search_by_year()
        elif ch == 4:
            resp = search_by_lang()
        elif ch == 5:
            resp = adv_search()


        try:
            for index, stuff in resp.iterrows():
                print()
                print("Title:", stuff["title"], end = " ")

                if str(stuff["tagline"]) != "nan":
                    print("-", stuff["tagline"])
                else:
                    print()

                print("Release year:", str(stuff["release_date"])[:4], "    Original language:", stuff["original_language"])
                genres_list = convert_string_to_list(stuff["genres"])
                gen = ""
                for i in genres_list:
                    gen = gen + i + ", "
                gen = gen.strip()[:-1]
                print("Genres:", gen)
                print()
                print("Overview:", stuff["overview"])
                print()

                prod_list = convert_string_to_list(stuff["production_companies"])
                prod = ""
                for i in prod_list:
                    prod = prod + i + ", "
                prod = prod.strip()[:-1]
                print("Production companies:", prod)
                print()
                op = input("Open the movie page on The Movie Database? (y/n): ")
                if op == "y":
                    webbrowser.open(f"https://www.themoviedb.org/movie/{index}")
                print()
        except:
            print("Sorry! Couldn't find anything.")
            print()


        ask = input("Do you want to try again? (y/n): ").lower()
        if ask != "y":
            break

    print()
    print("Thanks for using MoviPal.")
    print("CS50P Final Project submission by Saurabh Suman.")
    print("The information is from The Movie Database (TMDB)")
    print("Downloaded from https://www.kaggle.com/datasets/ursmaheshj/top-10000-popular-movies-tmdb-05-2023")

if __name__ == "__main__":
    main()
