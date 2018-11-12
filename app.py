from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

# Create Flask instance
app = Flask(__name__)


# Use flask_pymongo to establish Mongo connection
app.config['MONGO_URI'] = "mongodb://localhost:27017/mission_to_mars_app"
mongo = PyMongo(app)

# mongo = PyMongo(app, uri="mongodb://localhost:27017/mission_to_mars_app")


# Route to index.html, using data loaded from Mongo
@app.route("/")
def index():
	mars_news_from_mongo = mongo.db.mars_news.find_one()
	return render_template('index.html', mars_news_from_mongo=mars_news_from_mongo)


@app.route("/scrape")
def scraper():
	mars_news = mongo.db.mars_news

	####### to be finished: add try here
	mars_news_data = scrape_mars.scrape()

	####### to be finished: only update MongoDb data if mars_news_data get updated successfully
	mars_news.update({}, mars_news_data, upsert=True)
	return redirect("/", code=302)


if __name__ == "__main__":
	app.run(debug=True)

