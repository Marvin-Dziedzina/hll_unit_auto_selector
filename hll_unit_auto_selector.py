import time
import sys
import argparse

import pyautogui
from pytweening import easeOutElastic
import keyboard

GOTO_MOUSE_POS_COMMAND = "goto"
CLICK_MOUSE_POS_COMMAND = "click"
WAIT_COMMAND = "wait"
DEFAULT_WAIT_TIME = 0.3

is_running = True


def display_screen_size():
    screen_size = pyautogui.size()
    print(f"Display size: {screen_size.width}x{screen_size.height}")


def record(path: str):
    def instruction_count_str(rec_buf: list[str]) -> str:
        return f"Instruction Number: {len(rec_buf)}"

    def add_mouse_pos(rec_buf: list[str]):
        pos = pyautogui.position()
        print(
            f"Added {GOTO_MOUSE_POS_COMMAND} {pos[0]} {pos[1]}; {instruction_count_str(rec_buf)}"
        )
        rec_buf.append(f"{GOTO_MOUSE_POS_COMMAND} {pos[0]} {pos[1]}\n")

    def add_click(rec_buf: list[str]):
        pos = pyautogui.position()
        print(
            f"Added {CLICK_MOUSE_POS_COMMAND} {pos[0]} {pos[1]}; {instruction_count_str(rec_buf)}"
        )
        rec_buf.append(f"{CLICK_MOUSE_POS_COMMAND} {pos[0]} {pos[1]}\n")

    def add_wait(rec_buf: list[str]):
        print(
            f"Added {WAIT_COMMAND} {DEFAULT_WAIT_TIME}; {instruction_count_str(rec_buf)}; (You can change the duration in the recording file)"
        )
        rec_buf.append(f"{WAIT_COMMAND} {DEFAULT_WAIT_TIME}\n")

    def wait_for_key_release(key: str):
        while keyboard.is_pressed(key):
            time.sleep(0.01)

    display_screen_size()

    rec_buf = []
    while is_running:
        time.sleep(0.01)

        if keyboard.is_pressed("ctrl+f1"):
            add_mouse_pos(rec_buf)
            wait_for_key_release("ctrl+f1")
        elif keyboard.is_pressed("ctrl+f2"):
            add_click(rec_buf)
            wait_for_key_release("ctrl+f2")
        elif keyboard.is_pressed("ctrl+f3"):
            add_wait(rec_buf)
            wait_for_key_release("ctrl+f3")

    with open(path, mode="w") as rec:
        rec.writelines(rec_buf)


def execute(recording: list[str]):
    def get_xy(tokens: list[str]) -> tuple[int, int]:
        return int(tokens[1]), int(tokens[2])

    print("Starting to execute...")
    for i, line in enumerate(recording):
        line = line.rstrip("\n")

        # Ingore comments and empty lines .
        if line.lstrip().startswith("#") or not line.strip():
            continue

        tokens = line.split(" ")
        command = tokens[0]

        # Check for all valid commands.
        if command == WAIT_COMMAND:
            sleep_duration = float(tokens[1])
            print(f"Waiting for {sleep_duration}")
            time.sleep(sleep_duration)
        elif command == GOTO_MOUSE_POS_COMMAND:
            x, y = get_xy(tokens)
            print(f"Moving to {x} {y}")
            pyautogui.moveTo(x, y, duration=0.2, tween=easeOutElastic)
        elif command == CLICK_MOUSE_POS_COMMAND:
            x, y = get_xy(tokens)
            print(f"Clicking on {x} {y}")
            pyautogui.click(x, y, duration=0.2, tween=easeOutElastic)
        else:
            sys.exit(f"Invalid command found: {command}, line {i + 1}")

    print("Done executing.")


def run(path: str):
    # Load recording
    recording = []
    with open(path, mode="r") as rec:
        recording = rec.readlines()

    keyboard.add_hotkey("f4", execute, args=(recording,), suppress=True)

    while is_running:
        keyboard.wait("ctrl+f4")


def main(args: argparse.Namespace):
    def set_dead():
        global is_running
        is_running = False

    keyboard.add_hotkey("ctrl+f4", set_dead, suppress=True)

    if args.record:
        record(args.record)
    elif args.execute:
        run(args.execute)
    elif args.size:
        display_screen_size()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="hll_unit_auto_selector",
        usage="hll_unit_auto_selector [ARGUMENT] [PATH]",
        epilog=f"""
        Recording:
            CTRL+F1: move the mouse to the current position.
            CTRL+F2: move to and click on the current mouse position.
            CTRL+F3: wait for {DEFAULT_WAIT_TIME}. This can be manually changed in the record file.
            CTRL+F4: save and quit.
        
        Executing:
            F4: Execute
            CTRL+F4: quit. 
        """,
    )

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        "-r",
        "--record",
        metavar="PATH",
        type=str,
        help="Record a new record to the specified file path.",
    )
    group.add_argument(
        "-e", "--execute", metavar="PATH", type=str, help="Execute the specified file."
    )
    group.add_argument("-s", "--size", action="store_true")

    main(parser.parse_args())
