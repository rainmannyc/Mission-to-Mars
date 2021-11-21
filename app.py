# Using Flask to render a template, redirecting to another url, and creating a URL
from flask import Flask, render_template, redirect, url_for

# Using PyMongo to interact with Mongo database
from flask_pymongo import PyMongo

# Using the scraping code we will convert from Jupyter notebook to Python
import scraping


app = Flask(__name__) # Use flask_pymongo to set up mongo connection

app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)

@app.route("/")
def index():
    mars = mongo.db.mars.find_one() # using PyMongo to find the "mars" collection in our database, which we will create when we convert our jupyter scraping code to Python Script. 
    return render_template("index.html", mars=mars) # return an HTML template using a file: index.html, mars=mars commands python to use mars collection in MongoDB

@app.route("/scrape") # defining the route for Flask
def scrape(): 
   mars = mongo.db.mars # assigning a new variable for Mongo database
   mars_data = scraping.scrape_all() # using the scrape_all() in the scraping.py file exported from Jupyter Notebook
   mars.update({}, mars_data, upsert=True) # after gathering the data, update database using .udpate() with {} as an empty JSON object for query parameters, as for the data: mars_data, and then upsert=True, indicates to MOngo to create a new document if one doesnt existn and saved
   return redirect('/', code=302) # redirect after successful scrape the data , navigate our page bafck to / where we can see the updated content

# Tell Flask to run:
if __name__ == "__main__":
   app.run()