from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars
# Create Flask Instance
app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
mongo = PyMongo(app, uri = "mongodb://localhost:27017/mars_app")
mars = mongo.db.mars_collection


#Create route to render html template from Mongo DB
@app.route("/")
def home():
    scrape_data = mars.find_one()
    #print(str(scrape_data["mars_table"]))
    return render_template("index.html", disp_data=scrape_data)

# Create scrape route
@app.route("/scrape")
def scraper():
    
    mars.drop()
    
    
    results = scrape_mars.scrape()
    
    mars.insert_one(results)

    return redirect("/", code=302)


if __name__ == "__main__":
    app.run(debug=True)