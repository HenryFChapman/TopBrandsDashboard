#We need these imports for the script to work.
import requests
import json
import sys
import urllib
import pandas as pd
import re

def split_into_sentences(text):
	alphabets= "([A-Za-z])"
	prefixes = "(Mr|St|Mrs|Ms|Dr)[.]"
	suffixes = "(Inc|Ltd|Jr|Sr|Co)"
	starters = "(Mr|Mrs|Ms|Dr|He\s|She\s|It\s|They\s|Their\s|Our\s|We\s|But\s|However\s|That\s|This\s|Wherever)"
	acronyms = "([A-Z][.][A-Z][.](?:[A-Z][.])?)"
	websites = "[.](com|net|org|io|gov)"
	digits = "([0-9])"

	text = " " + text + "  "
	text = text.replace("\n"," ")
	text = re.sub(prefixes,"\\1<prd>",text)
	text = re.sub(websites,"<prd>\\1",text)
	text = re.sub(digits + "[.]" + digits,"\\1<prd>\\2",text)
	if "..." in text: text = text.replace("...","<prd><prd><prd>")
	if "Ph.D" in text: text = text.replace("Ph.D.","Ph<prd>D<prd>")
	text = re.sub("\s" + alphabets + "[.] "," \\1<prd> ",text)
	text = re.sub(acronyms+" "+starters,"\\1<stop> \\2",text)
	text = re.sub(alphabets + "[.]" + alphabets + "[.]" + alphabets + "[.]","\\1<prd>\\2<prd>\\3<prd>",text)
	text = re.sub(alphabets + "[.]" + alphabets + "[.]","\\1<prd>\\2<prd>",text)
	text = re.sub(" "+suffixes+"[.] "+starters," \\1<stop> \\2",text)
	text = re.sub(" "+suffixes+"[.]"," \\1<prd>",text)
	text = re.sub(" " + alphabets + "[.]"," \\1<prd>",text)
	if "”" in text: text = text.replace(".”","”.")
	if "\"" in text: text = text.replace(".\"","\".")
	if "!" in text: text = text.replace("!\"","\"!")
	if "?" in text: text = text.replace("?\"","\"?")
	text = text.replace(".",".<stop>")
	text = text.replace("?","?<stop>")
	text = text.replace("!","!<stop>")
	text = text.replace("<prd>",".")
	sentences = text.split("<stop>")
	sentences = sentences[:-1]
	sentences = [s.strip() for s in sentences]
	return sentences



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


def parseEmotions(name, data):
	emotionsData = pd.DataFrame()

	date = []

	totalDocuments = data[0]['documents']
	emotions = data[0]['emotions']

	for emotion in emotions:
		if emotion['name'] == 'trust':
			trust = emotion['documents']

	trustPercentage = trust/totalDocuments

	trustString = str(round(trustPercentage*100, 2)) + "%"

	return trustString, totalDocuments


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
def createQuery(entityName, period):

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
  "group_by": period,
  "group_on": "published"
 }

	return query

def main():

	entities = pd.read_excel("entities.xlsx")


	oneSentence = []
	trustSentences = []
	totalDocuments = []

	for i, row in entities.iterrows():
		print(row['EntityName'])

		query = createQuery(row['EntityCode'], "week")

		#volumeData = getData(query, "volume", 50)
		#parseVolume(row['EntityName'], volumeData)

		#volumeData = getData(query, "sentiment", 50)
		#parseSentiment(row['EntityName'], volumeData)

		query = createQuery(row['EntityCode'], "year")
		emotionData = getData(query, "emotions", 50)
		trustSentences.append(parseEmotions(row['EntityName'], emotionData)[0])
		totalDocuments.append(parseEmotions(row['EntityName'], emotionData)[1])
		oneSentence.append(split_into_sentences(row['WikiDescrip'])[0])

	entities['oneSentence'] = oneSentence
	entities['trustMetric'] = trustSentences
	entities['totalDocuments'] = totalDocuments

	entities = entities.sort_values(by='trustMetric', ascending = False)

	entities.to_csv("entities.csv")

main()


