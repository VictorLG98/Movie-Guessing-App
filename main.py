from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from movie_scraping_2 import shot_cafe_scraping, movie_scraping
from random import choice

app = FastAPI()
INTENTOS = None
FILM_NAME = None
FILM_IMGS = None
templates = Jinja2Templates(directory="templates/")

@app.get('/')
def read_form(request: Request):
    global INTENTOS
    INTENTOS = 0
    global FILM_NAME
    global FILM_IMGS
    while True:
        try:
            FILM_NAME, FILM_IMGS  = choice([shot_cafe_scraping()])
            break
        except:
            print("Error")
    return templates.TemplateResponse('index.html', context={"request": request, 'img': choice(FILM_IMGS),
                                                             'film_name': FILM_NAME})

@app.post("/submit/")
async def submit(request: Request, film_guess: str = Form(...)):
    global INTENTOS
    global FILM_NAME
    global FILM_IMGS
    
    film_guess = film_guess.strip().lower()
    if film_guess != FILM_NAME.lower():
        INTENTOS += 1
        if INTENTOS < 6:
            return templates.TemplateResponse('index.html', context={"request": request, 'incorrect_guess': "Incorrecto!",
                                                                    "img": choice(FILM_IMGS)})
        return templates.TemplateResponse('index.html', context={"request": request, 'incorrect_guess': f"Has perdido! La película era: {FILM_NAME}",
                                                                    "img": choice(FILM_IMGS), "desactiva": True})
        
    return templates.TemplateResponse('index.html', context={"request": request, 
                                                             'correct_guess': f"Correcto, la película era: {FILM_NAME}!",
                                                             "img": choice(FILM_IMGS), "desactiva": True})
    
