# -*- coding: utf-8 -*-
"""
Created on Sat Sep 12 13:51:16 2020

@author: eateren
jpg to ascii from: https://www.geeksforgeeks.org/converting-image-ascii-image-python/
mp4 to frames from: https://stackoverflow.com/questions/33311153/python-extracting-and-saving-video-frames

"""


from  PIL import Image, ImageDraw, ImageFont
import argparse
import cv2
import os
import glob
import numpy as np
import imageio


# gray scale level values from:  
# http://paulbourke.net/dataformats/asciiart/ 
  
# 70 levels of gray 
gscale1 = "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,\"^`'. "
  
# 10 levels of gray 
gscale2 = '@%#*+=-:. '

# set var
fPath = os.getcwd()
frameFolderPath = fPath + "\\frames\\"
frameAFolderPath = fPath + "\\asciiFrames\\"



def avgFPSgif(videoFilePath):
    """
    Returns the average framerate of a gif object
    """
    
    vidObj = Image.open(videoFilePath)
    
    vidObj.seek(0)
    frames = duration = 0
    while True:
        
        try:
            frames += 1
            
            # duration is the length of time one frame waits in gif
            duration += vidObj.info["duration"]
            
            vidObj.seek(vidObj.tell() + 1)
        
        except EOFError:
            return frames / duration * 1000
    
    return None



def avgFPSwebm(videoFilePath):
    """
    Returns the average framerate of an webm object
    """
    
    vidcap = cv2.VideoCapture(videoFilePath)
    fps = vidcap.get(cv2.CAP_PROP_FPS)
    return fps



def getAverageL(image): 
  
    """ 
    Given PIL Image, return average value of grayscale value 
    """
    
    # get image as numpy array 
    im = np.array(image) 
  
    # get shape 
    w,h = im.shape 
  
    # get average 
    return np.average(im.reshape(w*h)) 



def getImageRows(framePath, cols, scale):
    
    # open image and convert to grayscale 
    image = Image.open(framePath)
  
    # store dimensions 
    W, H = image.size[0], image.size[1] 
    print("input image dims: %d x %d" % (W, H)) 
  
    # compute width of tile 
    w = W/cols 
  
    # compute tile height based on aspect ratio and scale 
    h = w/scale 
  
    # compute number of rows 
    return int(H/h)


def covertImageToAscii(framePath, cols, rows, scale):
    """ 
    Given Image and dims (rows, cols) returns an m*n list of Images  
    """
    
    # declare globals 
    global gscale1, gscale2 
  
    # open image and convert to grayscale 
    image = Image.open(framePath).convert('L') 
  
    # store dimensions 
    W, H = image.size[0], image.size[1] 
    print("input image dims: %d x %d" % (W, H)) 
  
    # compute width of tile 
    w = W/cols 
  
    # compute tile height based on aspect ratio and scale 
    h = w/scale 
  
    # compute number of rows 
    rows = int(H/h)
  
    # ascii image is a list of character strings 
    aimg = [] 
    # generate list of dimensions 
    for j in range(rows): 
        y1 = int(j*h) 
        y2 = int((j+1)*h) 
  
        # correct last tile 
        if j == rows-1: 
            y2 = H
  
        # append an empty string 
        aimg.append("")
  
        for i in range(cols): 
  
            # crop image to tile 
            x1 = int(i*w)
            x2 = int((i+1)*w)
  
            # correct last tile 
            if i == cols-1: 
                x2 = W 
  
            # crop image to extract tile 
            img = image.crop((x1, y1, x2, y2)) 
  
            # get average luminance 
            avg = int(getAverageL(img)) 
  
            gsval = gscale2gi[-(int((avg*9)/255)+1)] 
  
            # append ascii char to string 
            aimg[j] += gsval 
      
    # return txt image 
    return aimg 



# generate image with ASCII art
def stringToImage(imgText, width, height, imgName):
    
	img = Image.new("L", (width, height))
	draw = ImageDraw.Draw(img)
	font = ImageFont.truetype("cour.ttf", 12)
	draw.multiline_text((0, 0), str(imgText), fill=(255), font=font, spacing=0, align="left")
	img.save(imgName)





