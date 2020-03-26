import cython
from cython.parallel import prange, parallel
import numpy as np
import cv2
import threading
from threading import Thread
import os
from socket import *
import time
@cython.boundscheck(False)
def slope_cython_openmp(double [:, :] indata, double [:, :] outdata):
    cdef int I, J
    cdef int i, j, x
    cdef double k, slp, dzdx, dzdy
    I = outdata.shape[0]
    J = outdata.shape[1]
    with nogil, parallel(num_threads=4):
        for i in prange(I, schedule='dynamic'):
            for j in range(J):
                dzdx = (indata[i+1, j] - indata[i+1, j+2]) / 2
                dzdy = (indata[i, j+1] - indata[i+2, j+1]) / 2
                k = (dzdx * dzdx) + (dzdy * dzdy)
                slp = k**0.5 * 100
                outdata[i, j] = slp

def match_with_cascade(cascade,gray,objlist,n):

	    detected_obj = cascade.detectMultiScale(
		gray,
		scaleFactor=1.1,
		minNeighbors=n,
		minSize=(50, 50),
		#flags=cv2.cv.CV_HAAR_SCALE_IMAGE
	    )

	# add this
	    for (x,y,w,h) in detected_obj:
		cv2.rectangle(img,(x,y),(x+w,y+h),(255,255,0),2)
		objlist.append(1)


if __name__ == '__main__':
	message="null"
	threadlist=[]

	#this is the cascade we just made. Call what you want
	lays_cascade = cv2.CascadeClassifier('/home/pranjal/opencv/data/haarcascades/lays.xml')
	frooti_cascade = cv2.CascadeClassifier('/home/pranjal/opencv/data/haarcascades/frootin.xml')
	pepsi_cascade = cv2.CascadeClassifier('/home/pranjal/opencv/data/haarcascades/can.xml')
	cap = cv2.VideoCapture(0)
	#cap.set(3,1280)
	#cap.set(4,720)
	while 1:
	    ret, img = cap.read()
	    if ret ==1:
		l=[]
		f=[]
		p=[]
		gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
		t1=threading.Thread(target=match_with_cascade,args=(lays_cascade,gray,l,100,))
		t2=threading.Thread(target=match_with_cascade,args=(frooti_cascade,gray,f,150,))
		t3=threading.Thread(target=match_with_cascade,args=(pepsi_cascade,gray,p,150,))
		t4=threading.Thread(target=smess,args=(message,))
		t1.start()
		t2.start()
		t3.start()

		while t3.isAlive():
			continue
		while t2.isAlive():
			continue
		while t1.isAlive():
			continue
		message="null";

		if len(l)>0:
			print "plastic"
			message="plastic"
			#time.sleep(2)
			#plt.imshow(img3,),plt.show()
		if len(f)>0:
			print "cardboard"
			message="cardboard"
			#time.sleep(2)
		if len(p)>0:
			print "cans"
			message="cans"	
			#time.sleep(100)

		if message!="null":
			t4.start()
			#time.sleep(100)
			while t4.isAlive():
				print "sending"		

		cv2.imshow('img',img)
		k = cv2.waitKey(30) & 0xff
		if k == 27:
			break
		#t4.start()

	cap.release()
	cv2.destroyAllWindows()
