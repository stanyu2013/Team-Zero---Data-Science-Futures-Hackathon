from elasticsearch import helpers, Elasticsearch
import csv

es = Elasticsearch(['http://52.247.174.154'],
    port=9200)

settings = {
    "settings": {
        "number_of_shards": 5,
        "number_of_replicas": 1
    },
    "videolabel": {
            "properties": {
                "Name": {
                    "type": "text"
                },
                "Path":{
                    "type":"text"
                },
                "Values": {
                    "type": "text"
                },
                "Label":{
                    "type":"text"
                },
                "Confidence":{
                    "type":"text"
                }
            }
     }
}

es.indices.create(index="madscientist", ignore=400, body=settings)

with open('video_recognition_fixed.csv') as f:
    reader = csv.DictReader(f)
    helpers.bulk(es, reader, index='madscientist', doc_type='videolabel')
