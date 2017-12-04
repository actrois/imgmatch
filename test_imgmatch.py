import cv2
from .. import imgmatch

def test_duplicate():
	img1 = cv2.imread('test/just_donwloaded_file.jpg') 
	img2 = cv2.imread('test/selfie.jpg')
	assert imgmatch.is_duplicate(img1,img2) == True

def test_not_duplicate():
	img1 = cv2.imread('test/just_donwloaded_file.jpg') 
	img2 = cv2.imread('test/unrelated.jpg')
	assert imgmatch.is_duplicate(img1,img2) == False