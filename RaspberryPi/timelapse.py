#!/usr/bin/python

import time
import picamera
import os
import pyrebase
import re


config = {
    "apiKey": "AIzaSyD03IMGuSv8LLBKvStkOJJm6cath-yTbKg",
    "authDomain": "model-2.firebaseapp.com",
    "databaseURL": "https://model-2.firebaseio.com",
    "storageBucket": "model-2.appspot.com",
    
  }
firebase = pyrebase.initialize_app(config)
storage = firebase.storage()

picam = picamera.PiCamera()
#picam.resolution = (1024,768)
picam.resolution = (800,600)

os.chdir("/home/pi/VET4/Raspgarden")

try:
    while True:
      
     # for i in range(270):

      i = 0

      while True:
          hour = time.strftime('%H')
          if  re.match("..:00:2.",hour):
              break
          i =+1  
          picam.capture('real.jpg')
          storage.child("images/realTime.jpg").put("real.jpg")
          picam.capture('images/img{0:04d}.jpg'.format(i))
          time.sleep(300)  #each 5 min 



##########  MP4  o AVI    ####################

# Before using avconv we need install libav-tools



 #     nameVideo = time.strftime("%d") + time.strftime("%B")+".mp4"

      nameVideo = time.strftime('%H') + time.strftime("%A")+".mp4"
      namePicture = time.strftime('%H') + time.strftime("%A")+".jpg"

      print( time.strftime("%H") + time.strftime("%A"))

      os.system('avconv -r 10 -i images/img%04d.jpg -r 10 -vcodec libx264 -crf 20 -g 15 video/timelapse.mp4 ')

#os.system('avconv -r 10 -i img%04d.jpg -r 10 -vcodec libx264 -crf 20 -g 15 timelapse.avi ')

      os.rename("video/timelapse.mp4", "video/{}".format(nameVideo))

      storage.child("video/" + nameVideo).put("video/" + nameVideo)
      storage.child("images/" + namePicture).put("real.jpg")

      print('done')
      time.sleep(8)

except KeyboardInterrupt: # If there is a KeyboardInterrupt (when you press ctrl+c), exit the program and cleanup
      print("Finalized!")



