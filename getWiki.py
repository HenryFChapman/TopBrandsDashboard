import wikipedia 
import pandas as pd

# -*- coding: utf-8 -*-
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

def getWiki():

	entities = pd.read_csv("entities.csv")

	summaries = []
	for i, row in entities.iterrows():

		print(row['EntityName'])

		try:
			ny = wikipedia.page(row['EntityName'])
			sentences = split_into_sentences(ny.summary)[0:3]

			tempSummary = " ".join(sentences)
			print(tempSummary)

		except Exception:
			tempSummary = "none found"
				
		summaries.append(tempSummary)

	entities['WikiDescrip'] = summaries

	entities.to_csv("newNewEntities.csv")

	print(wikipedia.summary("Wikipedia"))