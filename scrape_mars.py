from splinter import Browser
from bs4 import BeautifulSoup
import pandas as pd
import time

def init_brawser():
	# On my machine, chromedriver is installed using rvm
	# executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
	executable_path = {'executable_path': '/Users/c/.rvm/gems/ruby-2.5.1/bin/chromedriver'}
	# Create Browser instance
	return Browser('chrome', **executable_path, headless=False)


def grab_html(browser, url):
	browser.visit(url)
	time.sleep(2)
	html = browser.html
	return BeautifulSoup(html, 'html.parser').body


def scrape():
	### Scraping NASA Mars News
	browser = init_brawser()
	news_url = "https://mars.nasa.gov/news/"
	news_soup = grab_html(browser, news_url)

	news_container = news_soup.find('div', class_='image_and_description_container')
	news_date = news_container.find('div', class_='list_date').text
	news_title = news_container.find('div', class_='content_title').text.strip()
	news_p = news_container.find('div', class_='rollover_description_inner').text.strip()
	browser.quit()	


	### Scraping JPL Mars Space Images - Featured Images
	browser = init_brawser()
	img_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
	img_soup = grab_html(browser, img_url)

	# Get file name for the front image 
	img_style = img_soup.find('div', class_='carousel_items')
	img_style_orig = img_style.find('article')['style']
	img_file = img_style_orig.split(".")[0].split("/")[-1].split("-")[0]
	img_base_url = "https://www.jpl.nasa.gov/spaceimages/images/largesize/"
	featured_image_url = img_base_url + img_file + "_hires.jpg"
	browser.quit()	


	### Scraping Mars Most Recent Weather info
	browser = init_brawser()
	weather_url = 'https://twitter.com/marswxreport?lang=en'
	weather_soup = grab_html(browser, weather_url)
	mars_weather = weather_soup.find('p', class_="tweet-text").text.strip()
	browser.quit()	


	### Scraping Mars Facts, Put it into html table using panda
	# Read the data into a panda table
	browser = init_brawser()
	facts_url = 'http://space-facts.com/mars/'
	tables = pd.read_html(facts_url)

	# Put the data into Panda df
	df = tables[0]

	# Add column name
	df.columns = ['', 'Values']

	# Add index to the data frame
	df.set_index('', inplace=True)
	html_table = df.to_html(table_id=None).strip()
	html_table = html_table.replace('\n', '')
	# html_table = html_table.replace('<tr><th></th><th></th></tr>', '')
	browser.quit()	


	### Scraping Mars Hemispheres images
	# Visit each of the links from the url to get image links
	browser = init_brawser()
	hemi_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
	browser.visit(hemi_url)

	hemisphere_image_urls = []

	for i in range(4):
		# Find the elements on each loop to avoid a stale element exception
		hemi_link_item = browser.find_by_css("a.product-item h3")[i]

		# Find img title
		img_title = hemi_link_item.text

		# Click the link, find the sample anchor, return the href
		hemi_link_item.click()

		# Find the link to the full image
		hemi_html = browser.html
		hemi_soup = BeautifulSoup(hemi_html, 'lxml').body
		hemi_img_url = hemi_soup.find('div', class_="downloads").li.a['href']

		hemi_img_info = {'title': img_title, 'url': hemi_img_url}

		# Append image info to list
		hemisphere_image_urls.append(hemi_img_info)

		# Navigate back to previous page
		browser.back()


	browser.quit()	
	return {"publish_date": news_date,
					"title": news_title,
					"paragraph": news_p,
					"weather": mars_weather,
					"featured_image_url": featured_image_url,
					"html_table": html_table,
					"hemisphere_image_urls": hemisphere_image_urls
					}



print(scrape())



