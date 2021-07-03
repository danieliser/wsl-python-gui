from tkinter import *
from tkinter import ttk
from tkinter import filedialog
import subprocess

class ImportWSL:

    def __init__(self, root):
        self.root = root

        self.root.title('Import WSL Image')
        self.root.bind('<Control-w>', self.quit)

        self.name = StringVar()
        self.path = StringVar()
        self.image = StringVar()
        self.done = BooleanVar()

        self.done.set(False)

        if (True == self.done.get()):
            self.draw_done()

        elif (False == self.done.get() and ( not self.name.get() or not self.path.get() or not self.image.get() )):
            self.draw_fields()

    def validate_name(self, inStr):
        return ' ' not in inStr

    def draw_done(self):
        mainframe = ttk.Frame(self.root, padding="3 3 12 12")
        mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
        mainframe.columnconfigure(0, weight=4)
        mainframe.rowconfigure(0, weight=1)

        success_text = Label(mainframe, text="Successfully imported.",
                             fg="green", font="none 18 bold")
        success_text.config(anchor=CENTER, padx=30, pady=50)
        success_text.grid(column=1, row=2, sticky=(N, W, E, S))

    def draw_fields(self):
        mainframe = ttk.Frame(self.root, padding="3 3 12 12")
        mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
        mainframe.columnconfigure(0, weight=4)
        mainframe.rowconfigure(0, weight=1)

        validation = self.root.register(self.validate_name)
        name_label = ttk.Label(mainframe, text="Name")
        name_entry = ttk.Entry(mainframe, textvariable=self.name,
                               validate="key", validatecommand=(validation, '%S'))

        path_label = ttk.Label(mainframe, text="Path")
        path_entry = ttk.Entry(mainframe, textvariable=self.path)
        path_browser = ttk.Button(mainframe, text="...", command=self.browsepath)

        image_label = ttk.Label(mainframe, text="Image")
        image_entry = ttk.Entry(mainframe, textvariable=self.image)
        image_browser = ttk.Button(mainframe, text="...", command=self.browseimage)

        submit_button = ttk.Button(mainframe, text="Import", command=self.process)

        name_entry.config(width=20)
        path_entry.config(width=20)

        name_label.grid(column=0, row=1, sticky=W)
        name_entry.grid(column=1, row=1, columnspan=3, sticky=(W, E))

        path_label.grid(column=0, row=2, sticky=W)
        path_entry.grid(column=1, row=2, columnspan=2, sticky=(W, E))
        path_browser.grid(column=3, row=2, sticky=(W))

        image_label.grid(column=0, row=3, sticky=W)
        image_entry.grid(column=1, row=3, columnspan=2, sticky=(W, E))
        image_browser.grid(column=3, row=3, sticky=(W))

        submit_button.grid(column=2, row=4, sticky=(W))

        for child in mainframe.winfo_children():
            child.grid_configure(padx=5, pady=5)

        if (len(self.name.get()) and len(self.path.get()) and len(self.image.get()) and not self.run.get()):
            self.root.bind("<Return>", self.process)

    def browsepath(self):
        Tk().withdraw()
        filepath = filedialog.askdirectory()
        self.path.set(filepath)

    def browseimage(self):
        Tk().withdraw()
        filepath = filedialog.askopenfilename()
        self.image.set(filepath)

    def process(self):
        cmd = 'wsl --import {} "{}" "{}"'.format(self.name.get(), self.path.get(), self.image.get())
        completed = subprocess.run(["powershell", "-Command", cmd], capture_output=True)
        if completed.returncode != 0:
            print("An error occured: %s", completed.stderr)
        else:
            self.done.set(True)
            self.draw_done()
        return completed

    def quit(self, event):
        self.root.quit()


root = Tk()
ImportWSL(root)
root.mainloop()
