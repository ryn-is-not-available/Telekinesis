import pyautogui as pg
import math
import time
import config
from mapping import mapAxis
from landmarks import landmark



class GestureController:
    def __init__(self, camera_width=config.CAMERA_WIDTH, camera_height=config.CAMERA_HEIGHT):
        pg.PAUSE = 0
        self.camera_width, self.camera_height = camera_width, camera_height
        self.width , self.height = pg.size()
        self.isClicked = False
        self.oldFistPosition = None

        self.prev_screen_x = 0
        self.prev_screen_y = 0
        self.smoothening = config.SMOOTHING_FACTOR

        self.last_action_time = 0

    def moveCursor(self, x, y):
        raw_screen_x = mapAxis((x / self.camera_width), 0.3, self.width)
        raw_screen_y = mapAxis((y / self.camera_height), 0.3, self.height)

        smooth_x = int(self.prev_screen_x + (raw_screen_x - self.prev_screen_x) * self.smoothening)
        smooth_y = int(self.prev_screen_y + (raw_screen_y - self.prev_screen_y) * self.smoothening)

        pg.moveTo(smooth_x, smooth_y)

        self.prev_screen_x = smooth_x
        self.prev_screen_y = smooth_y

    def handleClick(self, thumb_tip, middle_tip):
        distance = math.sqrt((thumb_tip[0] - middle_tip[0])**2 + (thumb_tip[1] - middle_tip[1])**2)
        if distance <= 30:
            if not self.isClicked:
                pg.click()
                self.isClicked = True
        else:
            self.isClicked = False

    def isFist(self, lm_list):
        """
        Returns True if all four main fingertips (index, middle, ring, pinky) 
        are curled inward towards the palm/wrist compared to their PIP joints.
        """
        
        tips = [landmark.INDEX_TIP, landmark.MIDDLE_TIP, landmark.RING_TIP, landmark.PINKY_TIP]
        pips = [landmark.INDEX_PIP, landmark.MIDDLE_PIP, landmark.RING_PIP, landmark.PINKY_PIP]
        
        curled_count = 0
        for tip, pip in zip(tips, pips):
            if lm_list[tip][2] >= lm_list[pip][2]:
                curled_count += 1
                
        # If all 4 fingers are curled, it's a fist
        return curled_count >= 4

    def fistControlGesture(self, lm_list):
        """
        Handles the 'Grab-and-Pull' action when a fist is made.
        Returns True if in fist-control mode (suppressing mouse move/click), False otherwise.
        """
        if not self.isFist(lm_list):
            self.oldFistPosition = None
            return False

        
        wrist = lm_list[landmark.WRIST]
        fist_current_pos = [wrist[1], wrist[2]]

        if self.oldFistPosition is None:
            self.oldFistPosition = fist_current_pos
            return True  # Captured initial grab point, suppress normal mouse for this frame

        # Calculate pull deltas
        delta_y = fist_current_pos[1] - self.oldFistPosition[1]
        delta_x = fist_current_pos[0] - self.oldFistPosition[0]
        print(f"Delta X: {delta_x}, Delta Y: {delta_y}")
        # Pixels of movement required to trigger action
        if time.monotonic() - self.last_action_time < config.COOLDOWN:
            return True  

        if abs(delta_y) > abs(delta_x):
            if delta_y > config.PULL_THRESHOLD:
                # Pulled Down: Show Desktop / Minimize
                pg.hotkey('win', 'd')
                self.oldFistPosition = None
            elif delta_y < -config.PULL_THRESHOLD:
                # Pulled Up: Restore / Switch
                pg.hotkey('win', 'd')
                self.oldFistPosition = None
        else :
            if abs(delta_x) > config.PULL_THRESHOLD:
                if delta_x > 0:
                    pg.hotkey('alt', 'tab')  # Pull Right
                else:
                    pg.hotkey('win', 'tab')  # Pull Left
                self.oldFistPosition = None
        


        return True