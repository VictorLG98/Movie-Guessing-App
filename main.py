from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from movie_scraping_2 import shot_cafe_scraping
from random import choice

app = FastAPI()

# Variables to store the current film information
attempts = 0
film_name = None
film_imgs = None

# Initialize the Jinja2 template engine
templates = Jinja2Templates(directory="templates/")

# Define the root endpoint
@app.get("/")
def read_form(request: Request):
    global attempts
    global film_name
    global film_imgs

    # Reset the attempts count
    attempts = 0

    # Choose a random film and its images
    while True:
        try:
            film_name, film_imgs = choice([shot_cafe_scraping()])
            break
        except:
            print("Error")
            
    # Render the template with the chosen film image and name
    return templates.TemplateResponse(
        "index.html",
        context={
            "request": request,
            "img": choice(film_imgs),
            "film_name": film_name,
        },
    )


# Define the endpoint for form submissions
@app.post("/submit/")
async def submit(request: Request, film_guess: str = Form(...)):
    global attempts
    global film_name
    global film_imgs

    # Strip whitespaces and convert the guess to lowercase
    film_guess = film_guess.strip().lower()

    # Check if the guess is correct
    if film_guess != film_name.lower():
        attempts += 1
        if attempts < 6:
            # If the guess is incorrect and the user has attempts left, render the template with an error message
            return templates.TemplateResponse(
                "index.html",
                context={
                    "request": request,
                    "incorrect_guess": "Incorrect!",
                    "img": choice(film_imgs),
                },
            )
        else:
            # If the guess is incorrect and the user has no attempts left, render the template with a "game over" message
            return templates.TemplateResponse(
                "index.html",
                context={
                    "request": request,
                    "incorrect_guess": f"You Lost! The film was: {film_name}",
                    "img": choice(film_imgs),
                    "desactiva": True,
                },
            )
    else:
        # If the guess is correct, render the template with a "correct" message
        return templates.TemplateResponse(
            "index.html",
            context={
                "request": request,
                "correct_guess": f"Correct!, the film was: {film_name}!",
                "img": choice(film_imgs),
                "desactiva": True,
            },
        )
