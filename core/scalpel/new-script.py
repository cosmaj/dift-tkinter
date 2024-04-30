import tkinter as tk
import tkinter.filedialog
import tkinter.ttk
import subprocess
import threading
import time
import os
import re


def execute_scalpel(input_file, output_folder):
    current_directory = os.path.dirname(os.path.realpath(__file__))
    command = [
        os.path.join(current_directory, "scalpel.exe"),
        "-c",
        os.path.join(current_directory, "scalpel.conf"),
        input_file,
        "-o",
        output_folder,
    ]
    process = subprocess.Popen(
        command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True
    )
    return process


def update_progress_bar(progress_bar, progress_var, process):
    progress_var.set(0)
    max_value = 100
    progress_bar.config(maximum=max_value)
    root.update_idletasks()
    # print("1: Progress bar configured")

    file_size = 0
    with open(input_file, "rb") as f:
        file_size = len(f.read())
    # print("2: File size determined")

    processed_bytes = 0
    current_pass = 0
    total_passes = 0
    pass_started = False
    accumulated_bytes = 0
    carving_finished = False

    while not carving_finished:
        # print("3: Inside while loop")
        line = process.stdout.readline()
        print(f"Line: {line}")

        if line.strip().endswith("MB"):
            processed_mb = float(line.strip()[:-3])
            processed_bytes = int(processed_mb * 1024 * 1024)
            accumulated_bytes += processed_bytes
            if pass_started:
                progress_var.set(int((accumulated_bytes / file_size) * max_value))
                root.update_idletasks()
                # print(f"4: Progress updated to {progress_var.get()}")

        # Check for the current pass and total passes
        pass_match = re.search(r"Image file pass (\d+)/(\d+)\.", line)
        if pass_match:
            current_pass = int(pass_match.group(1))
            total_passes = int(pass_match.group(2))
            pass_started = True
            print(
                f"5: Pass info updated. Current pass: {current_pass}, Total passes: {total_passes}"
            )
            accumulated_bytes = 0  # Reset accumulated_bytes for each pass

        # Check if carving is finished
        if (
            current_pass == total_passes
            and line.strip() == f"Image file pass {current_pass}/{total_passes}."
        ):
            carving_finished = True

        # time.sleep(0.1)

    # Update the progress bar to 100% when all passes are completed
    if current_pass == total_passes:
        progress_var.set(max_value)
        root.update_idletasks()
        # print("6: Progress updated to 100%")
        print("Carving process has finished.")

    print("7: Exiting update_progress_bar function")


def start_carving():
    global input_file, output_folder

    input_file = tkinter.filedialog.askopenfilename(title="Select input file")
    output_folder = tkinter.filedialog.askdirectory(title="Select output folder")

    process = execute_scalpel(input_file, output_folder)

    progress_thread = threading.Thread(
        target=update_progress_bar, args=(progress_bar, progress_var, process)
    )
    progress_thread.start()


root = tk.Tk()
root.title("Scalpel GUI")

frame = tk.Frame(root)
frame.pack(pady=10)

button = tk.Button(frame, text="Start carving", command=start_carving)
button.pack(side=tk.LEFT, padx=(0, 10))

progress_var = tk.DoubleVar()
progress_bar = tkinter.ttk.Progressbar(frame, variable=progress_var)
progress_bar.pack(side=tk.LEFT, fill=tk.X, expand=True)

root.mainloop()
