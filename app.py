from flask import Flask, render_template, request, redirect, url_for
from bs4 import BeautifulSoup
import requests, random


def rand_restaurants(city, state):
    restaurants = ["Cook your own dinner", "Bake something together", "It's not delivery, it's digiorno"]
    # requesting information on yelp depending on what city was inputed
    URL = 'https://www.yelp.com/search?find_desc=&find_loc=' + city + '%2C%20' + state
    page = requests.get(URL)
    # sorting html in page to just headings
    soup = BeautifulSoup(page.content, 'html.parser')
    rest_names = soup.find_all('a', class_='link__09f24__1MGLa link-color--inherit__09f24__3Cplm link-size--inherit__09f24__3Javq')
    # adding restaurant names into the restaurant list
    for rest_name in rest_names:
        for child in rest_name.descendants:
            restaurants.append("Go to " + child)
    return str(restaurants[random.randint(0, len(restaurants) - 1)]) + "!"

def rand_outdoor(city, state):
    outdoor = ["Go for a hike", "Throw a ball", "Skydiving would be fun", "Go on a bike ride", "Find a carnival", "Watch a concert", 
            "Watch an outdoor sporting event", "Stargaze until you see a shooting star", "Do a photoshoot", "Make a picnic",
            "Go horseback riding", "Take a hot air balloon ride", "Go fising", "Search for a bouquet of flowers", "Go roller blading"]

            
    URL = 'https://www.yelp.com/search?cflt=active&find_loc=' + city + '%2C ' + state
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, 'html.parser')
    rest_names = soup.find_all('a', class_='link__09f24__1MGLa link-color--inherit__09f24__3Cplm link-size--inherit__09f24__3Javq')
    for rest_name in rest_names:
        for child in rest_name.descendants:
            outdoor.append("Go to " + child)
    return str(outdoor[random.randint(0, len(outdoor) - 6)]) + "!"

def rand_indoor(city, state):
    indoor = ["Read a book at a bookstore", "Complete a puzzle", "Go to a bowling alley", "Watch a movie", "Visit an arcade",
            "Visit an art gallery","Go thrift shopping", "Play a board game", "Take dance lessons", "Go for some wine tasting", 
            "Escape an escape room", ]
    URL = 'https://www.yelp.com/search?find_desc=beauty%20%26%20spas&find_loc=' + city + '%2C ' + state
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, 'html.parser')
    rest_names = soup.find_all('a', class_='link__09f24__1MGLa link-color--inherit__09f24__3Cplm link-size--inherit__09f24__3Javq')
    for rest_name in rest_names:
        for child in rest_name.descendants:
            indoor.append("Go to " + child)
    return str(indoor[random.randint(0, len(indoor) - 6)]) + "!"

app = Flask(__name__)

@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        user_state = request.form['state']
        user_city = request.form['city']
        activities = []

        if len(user_state) == 0 or len(user_city) == 0:
            pick = "Input Error: Please enter a loacation"
            return render_template('index.html', pick = pick)
        
        if not request.form.get("restaurants") and not request.form.get("indoors") and not request.form.get("outdoors"):
            pick = "Input Error: Please check an option"
            return render_template('index.html', pick = pick)

        if request.form.get("restaurants"):
            activities.append("restaurants")
        if request.form.get("indoors"):
            activities.append("indoors")
        if request.form.get("outdoors"):
            activities.append("outdoors")

        choice = random.choice(activities)

        if choice == "restaurants":
            pick = rand_restaurants(user_city, user_state)
            return render_template('index.html', pick = pick)
        elif choice == "indoors":
            pick = rand_indoor(user_city, user_state)
            return render_template('index.html', pick = pick)
        elif choice == "outdoors":
            pick = rand_outdoor(user_city, user_state)
            return render_template('index.html', pick = pick)

    else:
        return render_template('index.html')

    return render_template('index.html')
    
if __name__ == "__main__":
    app.run(debug=True)