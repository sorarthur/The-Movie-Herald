# The Movie Herald
# Author: Arthur Clemente Machado (d0pp3lg4nger)
# Date: 15-01-2025
# Description: A simple script to get a random movie from a Letterboxd watchlist.
# Version: 1.0

# Importing libraries
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time
import random

# Selenium configuration
chrome_options = Options()
chrome_options.add_argument("--headless")
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

# Open the watchlist page
url = "https://letterboxd.com/d0pp3lg4nger/watchlist/"
driver.get(url)

# Wait for the page to load
time.sleep(5)

# Get the movies from the watchlist
movies = driver.find_elements(By.CLASS_NAME, 'poster-container')

movie_list = []
    
for movie in movies:
    try:  
        # Get the movie title
        title = movie.find_element(By.CLASS_NAME, 'react-component').get_attribute('data-film-name')
        
        # Get the movie link
        link = movie.find_element(By.CLASS_NAME, 'frame').get_attribute('href')
        
        # Get the movie image
        image_url = movie.find_element(By.CLASS_NAME, 'image').get_attribute('src')
        
        movie_list.append({
            'title': title,
            'link': link,
            'image_url': image_url
        })
    except Exception as e:
        print(f"Erro ao processar filme: {e}")
    
# Get a random movie from the list
random_movie = random.choice(movie_list)

print(f"Filme escolhido: {random_movie['title']}")

# if movie_list:
#     for filme in movie_list:
#         print(f"Título: {filme['title']}")
#         print(f"Link: {filme['link']}")
#         print(f"Imagem: {filme['image_url']}")
#         print("-" * 40)
# else:
#     print("Nenhum filme encontrado na watchlist.")


driver.quit()