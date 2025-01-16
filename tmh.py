# The Movie Herald
# Author: Arthur Clemente Machado (d0pp3lg4nger)
# Date: 15-01-2025
# Description: A simple script to get a random movie from a Letterboxd watchlist.
# Version: 1.1

# Importing libraries
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import random

# Selenium configuration
chrome_options = Options()
chrome_options.add_argument("--headless")
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

# Open the watchlist page
url = "https://letterboxd.com/d0pp3lg4nger/watchlist/"
driver.get(url)

# Wait for the page to load
WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'poster-container')))

# Get the movies from the watchlist
def get_movies():
    # Explicitly wait for the poster containers to be visible before proceeding
    WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'poster-container')))
    
    movies = driver.find_elements(By.CLASS_NAME, 'poster-container')

    movie_list = []
        
    for movie in movies:
        try:  
            # Get the movie title
            title_element = movie.find_element(By.CSS_SELECTOR, '[data-film-name]')
            title = title_element.get_attribute('data-film-name')
            
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
    
    return movie_list
    
# Get the movies from the first page
movie_list = get_movies()

# Loop through pages to get all movies
number_of_pages = 2
while True:
    try:
        # Check if there is a "Next" page button
        next_page_button = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//a[@href='/d0pp3lg4nger/watchlist/page/" + str(number_of_pages) + "/']"))
        )
        
        next_page_href = next_page_button.get_attribute('href')
        if not next_page_href:
            print("Nenhuma próxima página encontrada.")
            break        # If the next page button is found, click it
        next_page_button.click()
        
        # Wait for the page to load before getting movies again
        WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'poster-container')))
        
        # Get movies from the next page
        movie_list += get_movies()
        number_of_pages += 1
    except Exception as e:
        # Break the loop if no more pages are found
        print("Nenhuma próxima página encontrada ou erro ao carregar a próxima página.")
        break

# Get a random movie from the list
random_movie = random.choice(movie_list)

# Print the random movie
print("-" * 40)
print(f"Filme escolhido: {random_movie['title']}")
print(f"Link: {random_movie['link']}")
print(f"Imagem: {random_movie['image_url']}")
print("-" * 40)

# if movie_list:
#      for filme in movie_list:
#          print(f"Título: {filme['title']}")
#          print(f"Link: {filme['link']}")
#          print(f"Imagem: {filme['image_url']}")
#          print("-" * 40)
# else:
#      print("Nenhum filme encontrado na watchlist.")


driver.quit()