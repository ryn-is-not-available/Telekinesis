import cv2
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision

class HandTracker:
    def __init__(self, model_path='hand_landmarker.task', max_hands=1):
        base_options = python.BaseOptions(model_asset_path=model_path)
        options = vision.HandLandmarkerOptions(
            base_options=base_options,
            num_hands=max_hands
        )
        self.detector = vision.HandLandmarker.create_from_options(options)

    def findHands(self, img, hand_no=0):
        landmarks = []
        # Convert OpenCV BGR to 
        cv2.flip(img, 1, img)
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=imgRGB)
        self.results = self.detector.detect(mp_image)

        if self.results.hand_landmarks:
            myHand = self.results.hand_landmarks[hand_no]
            h, w, c = img.shape 
            for id, landmark in enumerate(myHand):
                cx = int(landmark.x * w)
                cy = int(landmark.y * h)
                landmarks.append([id, cx, cy])
                cv2.circle(img, (cx, cy), 5, (255, 0, 0), cv2.FILLED)

        return img, landmarks
        


    def findIndexFingerTip(self,img) :

        cv2.flip(img, 1,img)
        img_RGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=img_RGB)

        self.results = self.detector.detect(mp_image)
        x,y = None, None
        if self.results.hand_landmarks:
            for hand in self.results.hand_landmarks:
                index_finger_tip = hand[8]  # Index finger tip is the 8th landmark
                x = int(index_finger_tip.x * img.shape[1])
                y = int(index_finger_tip.y * img.shape[0])
                cv2.circle(img, (x, y), 10, (0, 255, 0), cv2.FILLED)
        
        return (img ,x, y)