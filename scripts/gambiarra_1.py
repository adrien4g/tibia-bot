"""
Essa foi a primeira versão do código, não está mais em uso.
"""

import cv2 as cv
import numpy as np
from mss import mss
import pyautogui

# Screem
monitor = mss().monitors[1]
monitor['width'] = 180
monitor['height'] = 300

# Amazon template
template = cv.imread('amazon.png', cv.IMREAD_UNCHANGED)
template_gray = cv.cvtColor(template, cv.COLOR_RGB2GRAY)

target = cv.imread('target.png', cv.IMREAD_UNCHANGED)
target_gray =  cv.cvtColor(target, cv.COLOR_RGB2GRAY)

template_h, template_w = template_gray.shape

#While true print screen
old_loc = [()]
while True:
    screen = np.array(mss().grab(monitor))
    screen_gray = cv.cvtColor(screen, cv.COLOR_RGB2GRAY)

    result = cv.matchTemplate(
        image = screen_gray,
        templ = template_gray,
        method= cv.TM_CCOEFF_NORMED
    )
    loc = np.where(result >= 0.8)
    min_val, max_val, min_loc, max_loc = cv.minMaxLoc(result)

    if max_val >= 0.80:
        if len(loc[0]) != len(old_loc[0]):
            target_print = {
                'width':1366 + loc[1][0],
                'height': loc[0][0],
                'top': 0,
                'left': 0
            }
            target_screen = np.array(mss().grab(target_print))
            target_screen_gray = cv.cvtColor(target_screen, cv.COLOR_RGB2GRAY)

            target_h, target_w = target_screen_gray.shape

            result_target = cv.matchTemplate(
                image = screen_gray,
                templ= target_gray,
                method= cv.TM_CCOEFF_NORMED
            )

            target_min_val, target_max_val, target_min_loc, target_max_loc = cv.minMaxLoc(result_target)
            print(target_max_val)
            if target_max_val > 0.7:
                target_image = cv.rectangle(
                img = screen,
                pt1 = target_max_loc,
                pt2 = (
                    target_max_loc[0] + target_w,
                    target_max_loc[1] + target_h
                ),
                color = (0, 0, 255),
                thickness=2
            )
            else:
                target_image = screen
            cv.imshow('image222', target_image)
            if cv.waitKey(1) == ord('d'):
                cv.destroyAllWindows()
                break
            if not target_max_val >= 40:
                pyautogui.click(
                   x = 1366 + loc[1][0],
                   y = loc[0][0],
                )
            old_loc = loc
        image = cv.rectangle(
            img = screen,
            pt1 = max_loc,
            pt2 = (
                max_loc[0] + template_w,
                max_loc[1] + template_h
            ),
            color = (0, 0, 255),
            thickness=2
        )
    else:
        image = screen
        old_loc = loc
    
    cv.imshow('image', image)
    if cv.waitKey(1) == ord('d'):
        cv.destroyAllWindows()
        break
