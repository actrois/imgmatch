#!/usr/bin/python
import cv2
import sys
import getopt
from os import listdir, getcwd
from os.path import isfile, isdir, join
from math import sqrt

INF = 999999999
SUPPORTED_EXTENSIONS = (".png", ".jpg", ".jpeg", ".bmp", ".tiff")
SIMILARITY_TRESHOLD = 1.8 	# Similarity value closer to zero means the images are more similar.
							# Lower treshold means the check will be more strict (i.e. only images 
							# that are very similar will be marked) and vice versa
TOP_MATCHES = 50
DISTANCE_TRESHOLD = 64
LOG_FLAG = False

def print_log(log, lv=1):
	if(LOG_FLAG):
		print (" "*lv)+">> "+str(log)

def print_help():
	print "imgmatch is a tool to find duplicate images in a specified folder"
	print "Usage example: python imgmatch.py -d <your_folder_path>"
	print "Arguments: "
	print "  -h, --help          :  Show help and exit"
	print "  -l, --log           :  Show log"
	print "  -d, --dir=<DIR>     :  The directory to search for duplicate images"
	print "                          default is current working directory"
	print "  -r, --recursive     :  Search image recursively in subdirectories"
	print "  -s <VALUE>          :  Similarity treshold to recognize duplicate images"
	print "                          default value is 1.8, lower treshold means the"
	print "                          check will be more strict (i.e. only images"
	print "                          that are very similar will be marked) and vice versa"

def print_err(err_code):
	if err_code == 1:
		print "No/wrong argument. Use -h or --help for help"
	elif err_code == 2:
		print "Error accessing specified folder"
	elif err_code == 3:
		print "Error reading image files in specified folder"
	else:
		print "Unknown Error"


def find_matches(img1, img2):
	orb = cv2.ORB_create()
	# find the keypoints and descriptors with ORB
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

def is_duplicate(img1, img2):
	similarity = compute_similarity(find_matches(img1, img2))
	print_log(str(similarity),1)
	# If similaryty value is less than certain treshold, the image is marked as duplicate
	return (similarity < SIMILARITY_TRESHOLD) 

def get_all_image_files(mypath, recursive_flag):
	files = []
	print_log(listdir(mypath))
	for f in listdir(mypath):
		cur_path = join(mypath, f)
		
		if(isfile(cur_path)):
			print_log(cur_path)
			if f.lower().endswith(SUPPORTED_EXTENSIONS):
				files.append(cur_path)
		
		elif recursive_flag and isdir(cur_path):
			files.extend(get_all_image_files(cur_path, True))
		
	return files


def main(argv):
	try:
		opts, args = getopt.getopt(argv, 'hlrs:d:', ['help', 'log', 'recursive', 'dir'])
	except getopt.GetoptError as err:
		# print help information and exit:
		print(err) # will print something like "option -a not recognized"
		print_help()
		return

	recursive = False
	mypath = getcwd()
	for flag, value in opts:
		if flag == '-h' or flag == '--help':
			print_help()
			return
		if flag == '-l' or flag == '--log':
			LOG_FLAG = True
		if flag == '-r' or flag == '--recursive':
			recursive = True
		if flag == '-s':
			SIMILARITY_TRESHOLD = value
		if flag == '-d' or flag == '--dir':
			mypath = value

	try:
		img_filenames = get_all_image_files(mypath, True)
	except OSError:
		print_err(2)
		return

	print_log(img_filenames)
	img_files = []
	duplicate_flag = []
	try:
		for f in img_filenames:
			img_files.append(cv2.imread(f))
			duplicate_flag.append(False)
	except Exception:
		print_err(3)
		return

	for i in range(len(img_files)-1):
		if duplicate_flag[i]: continue
		for j in range(i+1,len(img_files)):
			if duplicate_flag[j]: continue
			print_log("comparing "+img_filenames[i]+" and "+img_filenames[j])
			if(is_duplicate(img_files[i], img_files[j])):
				duplicate_flag[i] = True
				duplicate_flag[j] = True
				print "   "+img_filenames[j]+" is a duplicate of "+img_filenames[i]


if __name__ == '__main__':
	if len(sys.argv) < 2:
		print_err(1)
	else:
		main(sys.argv[1:])