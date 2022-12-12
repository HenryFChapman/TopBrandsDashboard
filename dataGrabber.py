#We need these imports for the script to work.
import requests
import json
import sys
import urllib
import pandas as pd

def parseVolume(name, data):

	volumeData = pd.DataFrame()
	date = []
	posts_universe = []

	for point in data:

		date.append(point['date'])
		posts_universe.append(point['posts_universe'])

	volumeData['Date'] = date
	volumeData['Universe'] = posts_universe

	volumeData.to_csv("data/volume/" + name + ".csv")

def parseSentiment(name, data):

	volumeData = pd.DataFrame()
	date = []
	posts_universe = []

	for point in data:

		date.append(point['date'])
		posts_universe.append(point['net_sentiment'])

	volumeData['Date'] = date
	volumeData['Net Sentiment'] = posts_universe

	volumeData.to_csv("data/sentiment/" + name + ".csv")


#Calling Function that Identifies a query + target endpoint and returns a dataframe
#Parameters:
#			query: A properly url encoded string in a format that Infegy Atlas understands. 
#			endpoint: The Infegy Atlas endpoint that you're looking for (eg. Ages, Volume, Entities, etc.)
#			limit: Number of results that you want in a query request. 
def getData(query, endpoint, limit):
	
	#This converts our query into a url_encoded string.
	query = urllib.parse.quote(str(json.dumps(query, indent = 4)))

	#This opens and loads the api.txt file that we created with your API key. 
    #We do this so you don't store your API key in the script.
	text_file = open("api.txt", "r")
	key = text_file.read()
	text_file.close()

	#Base URL. This allows us to pass in a different endpoint (e.g. volume, ages, entities, etc.) To look at all the entities, please reference our API documentation. 
	url = "https://atlas.infegy.com/api/v3/" + endpoint + "?api_key=" + key +  "&limit=" + str(limit) + "&q="+ query

	#The meat of the script. This line of code sends a request to Infegy with all  those parameters and gets the data back in a formatted json.
	data = requests.get(url).json()

	return data['output']


#This function properly formats a query for Infegy Atlas.
#Parameters:
#			queryText: A properly formatted boolean string. For example, if you want to query all posts that mention "Tesla", the query would be "tesla".
#			dateRange: A string saying from when you want data from. For example, if you want data from three months ago to the present, this value would be "3 months ago"
def createQuery(entityName):

	#Nested Query Dictionary
	query = {
  "query_fields": ["body","title"],
  "analyze_fields": ["body","title"],
  "query_builder": {
   "and_items": [{
     "type": "entity",
     "value": entityName
    }]
  },
  "filter": [{
    "id": "published",
    "min": 1640995200,
    "max": 1670889599
   }],
  "group_by": "week",
  "group_on": "published"
 }

	return query


#This function is the main() method
#Parameters:
#			queryText: A string of what you're searching for in Infegy Atlas
#			dateRange: from when you want data. For example, you can use "3 months ago" to get data from the past three months. 
def main():

	entities = pd.read_csv("entities.csv")

	for i, row in entities.iterrows():
		print(row['EntityName'])

		query = createQuery(row['EntityCode'])

		volumeData = getData(query, "volume", 50)
		parseVolume(row['EntityName'], volumeData)

		volumeData = getData(query, "sentiment", 50)
		parseSentiment(row['EntityName'], volumeData)

main()


