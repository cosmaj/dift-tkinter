import re
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog

# import ttkbootstrap as tb
# from ttkbootstrap.toast import ToastNotification
from tkinter import messagebox
from PIL import Image, ImageTk
import tempfile
import os
import uuid
import platform
import psutil
import subprocess
import threading
import phonenumbers
import time
import getpass
import platform
from core.utils.dates import Utils
from winotify import Notification, audio

# -------------------------- DEFINING GLOBAL VARIABLES -------------------------

selectionbar_color = "#eff5f6"
sidebar_color = "#F5E1FD"
header_color = "#53366b"
visualisation_frame_color = "#ffffff"

# ------------------------------- ROOT WINDOW ----------------------------------


class TkinterApp(tk.Tk):
    """
    The class creates a header and sidebar for the application. Also creates
    two submenus in the sidebar, one for Image curving with options to
    Disk mount and beggin recovery and another for
    Image Autheticity check, with options to upload image and analyse the
    image.
    """

    def __init__(self):
        tk.Tk.__init__(self)
        self.title("Digital Forensics App")

        # ------------- BASIC APP LAYOUT -----------------

        self.geometry("1100x700")
        self.resizable()
        self.title("Digital Image Forensic Tool")
        self.config(background=selectionbar_color)
        icon = tk.PhotoImage(file="images\\dift-logo.png")
        self.iconphoto(True, icon)

        # ---------------- HEADER ------------------------

        self.header = tk.Frame(self, bg=header_color)
        self.header.place(relx=0.3, rely=0, relwidth=0.7, relheight=0.1)

        # ---------------- SIDEBAR -----------------------
        # CREATING FRAME FOR SIDEBAR
        self.sidebar = tk.Frame(self, bg=sidebar_color)
        self.sidebar.place(relx=0, rely=0, relwidth=0.3, relheight=1)

        # APPLICATION LOGO AND NAME
        self.brand_frame = tk.Frame(self.sidebar, bg=sidebar_color)
        self.brand_frame.place(relx=0, rely=0, relwidth=1, relheight=0.15)
        self.uni_logo = icon.subsample(9)
        logo = tk.Label(self.brand_frame, image=self.uni_logo, bg=sidebar_color)
        logo.place(x=5, y=20)

        # uni_name = tk.Label(
        #     self.brand_frame, text="", bg=sidebar_color, font=("", 15, "bold")
        # )
        # uni_name.place(x=55, y=27, anchor="w")

        # uni_name = tk.Label(
        #     self.brand_frame,
        #     # text="Digital Image Forensic Tool",
        #     bg=sidebar_color,
        #     font=("", 15, "bold"),
        # )
        # uni_name.place(x=55, y=60, anchor="w")

        # SUBMENUS IN SIDE BAR

        # # SUBMENU 1
        self.submenu_frame = tk.Frame(self.sidebar, bg=sidebar_color)
        self.submenu_frame.place(relx=0, rely=0.2, relwidth=1, relheight=0.85)
        submenu1 = SidebarSubMenu(
            self.submenu_frame,
            sub_menu_heading="SUBMENU",
            sub_menu_options=[
                "Register Case",
                "Image Carving",
                "Image Authenticity",
            ],
        )
        submenu1.options["Register Case"].config(
            command=lambda: self.show_frame(Home, "Register Case")
        )
        submenu1.options["Image Carving"].config(
            command=lambda: self.show_frame(
                ImageCarving, "Mount Disk to begin recovery"
            )
        )
        submenu1.options["Image Authenticity"].config(
            command=lambda: self.show_frame(ImageAutheticity, "Image Autheticity Check")
        )

        submenu1.place(relx=0, rely=0.025, relwidth=1, relheight=0.3)

        # --------------------  MULTI PAGE SETTINGS ----------------------------

        container = tk.Frame(self)
        container.config(highlightbackground="#808080", highlightthickness=0.5)
        container.place(relx=0.3, rely=0.1, relwidth=0.7, relheight=0.9)

        self.frames = {}

        for F in (
            Home,
            ImageCarving,
            ImageAutheticity,
        ):

            frame = F(container, self)
            self.frames[F] = frame
            frame.place(relx=0, rely=0, relwidth=1, relheight=1)
        self.show_frame(Home, "Register Case")

    def show_frame(self, cont, title):
        """
        The function 'show_frame' is used to raise a specific frame (page) in
        the tkinter application and update the title displayed in the header.

        Parameters:
        cont (str): The name of the frame/page to be displayed.
        title (str): The title to be displayed in the header of the application.

        Returns:
        None
        """
        frame = self.frames[cont]

        # Check if the clicked button is ImageCurving to refresh the available disks
        if cont == ImageCarving:
            frame.refresh_data()

        # Added
        for widget in self.header.winfo_children():
            widget.destroy()
        label = tk.Label(
            self.header, text=title, font=("Helvetica", 17), bg=header_color, fg="white"
        )
        label.pack(side=tk.LEFT, padx=10)
        # End Added
        frame.tkraise()


