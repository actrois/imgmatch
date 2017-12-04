import cv2
import imgmatch

def test_duplicate():
	img1 = cv2.imread('test_images/just_donwloaded_file.jpg') 
	img2 = cv2.imread('test_images/selfie.jpg')
	assert imgmatch.is_duplicate(img1,img2) == True

def test_not_duplicate():
	img1 = cv2.imread('test_images/just_donwloaded_file.jpg') 
	img2 = cv2.imread('test_images/unrelated.jpg')
	assert imgmatch.is_duplicate(img1,img2) == False