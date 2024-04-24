import tkinter as tk
from tkinter import ttk

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
            command=lambda: self.show_frame(ImageCarving, "Image Recover")
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


# ------------------------ MULTIPAGE FRAMES ------------------------------------


class Home(tk.Frame):
    def __init__(self, parent, controller):

        tk.Frame.__init__(self, parent)

        label = tk.Label(
            self, text="DIGITAL IMAGE FORENSICS TOOL (DIFT)", font=("Arial", 24)
        )
        label.pack()


class NewProject(tk.Frame):
    def __init__(self, parent, controller):

        tk.Frame.__init__(self, parent)

        label = tk.Label(self, text="Project Info goes here", font=("Arial", 24))
        label.pack()


class ImageCarving(tk.Frame):
    from core.disks.disk import Disk

    def __init__(self, parent, controller):

        tk.Frame.__init__(self, parent)

        label = tk.Label(self, text="Return deleted Images", font=("Arial", 15))
        label.pack()

        # Create Tree Styles
        style = ttk.Style()
        style.configure("Treeview", font=("Arial", 12))

        # Create a Treeview widget
        self.tree = ttk.Treeview(self, style="Treeview")

        # Define the columns
        self.tree["columns"] = ("one", "two", "three", "four", "five")

        # Format the columns
        self.tree.column("#0", width=50, minwidth=50, stretch=tk.YES)
        self.tree.column("one", width=80, minwidth=80, stretch=tk.YES)
        self.tree.column("two", width=400, minwidth=200, stretch=tk.YES)
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


app = TkinterApp()
app.mainloop()
