import subprocess
import re
import os
import platform
import time
import psutil

# To be removed
import tkinter as tk
from tkinter import ttk


# class Scalpel:
def run_dd(input_disk=None, output_image=None):
    # Get the path to the current script's directory
    current_dir = os.path.dirname(os.path.abspath(__file__))
    dd = os.path.join(current_dir, "dd.exe")

    # Get current OS
    current_os = platform.system().lower()
    disk_mount_point = input_disk

    if current_os == "windows":
        disk_mount_point = input_disk + ":/"
        # print(disk_mount_point)
        # return
        # """
        # Get current Disk name i.e E
        # for windows the disk name should be modified to \\.\e:
        # """
        input_disk = input_disk.lower()
        pre_d = "\\\\.\\"
        input_disk = pre_d + input_disk + ":"
        del pre_d

    # scalpel_command = ["scalpel", "-i", "input_image.dd", "-o", "output_directory"]

    input_disk_size = psutil.disk_usage(disk_mount_point).total
    update_progress(0)
    # print("Disk size: ", input_disk_size)
    # return

    dd_command = [
        dd,
        f"if={input_disk}",
        f"of={output_image}",
        "bs=1M",
        "--size",
        "--progress",
    ]
    progress_var.set(0)
    # time.sleep(4)
    # time.sleep(10)
    # update_progress(10)

    # print(f"DD command: {dd_command}")

    # Execute Scalpel and capture output
    process = subprocess.Popen(
        dd_command,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        universal_newlines=True,
    )

    # Try the following
    current_progress_value = 3
    for line in process.stdout:
        current_progress_value = current_progress_value + 1
        # print(f"Line: \n{line}\n")
        if "--progress" in line:
            # progress_str = line.strip().split()[-1]  # Extract the last element
            # progress_str = progress_str.replace(",", "")  # Remove commas
            # current_progress_value = (int(progress_str) / input_disk_size) * 100
            # progress_var.set(current_progress_value)
            progress_str = line.strip().replace(",", "")  # Remove commas
            current_progress_value = (int(progress_str) / input_disk_size) * 100
            progress_var.set(current_progress_value)
        else:
            progress_str = line.strip().replace(",", "")  # Remove commas
            # print(f"Progress line: {line}, Type: {type(line)}")
            try:
                value = int(progress_str)
                current_progress_value = (value / input_disk_size) * 100
                progress_var.set(current_progress_value)
                print("Integer value:", value)
            except ValueError:
                print("Invalid input: not a valid integer")
            # print(f"Progress str: {progress_str}, Type: {type(progress_str)}")
            # progress_int = int(progress_str)
            # print(f"Progress int: {progress_int}, Type: {type(progress_int)}")
            # current_progress_value = (progress_int / input_disk_size) * 100
            # progress_var.set(current_progress_value)

    print("Task completed")
    # print(f"Line: \n{line}\n")
    progress_var.set(100)
    # End try the following

    # print(f"Process: {process}")
    # print(f"\nBefore going through while loop\n")
    # update_progress(19)
    # progress_value = 25
    # while True:
    #     # progress_value = progress_value + 1
    #     # update_progress(progress_value)
    #     # print(f"\nIn while loop\n")
    #     # print(f"\nProgress {process}\n")
    #     line = process.stdout.readline().decode("utf-8")
    #     # update_progress(100)
    #     # print(f"Line: {line}")
    #     if not line:
    #         update_progress(100)
    #         break
    #     else:
    #         print(int(line), type(line))
    #         break
    #     # Example: Extract progress percentage from the line
    #     current_progress_value = (int(line) / input_disk_size) * 100
    #     print(f"Current value: {current_progress_value}")
    #     # break
    #     return
    # match = re.search(r"(\d+)% complete", line)
    # if match:
    #     print("\nMatch found")
    #     progress_percentage = int(match.group(1))
    #     # Update the progress bar here with progress_percentage
    #     update_progress(progress_percentage)


def update_progress(value):
    # Update the progress bar's value
    progress_var.set(value)


def main():
    root = tk.Tk()
    root.title("DD Progress")

    # Create a progress bar
    global progress_var
    progress_var = tk.DoubleVar(value=0)
    progress_bar = ttk.Progressbar(
        root, length=200, mode="determinate", orient="horizontal", variable=progress_var
    )
    progress_bar.pack(pady=10)

    # Disk Image Test
    output_image = "E:\\SDCARD.dd"
    input_disk = "F"

    # Button to start Scalpel
    start_button = tk.Button(
        root, text="Start dd", command=lambda: run_dd(input_disk, output_image)
    )
    start_button.pack()

    root.mainloop()


if __name__ == "__main__":
    main()
