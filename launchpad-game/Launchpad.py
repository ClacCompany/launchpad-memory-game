from launchpad_py import LaunchpadPro as LpPro
from threading import Thread
import cv2.cv2 as cv2
import numpy as np
import atexit
import time


class LaunchpadPro(LpPro):
    on_finish = []
    on_button = []

    continue_listener = True
    listener_thread: Thread = None

    def __init__(self, number=0, name="pad pro"):
        super().__init__()
        super().Open(number, name)
        super().ButtonFlush()
        atexit.register(self.__on_exit__)
        self.continue_listener = True
        self.listener_thread = Thread(target=self.__start_listener__)
        self.listener_thread.setName("Launchpad Pro")
        self.listener_thread.start()

    def __on_exit__(self):
        time.sleep(5)
        super().ButtonFlush()
        super().Reset()
        super().Close()

    def __start_listener__(self):
        sTime = time.time()
        self.continue_listener = True
        while self.continue_listener:
            btns = super().ButtonStateXY(mode="pro")
            if btns:
                for event in self.on_button:
                    event(btns[0], btns[1], btns[2])
        for finisher in self.on_finish:
            finisher(sTime - time.time())

    def show_image(self, img: np.ndarray):
        ri = cv2.resize(img, dsize=(8, 8), interpolation=cv2.INTER_CUBIC)
        for x in range(1, 8):
            for y in range(1, 8):
                self.LedCtrlXY(x-1, y+1, ri[x-1][y-1][0], ri[x-1][y-1][1], ri[x-1][y-1][2])

    def register_on_button_press(self, on_button: callable, on_finish=lambda t: print(f"Finished in {round(-t, 3)}s!")):
        self.on_button.append(on_button)
        self.on_finish.append(on_finish)
