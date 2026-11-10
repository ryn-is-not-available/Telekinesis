import cv2
from handTracker import HandTracker
from gestureController import GestureController

wCam, hCam = 640, 480
cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)


tracker = HandTracker()
controller = GestureController(camera_width=wCam, camera_height=hCam)

while True:
    success, img = cap.read()
    if not success:
        break
    
    img ,lm_list = tracker.findHands(img)

    
    if len(lm_list) == 0:
        cv2.imshow("Air-Mouse Tracker", img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        continue

    thumb_tip = lm_list[4][1:]
    index_tip = lm_list[8][1:]
    middle_tip = lm_list[12][1:]
    ring_tip = lm_list[16][1:]

    is_gesture_active = controller.fistControlGesture(lm_list)

    if not is_gesture_active:
        controller.moveCursor(index_tip[0], index_tip[1])
        controller.handleClick(thumb_tip, middle_tip)

    cv2.imshow("Air-Mouse Tracker", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()