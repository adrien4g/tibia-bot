import cv2 as cv
import numpy as np
import pyautogui
from time import sleep

from scripts.screen_manager import  get_battle_list_window, monitor

class Enemy:
    def __init__(self):
        # Amazon template
        self.amazon_template = cv.imread('templates/amazon.png', cv.IMREAD_UNCHANGED)
        self.amazon_template_gray = cv.cvtColor(self.amazon_template, cv.COLOR_RGB2GRAY)
        self.amazon_template_height, self.amazon_template_width = self.amazon_template_gray.shape

        # Target template
        self.target_template = cv.imread('templates/target.png', cv.IMREAD_UNCHANGED)
        self.target_template_gray =  cv.cvtColor(self.target_template, cv.COLOR_RGB2GRAY)
        self.target_template_height, self.target_template_width = self.target_template_gray.shape

        # Battle list
        self.battle_list = np.array(get_battle_list_window())
        self.battle_list_gray = cv.cvtColor(self.battle_list, cv.COLOR_RGB2GRAY)

        # Match variables
        self.match_monsters = ([[]])
        self.old_match_monsters = ([[]])
        self.match_target = ([[]])

        # Control variables
        self.attacking = False

    def debug(self):
        # Amazon
        if len(self.match_monsters[0]) > 0:
            amazon_position_start = (self.match_monsters[1][0], self.match_monsters[0][0])
            amazon_position_end   = (
                self.match_monsters[1][0] + self.amazon_template_width,
                self.match_monsters[0][0] + self.amazon_template_height
            )
            battle_list_window = cv.rectangle(
                img   = self.battle_list,
                pt1   = amazon_position_start,
                pt2   = amazon_position_end,
                color = (0, 0, 255)
            )
        else:
            battle_list_window = self.battle_list
            target_window = self.battle_list

        cv.imshow('Amazon list', battle_list_window)
        
        # Target
        if len(self.match_target[0]) > 0:
            target_position_start = (self.match_target[1][0], self.match_target[0][0])
            target_position_end   = (
                self.match_target[1][0] + self.target_template_width,
                self.match_target[0][0] + self.target_template_height
            )
            target_window = cv.rectangle(
                img   = self.battle_list,
                pt1   = target_position_start,
                pt2   = target_position_end,
                color = (0, 255, 0)
            )
        else:
            target_window = self.battle_list
            
        cv.imshow('Target list', target_window)

        if cv.waitKey(1) == ord('d'):
            cv.destroyAllWindows

    def update_battle_list(self):
        self.battle_list = np.array(get_battle_list_window())
        self.battle_list_gray = cv.cvtColor(self.battle_list, cv.COLOR_RGB2GRAY)
        return self.battle_list_gray

    def detect_monsters(self):
        # Pega o dado da tela de battle list
        battle_list = np.array(get_battle_list_window())
        battle_list_gray = cv.cvtColor(battle_list, cv.COLOR_RGB2GRAY)

        # Faz o match
        battle_list_result = cv.matchTemplate(
            image = battle_list_gray,
            templ = self.amazon_template_gray,
            method= cv.TM_CCOEFF_NORMED
        )

        # Retorna apenas os matchs com 80% de fidelidade
        self.old_match_monsters = self.match_monsters
        self.match_monsters = np.where(battle_list_result >= 0.8)
        return self.match_monsters

    def attack_monsters(self):
        if len(self.match_monsters[0]) > 0:
            if len(self.match_monsters[0]) != len(self.old_match_monsters[0]):
                # Ataca os inimigos
                if not self.attacking:
                    self.attack_monster()

    def check_if_attacking(self):
        res = cv.matchTemplate(self.battle_list_gray, self.target_template_gray, cv.TM_CCOEFF_NORMED)
        self.match_target = np.where(res > 0.99)
        if len(self.match_target[0]) > 0:
            self.attacking = True
            return True
        self.attacking = False
        return False

    def attack_monster(self):
        old_mouse_x, old_mouse_y = pyautogui.position()
        new_mouse_x = self.match_monsters[1][0] + monitor['left']
        new_mouse_y = self.match_monsters[0][0] + monitor['top']
        pyautogui.click(new_mouse_x, new_mouse_y)
        pyautogui.moveTo(old_mouse_x, old_mouse_y)
