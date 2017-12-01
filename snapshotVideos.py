import sys, glob, fnmatch
import os, re, json, argparse
import shutil, random
from subprocess import Popen, PIPE
import datetime

VID_EXT = ['.avi', '.AVI', '.mov', '.MOV', '.wmv', '.WMV', '.mp4', '.MP4', '.m4v', '.M4V']

if len(sys.argv) <= 1:
    print("Usage: python snapshotVideos.py <startPath>")
    sys.exit()

start_dir = sys.argv[1]
if not os.path.exists(start_dir):
    print(start_dir + " does not exist.")
    sys.exit()

vid_paths = []
for ext in VID_EXT:
    for root, dirnames, filenames in os.walk( start_dir ):
        for filename in fnmatch.filter(filenames, '*'+ext):
            vid_paths.append( os.path.join(root, filename))

home = os.path.expanduser("~")
snapshot_outdir = home + "/image-snapshots"
if not os.path.exists(snapshot_outdir):
    os.makedirs(snapshot_outdir)

#print(snapshot_outdir)
if len(vid_paths) > 0:
    for path in vid_paths:
	outdirname=snapshot_outdir + "/" + os.path.splitext(os.path.basename(path))[0]
        if os.path.exists(outdirname):
            print (path + " already processed; skipping")
        else:
            os.makedirs(outdirname)
            outpath = outdirname + "/image-%002d.png"
            cmd = ['ffmpeg', '-i', path, '-r', '0.05', '-vf', 'scale=800:-1', '-vcodec', 'png', outpath]
            print("Taking snapshots for " + path)
            proc = Popen(cmd, stdout=PIPE, stderr=PIPE, shell=False)
            stdoutdata, stderrdata = proc.communicate()
            print(stderrdata)
            print()

