#!/usr/bin/env python3
import logging, sys, keyboard, pyautogui, json, time, random, threading
from datetime import datetime, timedelta


FORMAT = '%(levelname)s:    %(asctime)s - %(message)s'
logging.basicConfig(stream=sys.stdout, level=logging.DEBUG, format=FORMAT)

pyautogui.FAILSAFE = True

class ScrollMe(object):

    DEFAULT_START_SCROLLING_HOTKEY = 'ctrl + shift + < + >'
    DEFAULT_TERMINATE_PROGRAM_HOTKEY = 'ctrl + shift + k + l'
    DEFAULT_SLEEP_TIME_BETWEEN_SCROLLS = 1.3
    DEFAULT_CLICKS_TO_SCROLL = 1
    SCREEN_WIDTH, SCREEN_HEIGHT = pyautogui.size()

    def __init__(self):
        self._running = True
        self.active = False

        self.config = self.load_config()
                
        self.threads = []

        t = threading.Thread(target=self.run)
        self.threads.append(t)

        for t in self.threads:
            t.start()

    def load_config(self):
        try:
            with open('config', 'r') as f:
                c = json.loads(f.read())
                assert c
                assert "HOT_KEYS" in c
                assert "START_SCROLLING" in c["HOT_KEYS"]
                assert "TERMINATE_PROGRAM" in c["HOT_KEYS"]
                assert "SLEEP_TIME_BETWEEN_SCROLLS" in c
                assert "CLICKS_TO_SCROLL" in c
                assert c["SLEEP_TIME_BETWEEN_SCROLLS"] == int(c["SLEEP_TIME_BETWEEN_SCROLLS"])
                assert c["CLICKS_TO_SCROLL"] == int(c["PIXELS_TO_SCROLL"])
                assert 0.1 <= c["SLEEP_TIME_BETWEEN_SCROLLS"] <= 999
                assert 0.1 <= c["CLICKS_TO_SCROLL"]
                return c
        except Exception as e:
            logging.error("There was an error loading config file")
            config = {}
            config["HOT_KEYS"] = {
                "START_SCROLLING": self.DEFAULT_START_SCROLLING_HOTKEY,
                "TERMINATE_PROGRAM": self.DEFAULT_TERMINATE_PROGRAM_HOTKEY,
            }
            config["SLEEP_TIME_BETWEEN_SCROLLS"] = self.DEFAULT_SLEEP_TIME_BETWEEN_SCROLLS
            config["CLICKS_TO_SCROLL"] = self.DEFAULT_CLICKS_TO_SCROLL
            return config

    def status_change(self, force_quit=False):
        if not self.active and not force_quit:
            self.active = True
            t = threading.Thread(target=self.start_working)
            self.threads.append(t)
            t.start()
        else:
            if self.active:
                self.active = False

    def run(self):
        print("""\
▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄
█░▄▄█▀▄▀█░▄▄▀█▀▄▄▀█░██░████░▄▀▄░█░▄▄
█▄▄▀█░█▀█░▀▀▄█░██░█░██░████░█▄█░█░▄▄
█▄▄▄██▄██▄█▄▄██▄▄██▄▄█▄▄███▄███▄█▄▄▄
▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀""")
        logging.info("press {} to activate".format(self.config["HOT_KEYS"]["START_SCROLLING"]))
        logging.info("press {} to terminate program".format(self.config["HOT_KEYS"]["TERMINATE_PROGRAM"]))
        logging.info("Move the mouse to stop scrolling")

        keyboard.add_hotkey(self.config["HOT_KEYS"]["START_SCROLLING"], lambda: self.status_change())
        keyboard.add_hotkey(self.config["HOT_KEYS"]["TERMINATE_PROGRAM"], lambda: self.exit())
        while self._running:
            time.sleep(5)

    def exit(self):
        self.status_change(force_quit=True)
        self._running = False
        sys.exit()

    def scroll(self):
        logging.info("Scrolling")
        x,y = pyautogui.position()
        pyautogui.scroll((0 - self.config["CLICKS_TO_SCROLL"]), x=x, y=y)

    def start_working(self):
        logging.info("Started working")

        mouse_position = pyautogui.position()
        logging.debug("mouse_position: {}".format(mouse_position))

        mouse_moved = False
        while self.active and not mouse_moved:
            logging.debug("active: {}".format(self.active))
            
            self.scroll()
            mouse_moved = (mouse_position != pyautogui.position())

            if not mouse_moved:
                logging.debug("Mouse not moved")
                time.sleep(self.config["SLEEP_TIME_BETWEEN_SCROLLS"])
            else:
                logging.debug("Mouse moved")
                self.active = False

scroll_me = ScrollMe()