# ------------------------ MULTIPLE FRAMES ------------------------------------


class Home(tk.Frame):
    def __init__(self, parent, controller):

        tk.Frame.__init__(self, parent)

        # Load the image
        self.image = Image.open("images\\cover.png")
        # self.image = self.image.resize((800, 600))  # Adjust the size as needed
        self.image = ImageTk.PhotoImage(self.image)

        # Create a canvas for the image
        self.canvas = tk.Canvas(self)  # Adjust the size as needed
        self.canvas.pack(fill=tk.BOTH, expand=True)

        # Display the image on the canvas
        self.canvas.create_image(0, 0, image=self.image, anchor=tk.NW)

        # Create a text for the title
        self.title_text = self.canvas.create_text(
            400,
            400,
            text="CREATE NEW CASE TO START THE ANALYSIS",
            fill="white",
            font=("Arial", 20, "bold"),
        )  # Adjust the position as needed
        self.sub_title_text = self.canvas.create_text(
            400,
            450,
            text="Discover more with AI Assistance",
            fill="white",
            font=("Arial", 14, "bold"),
        )  # Adjust the position as needed

        # Create a button for starting the project
        self.start_button = tk.Button(
            self,
            text="NEW CASE >",
            command=self.open_popup,
            bg=header_color,
            fg="white",
            padx=10,
            pady=5,
            borderwidth=0,
            relief="flat",
            font=("Arial", 12, "bold"),
        )
        self.start_button.place(
            relx=0.9, rely=0.9, anchor=tk.SE
        )  # Adjust the position as needed

    def open_popup(self):
        popup = Popup(self)

    def resize_image(self, event=None):
        # Get the current width and height of the window
        width = self.winfo_width()
        height = self.winfo_height()

        # Resize the image to fit the window dimensions
        self.image = self.image.resize((width, height))
        self.image = ImageTk.PhotoImage(self.image)

        # Update the image on the canvas
        self.canvas.delete(self.image_on_canvas)
        self.image_on_canvas = self.canvas.create_image(
            0, 0, image=self.image, anchor=tk.NW
        )


