# -*- coding: utf-8 -*-
"""
Created on Mon Mar 28 19:35:54 2022

@author: KuroAzai
"""

import pyautogui
import pygetwindow
import glob
import time
import os
import keyboard
import pandas as pd
from dataclasses import dataclass
from pywinauto.findwindows import find_window
from pywinauto.win32functions import SetForegroundWindow


@dataclass
class Config():
    expendable_gems: int = 767
    expendable_gold: int = 1000000

    gem_per_refresh = 3
    gold_per_purchase = 184000

    x_offset: int = 400
    y_offset: int = 20

    win_x_size: int = 960
    win_y_size: int = 555

    active_win_x: int = 500
    active_win_y: int = 180

    region: tuple = (0, 0, 960, 555)

    path: str = r'C:\Users\Odin\Pictures\BlueEye\Epic Seven'

    instances = ['GachaSim Alchemist',
                 'Gachasim Wotv']

    farm_covenant: bool = True
    farm_mystic: bool = False
    farm_friendship: bool = False

    logging: bool = False

    def setup_bluestacks(self):
        win = pygetwindow.getWindowsWithTitle(self.instances[0])[0]
        win.size = (960, 555)
        win.resizeTo = (960, 555)
        win.moveTo(0, 0)


class PathManager():

    def __init__(self):
        self.cfg = Config()

    def find_image(self, image):
        matches = glob.glob(self.cfg.path + f'/{image}')
        if matches:
            return matches[0]


@dataclass
class DataCollector():
    covenant_runs: int = 0
    mystic_runs: int = 0
    gems_spent: int = 0
    gold_spent: int = 0
    bookmarks: int = 0
    mystics: int = 0

    datastore = {'Covenants': 0,
                 'Mystics': 0}

    def save(self):
        filename = 'covenant_tracker.csv'

        if os.path.exists(filename):
            self.df = pd.read_csv(filename)
        else:
            self.df = pd.DataFrame.from_dict(self.datastore)

        self.df = self.df.append(self.datastore,
                                 ignore_index=True)

        header = ["Covenants"]
        self.df.to_csv('covenant_tracker.csv',
                       columns=header)
        self.datastore = {'Covenants': 0,
                          'Mystics': 0}


def check_frienship():
    path = PM.find_image('friendship.png')
    for i in range(2):
        if (pyautogui.locateOnScreen(path) is not None):
            x, y = pyautogui.locateCenterOnScreen(path,
                                                  confidence=0.9,
                                                  )
            buy_friendship(x, y)
            break
        scroll_down()


def check_mystic():
    path = PM.find_image('mystic.png')
    for i in range(2):
        if (pyautogui.locateOnScreen(path) is not None):
            x, y = pyautogui.locateCenterOnScreen(path,
                                                  confidence=0.9,
                                                  )
            buy_mystic(x, y)
            break
        scroll_down()


def check_covenant():
    for n in range(1, 4):
        path = PM.find_image(f'covenant{n}.png')
        for i in range(2):
            if (pyautogui.locateOnScreen(path, confidence=0.75, region=CFG.region) is not None):
                x, y = pyautogui.locateCenterOnScreen(path,
                                                      confidence=0.75,
                                                      region=CFG.region)
                buy_covenant(x, y)
                return
            if i == 0:
                scroll_down()
                time.sleep(0.5)
            elif i == 1:
                scroll_up()
                time.sleep(0.5)


def buy_covenant(x, y):
    pyautogui.click(x + CFG.x_offset, y + CFG.y_offset)
    time.sleep(0.35)
    path = PM.find_image('buy.png')
    if (pyautogui.locateOnScreen(path) is not None):
        x, y = pyautogui.locateCenterOnScreen(path,
                                              confidence=0.75)
        pyautogui.click(x, y)
        time.sleep(0.05)
        pyautogui.click(x, y)
        LOGGER.datastore['Covenants'] = LOGGER.covenant_runs
        LOGGER.covenant_runs = 0
        LOGGER.bookmarks += 5
        LOGGER.gold_spent += 184000
        LOGGER.save()


def buy_mystic(x, y):
    pyautogui.click(x + CFG.x_offset, y + CFG.y_offset)
    time.sleep(0.35)
    path = PM.find_image('buy.png')
    if (pyautogui.locateOnScreen(path) is not None):
        x, y = pyautogui.locateCenterOnScreen(path,
                                              confidence=0.75)
        pyautogui.click(x, y)

        LOGGER.datastore['Mystics'] = LOGGER.covenant_runs
        LOGGER.mystic_runs = 0
        LOGGER.bookmarks += 5
        LOGGER.gold_spent += 184000
        LOGGER.save()


def buy_friendship(x, y):
    pyautogui.click(x + CFG.x_offset, y + CFG.y_offset)
    time.sleep(0.35)
    path = PM.find_image('buy.png')
    if (pyautogui.locateOnScreen(path) is not None):
        x, y = pyautogui.locateCenterOnScreen(path,
                                              confidence=0.75)
        pyautogui.click(x, y)


def refresh_store():
    while True:
        if keyboard.is_pressed("q"):
            break
        try:
            path = PM.find_image('refresh.png')
            if (pyautogui.locateOnScreen(path) is not None):
                x, y = pyautogui.locateCenterOnScreen(path,
                                                      confidence=0.9)
                pyautogui.click(x, y)
                time.sleep(0.5)

                path = PM.find_image('confirm.png')
                x, y = pyautogui.locateCenterOnScreen(path,
                                                      confidence=0.9)
                pyautogui.click(x, y)
                time.sleep(0.05)
                pyautogui.click(x, y)
                return
        except Exception as ValueError:
            pass


def bring_to_front():
    SetForegroundWindow(find_window(title=CFG.instances[0]))
    pyautogui.click(CFG.active_win_x, CFG.active_win_y)


def scroll_down():
    pyautogui.scroll(-2)


def scroll_up():
    pyautogui.scroll(2)


def main():
    while CFG.expendable_gems > 0:
        os.system('cls')

        if CFG.logging:
            c_avg = LOGGER.df['Covenants'].sum() / len(LOGGER.df['Covenants'])
            # m_avg = LOGGER.df['Mystics'].sum() / len(LOGGER.df['Mystics'])
            # f_avg = LOGGER.df['Covenants'].sum() / len(LOGGER.df['Covenants'])

            print('\n\ntotal gems spent {}'.format(LOGGER.gems_spent),
                  '\nbookmarks acquired {}'.format(LOGGER.bookmarks),
                  '\nAverage rolls per bookmark', c_avg)

        bring_to_front()

        if CFG.farm_friendship:
            check_frienship()
        if CFG.farm_covenant:
            check_covenant()
        if CFG.farm_mystic:
            check_mystic()

        LOGGER.mystic_runs += 1
        LOGGER.covenant_runs += 1
        LOGGER.gems_spent += 3

        if keyboard.is_pressed("q"):
            break

        refresh_store()
        CFG.expendable_gems -= 3

        time.sleep(1)

    if CFG.logging:
        LOGGER.save()


if __name__ == "__main__":
    CFG = Config()
    CFG.setup_bluestacks()
    PM = PathManager()
    LOGGER = DataCollector()
    bring_to_front()
    main()
