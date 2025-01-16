# The Movie Herald
# Author: Arthur Clemente Machado (d0pp3lg4nger)
# Date: 15-01-2025
# Description: A simple script to get a random movie from a Letterboxd watchlist.
# Version: 1.2

# Importing libraries
import random
import tkinter as tk
import sv_ttk as sv
import requests
from PIL import Image, ImageTk
from tkinter import ttk
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

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

# if movie_list:
#      for filme in movie_list:
#          print(f"Título: {filme['title']}")
#          print(f"Link: {filme['link']}")
#          print(f"Imagem: {filme['image_url']}")
#          print("-" * 40)
# else:
#      print("Nenhum filme encontrado na watchlist.")


driver.quit()

# GUI

# Create the main window
root = tk.Tk()
root.title("The Movie Herald")
root.geometry("800x600")
root.resizable(False, False)


# Title
title = tk.Label(root, text="The Movie Herald", font=("Arial", 24, "bold"), bg="#1a1a1a", fg="#ffffff")
title.pack(fill="x")

# Movie list
movie_list_frame = tk.Frame(root, bg="#1a1a1a")
movie_list_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

scrollbar = ttk.Scrollbar(movie_list_frame)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

movies_listbox = tk.Listbox(
    movie_list_frame, 
    bg="#1a1a1a", 
    fg="#ffffff", 
    font=("Arial", 12), 
    selectbackground="#1d4369",
    selectforeground="#ffffff",
    highlightthickness=0,
    activestyle="none",
    yscrollcommand=scrollbar.set
)

for movie in movie_list:
    movies_listbox.insert(tk.END, movie['title'])
movies_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

scrollbar.config(command=movies_listbox.yview)

main_frame = tk.Frame(root, bg="#1a1a1a")
main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

# Image frame
image_frame = tk.Label(main_frame, bg="#1a1a1a", text="Imagem do filme", fg="#ffffff", font=("Arial", 12))
image_frame.grid(row=0, column=0, rowspan=2, sticky="nw", padx=10, pady=10)

details_frame = tk.Frame(main_frame, bg="#1a1a1a")
details_frame.grid(row=0, column=1, sticky="nw", padx=10, pady=10)

movie_title_label = tk.Label(details_frame, text="Título: ", bg="#1a1a1a", fg="#ffffff", font=("Arial", 16, "bold"))
movie_title_label.pack(anchor="w")

movie_link_label = tk.Label(details_frame, text="Link: ", bg="#1a1a1a", fg="#ffffff", font=("Arial", 12))
movie_link_label.pack(anchor="w")

current_movie_link = ""

def display_movie_image(movie):
    global current_movie_link
    try:
        movie_title_label.config(text=f"Título: {movie['title']}")
        current_movie_link = movie['link'] 
        movie_link_label.config(text="Ver mais sobre o filme", fg="#29649e", cursor="hand2")
        
        response = requests.get(movie['image_url'], stream=True)
        response.raise_for_status
        
        img_data = Image.open(response.raw)
        img_data = img_data.resize((200, 200)) 
        img = ImageTk.PhotoImage(img_data)
        
        image_frame.config(image=img)
        image_frame.image = img
    
    except Exception as e:
        print(f"Erro ao carregar imagem: {e}")
        image_frame.config(text="Imagem não encontrada.", font=("Arial", 14), bg="#1a1a1a", fg="#ff0000")

# Open the movie link in the browser
def open_link(event):
    global current_movie_link
    if current_movie_link:
        import webbrowser
        webbrowser.open_new(current_movie_link)
    
# Go to the movie link when clicking the link label
movie_link_label.bind("<Button-1>", open_link)
# Funcion to chose a random movie
def choose_movie():
    if movie_list:
        selected_movie = random.choice(movie_list) 
        display_movie_image(selected_movie)
    else:
        image_frame.config(text="Imagem não encontrada.", font=("Arial", 14), bg="#1a1a1a", fg="#ff0000")
        image_frame.image = None

choose_button = ttk.Button(root, text="Sortear Filme", command=choose_movie)
choose_button.pack(pady=10)

# Button to close the app
exit_button = ttk.Button(root, text="Sair", command=root.destroy)
exit_button.pack(pady=10)

sv.set_theme("dark")
# Run the main loop
root.mainloop()
