import cv2
from handTracker import HandTracker
from gestureController import GestureController
from videoStream import VideoStream

tracker = HandTracker()
controller = GestureController()

vs = VideoStream()

try:
    while True:
        success, img = vs.read()
        if not success:
            break
        
        img, lm_list = tracker.findHands(img)
        
        if len(lm_list) == 0:
            cv2.imshow("Air-Mouse Tracker", img)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            continue

        thumb_tip = lm_list[4][1:]
        index_tip = lm_list[8][1:]
        middle_tip = lm_list[12][1:]

        is_gesture_active = controller.fistControlGesture(lm_list)

        if not is_gesture_active:
            controller.moveCursor(index_tip[0], index_tip[1])
            controller.handleClick(thumb_tip, middle_tip)

        cv2.imshow("Air-Mouse Tracker", img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

finally:
    vs.release()
    cv2.destroyAllWindows()