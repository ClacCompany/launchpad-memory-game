from threading import Thread
import LaunchpadPro
import LaunchpadMk2
import launchpad_py as launchpad
import playsound
import atexit
import time
import json
import os


def check_launchpad():
    global lp
    mode = None

    if LaunchpadPro.LaunchpadPro().Check(0):
        lp = LaunchpadPro.LaunchpadPro()
        if lp.Open(0):
            mode = "Pro"
    elif LaunchpadMk2.LaunchpadMk2().Check(0):
        lp = LaunchpadMk2.LaunchpadMk2()
        if lp.Open(0):
            mode = "Mk2"
    return lp


def on_exit():
    os.system(f"python {os.getcwd()}/start.py")


def play_sound(fname: str):
    playsound.playsound(fname)


class Game:
    def __init__(self):
        self.lp = check_launchpad()
        if self.lp.Check(0):
            self.lp.Reset()
        self.lp.register_on_button_press(on_button=self.on_button_press)
        self.press = []
        self.cur_level = 0
        self.can_gameover = False
        self.isDead = False
        self.levels = json.loads(open("levels.json", "r").read())
        self.next_level()

    def next_level(self):
        self.lp.Reset()
        self.lp.LedCtrlString(str(self.cur_level + 1), self.levels[self.cur_level]["color"][0],
                              self.levels[self.cur_level]["color"][1], self.levels[self.cur_level]["color"][2])
        time.sleep(1)
        self.lp.Reset()
        self.can_gameover = True
        for i in self.levels[self.cur_level]["pos"]:
            self.lp.LedCtrlXY(i[0] - 1, i[1], self.levels[self.cur_level]["color"][0],
                              self.levels[self.cur_level]["color"][1], self.levels[self.cur_level]["color"][2])
            time.sleep(0.015)
        while not self.levels[self.cur_level]["pos"] == self.press:
            if self.isDead:
                self.on_death()
        self.cur_level += 1
        self.press = []
        Thread(target=play_sound, args=("sounds/win.wav",)).start()
        if self.cur_level + 1 > len(self.levels):
            self.can_gameover = False
            self.on_win()
        else:
            self.can_gameover = False
            self.next_level()

    def on_button_press(self, x, y, pres):
        if pres > 0:
            if self.levels[self.cur_level]["pos"][len(self.press)] != [x, y] and self.can_gameover:
                self.isDead = True
                return
            if [x, y] in self.press and self.can_gameover:
                self.isDead = True
                return
            if self.can_gameover:
                self.lp.LedCtrlXY(x - 1, y, 0, 255, 0)
                self.press.append([x, y])
                if self.levels[self.cur_level]["pos"][-1] != [x, y]:
                    Thread(target=play_sound, args=("sounds/correct.wav",)).start()

    def on_win(self):
        self.lp.Reset()
        self.lp.LedCtrlString("Win", 0, 255, 0, direction=self.lp.SCROLL_LEFT, waitms=50)
        exit()

    def on_death(self):
        self.lp.Reset()
        self.lp.LedCtrlString("X", 255, 0, 0)
        self.lp.continue_listener = False
        exit()


if __name__ == "__main__":
    atexit.register(on_exit)
    Game()
