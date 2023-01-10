#We need these imports for the script to work.
import requests
import json
import sys
import urllib
import pandas as pd
import re
import matplotlib.cm

def split_into_sentences(text):
	alphabets= "([A-Za-z])"
	prefixes = "(Mr|St|Mrs|Ms|Dr|Ing|h|c|F)[.]"
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

	totalVolume = volumeData['Universe'].sum()

	volumeData.to_csv("data/volume/" + name + ".csv")

	return totalVolume

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


def parseTopics(name, data):

	volumeData = pd.DataFrame()

	names = []
	scores = []
	posAppearances = []
	appearances = []
	colors = []

	cmap = matplotlib.cm.get_cmap('Greens')


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

	topicData = topicData.head(15)

	topicData.to_csv("data/topics/" + name + ".csv")


def parseLinks(name, data):



	#Handles Links
	links = []
	#edgeList = []
	for topic in data:

		for relatedTopics in topic["related_topics"]:

			tempNode = dict()
			tempNode['source'] = topic['key']
			tempNode['target'] = relatedTopics['key']

			tempList = []
			tempList.append(topic['key'])
			tempList.append(relatedTopics['key'])
			tempList.sort()

			#s = '-'.join(tempList)
			#edgeList.append(s)
			links.append(tempNode)

	linkDF = pd.DataFrame(links)
	linkDF = pd.concat([linkDF['source'], linkDF['target']]).to_frame()
	linkDF = linkDF.rename(columns={0:"id"}).value_counts().reset_index().rename(columns={0:"degree"})

	nodes = []
	for topic in data:
		tempNode = dict()
		tempNode['name'] = topic['topic']
		tempNode['id'] = topic['key']
		tempNode['score'] = topic['score']

		if "cluster_id" not in topic.keys():
			tempNode['cluster_id'] = -1
		else:
			tempNode['cluster_id'] = topic['cluster_id']

		nodes.append(tempNode)

		#loop through related nodes
		for relatedTopic in topic['related_topics']:
			tempNode = dict()
			tempNode['name'] = relatedTopic['name']
			tempNode['id'] = relatedTopic['key']
			tempNode['score'] = relatedTopic['score']

			if "cluster_id" not in topic.keys():
				tempNode['cluster_id'] = -1
			else:
				tempNode['cluster_id'] = topic['cluster_id']

			nodes.append(tempNode)

			nodeDF = pd.DataFrame(nodes)
			nodeDF = nodeDF.drop_duplicates(subset = 'id')
	
			#Merge in Degrees
			nodeDF = nodeDF.merge(linkDF, how='left', on='id')

			#Merge in Most Important Labels
	#Get Unique Cluster IDs
	clusterIDs = list(set(nodeDF['cluster_id'].tolist()))

	justClusterList = {}
	for clusterID in clusterIDs:
		justCluster = nodeDF[nodeDF['cluster_id']==clusterID]

		labelNum = 2

		justCluster = justCluster.sort_values(by=['degree'], ascending = False).head(labelNum)
		mostImportantLabels = '·'.join(justCluster['name'].tolist())

		topID = justCluster.head(1)['id'].tolist()[0]

		justClusterList.update({topID:mostImportantLabels})

	mainLabels = []
	for i, row in nodeDF.iterrows():
		if row['id'] in justClusterList.keys():
			mainLabels.append(justClusterList.get(row['id']))
		else:
			mainLabels.append("No")

	nodeDF['mainLabel'] = mainLabels
	nodeDF = nodeDF.sort_values(by=['degree'], ascending = True).fillna(0)
	nodes = nodeDF.to_dict('records')

	graphJSON = {}
	graphJSON.update({"nodes":nodes})
	graphJSON.update({"links":links})

	with open('data/networks/'+name+'.json', 'w') as fp:
		json.dump(graphJSON, fp)

def parseEmotions(name, data):
	emotionsData = pd.DataFrame()

	date = []

	totalDocuments = data[0]['documents']
	emotions = data[0]['emotions']

	for emotion in emotions:
		if emotion['name'] == 'trust':
			trust = emotion['documents']

	trustPercentage = trust/totalDocuments

	trustString = round(trustPercentage*100, 2)

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

	for i, row in entities.iterrows():
		print(row['EntityName'])
		query = createQuery(row['EntityCode'], "week")

		volumeData = getData(query, "volume", 50)
		totalVolume = parseVolume(row['EntityName'], volumeData)

		sentimentData = getData(query, "sentiment", 50)
		parseSentiment(row['EntityName'], sentimentData)

		query = createQuery(row['EntityCode'], "year")
		emotionData = getData(query, "emotions", 50)

		topicData = getData(query, "topics", 50)
		parseTopics(row['EntityName'], topicData)
		parseLinks(row['EntityName'], topicData)

		trustSentences.append(parseEmotions(row['EntityName'], emotionData)[0])
		totalDocuments.append(totalVolume)

		oneSentence.append(split_into_sentences(row['WikiDescrip'])[0])

	entities['oneSentence'] = oneSentence
	entities['trustMetric'] = trustSentences
	entities['totalDocuments'] = totalDocuments

	entities = entities.sort_values(by='trustMetric', ascending = False)

	entities['trustMetric'] = entities['trustMetric'].astype(str)+"%"

	entities['totalDocuments'] = entities['totalDocuments'].astype(int).map('{:,d}'.format)

	entities.to_csv("entities.csv")

main()


