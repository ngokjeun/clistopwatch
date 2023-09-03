#!/usr/bin/env python3
from datetime import datetime
import os
import time
import yaml
import argparse

PINK = "\033[95m"
HIDE_CURSOR = "\033[?25l"
SHOW_CURSOR = "\033[?25h"
RESET = "\033[0m"


def show_history(history_file):
    try:
        with open(history_file, 'r') as f:
            history = yaml.safe_load(f)
        if history:
            print("stopwatch history")
            for idx, time in enumerate(history):
                print(f"{idx + 1}. {time}")
        else:
            print("no history available")
    except FileNotFoundError:
        print("no history available")


def main():
    parser = argparse.ArgumentParser(description='a cli stopwatch')
    parser.add_argument('--history', action='store_true',
                        help='show stopwatch history')
    parser.add_argument('--clear', action='store_true',
                        help='clear stopwatch history')
    args = parser.parse_args()

    history_file = os.path.join(os.path.expanduser(
        '~'), 'documents', 'stopwatch_history.yaml')

    if args.clear:
        try:
            with open(history_file, 'w') as f:
                yaml.dump([], f)
            print("byeeee")
        except Exception as e:
            print(f"failed to clear history {e}")
        return

    if args.history:
        show_history(history_file)
        return

    try:
        with open(history_file, 'r') as f:
            history = yaml.safe_load(f)
        if history is None:
            history = []
    except FileNotFoundError:
        history = []

    rows, columns = os.popen('stty size', 'r').read().split()

    start = datetime.now()
    print(HIDE_CURSOR, end="")

    try:
        while True:
            now = datetime.now()
            elapsed = now - start
            hours, remainder = divmod(elapsed.seconds, 3600)
            minutes, seconds = divmod(remainder, 60)

            time_str = f"{hours:02}:{minutes:02}:{seconds:02}"

            padding_time = (int(columns) - len(time_str)) // 2
            centered_time_str = " " * padding_time + time_str

            print(f"\r{PINK}{centered_time_str}{RESET}", end="")
            time.sleep(1)

    except KeyboardInterrupt:
        history.append(time_str)

        try:
            print("\r", end="", flush=True)

            with open(history_file, 'w') as f:
                yaml.dump(history, f)

        except PermissionError:
            print(f"permission denied could not write to {history_file}")

        print(f"\n{SHOW_CURSOR}", end="")
        word = "stopped"
        padding_word = (int(columns) - len(word)) // 2
        centered_word_str = " " * padding_word + word

        try:
            for i in range(8):
                if i % 2 == 0:
                    print(f"\r{centered_word_str}", end="")
                else:
                    print(f"\r{' ' * len(centered_word_str)}", end="")

                time.sleep(0.15)

            print(f"{SHOW_CURSOR}")

        except KeyboardInterrupt:
            print(f"{SHOW_CURSOR}")


if __name__ == '__main__':
    main()
