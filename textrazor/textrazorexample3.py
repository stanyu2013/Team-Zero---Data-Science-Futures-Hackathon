import textrazor

##use your own api key here!!
textrazor.api_key = "196b708e4921951a6b5fefff52c42a0ab2da06a2af304af8b96aa7ae"


client = textrazor.TextRazor(extractors=["entities", "topics"])
client.set_classifiers(["textrazor_newscodes"])
##response = client.analyze_url("http://www.bbc.co.uk/news/uk-politics-18640916")

##open a file to read and analyze
linestring = open('sample.txt', 'r').read()
linestring = linestring.decode('utf-8')
response = client.analyze(linestring)


##print topics
print '\ntopics: \n'
for topic in response.topics():
	if topic.score > 0.3:
		print topic.label, topic.score

##print categories
print '\ncategories: \n'
for category in response.categories():
	print category.category_id, category.label, category.score
		
##print entities
print '\nentities and scores: \n'
for entity in response.entities():
    print entity.id, entity.relevance_score, entity.confidence_score, entity.freebase_types