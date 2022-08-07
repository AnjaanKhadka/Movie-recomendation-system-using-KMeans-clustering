
import requests
import pandas as pd
from bs4 import BeautifulSoup
import numpy as np
import os


pages_of_each_genre = 5
filename = 'Dataset_'+str(pages_of_each_genre)


def get_all_titles(soup):
    result_topics = []
    all_topics = soup.find_all('h3',{"class":"lister-item-header"})
    # print(all_topics)
    # exit(0)
    for topic in all_topics:
        topic = str(topic.find('a'))
        topic = topic.replace("<","=")
        topic = topic.replace(">","=")
        topic = topic.split('=')
        topic = topic[int(len(topic)/2)]
        result_topics.append(topic)
    # print(result_topics)
    return  result_topics


def get_all_genres(soup):
    result_genres = []
    all_genres = soup.find_all("p",{"class":"text-muted"})
    
    for genre in all_genres:
        genre = str(genre.find_all("span",{"class":"genre"}))
        if genre == '[]':
            pass
        else:
            # print("Got here")
            # genre = str(genre.find('a'))
            genre = genre.replace("<","=")
            genre = genre.replace(">","=")
            genre = genre.split('=')
            genre = genre[int(len(genre)/2)]
            result_genres.append(genre)
    # print(result_genres)
    return result_genres
    # exit(0)

def post_process(genres):
    post_process_genres = []
    for genre in genres:
        genre = genre.replace("\n","")
        genre = genre.replace(" ","")
        post_process_genres.append(genre)
    return post_process_genres
        
def check_repeated_comma(x):
    list_x = x.split(',')
    if len(list_x) == 3:
        return x
    else:
        # print("Got Here !!!!!!!!!!!!!!!!!!!!")
        return np.nan



def data_set(url):
    data_set =pd.DataFrame(columns=["Movie","Primary Genre", "Secondary Genre", "Tertiary Genre"])
    
    page = requests.get(url)
    
    soup = BeautifulSoup(page.content,'html.parser')
    
    
    title = get_all_titles(soup)
    genres = get_all_genres(soup)
    genres = post_process(genres)
    # print (genres)
    
    data_set["Movie"] = pd.Series(title)
    data_set["Primary Genre"] = pd.Series(genres)
    data_set["Primary Genre"] = data_set["Primary Genre"].apply(check_repeated_comma)
    data_set["Secondary Genre"] = data_set["Secondary Genre"].fillna('To Be Filled')
    data_set["Tertiary Genre"] = data_set["Tertiary Genre"].fillna('To Be Filled')
    
    data_set = data_set.loc[data_set["Primary Genre"] != np.NaN]
    data_set = data_set.dropna(how="any")
    # print(data_set)
    data_set[["Primary Genre", "Secondary Genre","Tertiary Genre"]] = data_set["Primary Genre"].str.split(',',expand=True)
    
    data_set.to_csv(f"{filename}.csv", mode='a', header=False, index= False)
    

def execute_one_by_one():
    os.system('cls')

    print("IMDB Scraper")
    number_of_pages =  int(input('Enter the number of various packages to scrap: '))
    for i in range(number_of_pages):
        url = input('Enter the url: ')
        data_set(url)
    
    
def remove_duplicate():
    df = pd.read_csv(f"{filename}.csv")
    df = df.drop_duplicates(keep = 'first')
    df.to_csv(f"{filename}_removed.csv",header = False, index = False)
    
def execute_one_genre(genere):
    for i in range(pages_of_each_genre):
        url = f"https://www.imdb.com/search/title/?title_type=feature&genres={genere}&start={i*50+1}&ref_=adv_nxt"
        data_set(url)

def execute_multiple_genre():
    genres = ['horror','action','adventure','comedy','fantasy','animation','sci-fi']
    for genre in genres:
        execute_one_genre(genre)
    
    
    
if __name__ == "__main__":
    # execute_multiple_genre()
    remove_duplicate()



