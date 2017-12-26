#!/usr/bin/python
import cv2
import sys
import getopt
import daemon
import lockfile
import signal
import os
from os.path import isfile, isdir, join
from math import sqrt
from time import sleep
import gi
gi.require_version('Notify', '0.7')
from gi.repository import Notify


INF = 999999999
SUPPORTED_EXTENSIONS = (".png", ".jpg", ".jpeg", ".bmp", ".tiff")
SIMILARITY_TRESHOLD = 1.8 	# Similarity value closer to zero means the images are more similar.
							# Lower treshold means the check will be more strict (i.e. only images 
							# that are very similar will be marked) and vice versa
TOP_MATCHES = 50
DISTANCE_TRESHOLD = 64
LOG_FLAG = False
BG_CHECK_TIMEOUT = 15
MESSAGE_TIMEOUT = 3
DAEMON_PID_FILE = '/tmp/imgmatch_daemon.pid'
DAEMON_LOCK_FILE = '/tmp/imgmatch_daemon.lock'

#
# Helper functions
#

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
	print "  -b <start or stop>  :  Start or stop background mode"
	print "                          when using -b option, imgmatch will run in "
	print "                          background watching a specified directory by "
	print "                          -d option. When duplicate image is found, "
	print "                          it will make a desktop notification."

def print_err(err_code):
	if err_code == 1:
		print "No/wrong argument. Use -h or --help for help"
	elif err_code == 2:
		print "Error accessing specified folder"
	elif err_code == 3:
		print "Error reading image files in specified folder"
	elif err_code == 4:
		print "Background service currently not running (PID file not found)"
	else:
		print "Unknown Error"

#
# Image processing functions
#

def find_matches(img1, img2):
	orb = cv2.ORB_create()
	# Find the keypoints and descriptors with ORB
	kp1, des1 = orb.detectAndCompute(img1, None)
	kp2, des2 = orb.detectAndCompute(img2, None)

	# Create BFMatcher object
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

	# Compute the norm of the distances
	norm_d = 0
	for m in matches:
		norm_d += m.distance**2

	return sqrt(norm_d)/TOP_MATCHES

def is_duplicate(img1, img2):
	similarity = compute_similarity(find_matches(img1, img2))
	print_log(str(similarity),2)
	# If similarity value is less than certain treshold, the image is marked as duplicate
	return (similarity < SIMILARITY_TRESHOLD) 

#
# Folder checking functions
#

def get_all_image_files(mypath, parent, recursive_flag):
	files = []
	print_log('path : ' + mypath)
	print_log(os.listdir(mypath))
	for f in os.listdir(mypath):
		cur_path = join(mypath, f)
		print_log('f : ' + f)
		print_log('path : ' + cur_path)

		if(isfile(cur_path)):
			if f.lower().endswith(SUPPORTED_EXTENSIONS):
				print_log('p : ' + str(parent))
				files.append(join(str(parent),f))
		
		elif recursive_flag and isdir(cur_path):
			files.extend(get_all_image_files(cur_path, join(parent,f), recursive_flag))

		print_log('')
		
	return files

def check_folder(mypath, is_recursive):
	# Find all images in the directory
	if(is_recursive):
		print_log('Finding images in directory recursively...')
	else:
		print_log('Finding images in directory...')
	try:
		img_filenames = get_all_image_files(mypath, '', is_recursive)
	except Exception as err:
		# print(err)
		print_err(2)
		return

	print_log(img_filenames)
	img_files = []
	duplicate_flag = []

	# Read the images
	try:
		for f in img_filenames:
			print_log(join(mypath,f))
			img_files.append(cv2.imread(join(mypath,f)))
			duplicate_flag.append(False)
	except Exception:
		print_err(3)
		return

	# Check for duplicates
	output = ""
	for i in range(len(img_files)-1):
		if duplicate_flag[i]: continue
		for j in range(i+1,len(img_files)):
			if duplicate_flag[j]: continue
			print_log("comparing "+img_filenames[i]+" and "+img_filenames[j])
			if(is_duplicate(img_files[i], img_files[j])):
				duplicate_flag[i] = True
				duplicate_flag[j] = True
				output += "   "+img_filenames[j]+" is a duplicate of "+img_filenames[i]+'\n'

	return output

#
# Daemon service functions
#

def get_pid():
	with open(DAEMON_PID_FILE, 'r') as tpid:
		pid = int(tpid.read())
	return pid

def is_service_running():
	if isfile(DAEMON_PID_FILE) == False:
		return False
	pid = get_pid()
	try:
		os.kill(pid, 0)
	except OSError:
		return False
	else:
		return True

def start_service(mypath, is_recursive):
	# Stop currently running service if exist
	if is_service_running():
		stop_service()

	# Create notify object
	Notify.init("imgmatch")
	notify = Notify.Notification()
	
	# Start new daemon
	with daemon.DaemonContext(
			working_directory=os.getcwd(),
			pidfile=lockfile.FileLock(DAEMON_LOCK_FILE)
		):
		print_log("Daemon hajimaru yo~")
		
		# Write pid to temp file
		with open(DAEMON_PID_FILE, 'w') as tpid:
			tpid.write(str(os.getpid()))
		
		# Run the service
		service(mypath, is_recursive, notify)

def stop_service():
	if is_service_running() == False	:
		print_err(4)
		return
	pid = get_pid()
	# Kill the daemon
	os.kill(pid, signal.SIGTERM)
	# Delete pid file
	os.remove(DAEMON_PID_FILE)

def service(mypath, is_recursive, notify):
	while True:
		output = check_folder(mypath, is_recursive)
		message = notify.new(output)
		message.show()
		sleep(MESSAGE_TIMEOUT)
		message.close()

		sleep(BG_CHECK_TIMEOUT)


#
# Main Function
#
def main(argv):
	global LOG_FLAG, SIMILARITY_TRESHOLD
	try:
		opts, args = getopt.getopt(argv, 'hlrs:d:b:', ['help', 'log', 'recursive', 'dir', 'background'])
	except getopt.GetoptError as err:
		print(err)
		print_help()
		return

	is_recursive = False
	is_background = False
	background = ""
	mypath = os.getcwd()
	for flag, value in opts:
		if flag == '-h' or flag == '--help':
			print_help()
			return
		if flag == '-l' or flag == '--log':
			LOG_FLAG = True
		if flag == '-r' or flag == '--recursive':
			is_recursive = True
		if flag == '-s':
			SIMILARITY_TRESHOLD = value
		if flag == '-d' or flag == '--dir':
			mypath = value
		if flag == '-b' or flag == '--background':
			is_background = True
			backround = value

	if is_background:
		if backround.lower() == 'start':
			print "Starting backround service to watch " + mypath + " for duplicate images..."
			start_service(mypath, is_recursive)
		elif backround == 'stop':
			print "Stopping backround service..."
			stop_service()
	else:
		print check_folder(mypath, is_recursive)

if __name__ == '__main__':
	if len(sys.argv) < 2:
		print_err(1)
	else:
		main(sys.argv[1:])