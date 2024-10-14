import Ahnytracker as AT
import cv2 as cv
import math
import numpy as np
import pycaw 
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
import pyautogui as pg
import screen_brightness_control as sbc
from vosk import Model, KaldiRecognizer
import pyaudio
    
#-----------GLOBAL PARAMETERS----------#
cap = cv.VideoCapture(0)
wCam, hCam = 640, 480
#index, middele finger, ring finger, pinky! :)
tipIds = [8, 12, 16, 20]
font = cv.FONT_HERSHEY_COMPLEX
fontScale = 1
text ='Select a mode'
textColor = (255,255,255)
detector = AT.handDetector()
# Initialize Vosk model
model = Model("vosk-model") 
recognizer = KaldiRecognizer(model, 16000)
# Prepare for audio input
p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=8192)
stream.start_stream()



#--------- VOLUME SECTION  -------------#
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = interface.QueryInterface(IAudioEndpointVolume)
#volume.GetMute()
#volume.GetMasterVolumeLevel()
volRange=volume.GetVolumeRange()
minVol = volRange[0]
maxVol= volRange[1]



#----GET THUMB AND INDEX FINGER LANDMARKS AND CONNECTIONS-----#
def gestureController(right_Hms):
    #thumb tip is 4, index tip is 8
    x1, y1 = right_Hms[4][1], right_Hms[4][2]
    x2, y2 = right_Hms[8][1], right_Hms[8][2]
    cv.circle(img, (x1,y1), 15, (0,255,0),2)
    cv.circle(img, (x2,y2), 15, (0,255,0),2)
    cv.line(img, (x1,y1),(x2,y2), (0,0,0), 3)
    #get center of the line
    cx, cy = int((x1+x2)//2), int((y1+y2)//2)
    cv.circle(img, (cx,cy), 15, (255,0,0),1)
    #find the length of the line. 
    length = math.hypot(x2-x1, y2-y1)
    return length
#----------------MODE FUNCTIONS-----------------#
def volAdjust(img,length):
         #convert length range to volume range using numpy
         vol = np.interp(length, [20, 230], [minVol, maxVol])
         volume.SetMasterVolumeLevel(vol, None)

         #create volume bar
         cv.rectangle(img, (20, 250), (70, 460), (0,0,0), 3)
         volbar = np.interp(length, [20, 230], [460, 250]) 
         if volbar > 355 : #getting pretty high
            cv.rectangle(img, (20, int(volbar)), (70, 460), (255,0,0), cv.FILLED)
         else:
             cv.rectangle(img, (20, int(volbar)), (70, 460), (0,0,150), cv.FILLED)

         volPercentage = np.interp(length, [20, 230], [0, 100])
         cv.putText(img, f'{int(volPercentage)}%', (20,240), font, 1, textColor, 3)

def snapShot(angle):
    if angle >340:
        pg.screenshot("screenshot.png")
        pic = cv.imread('screenshot.png')
        rez_img = cv.resize(pic, (200,200), interpolation=cv.INTER_CUBIC)
    
        h, w, c = rez_img.shape
        img[0:h, -w:] = rez_img

def setBrightness(length):
    brightness = np.interp(length, [20, 230], [0, 100])
    sbc.set_brightness(brightness)



while True:
    isTrue, img = cap.read()
    img=detector.detectHands(img, draw=False)
    left_Hms, right_Hms = detector.HandTracker(img, draw=False)

    mode =[]
    

    if left_Hms is not None:
        #-----SET MODES------#
        for id in range(0,4):
            if left_Hms[tipIds[id]][2]<left_Hms[tipIds[id]-2][2]:
                mode.append(1)
            else:
                mode.append(0)
        
    

    modeStamp = mode.count(1)
    if modeStamp == 1:
        #-----VOLUME SECTION-----#
        text = 'Volume Adjustment Mode'
        if right_Hms is not None:
            length=gestureController(right_Hms)
            volAdjust(img, length)
    elif modeStamp ==2:
        text = 'Brightness Adjustment Mode'
        if right_Hms is not None:
            length=gestureController(right_Hms)
            setBrightness(length)
    elif modeStamp ==3:
        text = 'Take a Screenshot!'
        if right_Hms is not None:
            angle=detector.findAngle(img,8,1,4)
            snapShot(angle)
    elif modeStamp==4:
        text='Recorder Mode'
        with open("spoken_words.txt", "a") as file:
            data = stream.read(4096, exception_on_overflow=False)
            if recognizer.AcceptWaveform(data):
                text = recognizer.Result()
                spoken_text=text[14:-3]
                file.write(spoken_text + "\n")
                file.flush()
                print(spoken_text)
    else:
        text ='Select a mode'
            
        
    cv.putText(img, text, (10,20), font, fontScale,textColor,3)
                    
    cv.imshow("Image", img)

    if cv.waitKey(20) & 0xFF==ord('d'):
        break


cap.release()
cv.destroyAllWindows()