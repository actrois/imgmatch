import numpy as np
import cv2
from matplotlib import pyplot as plt
from timeit import default_timer as timer
from math import sqrt

import numpy as np
import cv2

def drawMatches(img1, kp1, img2, kp2, matches):
    """
    My own implementation of cv2.drawMatches as OpenCV 2.4.9
    does not have this function available but it's supported in
    OpenCV 3.0.0

    This function takes in two images with their associated 
    keypoints, as well as a list of DMatch data structure (matches) 
    that contains which keypoints matched in which images.

    An image will be produced where a montage is shown with
    the first image followed by the second image beside it.

    Keypoints are delineated with circles, while lines are connected
    between matching keypoints.

    img1,img2 - Grayscale images
    kp1,kp2 - Detected list of keypoints through any of the OpenCV keypoint 
              detection algorithms
    matches - A list of matches of corresponding keypoints through any
              OpenCV keypoint matching algorithm
    """

    # Create a new output image that concatenates the two images together
    # (a.k.a) a montage
    rows1 = img1.shape[0]
    cols1 = img1.shape[1]
    rows2 = img2.shape[0]
    cols2 = img2.shape[1]

    # Create the output image
    # The rows of the output are the largest between the two images
    # and the columns are simply the sum of the two together
    # The intent is to make this a colour image, so make this 3 channels
    out = np.zeros((max([rows1,rows2]),cols1+cols2,3), dtype='uint8')

    # Place the first image to the left
    out[:rows1,:cols1] = np.dstack([img1, img1, img1])

    # Place the next image to the right of it
    out[:rows2,cols1:] = np.dstack([img2, img2, img2])

    # For each pair of points we have between both images
    # draw circles, then connect a line between them
    for mat in matches:

        # Get the matching keypoints for each of the images
        img1_idx = mat.queryIdx
        img2_idx = mat.trainIdx

        # x - columns
        # y - rows
        (x1,y1) = kp1[img1_idx].pt
        (x2,y2) = kp2[img2_idx].pt

        # Draw a small circle at both co-ordinates
        # radius 4
        # colour blue
        # thickness = 1
        cv2.circle(out, (int(x1),int(y1)), 4, (255, 0, 0), 1)   
        cv2.circle(out, (int(x2)+cols1,int(y2)), 4, (255, 0, 0), 1)

        # Draw a line in between the two points
        # thickness = 1
        # colour blue
        cv2.line(out, (int(x1),int(y1)), (int(x2)+cols1,int(y2)), (255,0,0), 1)


    # Show the image
    cv2.imshow('Matched Features', out)
    cv2.waitKey(0)
    cv2.destroyWindow('Matched Features')

    # Also return the image if you'd like a copy
    return out

def match_image(img1, img2):
	t = timer()
	orb = cv2.ORB_create()
	# find the keypoints and descriptors with SIFT
	kp1, des1 = orb.detectAndCompute(img1,None)
	kp2, des2 = orb.detectAndCompute(img2,None)
	# print "Keypoints found: img1: {}, img2: {} ({}s)".format(len(des1), len(des2), timer()-t)

	# create BFMatcher object
	bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
	# Match descriptors.
	matches = bf.match(des1,des2)
	print "Matches found: {} matches ({}s)".format(len(matches), timer()-t)

	# Sort them in the order of their distance.
	matches = sorted(matches, key = lambda x:x.distance)
	# print "Matches sorted ({}s)".format(timer()-t)

	avg_d = 0
	norm_d = 0
	distances = []
	for m in matches:
		avg_d += m.distance
		norm_d += m.distance**2
		distances.append(m.distance)
	avg_d /= len(matches)
	norm_d = sqrt(norm_d)

	print "Min dist: "+(str(matches[0].distance))
	print "Max dist: "+(str(matches[-1].distance))
	print "Average dist: "+str(avg_d)
	print "Norm dist: "+str(norm_d)

	# plt.plot(distances), plt.show()
	# Draw first 20 matches.
	img3 = drawMatches(img1,kp1,img2,kp2,matches[:20])
	plt.imshow(img3)
	# plt.show()
	cv2.imwrite("result.jpg", img3)
	return distances[:200]

print "Reading images..."
t = timer()
img1 = cv2.imread('test/meme_crop.jpg',0)
img2 = cv2.imread('test/meme.jpg',0)
# img3 = cv2.imread('test/unrelated.jpg',0)
# img4 = cv2.imread('test/meme_format.bmp',0)
# img5 = cv2.imread('test/meme_resize.jpg',0)
# img6 = cv2.imread('test/meme_rotate.jpg',0)
# img7 = cv2.imread('test/meme_filter.jpg',0)
print "Images read ({}s)\n".format(timer()-t)

print "1-2"
d1 = match_image(img1, img2)
# print "1-3"
# d2 = match_image(img1, img3)
# print "2-3"
# d3 = match_image(img2, img3)
# print "m-f"
# d4 = match_image(img2, img4)
# print "m-r"
# d5 = match_image(img2, img5)
# d6 = match_image(img2, img6)
# d7 = match_image(img2, img7)

# ix = np.arange(0,200)
# plt.plot(ix, d1, 'r', ix, d2, 'g', ix, d3, 'b', ix, d4, 'r', ix, d5, 'r', ix, d6, 'r', ix, d7, 'r')
# plt.show()
