from scripts.detect_enemy import Enemy

enemy = Enemy()

while True:
    enemy.update_battle_list()
    enemy.detect_monsters()
    enemy.check_if_attacking()
    enemy.attack_monsters()
    enemy.debug()