class ImageCarving(tk.Frame):
    from core.disks.disk import Disk

    def __init__(self, parent, controller):

        tk.Frame.__init__(self, parent)

        # Create Tree Styles
        style = ttk.Style()
        style.configure("Treeview", font=("Helvetica", 12))

        # Create a Treeview widget
        self.tree = ttk.Treeview(self, style="Treeview")

        # Define the columns
        self.tree["columns"] = ("one", "two", "three", "four", "five")

        # Format the columns
        self.tree.column("#0", width=50, minwidth=50, stretch=tk.YES)
        self.tree.column("one", width=80, minwidth=80, stretch=tk.YES)
        self.tree.column("two", width=100, minwidth=80, stretch=tk.YES)
        self.tree.column("three", width=80, minwidth=50, stretch=tk.YES)
        self.tree.column("four", width=270, minwidth=270, stretch=tk.YES)
        self.tree.column("five", width=150, minwidth=150, stretch=tk.YES)

        # Define the column headings
        # self.tree.heading("#0", text="Disk Name", anchor=tk.W)
        # self.tree.heading("one", text="Mounting point", anchor=tk.W)
        # self.tree.heading("two", text="FS Type", anchor=tk.W)
        # self.tree.heading("three", text="Size", anchor=tk.W)
        self.tree.heading("#0", text="Disk", anchor=tk.W)
        self.tree.heading("one", text="Mountpoint", anchor=tk.W)
        self.tree.heading("two", text="Fstype", anchor=tk.W)
        self.tree.heading("three", text="Opts", anchor=tk.W)
        self.tree.heading("four", text="Total", anchor=tk.W)
        self.tree.heading("five", text="Used", anchor=tk.W)

        # Bind the treeview selection event to a method
        self.tree.bind("<<TreeviewSelect>>", self.on_disk_select)

        # Create a tag for the odd rows
        self.tree.tag_configure("oddrow", background="white")

        # Create a tag for the even rows
        self.tree.tag_configure("evenrow", background="lightgrey")

        # Call the method to populate the Treeview
        self.refresh_data()

        # Creating disk image Progress Frame
        disk_image_frame = tk.LabelFrame(self, text="Disk image Acquisition")
        disk_image_frame.pack(pady=3, padx=2, fill="x")

        # Create a progress bar
        global disk_image_progress_var
        disk_image_progress_var = tk.DoubleVar(value=0)
        progress_bar = ttk.Progressbar(
            disk_image_frame,
            length=200,
            mode="determinate",
            orient="horizontal",
            variable=disk_image_progress_var,
        )
        progress_bar.pack(pady=10, padx=10, fill="x")

        # Curving Progress Frame
        image_recovering_frame = tk.LabelFrame(self, text="Image Curving")
        image_recovering_frame.pack(pady=5, padx=2, fill="x")

        # Create a progress bar
        global image_curving_progress_var
        image_curving_progress_var = tk.DoubleVar(value=0)
        global curving_progress_bar
        curving_progress_bar = ttk.Progressbar(
            image_recovering_frame,
            length=200,
            mode="determinate",
            orient="horizontal",
            variable=image_curving_progress_var,
        )
        curving_progress_bar.pack(pady=10, padx=10, fill="x")

        # Start Curving button
        # Create Save and Cancel buttons
        self.curve_button = tk.Button(
            self,
            text="Start Recovery",
            command=self.begin_curving,
            bg=header_color,
            fg="white",
            padx=10,
            pady=5,
            borderwidth=0,
            relief="flat",
            font=("Arial", 12, "bold"),
        )

        # Grid the Save and Cancel buttons at the bottom right of the form
        self.curve_button.pack(side="bottom", anchor="e", padx=10, pady=10)

    def begin_curving(self):
        # Validate the form fields
        if not self.validate_before_curving():
            return

        # Get Input disk(disk letter) from the selected disk
        input_disk = selected_disk["text"]

        # Get output disk image
        temp_path = tempfile.gettempdir()
        output_image = os.path.join(temp_path, f"{uuid.uuid4()}.dd")
        self.run_dd(input_disk, output_image)

        # Get disk image hash
        disk_image_md5, disk_image_sha1 = self.calulate_hashes(output_image)
        form_data["disk_image_md5_begin"] = disk_image_md5
        form_data["disk_image_sha1_begin"] = disk_image_sha1

        # call Execute scalpel
        self.start_carving(output_image, form_data["directory"])

    def validate_before_curving(self):
        # Check if Case was created
        try:
            if form_data:
                ...
        except:
            messagebox.showwarning("Warning", "Start by creating new case")
            return False

        # verify the disk is selected
        try:
            if selected_disk:
                ...
        except:
            messagebox.showwarning("Warning", "Select disk to recover from")
            return False
        # If all the fields are filled out, return True
        return True

    def refresh_data(self):
        # Clear the existing tree
        for i in self.tree.get_children():
            self.tree.delete(i)

        disk_instance = self.Disk()
        self.disks = disk_instance.get_disks()
        # print(self.disks)

        # # Add the disks to the Treeview
        # for disk in self.disks:
        #     self.tree.insert(
        #         "",
        #         0,
        #         text=disk["device"],
        #         values=(
        #             disk["mountpoint"],
        #             disk["fstype"],
        #             disk["opts"],
        #             disk["disk_usage"]["total"],
        #             disk["disk_usage"]["used"],
        #         ),
        #     )

        # Add the disks to the Treeview
        for i, disk in enumerate(self.disks):
            if i % 2 == 0:
                self.tree.insert(
                    "",
                    "end",
                    text=disk["device"],
                    values=(
                        disk["mountpoint"],
                        disk["fstype"],
                        disk["opts"],
                        disk["disk_usage"]["total"],
                        disk["disk_usage"]["used"],
                    ),
                    tags=("evenrow",),
                )
            else:
                self.tree.insert(
                    "",
                    "end",
                    text=disk["device"],
                    values=(
                        disk["mountpoint"],
                        disk["fstype"],
                        disk["opts"],
                        disk["disk_usage"]["total"],
                        disk["disk_usage"]["used"],
                    ),
                    tags=("oddrow",),
                )

        # Pack the Treeview to the frame
        self.tree.pack(fill=tk.X, expand=0)

    def on_disk_select(self, event):
        # Get selected item(Disk)
        global selected_disk
        selected_disk = None
        try:
            selected_disk = self.tree.selection()[0]
            selected_disk = self.tree.item(selected_disk)
        except Exception as e:
            print(f"Some errors: {e}")

    # Take disk Image
    def run_dd(self, input_disk=None, output_image=None):
        # Get the path to the current script's directory
        current_dir = os.path.dirname(os.path.abspath(__name__))
        dd = os.path.join(current_dir, "core", "dd", "dd.exe")

        # Get current OS
        current_os = platform.system().lower()
        disk_mount_point = input_disk

        if current_os == "windows":
            disk_mount_point = input_disk + ":/"
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

        dd_command = [
            dd,
            f"if={input_disk}",
            f"of={output_image}",
            "bs=1M",
            "--size",
            "--progress",
        ]
        self.update_disk_copying_progress(0)
        app.update_idletasks()

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
            if "--progress" in line:
                # progress_str = line.strip().split()[-1]  # Extract the last element
                # progress_str = progress_str.replace(",", "")  # Remove commas
                # current_progress_value = (int(progress_str) / input_disk_size) * 100
                # disk_image_progress_var.set(current_progress_value)
                progress_str = line.strip().replace(",", "")  # Remove commas
                current_progress_value = (int(progress_str) / input_disk_size) * 100
                # disk_image_progress_var.set(current_progress_value)
                self.update_disk_copying_progress(current_progress_value)
                app.update_idletasks()
            else:
                progress_str = line.strip().replace(",", "")  # Remove commas
                try:
                    value = int(progress_str)
                    current_progress_value = (value / input_disk_size) * 100
                    self.update_disk_copying_progress(current_progress_value)
                    app.update_idletasks()
                    # print("Integer value:", value)
                except ValueError:
                    print("Invalid input: not a valid integer")
                # print(f"Progress str: {progress_str}, Type: {type(progress_str)}")
                # progress_int = int(progress_str)
                # print(f"Progress int: {progress_int}, Type: {type(progress_int)}")
                # current_progress_value = (progress_int / input_disk_size) * 100
                # disk_image_progress_var.set(current_progress_value)

        print("Disk Acquisition Task was completed successfully!")
        # print(f"Line: \n{line}\n")
        self.update_disk_copying_progress(100)
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

    def update_disk_copying_progress(self, value):
        disk_image_progress_var.set(value)

    # Recovering/Curving process by Scalpel
    def execute_scalpel(self, input_file, output_folder):
        current_directory = os.path.dirname(os.path.realpath(__file__))
        command = [
            os.path.join(current_directory, "core", "scalpel", "scalpel.exe"),
            "-c",
            os.path.join(current_directory, "core", "scalpel", "scalpel.conf"),
            input_file,
            "-o",
            output_folder,
        ]
        process = subprocess.Popen(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            universal_newlines=True,
        )
        return process

    def update_progress_bar(
        self, input_file, curving_progress_bar, image_curving_progress_var, process
    ):
        image_curving_progress_var.set(0)
        max_value = 100
        curving_progress_bar.config(maximum=max_value)
        app.update_idletasks()
        # print("1: Progress bar configured")

        file_size = 0
        file_size = os.path.getsize(input_file)
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
            # print(f"Line: {line}")

            if line.strip().endswith("ETA"):
                # print(f"It ends with ETA")
                data_array = line.split()
                percentage_str = data_array[1][:-1]
                # size_processed = data_array[2]
                # unit_processed = data_array[3]

                try:
                    # print(f"Data type: {type(percentage_str)}, Value: {percentage_str}")
                    image_curving_progress_var.set(float(percentage_str))
                    app.update_idletasks()
                except Exception as err:
                    print("Issue while processing percentage string")
                    print(err)

                # processed_mb = float(line.strip()[:-3])
                # processed_bytes = int(processed_mb * 1024 * 1024)
                # accumulated_bytes += processed_bytes
                # if pass_started:
                #     image_curving_progress_var.set(int((accumulated_bytes / file_size) * max_value))
                #     root.update_idletasks()
                #     print(f"4: Progress updated to {image_curving_progress_var.get()}")

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

            # Try get the recovery summary
            if line.strip().startswith("jpg with header") and line.strip().endswith(
                "files"
            ):
                jpg_count = line.strip().split()[-2]
                try:
                    jpg_count = int(jpg_count)
                    form_data["jpg_count"] = jpg_count
                    del jpg_count
                except Exception as err:
                    print(f"Error while processing jpg result summary: {err}")

            elif line.strip().startswith("png with header") and line.strip().endswith(
                "files"
            ):
                png_count = line.strip().split()[-2]
                try:
                    png_count = int(png_count)
                    form_data["png_count"] = png_count
                    del png_count
                except Exception as err:
                    print(f"Error while processing png result summary: {err}")

            # Check if carving is finished
            if (
                current_pass == total_passes
                and line.strip() == f"Image file pass {current_pass}/{total_passes}."
            ):
                carving_finished = True

            time.sleep(0.1)
            # Break out of loop if no data in line
            if not line:
                break

        # Update the progress bar to 100% when all passes are completed
        if current_pass == total_passes:
            image_curving_progress_var.set(max_value)
            app.update_idletasks()

            # Calculate disk image hash
            disk_image_md5, disk_image_sha1 = self.calulate_hashes(input_file)
            form_data["disk_image_md5_end"] = disk_image_md5
            form_data["disk_image_sha1_end"] = disk_image_sha1
            # form_data["data_curving_ended_at"] = self.ge

            messagebox.showinfo("Nofication", "Carving process has finished.")

        # Remove the temp input file
        if os.path.exists(input_file):
            try:
                os.remove(input_file)
            except Exception as err:
                print(f"Failed to remove the input file: {input_file}")
                print(f"Error: {err}")
        print("7: Exiting update_progress_bar function")
        print(form_data)

    def calulate_hashes(self, file_name=None):
        from hashlib import md5, sha1
        from mmap import mmap, ACCESS_READ

        if file_name:
            with open(file_name) as file, mmap(
                file.fileno(), 0, access=ACCESS_READ
            ) as file:
                return md5(file).hexdigest(), sha1(file).hexdigest()

    def start_carving(self, input_file, output_folder):

        process = self.execute_scalpel(input_file, output_folder)

        progress_thread = threading.Thread(
            target=self.update_progress_bar,
            args=(
                input_file,
                curving_progress_bar,
                image_curving_progress_var,
                process,
            ),
        )
        progress_thread.start()


