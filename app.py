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

	# add try to handle data scraping exception
	try:
		mars_data = scrape_mars.scrape()
	except Exception as e:
		mars_data = {}
		print("Scraping data failed with error: ", e)

	# only update the mongodb when there is data returned from scraping
	if (mars_data and mars_data["publish_date"] and 
			mars_data["title"] and mars_data["paragraph"] and 
			mars_data["weather"] and 
			mars_data["featured_image_url"] and 
			mars_data["html_table"] and 
			mars_data["hemisphere_image_urls"]):
		mars_news.update({}, mars_data, upsert=True)

	return redirect("/", code=302)


if __name__ == "__main__":
	app.run(debug=True)

