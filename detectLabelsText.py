import sys, glob, fnmatch
import os, re, json, argparse
import shutil, random
from subprocess import Popen, PIPE
import datetime
from pathlib import Path

if len(sys.argv) <= 1:
    print("Usage: python detectLabelsText.py <startPath>")
    sys.exit()

start_dir = sys.argv[1]
if not os.path.exists(start_dir):
    print(start_dir + " does not exist.")
    sys.exit()

#for name in os.listdir(start_dir):
#    print(name)

pathlist = Path(start_dir).glob('*')
for path in pathlist:
    name = str(path)
    if os.path.isdir(name):
        outlog = str(path) + "/detectlabels.log"
        cmd = ['java', '-jar', '/home/ubuntu/DetectLabels.jar', name]
        print("Processing " + str(path))
        proc = Popen(cmd, stdout=PIPE, stderr=PIPE, shell=False)
        stdoutdata, stderrdata = proc.communicate()
        logfile = open(outlog, "w")
        logfile.write(stdoutdata)
        logfile.write(stderrdata)
        logfile.close()

