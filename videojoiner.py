import cv2
import canvasstitch as cs
import argparse
import os
import time

supportedformats = {'.mp4','.avi','.mjpg'}

if __name__ == "__main__":
	parser = argparse.ArgumentParser(description='Join 2 videos together on one canvas. \
		There must be exactly two videos in the folder if a folder is specified. \
		Both videos will use the resolution of the first video found.')
	parser.add_argument('-folder',dest='folderpath',action='store', \
		help='Path to folder containing 2 videos',default = '')
	parser.add_argument('-v1',dest='video1path',action='store', \
		help='Path to Video 1',default = '')
	parser.add_argument('-v2',dest='video2path',action='store', \
		help='Path to Video 2',default = '')
	parser.add_argument(dest='outputVideoPath',action='store', \
		help='Output Video path', default='')
	parser.add_argument('-sb',dest='sideBorder',action='store', \
		help='Thickness of side border in pixels',default=10)
	parser.add_argument('-mb',dest='middleBorder',action='store', \
		help='Thickness of the middle border in pixels',default=100)
	parser.add_argument('-d',dest='debug',action='store_true', \
		help='Enable debug')
	
	args = parser.parse_args()
	vidnames = []
	outpath = '.'
	
	#check if folder is specified 
	if len(args.folderpath) > 0:
		if os.path.exists(args.folderpath):
			#check if folder contains two videos 
			vidnames = os.listdir(args.folderpath)
			if len(vidnames) != 2:
				print('Folder does not contain exactly two files.')
				exit(1)
			vidnames=[os.path.join(args.folderpath,i) for i in vidnames]
		else:
			if os.path.isfile(args.video1path):
				vidnames[0] = args.video1path
			else:
				print(args.video1path,'is not a valid file.')
				exit(1)
			if os.path.isfile(args.video2path):
				vidnames[1] = args.video2path
			else:
				print(args.video2path,'is not a valid file.')
				exit(1)

	for vid in vidnames:
		if not vid[vid.rfind('.'):] in supportedformats:
			print('Filename', vid,'is not supported')
			exit(1)

	#check the output filepath
	if args.outputVideoPath.rfind('/') != -1 and not \
		os.path.isdir(args.outputVideoPath[:args.outputVideoPath.rfind('/')]):
		print(args.outputVideoPath[:args.outputVideoPath.rfind('/')], \
			'is not a valid directory.')
		exit(1)

	#check if outputpath is a directory
	if os.path.isdir(args.outputVideoPath):
		outpath = os.path.join(args.outputVideoPath, 'out.avi')
	else:
		outpath = args.outputVideoPath

	sideBorder = int(args.sideBorder)
	middleBorder = int(args.middleBorder)

	if sideBorder < 0:
		print('Side Border cannot be less than 0.')
		exit(1)
	if middleBorder < 0:
		print('Middle Border cannot be less than 0')
		exit(1)

	#all checks are complete, call joinvideo
	print('Joining ',vidnames[0], 'and', vidnames[1],'.')
	start_time = time.time()
	cs.joinVideo(vidnames[0], vidnames[1], outpath, sideBorder, middleBorder, args.debug)
	time_taken = (time.time() - start_time) * 1000
	print("Total Time Taken (ms): "+ str(time_taken)+"\n")
