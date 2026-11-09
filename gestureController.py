import pyautogui as pg
import math

class GestureController:
    def __init__(self, camera_width=640, camera_height=480):
        self.camera_width, self.camera_height = camera_width, camera_height
        self.height, self.width = pg.size()  # Get the screen size
        self.isClicked = False
        self.oldThreeFingerPosition = None

        self.prev_screen_x = 0
        self.prev_screen_y = 0
        self.smoothening = 0.5

    def moveCursor(self, x, y):
        raw_screen_x = int((x / self.camera_width) * self.width)
        raw_screen_y = int((y / self.camera_height) * self.height)

        smooth_x = int(self.prev_screen_x + (raw_screen_x - self.prev_screen_x) * self.smoothening)
        smooth_y = int(self.prev_screen_y + (raw_screen_y - self.prev_screen_y) * self.smoothening)

        pg.moveTo(smooth_x, smooth_y)

        self.prev_screen_x = smooth_x
        self.prev_screen_y = smooth_y

    def handleClick(self, thumb_tip, middle_tip):
        distance = math.hypot(thumb_tip[0] - middle_tip[0], thumb_tip[1] - middle_tip[1])

        if distance <= 30:
            if not self.isClicked:
                pg.click()          
                self.isClicked = True 
        else:
            self.isClicked = False

    def threeFingerGesture(self, ring_finger_tip, index_finger_tip, middle_finger_tip):
        # Calculate distances between the three finger tips
        distance_index_middle = math.sqrt((index_finger_tip[1] - middle_finger_tip[1])**2 + (index_finger_tip[0] - middle_finger_tip[0])**2)
        distance_middle_ring = math.sqrt((middle_finger_tip[1] - ring_finger_tip[1])**2 + (middle_finger_tip[0] - ring_finger_tip[0])**2)
        distance_index_ring = math.sqrt((index_finger_tip[1] - ring_finger_tip[1])**2 + (index_finger_tip[0] - ring_finger_tip[0])**2)

        # Check if all three fingers are clustered close together (Control Mode active)
        if distance_index_middle <= 30 and distance_middle_ring <= 30 and distance_index_ring <= 40:
            if self.oldThreeFingerPosition is None:
                self.oldThreeFingerPosition = (
                    [index_finger_tip[0], index_finger_tip[1]], 
                    [middle_finger_tip[0], middle_finger_tip[1]], 
                    [ring_finger_tip[0], ring_finger_tip[1]]
                )
                return True  # Handled / Locked into gesture mode

            # Calculate movement delta for the middle finger (acting as the anchor of the cluster)
            delta_y = middle_finger_tip[1] - self.oldThreeFingerPosition[1][1]
            delta_x = middle_finger_tip[0] - self.oldThreeFingerPosition[1][0]

            
            SWIPE_THRESHOLD = 30

            if delta_y > SWIPE_THRESHOLD:
                # Swiped Down: Minimize / Show Desktop
                pg.hotkey('win', 'd')
                self.oldThreeFingerPosition = None  # Reset anchor after trigger
            elif delta_y < -SWIPE_THRESHOLD:
                # Swiped Up: Restore / Bring back application
                pg.hotkey('win', 'd')
                self.oldThreeFingerPosition = None
            elif abs(delta_x) > SWIPE_THRESHOLD:
                if delta_x > 0:
                    pg.hotkey('alt', 'tab')
                else:
                    pg.hotkey('win', 'tab')
                self.oldThreeFingerPosition = None
                
            return True
        else:
            
            self.oldThreeFingerPosition = None
            return False