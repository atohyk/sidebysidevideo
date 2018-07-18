import cv2
import numpy as np

#[height,width,3]

def stitchCanvas(canvas, frame1,frame2,sideBorder,middleBorder):
	frame2 = cv2.resize(frame2, (frame1.shape[1],frame1.shape[0]))
	canvas[sideBorder:(sideBorder+frame1.shape[0]),\
		sideBorder:sideBorder+frame1.shape[1], :] = frame1
	canvas[sideBorder:sideBorder+frame1.shape[0],\
		sideBorder+frame1.shape[1]+middleBorder:sideBorder+frame1.shape[1]*2+middleBorder,\
		:] = frame2

def joinVideo(vidpath1, vidpath2, outpath, sideBorder = 0, middleBorder = 30, debug=False):
	#print frame1 size and frame2 size
	print(vidpath1)
	print(vidpath2)
	vid1 = cv2.VideoCapture(vidpath1)
	vid2 = cv2.VideoCapture(vidpath2)
	ret1, frame1 = vid1.read()
	ret2, frame2 = vid2.read()
	if ret1 == False or ret2 == False:
		print('Problem with opening videos')
		exit(1)
	print('Frame 1 Height:', frame1.shape[0])
	print('Frame 1 Width:', frame1.shape[1])
	print('Frame 2 Height:', frame2.shape[0])
	print('Frame 2 Width:', frame2.shape[1])

	if frame1.shape != frame2.shape:
		print('Vid 1 and Vid 2 do not have the same resolution, will change Vid 2 to match Vid 1') 

	canvasHeight = sideBorder * 2 + frame1.shape[0]
	canvasWidth = sideBorder * 3 + middleBorder + frame1.shape[1] * 2
	fourcc = cv2.VideoWriter_fourcc(*'XVID')
	outvid = cv2.VideoWriter(outpath, fourcc, vid1.get(cv2.CAP_PROP_FPS), (canvasWidth, canvasHeight))

	framecounter = 1

	#compute canvas, make the output video
	while ret1!=False and ret2!=False:
		canvas = np.zeros((canvasHeight, canvasWidth, 3), dtype = np.uint8)
		#resize frame2
		stitchCanvas(canvas, frame1, frame2, sideBorder, middleBorder)
		#print(canvas.shape)
		outvid.write(canvas)
		if debug:
			ratio = 1.0/max((canvasHeight/1080),(canvasWidth/1920))/1.5
			canvas = cv2.resize(canvas, (int(ratio*canvas.shape[1]), int(ratio*canvas.shape[0])))
		cv2.imshow('canvas',canvas)	
		cv2.waitKey(1)
		ret1, frame1 = vid1.read()
		ret2,frame2 = vid2.read()
		framecounter+=1

	vid1.release()
	vid2.release()
	outvid.release()
	return framecounter

if __name__ == '__main__':
	print('This file is not meant to be ran as main, call this file through videojoiner.')
	exit(0)