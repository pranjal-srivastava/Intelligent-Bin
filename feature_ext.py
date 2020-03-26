import numpy as np
import cv2
from matplotlib import pyplot as plt
import threading
from threading import Thread
import os
from socket import *
#function
def smess(mess):
	host = "192.168.43.208" # set to IP address of target computer
	port = 13000
	addr = (host, port)
	#print mess
	UDPSock = socket(AF_INET, SOCK_DGRAM)
	#while True:
		#data = raw_input("Enter message to send or type 'exit': ")
	UDPSock.sendto(mess, addr)
	UDPSock.close()
	#os._exit(0)
def matchim(im1,im2,fimg,l):
	#img2 = cv2.imread('/home/jarvis/im2.jpg',0) # trainImage

	# Initiate SIFT detector
	sift = cv2.xfeatures2d.SIFT_create()

	# find the keypoints and descriptors with SIFT
	kp1, des1 = sift.detectAndCompute(im1,None)
	kp2, des2 = sift.detectAndCompute(im2,None)
	#print np.shape(kp1)
	# FLANN parameters
	FLANN_INDEX_KDTREE = 0
	index_params = dict(algorithm = FLANN_INDEX_KDTREE, trees = 5)
	search_params = dict(checks=50)   # or pass empty dictionary

	flann = cv2.FlannBasedMatcher(index_params,search_params)

	matches = flann.knnMatch(des1,des2,k=2)

	# Need to draw only good matches, so create a mask
	matchesMask = [[0,0] for i in xrange(len(matches))]
	if len(l)==0:
		l.append(0)
	else:
		l[0]=0
	# ratio test as per Lowe's paper
	for i,(m,n) in enumerate(matches):
	    if m.distance < 0.7*n.distance:
		matchesMask[i]=[1,0]
		l[0]=l[0]+1

	draw_params = dict(matchColor = (0,255,0),
			   singlePointColor = (255,0,0),
			   matchesMask = matchesMask,
			   flags = 0)
	#print len(matches)
	fimg = cv2.drawMatchesKnn(im1,kp1,im2,kp2,matches,None,**draw_params)
	cv2.imshow('res1',fimg)
	#return fimg,l
	# main code	
if __name__ == '__main__':
	cap = cv2.VideoCapture(0)
	threadlist=[]
	#cap.set(3,1280)
	#cap.set(4,720)
	img2 = cv2.imread('llogo.png',0)          # queryImage
	img3 = cv2.imread('/home/studio/flogo.png',0)
	img4 = cv2.imread('/home/studio/plogo1.png',0)
	fimg1 = np.zeros((50, 50, 3), np.uint8)
	fimg2 = np.zeros((50, 50, 3), np.uint8)
	fimg3 = np.zeros((50, 50, 3), np.uint8)
	l=[]
	p=[]
	f=[]
	message="null";
	while 1:
		ret, img1 = cap.read()
		if ret==1:
			t1=threading.Thread(target=matchim,args=(img1,img2,fimg1,l,))
			t2=threading.Thread(target=matchim,args=(img1,img3,fimg2,p,))
			t3=threading.Thread(target=matchim,args=(img1,img4,fimg3,f,))
			t4=threading.Thread(target=smess,args=(message,))
			t1.start()
			t2.start()
			t3.start()
			#fimg1,l=matchim(img2,img1)
			#fimg2,p=matchim(img3,img1)
			#fimg3,f=matchim(img4,img1)

			while t3.isAlive():
				continue
			while t2.isAlive():
				continue
			while t1.isAlive():
				continue
			cv2.imshow('res1',fimg1)
			cv2.imshow('res2',fimg2)
			cv2.imshow('res3',fimg3)
			cv2.waitKey(5)
			print l[0]
			print p[0]
			print f[0]

			message="null";

			if l[0]>5 :
				print "plastic"
				message="plastic"
				
				#plt.imshow(img3,),plt.show()
			if p[0]>5 :
				print "cardboard"
				message="cardboard"

			if f[0]>5 :
				print "cans"
				message="cans"
			if message!="null":
				t4.start()
			#	while t4.isAlive():
			#		print "sending"
			cv2.imshow('res1',fimg1)
			cv2.imshow('res2',fimg2)
			cv2.imshow('res3',fimg3)
			k = cv2.waitKey(5) & 0xFF
			if k == 27:
				break
	cv2.destroyAllWindows()
