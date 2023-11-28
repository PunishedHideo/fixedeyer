import time
import pyautogui
from pynput import keyboard, mouse
from shapely.geometry import Point, Polygon

pyautogui.PAUSE = 0

zone1 = [(332, 1), (1051, 721), (1770, 1)]
zone2 = [(1770, 1), (1051, 721), (1770, 1439)]
zone3 = [(1770, 1439), (1051, 721), (332, 1436)]
zone4 = [(332, 1436), (1051, 721), (332, 1)]

zone_key_mapping = {
    'zone1': ['ctrl', 'up'],
    'zone2': ['ctrl', 'right'],
    'zone3': ['ctrl', 'down'],
    'zone4': ['ctrl', 'left']
}
active = False
zone_keys_pressed = {zone: False for zone in zone_key_mapping}

def on_press(key):
    global active

    if key == keyboard.Key.esc:
        exit()

    if key == keyboard.Key.ctrl_r:  # Change this line to use RAlt
        active = not active

        if active:
            pyautogui.press('g')
            print("Activated")
        else:
            pyautogui.press('g')
            print("Deactivated")

        for zone in zone_key_mapping:
            zone_keys_pressed[zone] = False

def on_move(x, y):
    global active

    if not active:
        return

    current_position = Point(x, y)

    for zone in zone_key_mapping:
        if is_inside_zone(current_position, globals()[zone]) and not zone_keys_pressed[zone]:
            perform_action(zone)
            zone_keys_pressed[zone] = True
        elif not is_inside_zone(current_position, globals()[zone]):
            zone_keys_pressed[zone] = False

def is_inside_zone(point, zone):
    polygon = Polygon(zone)
    return polygon.contains(point)

def perform_action(zone):
    keys = zone_key_mapping.get(zone, [])

    if keys:
        pyautogui.keyDown('ctrl')
        pyautogui.press(keys[1])
        time.sleep(0.03)
        pyautogui.keyUp('ctrl')

with keyboard.Listener(on_press=on_press) as listener, mouse.Listener(on_move=on_move) as mouse_listener:
    listener.join()
    mouse_listener.join()