class ImageAutheticity(tk.Frame):
    def __init__(self, parent, controller):

        tk.Frame.__init__(self, parent)

        label = tk.Label(self, text="Check Image Autheticity", font=("Arial", 15))
        label.pack()


# ----------------------------- CUSTOM WIDGETS ---------------------------------


class SidebarSubMenu(tk.Frame):
    """
    A submenu which can have multiple options and these can be linked with
    functions.
    """

    def __init__(self, parent, sub_menu_heading, sub_menu_options):
        """
        parent: The frame where submenu is to be placed
        sub_menu_heading: Heading for the options provided
        sub_menu_operations: Options to be included in sub_menu
        """
        tk.Frame.__init__(self, parent)
        self.config(bg=sidebar_color)
        self.sub_menu_heading_label = tk.Label(
            self,
            text=sub_menu_heading,
            bg=sidebar_color,
            fg="#333333",
            font=("Arial", 10),
        )
        self.sub_menu_heading_label.place(x=30, y=10, anchor="w")

        sub_menu_sep = ttk.Separator(self, orient="horizontal")
        sub_menu_sep.place(x=30, y=30, relwidth=0.8, anchor="w")

        self.options = {}
        for n, x in enumerate(sub_menu_options):
            self.options[x] = tk.Button(
                self,
                text=x,
                bg=sidebar_color,
                font=("Arial", 9, "bold"),
                bd=0,
                cursor="hand2",
                activebackground="#ffffff",
            )
            self.options[x].place(x=30, y=45 * (n + 1), anchor="w")


