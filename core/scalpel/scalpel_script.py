import subprocess
import re
import os

# To be removed
import tkinter as tk
from tkinter import ttk


# class Scalpel:
def run_scalpel(input_disk_image=None, output_directory=None):
    # Get the path to the current script's directory
    current_dir = os.path.dirname(os.path.abspath(__file__))
    scalpel = os.path.join(current_dir, "scalpel.exe")

    print(f"Disk image: {input_disk_image}, Output dir: {output_directory}")

    # scalpel_command = ["scalpel", "input_image.dd", "-o", "output_directory"]
    scalpel_command = [scalpel, input_disk_image, "-o", output_directory]

    print(f"Scalpel command: {scalpel_command}")

    # Execute Scalpel and capture output
    process = subprocess.Popen(
        scalpel_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )

    print(f"Process: {process}")

    while True:
        line = process.stdout.readline().decode("utf-8")
        if not line:
            break
        # Example: Extract progress percentage from the line
        match = re.search(r"(\d+)% complete", line)
        if match:
            progress_percentage = int(match.group(1))
            # Update the progress bar here with progress_percentage
            update_progress(progress_percentage)


def update_progress(value):
    # Update the progress bar's value
    progress_var.set(value)


def main():
    root = tk.Tk()
    root.title("Scalpel Progress")

    # Create a progress bar
    global progress_var
    progress_var = tk.DoubleVar(value=0)
    progress_bar = ttk.Progressbar(
        root, length=200, mode="determinate", orient="horizontal", variable=progress_var
    )
    progress_bar.pack(pady=10)

    # Disk Image Test
    disk_image = "F:\\FYP\\DISK_IMAGES\\USB32GB.dd"
    output_dir = "E:\\OUTPUT\\"

    # Button to start Scalpel
    start_button = tk.Button(
        root, text="Start Scalpel", command=lambda: run_scalpel(disk_image, output_dir)
    )
    start_button.pack()

    root.mainloop()


if __name__ == "__main__":
    main()
