import urllib		# fetches raw web pages for us
import bs4		# turns raw web pages into object hierarchy and provides selectors (like CSS and Xpath does)
import csv		# simplifies the process of writing data to Comma Separated Values in a file
from urlparse import urlparse

# a list of URLs that we want to scrape data from
pagesToScrape = [
	'https://www.landvest.com/properties_for_sale/advanced_search/view//Forsale/1/SearchClass/timberland/count/12',
	'https://www.landvest.com/properties_for_sale/advanced_search/Forsale/1/SearchClass/timberland/NoMLS/PS/orderby/acres/descending/offset/12/count/12',
	'https://www.landvest.com/properties_for_sale/advanced_search/Forsale/1/SearchClass/timberland/NoMLS/PS/orderby/acres/descending/offset/24/count/12'
]

# open a file in append mode to write into in the same directory where we ran this script from
csvfile = open('propertydata.csv', 'w')
csvwriter = csv.writer(csvfile, delimiter=',')


property_arr = [['Name', 'State', 'Amount', 'Acreage', 'REF#', 'Website']]

# loop over our list of URL's one at a time
for URL in pagesToScrape:

	webpage = urllib.urlopen(URL)			# fetch webpage
	soup = bs4.BeautifulSoup(webpage, "html.parser")		# make an object from the HTML

	parsed_uri = urlparse(URL)
	hosturl = '{uri.scheme}://{uri.netloc}/'.format(uri=parsed_uri)

	# extract info from soup
	properties = soup.find_all('li', {'class':'standard-property'})

	for prop in properties:
		title = prop.find('h4', {'class': 'property-name'})
		name = title.a.text.strip()
		
		info = prop.find('div', {'class': 'property-info'})
		infos = info.find_all('div', {'class': 'info-row'})

		state = infos[0].text.encode('utf-8').strip() + infos[1].text.encode('utf-8').strip()
		amount = infos[2].text.encode('utf-8').strip()
		acres = infos[3].text.encode('utf-8').strip()
		ref = infos[4].text.encode('utf-8').strip()
		website = hosturl + title.a.get('href')

		property_arr.append([
			name,
			state,
			amount,
			acres,
			ref,
			website
		])

# for prop in property_arr:
csvwriter.writerows(property_arr)		# write a row in the file
