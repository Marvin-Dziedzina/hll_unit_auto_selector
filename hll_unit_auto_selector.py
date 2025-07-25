import time
import sys
import io
import argparse

import pyautogui
import keyboard

CREATE_UNIT_IMG_PATH = "./assets/create_a_unit.png"
JOIN_OR_CREATE_UNIT_IMG_PATH = "./assets/join_or_create_unit.png"

GOTO_MOUSE_POS_COMMAND = "goto"
CLICK_MOUSE_POS_COMMAND = "click"
WAIT_COMMAND = "wait"
DEFAULT_WAIT_TIME = 0.3

is_running = True


def record(path: str):
    screen_size = pyautogui.size()

    def add_mouse_pos(rec: io.TextIOWrapper):
        print("Added current mouse position to recording")
        pos = pyautogui.position()
        rec.writelines(f"{GOTO_MOUSE_POS_COMMAND} {pos[0]} {pos[1]}\n")

    def add_click(rec: io.TextIOWrapper):
        print("Added click on current mouse position to recording")
        pos = pyautogui.position()
        rec.writelines(f"{CLICK_MOUSE_POS_COMMAND} {pos[0]} {pos[1]}\n")

    def add_wait(rec: io.TextIOWrapper):
        print("Added wait time to recording (Don't forget to change the value)")
        rec.writelines(f"{WAIT_COMMAND} {DEFAULT_WAIT_TIME}\n")

    def wait_for_key_release(key: str):
        while keyboard.is_pressed(key):
            time.sleep(0.002)
    
    print(f"Display size: {pyautogui.size().width}x{pyautogui.size().height}")

    with open(path, mode="w") as rec:
        while is_running:
            time.sleep(0.001)

            if keyboard.is_pressed("ctrl+f1"):
                add_mouse_pos(rec)
                wait_for_key_release("ctrl+f1")
            elif keyboard.is_pressed("ctrl+f2"):
                add_click(rec)
                wait_for_key_release("ctrl+f2")
            elif keyboard.is_pressed("ctrl+f3"):
                add_wait(rec)
                wait_for_key_release("ctrl+f3")


def execute(recording: list[str]):
    def get_xy(tokens: list[str]) -> tuple[int, int]:
        return int(tokens[1]), int(tokens[2])

    for i, line in enumerate(recording):
        tokens = line.strip("\n").split(" ")

        command = tokens[0]

        # Ingore empty lines.
        if command == "":
            continue

        # Check for all valid commands.
        if command == WAIT_COMMAND:
            sleep_duration = float(tokens[1])
            print(f"Sleeping for {sleep_duration}")
            time.sleep(sleep_duration)
        elif command == GOTO_MOUSE_POS_COMMAND:
            x, y = get_xy(tokens)
            print(f"Moving to {x} {y}")
            pyautogui.moveTo(x, y, duration=0.1)
        elif command == CLICK_MOUSE_POS_COMMAND:
            x, y = get_xy(tokens)
            print(f"Clicking on {x} {y}")
            pyautogui.click(x, y)
        elif command == "#":
            # Ignore comments
            continue
        else:
            sys.exit(f"Invalid command found: {command}, line {i + 1}")

def run(path: str):
    # Load recording
    recording = []
    with open(path, mode="r") as rec:
        recording = rec.readlines()

    while is_running:
        time.sleep(0.001)

        try:
            if pyautogui.locateOnScreen(CREATE_UNIT_IMG_PATH, grayscale=True, confidence=0.9) or pyautogui.locateOnScreen(JOIN_OR_CREATE_UNIT_IMG_PATH, grayscale=True, confidence=0.9):
                execute(recording)
        except:
            continue


def main(args: argparse.Namespace):
    def set_dead():
        global is_running
        is_running = False
        sys.exit("User quitted")

    keyboard.add_hotkey("ctrl+f4", set_dead, suppress=True)

    if args.record:
        record(args.record)
    elif args.execute:
        run(args.execute)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_help = True

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--record", type=str, help="Record a new record to the specified file path.")
    group.add_argument("--execute", type=str, help="Execute the specified file.")

    main(parser.parse_args())
