import time
import sys
import threading

import pyautogui
import keyboard
import random

from pyscreeze import Box


def click(x: float, y: float):
    pyautogui.click(x, y, duration=0.1)

def get_center_of_box(box: Box) -> tuple[float, float]:
    return box.left + (box.width / 2), box.top + (box.height / 2)

def click_box(box: Box):
    center = get_center_of_box(box)
    click(center[0], center[1])

def move_to_box(box: Box):
    center = get_center_of_box(box)
    pyautogui.moveTo(center[0], center[1])

def locate_on_screen(image: str, confidence = 0.8, grayscale: bool = True) -> (Box | None):
    try:
        return pyautogui.locateOnScreen(image, confidence=confidence, grayscale=grayscale)
    except:
        print(f"{image} not found")
        return None

def get_create_unit_box() -> (Box | None):
    return locate_on_screen("./assets/create_unit.png")

def get_armor_card_box() -> (Box | None):
    armor_card = locate_on_screen("./assets/armor_selector_card.png", 0.8)
    if armor_card:
        return armor_card
    else:
        return locate_on_screen("./assets/armor_selector_card_highlighted.png", 0.8) 

def get_recon_card_box() -> (Box | None):
    recon_card = locate_on_screen("./assets/recon_selector_card.png", 0.8)
    if recon_card:
        return recon_card
    else:
        return locate_on_screen("./assets/recon_selector_card_highlighted.png", 0.8)

def get_create_locked_armor_unit_box() -> (Box | None):
    return locate_on_screen("./assets/create_locked_armor_unit.png", 0.9)

def get_create_locked_recon_unit_box() -> (Box | None):
    return locate_on_screen("./assets/create_locked_recon_unit.png", 0.9)

def create_unit(unit_type: str) -> bool:
    create_unit_box = get_create_unit_box()
    if create_unit_box:
        click_box(create_unit_box)
        time.sleep(0.005)

        if unit_type == "--armor":
            armor_card_box = get_armor_card_box()
            if armor_card_box:
                move_to_box(armor_card_box)

                time.sleep(0.25)

                create_locked_armor_unit = get_create_locked_armor_unit_box()
                if create_locked_armor_unit:
                    click_box(create_locked_armor_unit)
                    return True

        elif unit_type == "--recon":
            recon_card_box = get_recon_card_box()
            if recon_card_box:
                move_to_box(recon_card_box)

                time.sleep(0.25)

                create_locked_recon_unit = get_create_locked_recon_unit_box()
                if create_locked_recon_unit:
                    click_box(create_locked_recon_unit)
                    return True
    
    return False

jiggler_is_alive = False
def jiggler():
    while jiggler_is_alive:
        time.sleep(0.075)
        start_pos = pyautogui.position()
        pyautogui.moveRel(random.randrange(-10, 10), random.randrange(-10, 10), duration=0.1)
        time.sleep(0.01)
        pyautogui.moveTo(start_pos.x, start_pos.y, duration=0.1)

def reset_jiggler(jiggler_thread: threading.Thread) -> threading.Thread:
    global jiggler_is_alive

    if jiggler_is_alive:
        jiggler_is_alive = False
        jiggler_thread.join()

    jiggler_is_alive = True
    return threading.Thread(target=jiggler)


def main(unit_type: str):
    is_running = True
    is_searching = False

    def toggle_is_running():
        nonlocal is_searching
        is_searching = not is_searching

        if is_searching:
            print("Active")
        else:
            print("Idle")

    def set_dead():
        nonlocal is_running
        is_running = False

    time.sleep(1)

    keyboard.add_hotkey("ctrl+f4", set_dead, suppress=True)
    keyboard.add_hotkey("f4", toggle_is_running, suppress=True)

    jiggler_thread = threading.Thread(target=jiggler)
    while is_running:
        time.sleep(0.25)

        if is_searching:
            jiggler_thread = reset_jiggler(jiggler_thread)
            jiggler_thread.start()

        while is_searching:
            global jiggler_is_alive

            time.sleep(0.001)

            if not is_running:
                jiggler_is_alive = False
                jiggler_thread.join()
                break

            if create_unit(unit_type):
                toggle_is_running()
                jiggler_is_alive = False
                jiggler_thread.join()

def help():
    print("Unit Auto Selector")
    print()
    print("F4 to toggle")
    print("CTRL+F4 to quit")
    print()
    print("--help")
    print("--armor")
    print("--recon")

    exit(0)

if __name__ == "__main__":
    unit_type = ""

    if len(sys.argv) < 2:
        help()

    first_arg = sys.argv[1]
    if first_arg == "--help":
        help()
    elif first_arg == "--armor" or first_arg == "--recon":
        unit_type = first_arg
    else:
        help()

    main(unit_type)
