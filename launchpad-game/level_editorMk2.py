import json
import random

import keyboard

import LaunchpadMk2


class Editor:
    def __init__(self):
        self.colors = [[255, 0, 0], [255, 148, 3], [255, 247, 3], [0, 255, 0], [0, 255, 255], [0, 0, 255],
                       [128, 0, 255],
                       [255, 0, 255]]
        self.lp = LaunchpadMk2.LaunchpadMk2()
        self.lp.Reset()
        self.press = []
        self.color = []
        self.data = json.loads(open("levels.json", "r").read())

    def start(self):
        self.lp.register_on_button_press(on_button=self.on_button_press)
        self.color = random.choice(self.colors)

    def stop(self):
        self.data.append({
            "pos": self.press,
            "color": self.color
        })
        open("levels.json", "w").write(json.dumps(self.data))
        self.data = json.loads(open("levels.json", "r").read())
        self.color = []
        self.press = []
        self.lp.LedCtrlString("Saved", 0, 255, 0, self.lp.SCROLL_LEFT)
        self.lp.Reset()

    def on_button_press(self, x, y, pres):
        if [x, y] not in self.press and pres > 0:
            self.lp.LedCtrlXYByCode(x - 1, y, 0)
            self.press.append([x, y])


e = Editor()
e.start()
i = True
while not keyboard.is_pressed("q"):
    if i:
        e.lp.LedAllOn(17)
        i = False
    print("-- Press 'q' to stop --")
e.stop()

