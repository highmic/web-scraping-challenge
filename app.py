from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mission_to_mars_app"
mongo = PyMongo(app)



@app.route("/")
def index():
    Mission_to_mars_dict = mongo.db.Mission_to_mars_dict.find_one()
    return render_template("index.html", Mission_to_mars_dict=Mission_to_mars_dict)


@app.route("/scrape")
def scraper():
    
    Mission_to_mars_dict= scrape_mars.scrape()
    mongo.db.Mission_to_mars_dict.update({}, Mission_to_mars_dict, upsert=True)
    return redirect("/", code=302)


if __name__ == "__main__":
    app.run(debug=True)
