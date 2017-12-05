###############################################################
#
# This program will take a pathname of the dataset as the Input
# and extract text and metadata from all the files under the
# pathname and store it in a csv file.
#
# Usage: python extractText.py ./path/to/dataset
#
# Input: ./path/to/dataset
# Output: ./csv_output/extracted_text.csv
###############################################################

from __future__ import division
import sys, glob, fnmatch
import os, re, json, argparse
import shutil, random
from multiprocessing import Pool, cpu_count
from subprocess import Popen, PIPE
import speech_recognition as sr
import soundfile as sf
import datetime
import xmltodict

random.seed(1234)
reload(sys)
sys.setdefaultencoding('utf8')

START_DIR = './Test_Data'

DOC_EXT = ['.doc', '.docx', '.DOC', '.DOCX']
MISC_EXT = ['.csv', '.CSV', '.txt', '.TXT', '.xls', '.XLS', '.xlsx', '.XLSX', '.ppt', '.PPT', '.pptx', '.PPTX']
PDF_EXT = ['.pdf', '.PDF']
ALL_EXT = DOC_EXT + MISC_EXT + PDF_EXT
VID_EXT = ['.avi', '.AVI', '.mov', '.MOV', '.wmv', '.WMV', '.mp4', '.MP4', '.m4v', '.M4V']
NUM_WORDS = 20
CSV_FILE = 'csv_output/extracted_text.csv'
NUM_CPU_USE = cpu_count() - 2

text = ''
r = sr.Recognizer()
with sr.AudioFile("./wav_output/NETWORK.wav") as source:
    audio = r.record(source)

# text = r.recognize_sphinx(audio)
text = r.recognize_google(audio)

print(text)


