import cv2 as cv
import mediapipe as mp
import math


class handDetector():
    def __init__(self, mode=False, maxHands=2, detectionCon=0.5, trackCon=0.5): #these parameters were from the initial built in Hands mediapipe module
        self.mode = mode
        self.maxHands = maxHands
        self.detectionCon = detectionCon
        self.trackCon = trackCon
        #initialize Hands class
        self.mpHands= mp.solutions.hands
        #to detect hand
        self.hands = self.mpHands.Hands(static_image_mode=self.mode,
                                        max_num_hands=self.maxHands,
                                        min_detection_confidence=self.detectionCon,
                                        min_tracking_confidence=self.trackCon)
        #to draw landmarks on hand
        self.mpDraw = mp.solutions.drawing_utils

    def detectHands(self,frame, draw=True):
        # Flip the frame horizontally for a mirror view
        frame = cv.flip(frame, 1)
        # Convert the frame to RGB
        rgb_frame = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
        # Process the frame for hand landmarks
        self.results = self.hands.process(rgb_frame)

        if self.results.multi_hand_landmarks:
        #for each hand detected
            for HandLms in self.results.multi_hand_landmarks:
                if draw:
                #draw the connections of landmarks on the hand
                    self.mpDraw.draw_landmarks(frame, HandLms, self.mpHands.HAND_CONNECTIONS)
        return frame

    def HandTracker(self,frame, draw=True):
        self.left_Hlms=None
        self.right_Hlms=None
        if self.results.multi_hand_landmarks and self.results.multi_handedness:
            for hand_landmarks, handedness in zip(self.results.multi_hand_landmarks, self.results.multi_handedness):
            # Identify if the hand is Left or Right
                self.label = handedness.classification[0].label

            # Draw landmarks on the frame
                if draw:
                    self.mpDraw.draw_landmarks(frame, hand_landmarks, self.mpHands.HAND_CONNECTIONS)

                if self.label == "Right":
                    self.right_Hlms = self.extractLandmarks(frame,hand_landmarks)

                elif self.label == "Left":
                    self.left_Hlms = self.extractLandmarks(frame,hand_landmarks)
        return self.left_Hlms, self.right_Hlms

    def extractLandmarks(self,frame,hand_landmarks):
        self.lm_List = []
        for id, lm in enumerate(hand_landmarks.landmark):
                #landmarks are given in floating point numbers i.e as a ratio of the image. 
                #we must multiply it with image dimensions to get the actual pixels values
                h, w, c = frame.shape
                cx, cy = int(lm.x*w), int(lm.y*h)
                self.lm_List.append([id, cx, cy])
        return self.lm_List
    
    def findAngle(self, img, p1, p2, p3, draw=True):
        angle =0
        #GET LANDMARK COORDINATES
        if self.right_Hlms is not None:
            _, x1, y1 = self.right_Hlms[p1]
            x2, y2 = self.right_Hlms[p2][1:] #another way of doing it
            x3, y3 = self.right_Hlms[p3][1:] 

            #CALCLATE THE ANGLE
            angle = math.degrees(math.atan2(y3-y2, x3-x2) - math.atan2(y1-y2, x1-x2))
            if angle < 0 :
                angle +=360        

            if draw:
                cv.line(img, (x1,y1), (x2,y2), (0,0,255), 3)
                cv.line(img, (x2,y2), (x3,y3), (0,0,255), 3)
                cv.circle(img, (x1,y1), 15, (0,0,0), cv.FILLED)
                cv.circle(img, (x1,y1), 10, (255,0,0), 2)
                cv.circle(img, (x2,y2), 15, (0,0,0), cv.FILLED)
                cv.circle(img, (x2,y2), 10, (255,0,0), 2)
                cv.circle(img, (x3,y3), 15, (0,0,0), cv.FILLED)
                cv.circle(img, (x3,y3), 10, (255,0,0), 2)
                cv.putText(img, str(int(angle)), (x2-20, y2+70), cv.FONT_HERSHEY_COMPLEX, 1, (250,250,250), 2)
        return angle
        

def main():
    cap = cv.VideoCapture(0)
    detector = handDetector()
    

    while True:
        isTrue, img = cap.read()
        img=detector.detectHands(img)
        left_Hms, right_Hms = detector.HandTracker(img)
        print(right_Hms)

        cv.imshow("Image", img)

        if cv.waitKey(20) & 0xFF==ord('d'):
            break


    cap.release()
    cv.destroyAllWindows()


if __name__== '__main__':
    main()
        
    