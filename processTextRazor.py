import sys, glob, fnmatch
import os, re, json, argparse
import shutil, random
from subprocess import Popen, PIPE
import datetime
from pathlib import Path
import csv
import textrazor

if len(sys.argv) <= 1:
    print("Usage: python processTextRazor.py <startPath>")
    sys.exit()

start_dir = sys.argv[1]
if not os.path.exists(start_dir):
    print(start_dir + " does not exist.")
    sys.exit()

##use your own api key here!!
textrazor.api_key = "196b708e4921951a6b5fefff52c42a0ab2da06a2af304af8b96aa7ae"
client = textrazor.TextRazor(extractors=["entities", "topics"])
client.set_classifiers(["textrazor_newscodes"])

topicOut=open("./textrazor-out/topics.csv","w")
topicOut.write("Name, Topic Label, Score\n")

categoriesOut=open("./textrazor-out/categories.csv","w")
categoriesOut.write("Name, Category Id, Category label, Score\n")

#entitiesOut=open("./textrazor-out/entities.csv","w");
#entitiesOut.write("Name|Entity id|Relevance Score|Confidence Score|Freebase Types\n")

#for name in os.listdir(start_dir):
#    print(name)

pathlist = Path(start_dir).glob('*')
for path in pathlist:
    transcription_filename = str(path)
    print("Processing " + transcription_filename);
    basename = os.path.basename(transcription_filename)
    name = os.path.splitext(basename)[0]
    summary_csv_filename = "/home/ubuntu/image-snapshots-detect/" + name + "/recognition_summary.csv"
    text = ""
    if os.path.exists(summary_csv_filename):
        with open(summary_csv_filename, 'rb') as csvfile:
            reader = csv.reader(csvfile, delimiter=",")
            for row in reader:
                text = text + " " + row[3]
            csvfile.close()

    txtfile=open(transcription_filename)
    text = text + txtfile.read()
    txtfile.close()

    if len(text) > 0:
        text = text.decode('utf-8')
        try:
            response = client.analyze(text)

            ##print topics
            #print '\ntopics: \n'
            for topic in response.topics():
                if topic.score > 0.6:
                    topicOut.write(basename+", "+topic.label.encode('utf-8')+", "+str(topic.score)+"\n")

            ##print categories
            #print '\ncategories: \n'
            for category in response.categories():
                if category.score > 0.5:
                    categoriesOut.write(basename+", "+str(category.category_id)+", "+category.label.encode('utf-8')+", "+str(category.score)+"\n")

        except:
            print("Error occured for " + transcription_filename);

topicOut.close()
categoriesOut.close()
#entitiesOut.close()