#############################################################################
#############################################################################


### TODOS FOR NEXT TIME
    


"""
1    # check if image size is too small 
    if cols > W or rows > H: 
        print("Image too small for specified cols!") 
        exit(0) 

        
2 add more columns and more characters to increase visibility

3 dont process all frames, process the ones you need

4 optimize because this thing is slow
"""



# =============================================================================
# # main() function 
# def main():
# =============================================================================
    
# create parser 
descStr = "This program converts an image into ASCII art."
parser = argparse.ArgumentParser(description=descStr) 

# add expected arguments 
parser.add_argument('--file', dest='gifFile', required=True) 
parser.add_argument('--scale', dest='scale', required=False) 
parser.add_argument('--out', dest='outFile', required=False) 
parser.add_argument('--cols', dest='cols', required=False)
parser.add_argument('--fps', dest='fps', required=False)
parser.add_argument('--morelevels',dest='moreLevels',action='store_true') 
  
# parse args 
args = parser.parse_args() 
gifFile = args.gifFile 
videoFilePath = gifFile


# Takes gif/webm file and splits it to jpg frames
vidcap = cv2.VideoCapture(videoFilePath)
success,image = vidcap.read()

# empty out the frames folder
if success:
    files = glob.glob(frameFolderPath + "*")
    for f in files:
        os.remove(f)

# split video to frames
frameNo = 0
while success:
    
    frameNo += 1
    
    # saves frame
    cv2.imwrite(frameFolderPath + "frame%d.jpg" % frameNo, image)     
    
    success,image = vidcap.read()




# save all frames to ascii list
frameASCIIlist = []

# set scale default as 0.43 which suits 
# a Courier font 
scale = 0.7
if args.scale: 
    scale = float(args.scale) 
    
# set cols 
cols = 64
if args.cols: 
    cols = int(args.cols)
    
# set fps 
fps = 12
if args.fps: 
    fps = int(args.fps) 

# loop through frames in folder
frameList = os.listdir(frameFolderPath)
frmListCount = len(frameList)

# get rows
framePath = frameFolderPath + frameList[0]
rows = getImageRows(framePath, cols, scale)

# generate list of ASCII text
for x in range(1,frmListCount + 1):
    
    framePath = frameFolderPath + "frame" + str(x) + ".jpg"

    frameASCIIaimg = covertImageToAscii(framePath, cols, rows, scale)
    
    # take aimg and turn list into block of text
    frameASCII = ""
    for aimgLine in frameASCIIaimg:
        frameASCII += aimgLine
        frameASCII += "\n" if aimgLine != frameASCIIaimg[-1] else ""
        
    frameASCIIlist.append(frameASCII)



# turn ASCII frames back into image
width = cols * 7
height = int(7 / scale) * (rows + 2)

# empty out the frames folder
files = glob.glob(frameAFolderPath + "*")
for f in files:
    os.remove(f)

for frameANo, imgText in enumerate(frameASCIIlist):

    
    frameApath = frameAFolderPath + "frame%d.jpg" % frameANo
    
    stringToImage(imgText, width, height, frameApath)



# compile ASCII images to gif      
# find file type
gifExt = gifFile.split(".")[-1]

# get FPS
if gifExt == "gif":
    gifFPS = int(avgFPSgif(videoFilePath))
elif gifExt == "webm":
    gifFPS = int(avgFPSwebm(videoFilePath))
else:
    print("file not gif")
    exit()

frameCount = frameANo + 1
gifDur = frameCount / gifFPS
outFCount = int(fps * gifDur)

frameList = os.listdir(frameFolderPath)

with imageio.get_writer(fPath + "\\movie.gif", mode='I') as writer:
    for frame in range(1,outFCount):
        gifFrame = int(gifFPS/fps * frame)
        image = imageio.imread(frameAFolderPath + "frame%d.jpg" % gifFrame)
        writer.append_data(image)
        print("gif frame", frame)
writer.close()

            



# =============================================================================
# 
# # call main 
# if __name__ == '__main__': 
#     main() 
# =============================================================================
