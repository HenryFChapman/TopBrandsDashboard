#We need these imports for the script to work.
import requests
import json
import sys
import urllib
import pandas as pd
import matplotlib.cm
from splitSentences import split_into_sentences


def parseVolume(name, data):

	volumeData = pd.DataFrame()
	date = []
	posts_universe = []

	for point in data:
		date.append(point['date'])
		posts_universe.append(point['posts_universe'])

	volumeData['Date'] = date
	volumeData['Date'] = pd.to_datetime(volumeData['Date'])
	volumeData['Date'] = volumeData['Date'].dt.strftime('%b \'%y')

	volumeData['Universe'] = posts_universe
	volumeData['Universe'] = volumeData['Universe'].astype(int)

	totalVolume = volumeData['Universe'].sum()

	volumeDict = {} 
	volumeDict.update({'Date':volumeData['Date'].tolist()})
	volumeDict.update({'Universe':volumeData['Universe'].tolist()})

	return totalVolume, volumeDict

def parseSentiment(name, data):

	sentimentData = pd.DataFrame()
	date = []
	posts_universe = []

	for point in data:

		date.append(point['date'])
		posts_universe.append(point['net_sentiment'])

	sentimentData['Date'] = date
	sentimentData['Date'] = pd.to_datetime(sentimentData['Date'])
	sentimentData['Date'] = sentimentData['Date'].dt.strftime('%b \'%y')

	sentimentData['Net Sentiment'] = posts_universe

	sentimentData['Net Sentiment'] = sentimentData['Net Sentiment']*100

	sentimentData = sentimentData.round({'Net Sentiment': 3,})

	sentimentDict = {} 
	sentimentDict.update({'Date':sentimentData['Date'].tolist()})
	sentimentDict.update({'Net Sentiment':sentimentData['Net Sentiment'].tolist()})

	return sentimentDict


def parseTopics(name, data):

	volumeData = pd.DataFrame()

	names = []
	scores = []
	posAppearances = []
	appearances = []
	colors = []

	cmap = matplotlib.colors.LinearSegmentedColormap.from_list("", ["#ccff66", "#669900"])

	for topic in data:
		names.append(topic['name'])
		scores.append(topic['score'])
		posAppearances.append(topic['positive_documents'])
		appearances.append(topic['documents'])

		colors.append(matplotlib.colors.rgb2hex(cmap(topic['positive_documents'] / topic['documents'])))

	topicData = pd.DataFrame()
	topicData['Topic'] = names
	topicData['Score'] = scores
	topicData['positive_documents'] = posAppearances
	topicData['documents'] = appearances
	topicData['positive_percentage'] = topicData['positive_documents'] / topicData['documents']
	topicData['colors'] = colors

	topicData = topicData.sort_values(by = 'documents', ascending = False)
	topicData = topicData.head(10)

	topicData = topicData[['Topic', 'documents', 'colors']]

	topicDict = {} 
	topicDict.update({'Topic':topicData['Topic'].tolist()})
	topicDict.update({'documents':topicData['documents'].tolist()})
	topicDict.update({'colors':topicData['colors'].tolist()})

	return topicDict


def parseEmotions(name, data):
	emotionsData = pd.DataFrame()

	date = []
	totalDocuments = data[0]['documents']
	emotions = data[0]['emotions']

	for emotion in emotions:
		if emotion['name'] == 'trust':
			positiveDocuments = emotion['positive_documents']
			totalDocuments = emotion['documents']
			percentPositiveDocuments = positiveDocuments/totalDocuments

			trust = emotion['documents'] * percentPositiveDocuments

	return trust, totalDocuments


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
	url = "https://atlas-staging.infegy.com/api/v3/" + endpoint + "?api_key=" + key +  "&limit=" + str(limit) + "&q="+ query

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
    "max": 1672531199
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

	volume = {}
	sentiment = {}
	topics = {}

	entitiesHashMap = {}

	for i, row in entities.iterrows():
		print(row['EntityName'])
		query = createQuery(row['EntityCode'], "month")

		volumeQuery = getData(query, "volume", 50)
		totalVolume, volumeSeries = parseVolume(row['EntityName'], volumeQuery)
		volume.update({row['EntityName']:volumeSeries})

		sentimentQuery = getData(query, "sentiment", 50)
		sentiment.update({row['EntityName']:parseSentiment(row['EntityName'], sentimentQuery)})

		topicData = getData(query, "topics", 20)
		topics.update({row['EntityName']:parseTopics(row['EntityName'], topicData)})

		query = createQuery(row['EntityCode'], "year")
		emotionData = getData(query, "emotions", 50)

		tempEmotion = parseEmotions(row['EntityName'], emotionData)[0]
		tempEmotion = format(int(tempEmotion), ",")

		totalVolume = format(int(totalVolume), ",")

		trustSentences.append(tempEmotion)
		totalDocuments.append(totalVolume)
		oneSentence.append(split_into_sentences(row['WikiDescrip'])[0])

		tempDict = {}
		tempDict.update({"oneSentence":split_into_sentences(row['WikiDescrip'])[0]});
		tempDict.update({"totalDocuments": totalVolume});
		tempDict.update({"trustMetric": tempEmotion});
		tempDict.update({"WikiDescrip":row['WikiDescrip']});

		entitiesHashMap.update({row['EntityName']:tempDict})

	entities['oneSentence'] = oneSentence
	entities['trustMetric'] = trustSentences
	entities['totalDocuments'] = totalDocuments

	entities['trustMetricInt'] = entities['trustMetric'].str.replace(",", "").astype(int)


	entities = entities.sort_values(by='trustMetricInt', ascending = False)
	entities = entities[['EntityName', 'WikiDescrip', 'oneSentence', 'trustMetric', 'totalDocuments']]

	entities = entities.to_dict('records')

	bigJSON = {}
	bigJSON.update({"entities":entities})
	bigJSON.update({'entityHashMap':entitiesHashMap})
	bigJSON.update({"volume":volume})
	bigJSON.update({"sentiment":sentiment})
	bigJSON.update({"topics":topics})

	with open('siteData.json', 'w') as fp:
		json.dump(bigJSON, fp)

main()


