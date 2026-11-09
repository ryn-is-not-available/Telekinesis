import cv2
import handTracker as ht
import pyautogui as pg

def main():
    cap = cv2.VideoCapture(0)
    detector = ht.HandTracker()

    while True:
        success, img = cap.read()
        img, x, y = detector.findIndexFingerTip(img)
        if x is not None and y is not None:
            screen_x = (x / img.shape[1]) * pg.size().width
            screen_y = (y / img.shape[0]) * pg.size().height
            pg.moveTo(screen_x, screen_y)
        cv2.imshow("Image", img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break




if __name__ == "__main__":
    main()