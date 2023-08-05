from __future__ import absolute_import

import os
import os.path
from collections import deque

import pyautogui
from robot.api import logger as LOGGER

pyautogui.FAILSAFE = False

from ImageLibrary.GUIProcess import GUIProcess


class ErrorHandler(object):

    HISTORY_SIZE = 50

    def __init__(self, screenshot_folder):

        self.screenshot_folder = screenshot_folder
            
        self.screenshot_counter = 1
        self.clear_history()
        self.info_message_counter = 1

    def _save_to_disk(self, img, name):
        if not os.path.exists(self.screenshot_folder):
            os.makedirs(self.screenshot_folder)
            try:
                os.remove(os.path.join(self.screenshot_folder, name))
            except OSError:
                pass

        i = img.convert('RGB')
        i.save(os.path.join(self.screenshot_folder, name), "JPEG", quality=100)

    def save_state(self, level="INFO"):

        screenshot_name = "state-{}.png".format(self.screenshot_counter)
        self.screenshot_counter += 1
        self.area = GUIProcess().get_window_area()

        screen_img = pyautogui.screenshot(region=self.area)


        self._save_to_disk(screen_img, screenshot_name)

        msg = 'Saved screenshot <br/><img src="{}"/>'.format(os.path.join(self.screenshot_folder, screenshot_name))
        LOGGER.write(msg, level, html=True)


    def clear_history(self):
        self.history = deque(maxlen=ErrorHandler.HISTORY_SIZE)

    def dump_screenshots(self):
        LOGGER.info("Dumping screenshots to disk")
        for screen in self.history:
            self._save_to_disk(screen[0], screen[1])

        self.clear_history()

    def report_message(self, message, level, *images):
        #image is tuple(name, PIL image)
        msg = message
        for image in images:
            image_filename = "{}-{}.png".format(image[0], self.info_message_counter)
            self._save_to_disk(image[1], image_filename)
            msg += '<br/>{}: <img src="{}"/>'.format(image[0], os.path.join(self.screenshot_folder, image_filename))

        self.info_message_counter += 1
        LOGGER.write(msg, level, html=True)

    def report_error(self, message, *images):
        return self.report_message(message, "ERROR", *images)

    def report_warning(self, message, *images):
        return self.report_message(message, "WARN", *images)

    def report_info(self, message, *images):
        return self.report_message(message, "INFO", *images)

    #debug
    save_pictures_counter = 1

    def save_pictures(self, images):
        for image in images:
            image[0].save(os.path.join(self.screenshot_folder, "%s-%s.png" % (ErrorHandler.save_pictures_counter, image[1])), "PNG")

        ErrorHandler.save_pictures_counter += 1

