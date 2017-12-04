#!/usr/bin/python
import cv2
import sys
from os import listdir
from os.path import isfile, join
from math import sqrt

INF = 999999999
SUPPORTED_EXTENSIONS = [".png", ".jpg", ".jpeg", ".bmp", ".tiff"]
SIMILARITY_TRESHOLD = 1.8
TOP_MATCHES = 50
DISTANCE_TRESHOLD = 64
LOG_FLAG = False

def print_log(log, lv=0):
	if(LOG_FLAG):
		print (" "*lv)+">>"+log

def print_help():
	print "imgmatch is a tool to find duplicate images in a specified folder"
	print "usage: python imgmatch.py <your_folder>"

def print_err(err_code):
	if err_code == 1:
		print "No/wrong argument"
	elif err_code == 2:
		print "Error accessing specified folder"
	elif err_code == 3:
		print "Error reading image files in specified folder"
	else:
		print "Unknown Error"


def is_duplicate(img1, img2):
	similarity = compute_similarity(find_matches(img1, img2))
	print_log(str(similarity),1)
	# If similaryty value is less than certain treshold, the image is marked as duplicate
	return (similarity < SIMILARITY_TRESHOLD) 

def find_matches(img1, img2):
	orb = cv2.ORB_create()
	# find the keypoints and descriptors with SIFT
	kp1, des1 = orb.detectAndCompute(img1, None)
	kp2, des2 = orb.detectAndCompute(img2, None)

	# create BFMatcher object
	bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
	# Match descriptors.
	matches = bf.match(des1,des2)
	# Only select mathes with dostance less than DISTANCE_TRESHOLD
	matches = [m for m in matches if m.distance < DISTANCE_TRESHOLD]

	# Sort them in the order of their distance.
	matches = sorted(matches, key = lambda x:x.distance)
	# Only select top TOP_MATHCES points (if available)
	return matches[:min(TOP_MATCHES, len(matches))]

def compute_similarity(matches):
	# If the matches are too few, it's not likely to be duplicate
	if(len(matches) < TOP_MATCHES): 
		return INF

	# compute the norm of the distances
	norm_d = 0
	distances = []
	for m in matches:
		norm_d += m.distance**2

	return sqrt(norm_d)/TOP_MATCHES

def main(argv):
	try:
		if argv[0] == "--help":
			print_help()
			return
		else:
			mypath = argv[0]
			if(mypath[-1] != '/'):
				mypath += '/'
	except Exception:
		print_err(1)
		return

	try:
		files = [f for f in listdir(mypath) if isfile(join(mypath, f))]
	except OSError:
		print_err(2)
		return

	img_files = []
	img_filenames = []
	flag = []
	for f in files:
		for ext in SUPPORTED_EXTENSIONS:
			if ext in f:
				img_files.append(cv2.imread(join(mypath,f)))
				img_filenames.append(f)
				flag.append(False)

	for i in range(len(img_files)-1):
		if flag[i]: continue
		for j in range(i+1,len(img_files)):
			if flag[j]: continue
			print_log("comparing "+img_filenames[i]+" and "+img_filenames[j])
			if(is_duplicate(img_files[i], img_files[j])):
				flag[i] = True
				flag[j] = True
				print "   "+img_filenames[j]+" is a duplicate of "+img_filenames[i]

if __name__ == '__main__':
	if len(sys.argv) < 2:
		print_err(1)
	else:
		main(sys.argv[1:])