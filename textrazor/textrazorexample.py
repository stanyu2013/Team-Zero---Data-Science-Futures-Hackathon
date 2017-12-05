import textrazor

##use your own api key here!!
textrazor.api_key = "196b708e4921951a6b5fefff52c42a0ab2da06a2af304af8b96aa7ae"


client = textrazor.TextRazor(extractors=["entities", "topics"])
response = client.analyze_url("http://www.bbc.co.uk/news/uk-politics-18640916")

for entity in response.entities():
    print entity.id, entity.relevance_score, entity.confidence_score, entity.freebase_types