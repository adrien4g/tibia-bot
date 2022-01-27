from mss import mss

# Ative o debug para ver se as marcações estão certas (Nãi implementado)
debug = False

"""
Ele retorna um array com os monitores
Sendo [0] um objeto com todos os monitores somados (widtb e height) e [N] o valor diretamente do monitor
(Por exemplo, o monitor 2 da sua máquina é [2] em vez de [1])
"""
monitor = mss().monitors[1]

# Janelas do jogo
window_battle_list = monitor.copy()
window_battle_list['width'] = 180
window_battle_list['height'] = 300

def get_battle_list_window():
    return mss().grab(window_battle_list)