# ----------------------------- POPUP FORM --------------------------------------
class Popup(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)

        self.title("New Project")

        # Set the size of the popup window
        # self.geometry("600x400")  # Adjust the size as needed

        # Make the input fields expand to fill the available space
        self.columnconfigure(1, weight=1)

        # # Create Case Details Frame
        # case_details_frame = tk.LabelFrame(self, text="Case Details")
        # case_details_frame.pack(pady=5, padx=2, fill="x")

        # # Create Evidence Details Frame
        # evidence_details_frame = tk.LabelFrame(self, text="Ecidence/Device Details")
        # evidence_details_frame.pack(pady=5, padx=2, fill="x")

        # # Investigator Details Frame
        # investigator_details_frame = tk.LabelFrame(self, text="investigator Details")
        # investigator_details_frame.pack(pady=5, padx=2, fill="x")

        # Create the entry fields
        self.case_name_label = tk.Label(self, text="Case Name:")
        self.case_name_entry = tk.Entry(
            self, width=100
        )  # Set the width of the input field

        self.case_number_label = tk.Label(self, text="Case Number:")
        self.case_number_entry = tk.Entry(
            self, width=100
        )  # Set the width of the input field

        self.investigator_name_label = tk.Label(self, text="Investigator Name:")
        self.investigator_name_entry = tk.Entry(
            self, width=100
        )  # Set the width of the input field

        self.investigator_phone_label = tk.Label(self, text="Investigator Phone:")
        self.investigator_phone_entry = tk.Entry(
            self, width=100
        )  # Set the width of the input field

        self.email_label = tk.Label(self, text="Email Address:")
        self.email_entry = tk.Entry(self, width=100)  # Set the width of the input field

        self.directory_label = tk.Label(self, text="Folder to store results:")
        self.directory_entry = tk.Entry(
            self, width=100
        )  # Set the width of the input field
        self.browse_button = tk.Button(
            self, text="Browse", command=self.browse_directory
        )

        # Create Save and Cancel buttons
        self.cancel_button = tk.Button(
            self,
            text="Cancel",
            command=self.destroy,
            bg="red",
            padx=10,
            pady=5,
            borderwidth=0,
        )
        self.save_button = tk.Button(
            self,
            text="Save",
            command=self.save_and_close,
            bg="green",
            padx=10,
            pady=5,
            borderwidth=0,
        )

        # Grid the entry fields with padding
        self.case_name_label.grid(row=0, column=0, padx=(20, 0), pady=(20, 10))
        self.case_name_entry.grid(row=0, column=1, padx=(0, 20), pady=(20, 10))

        self.case_number_label.grid(row=1, column=0, padx=(20, 0), pady=(10, 10))
        self.case_number_entry.grid(row=1, column=1, padx=(0, 20), pady=(10, 10))

        self.investigator_name_label.grid(row=2, column=0, padx=(20, 0), pady=(10, 10))
        self.investigator_name_entry.grid(row=2, column=1, padx=(0, 20), pady=(10, 10))

        self.investigator_phone_label.grid(row=3, column=0, padx=(20, 0), pady=(10, 10))
        self.investigator_phone_entry.grid(row=3, column=1, padx=(0, 20), pady=(10, 10))

        self.email_label.grid(row=4, column=0, padx=(20, 0), pady=(10, 10))
        self.email_entry.grid(row=4, column=1, padx=(0, 20), pady=(10, 10))

        self.directory_label.grid(row=5, column=0, padx=(20, 0), pady=(10, 10))
        self.directory_entry.grid(row=5, column=1, padx=(0, 20), pady=(10, 10))
        self.browse_button.grid(row=5, column=2, padx=(0, 20), pady=(10, 10))

        # Grid the Save and Cancel buttons at the bottom right of the form
        self.cancel_button.grid(row=6, column=2, padx=(0, 10), pady=(10, 0), sticky="w")
        self.save_button.grid(row=6, column=1, padx=(0, 10), pady=(10, 0), sticky="e")

        # Make the popup form window the only window that can receive events
        self.grab_set()

        # Check if the form data dictionary exists and populate the form fields with the data
        try:
            if form_data:
                self.case_name_entry.insert(0, form_data["case_name"])
                self.case_number_entry.insert(0, form_data["case_number"])
                self.investigator_name_entry.insert(0, form_data["investigator_name"])
                self.investigator_phone_entry.insert(0, form_data["investigator_phone"])
                self.email_entry.insert(0, form_data["email_address"])
                self.directory_entry.insert(0, form_data["directory"])
        except:
            ...

    def browse_directory(self):
        directory = filedialog.askdirectory()
        self.directory_entry.delete(0, tk.END)
        self.directory_entry.insert(0, directory)

    def save_and_close(self):
        # Validate the form fields
        if not self.validate_form():
            return

        # Capture the data entered in the form fields
        case_name = self.case_name_entry.get()
        case_number = self.case_number_entry.get()
        investigator_name = self.investigator_name_entry.get()
        investigator_phone = self.investigator_phone_entry.get()
        email_address = self.email_entry.get()
        directory = self.directory_entry.get()

        # Store the data in a dictionary
        global form_data
        form_data = None
        p_form = platform.uname()
        current_time = Utils()
        form_data = {
            "case_name": case_name,
            "case_number": case_number,
            "case_created_at": current_time.get_current_time(self),
            "investigator_name": investigator_name,
            "investigator_phone": investigator_phone,
            "email_address": email_address,
            "directory": directory,
            "host_os": f"{p_form.system} {p_form.release}",
            "host_name": p_form.node,
            "cpu": p_form.machine,
            "logon_user": getpass.getuser(),
        }
        del p_form

        toast = Notification(
            app_id="DIFT",
            title="Notification",
            msg=f"Case {form_data['case_name']} was created successfuly",
            icon=os.path.join(
                os.path.dirname(os.path.realpath(__file__)), "images", "dift-logo.png"
            ),
            duration="short",
        )
        toast.set_audio(audio.SMS, loop=False)
        toast.show()

        # Print the dictionary to the console
        # print(form_data)

        # Close the popup window
        self.destroy()

    def validate_form(self):
        # Check if all the fields are filled out
        if not self.case_name_entry.get():
            messagebox.showwarning("Warning", "Please enter a case name.")
            return False

        if not self.case_number_entry.get():
            messagebox.showwarning("Warning", "Please enter a case number.")
            return False

        if not self.investigator_name_entry.get():
            messagebox.showwarning("Warning", "Please enter the investigator's name.")
            return False

        if not all(
            c.isalpha() or c.isspace()
            for c in self.investigator_name_entry.get().strip()
        ):
            messagebox.showwarning(
                "Warning",
                "Investigator's name should contain letters and whitespaces only.",
            )
            return False

        if not self.investigator_phone_entry.get():
            messagebox.showwarning(
                "Warning", "Please enter the investigator's phone number."
            )
            return False

        if not self.check_phone_number(self.investigator_phone_entry.get().strip()):
            messagebox.showwarning("Warning", "Investigator's phone number is invalid.")
            return False

        if not self.email_entry.get():
            messagebox.showwarning("Warning", "Please enter an email address.")
            return False

        if not self.check_email(self.email_entry.get()):
            messagebox.showwarning("Warning", "Please enter a valid email address.")
            return False

        if not self.directory_entry.get():
            messagebox.showwarning("Warning", "Please select a directory.")
            return False

        # If all the fields are filled out, return True
        return True

    def check_email(self, email):
        # Valid TDL can be A-Za-z length from 2 to 7
        regex = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b"
        return re.fullmatch(regex, email)

    def check_phone_number(self, phone_number):
        try:
            parsed_number = phonenumbers.parse(phone_number, "TZ")
            return phonenumbers.is_valid_number(parsed_number)
        except phonenumbers.phonenumberutil.NumberParseException:
            return False


# --------------------------- MAIN APP -----------------------------------
global app
app = TkinterApp()
app.mainloop()
