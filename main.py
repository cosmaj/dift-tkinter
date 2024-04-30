import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
from PIL import Image, ImageTk

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
        self.resizable(0, 0)
        self.title("Digital Image Forensic Tool")
        self.config(background=selectionbar_color)
        icon = tk.PhotoImage(file="images\\logo.png")
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

        uni_name = tk.Label(
            self.brand_frame, text="DIFT", bg=sidebar_color, font=("", 15, "bold")
        )
        uni_name.place(x=55, y=27, anchor="w")

        uni_name = tk.Label(
            self.brand_frame,
            text="Digital Image Forensic Tool",
            bg=sidebar_color,
            font=("", 15, "bold"),
        )
        uni_name.place(x=55, y=60, anchor="w")

        # SUBMENUS IN SIDE BAR

        # # SUBMENU 1
        self.submenu_frame = tk.Frame(self.sidebar, bg=sidebar_color)
        self.submenu_frame.place(relx=0, rely=0.2, relwidth=1, relheight=0.85)
        submenu1 = SidebarSubMenu(
            self.submenu_frame,
            sub_menu_heading="SUBMENU 1",
            sub_menu_options=[
                "Home",
                "Image Carving",
                "Image Authenticity",
            ],
        )
        submenu1.options["Home"].config(command=lambda: self.show_frame(Home, "Home"))
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
            NewProject,
            ImageCarving,
            ImageAutheticity,
        ):

            frame = F(container, self)
            self.frames[F] = frame
            frame.place(relx=0, rely=0, relwidth=1, relheight=1)
        self.show_frame(Home, "Home")

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
        self.title_text = self.canvas.create_text(400, 400, text="CREATE NEW CASE TO START THE ANALYSIS", fill="white", font=("Arial", 20, "bold"))  # Adjust the position as needed
        self.sub_title_text = self.canvas.create_text(400, 450, text="Discover more with AI Assistance", fill="white", font=("Arial", 14, "bold"))  # Adjust the position as needed
        
        # Create a button for starting the project
        self.start_button = tk.Button(self, text="NEW CASE >", command=self.open_popup, bg=header_color, fg="white", padx=10, pady=5, borderwidth=0,relief='flat', font=('Arial', 12, 'bold'))
        self.start_button.place(relx=0.9, rely=0.9, anchor=tk.SE)  # Adjust the position as needed

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
        self.image_on_canvas = self.canvas.create_image(0, 0, image=self.image, anchor=tk.NW)


class NewProject(tk.Frame):
    def __init__(self, parent, controller):

        tk.Frame.__init__(self, parent)

        label = tk.Label(self, text="Project Info goes here", font=("Arial", 24))
        label.pack()


class ImageCarving(tk.Frame):
    from core.disks.disk import Disk

    def __init__(self, parent, controller):

        tk.Frame.__init__(self, parent)

        # label = tk.Label(self, text="Return deleted Images", font=("Arial", 15))
        # label.pack()

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
        # Get selected item
        selected_disk = None
        try:
            selected_disk = self.tree.selection()[0]
            print("Selected item:", self.tree.item(selected_disk))
        except Exception as e:
            print(f"Some errors: {e}")


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

        # Create the entry fields
        self.case_name_label = tk.Label(self, text="Case Name:")
        self.case_name_entry = tk.Entry(self, width=100)  # Set the width of the input field

        self.case_number_label = tk.Label(self, text="Case Number:")
        self.case_number_entry = tk.Entry(self, width=100)  # Set the width of the input field

        self.investigator_name_label = tk.Label(self, text="Investigator Name:")
        self.investigator_name_entry = tk.Entry(self, width=100)  # Set the width of the input field

        self.investigator_phone_label = tk.Label(self, text="Investigator Phone:")
        self.investigator_phone_entry = tk.Entry(self, width=100)  # Set the width of the input field

        self.email_label = tk.Label(self, text="Email Address:")
        self.email_entry = tk.Entry(self, width=100)  # Set the width of the input field

        self.directory_label = tk.Label(self, text="Directory:")
        self.directory_entry = tk.Entry(self, width=100)  # Set the width of the input field
        self.browse_button = tk.Button(self, text="Browse", command=self.browse_directory)

        # Create Save and Cancel buttons
        self.cancel_button = tk.Button(self, text="Cancel", command=self.destroy, bg="red",  padx=10, pady=5, borderwidth=0)
        self.save_button = tk.Button(self, text="Save", command=self.save_and_close, bg="green",  padx=10, pady=5, borderwidth=0)

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
        form_data = {
            "case_name": case_name,
            "case_number": case_number,
            "investigator_name": investigator_name,
            "investigator_phone": investigator_phone,
            "email_address": email_address,
            "directory": directory
        }

        # Print the dictionary to the console
        print(form_data)

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

        if not self.investigator_phone_entry.get():
            messagebox.showwarning("Warning", "Please enter the investigator's phone number.")
            return False

        if not self.email_entry.get():
            messagebox.showwarning("Warning", "Please enter an email address.")
            return False

        if not self.directory_entry.get():
            messagebox.showwarning("Warning", "Please select a directory.")
            return False

        # If all the fields are filled out, return True
        return True


# --------------------------- MAIN APP -----------------------------------
app = TkinterApp()
app.mainloop()