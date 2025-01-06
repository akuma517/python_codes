"""Utility to automate the switching between window1 and window2.
"""

import subprocess
import threading
import time

import click
from pynput import keyboard
from pynput.keyboard import Controller, Key

# control parameter of loop mechanism
stop_program = False


class StopProgramException(Exception):
    """Exception to stop the looping mechanism."""


def activate_window(window_id: str) -> None:
    """Activate the window correspodinding to given id."""
    if window_id:
        subprocess.run(["wmctrl", "-ia", window_id])


def get_window_id_by_title(title: str, result: str) -> str:
    """Get window id based on the title."""
    try:
        for line in result.strip().split("\n"):
            parts = line.split(None, 3)
            if len(parts) >= 4:
                window_id = parts[0]
                window_title = parts[3]

                if title.lower() in window_title.lower():
                    return window_id

        temp_keyboard = Controller()
        temp_keyboard.press(Key.esc)
        temp_keyboard.release(Key.esc)
        raise ValueError(f"No window found with title: {title}")

    except subprocess.CalledProcessError as e:
        temp_keyboard = Controller()
        temp_keyboard.press(Key.esc)
        temp_keyboard.release(Key.esc)
        raise ValueError(e)


def on_press(key: keyboard.Key) -> None:
    """Callback to monitor if ESC is pressed."""
    global stop_program
    if key == keyboard.Key.esc:
        stop_program = True
        raise StopProgramException("Listner Stopped.")


def perform_switching(
    title_to_find_1: str, duration_for_window1_in_secs: int, title_to_find_2: str, duration_for_window2_in_secs: int
) -> None:
    """Switch between window 1 and window 2."""
    global stop_program
    
    # get all active windows in the Linux machine
    all_active_windows = subprocess.check_output(["wmctrl", "-l"], text=True)

    while not stop_program:
        # switch to first window
        first_window = get_window_id_by_title(title_to_find_1, all_active_windows)
        activate_window(first_window)
        time.sleep(duration_for_window1_in_secs)
        # switch to second window
        second_window = get_window_id_by_title(title_to_find_2, all_active_windows)
        activate_window(second_window)
        time.sleep(duration_for_window2_in_secs)


@click.command()
@click.option(
    "--window1",
    "-w1",
    type=str,
    required=True,
    help="Title of the first window.",
)
@click.option(
    "--duration1",
    "-t1",
    type=int,
    required=True,
    help="Duration for the first window.",
)
@click.option(
    "--window2",
    "-w2",
    type=str,
    required=True,
    help="Title of the second window.",
)
@click.option(
    "--duration2",
    "-t2",
    type=int,
    required=True,
    help="Duration for the second window.",
)
def run(window1: str, duration1: int, window2: str, duration2: int) -> None:
    """Run the keyboard listner to monitor the keyboard inputs."""

    # add a listner to stop the process when ESC is pressed
    listener_thread = threading.Thread(target=start_keyboard_listener)
    listener_thread.start()

    perform_switching(window1, duration1, window2, duration2)

    listener_thread.join()


def start_keyboard_listener() -> None:
    """Start keyboard listner for on_press."""
    with keyboard.Listener(on_press=on_press) as listener:
        listener.join()


if __name__ == "__main__":
    """Main function.

    Press ESC to end the process.
    """
    run()
