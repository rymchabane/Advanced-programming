import cv2
import os
from pathlib import Path
from datetime import datetime
import time
from PIL import ImageGrab
from multiprocessing import Process

def camera(path):
    cam_path = os.path.join(path, 'camera')
    Path(cam_path).mkdir(parents=True, exist_ok=True)

    cam = cv2.VideoCapture(0)
    
    if not cam.isOpened():
      raise RuntimeError("Cannot open camera")
    else:
       timenow = datetime.now().strftime("%Y%m%d_%H%M%S")
       file = os.path.join(cam_path, f'{timenow}.mp4')
       width  = int(cam.get(cv2.CAP_PROP_FRAME_WIDTH))
       height = int(cam.get(cv2.CAP_PROP_FRAME_HEIGHT))
       output = cv2.VideoWriter(file, cv2.VideoWriter_fourcc(*'mp4v'), 30, (width, height))
       while True:
         ret, vid = cam.read()
         if not ret:
          raise RuntimeError("Cannot record video")
         output.write(vid)
         cv2.imshow("Recording (press ESC to stop)", vid)
         key = cv2.waitKey(1) 
         if key == 27:
           break
       output.release()
       cam.release()
       cv2.destroyAllWindows()

def screen_grabber(file_path):
   pic_path = os.path.join(file_path,'screenshots')
   Path(pic_path).mkdir(parents=True, exist_ok=True)
   for x in range(10):
      pic = ImageGrab.grab()
      timenow = datetime.now().strftime("%Y%m%d_%H%M%S")
      file = os.path.join(pic_path,f'{timenow}.jpg')
      pic.save(file)
      time.sleep(5)
      
def main():
  p1 = Process(target=camera, args=('C:\\Noor\\Desktop',)) 
  p2 = Process(target=screen_grabber, args=('C:\\Noor\\Desktop',))  

  p1.start()
  p2.start()
  
  p1.join()
  p1.join()

if __name__ == "__main__":
    main()