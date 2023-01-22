import requests
from random import randint, choice
from urllib.parse import urljoin
from scrapy import Selector
import re

def movie_scraping():
    years = [
        2000, 2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010,
        2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020
    ]

    params = {
        "year": choice(years),
        "page": randint(1, 5)
    }

    base_url = "https://www.moviestillsdb.com/"
    url = "https://www.moviestillsdb.com/movies"

    response = requests.get(url=url, params=params)
    data = Selector(response=response)

    movies_url = [urljoin(base_url, movie_url) for movie_url in data.css("td.title a ::attr(href)").getall()]

    url = choice(movies_url)
    response = requests.get(url=url)
    data = Selector(response=response)
    urls = re.findall(r'https[^"]*\.jpg', data.css("gallery").get())

    movie_images = [img.replace("\\", "") for img in urls if "500x" in img] 
    movie_title = data.css("a[itemprop=url] ::text").get()
    if len(movie_images) >= 5:
        print(response.url)
        return [movie_title, movie_images]
    movie_scraping()
    
def shot_cafe_scraping():
    
    genres = ["action", "adventure", "comedy", "crime", "drama", "family",
              "fantasy", "history", "horror", "lgtb", "mystery", "romance",
              "science fiction", "thriller", "war", "western"]
    
    base_url = "https://shot.cafe/"
    url = f"https://shot.cafe/genres/{choice(genres)}"
    response = requests.get(url=url)
    data = Selector(response=response)
    
    films = []
    for film in data.css(".project-list-item"):
        if int(film.css("span::text").get()) >= 5:
            films.append(urljoin(base_url, film.css("a::attr(href)").get()))
            
    chosen_film = choice(films)
    response = requests.get(url=chosen_film)
    data = Selector(response=response)
    
    film_title = data.css("h4 a ::text").get()
    film_images = data.css("img.box-img ::attr(src)").getall()
    final_images = []
    for img in film_images:
        final_images.append(urljoin(base_url, img.replace("/t/", "/o/")))
        
        
    return [film_title, final_images]
