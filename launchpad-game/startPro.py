import LaunchpadPro
from playsound import playsound
import atexit
import time
import json
import os
from threading import Thread


def on_exit():
    os.system(f"python {os.getcwd()}/startPro.py")


class Game:
    def __init__(self):
        self.lp = LaunchpadPro.LaunchpadPro()
        self.lp.Reset()
        self.lp.register_on_button_press(on_button=self.on_button_press)
        self.press = []
        self.cur_level = 0
        self.isDead = False
        self.levels = json.loads(open("levels.json", "r").read())
        self.next_level()

    def next_level(self):
        self.lp.Reset()
        self.lp.LedCtrlString(str(self.cur_level + 1), self.levels[self.cur_level]["color"][0],
                              self.levels[self.cur_level]["color"][1], self.levels[self.cur_level]["color"][2])
        time.sleep(1)
        self.lp.Reset()
        for i in self.levels[self.cur_level]["pos"]:
            self.lp.LedCtrlXY(i[0], i[1], self.levels[self.cur_level]["color"][0],
                              self.levels[self.cur_level]["color"][1], self.levels[self.cur_level]["color"][2])
            time.sleep(0.05)
        while not self.levels[self.cur_level]["pos"] == self.press:
            if self.isDead:
                self.on_death()
        self.cur_level += 1
        self.press = []
        Thread(target=playsound, args=("sounds/win.wav",)).start()
        if self.cur_level + 1 > len(self.levels):
            self.on_win()
        else:
            self.next_level()

    def on_button_press(self, x, y, pres):
        x = x - 1
        if pres > 0:
            if self.levels[self.cur_level]["pos"][len(self.press)] != [x, y]:
                self.isDead = True
                return
            if [x, y] in self.press:
                self.isDead = True
                return
            self.lp.LedCtrlXY(x, y, 0, 255, 0)
            self.press.append([x, y])
            if self.levels[self.cur_level]["pos"][-1] != [x, y]:
                Thread(target=playsound, args=("sounds/correct.wav",)).start()

    def on_win(self):
        self.lp.Reset()
        self.lp.LedCtrlString("Win", 0, 255, 0, direction=self.lp.SCROLL_LEFT, waitms=50)
        self.lp.continue_listener = False
        exit()

    def on_death(self):
        self.lp.Reset()
        self.lp.LedCtrlString("X", 255, 0, 0)
        self.lp.continue_listener = False
        exit()


if __name__ == "__main__":
    atexit.register(on_exit)
    Game()
