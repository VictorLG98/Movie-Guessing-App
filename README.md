# Movie-Guessing-App

This script uses the FastAPI framework to create a web application. When a user navigates to the root URL ("/"), the script will randomly choose a film from a list obtained by the function **shot_cafe_scraping()** and display an image of the film along with a form for the user to guess the name of the film. If the user submits a guess, the script will check if it is correct and increment a counter if it is not. If the user has not guessed the correct film after 6 incorrect attempts, the script will display a message saying that the user has lost and reveal the name of the correct film. Otherwise, the script will display a message saying that the user has guessed the correct film. You can also start a new game whenever you want.

Page: <a href="https://7tthsj.deta.dev/" target="_blank">page</a>
