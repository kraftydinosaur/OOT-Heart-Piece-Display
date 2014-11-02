from ctypes import *
from ctypes.wintypes import *
from Tkinter import *
import ConfigParser
import os.path
import tkMessageBox
import sys

OpenProcess = windll.kernel32.OpenProcess
ReadProcessMemory = windll.kernel32.ReadProcessMemory
CloseHandle = windll.kernel32.CloseHandle


def res_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


def findPID(search):
    """Finds Process that contains PROCNAME and returns pid"""
    import psutil
    for proc in psutil.process_iter():
        if search in str(proc.name):
            return proc.pid
    return None


def readByte(address, handle):
    """Reads byte at given address in given process handle and returns value"""
    if ReadProcessMemory(handle, address, buffer, 1, byref(bytesRead)):
        memmove(byref(val), buffer, sizeof(val))
        return val.value
    else:
        return 0


buffer = c_char_p(b"")
val = c_ubyte()
bytesRead = c_long(0)
processHandle = OpenProcess(0x10, False, findPID("mupen64"))


class App(Frame):

    def getConf(self):
        conf = ConfigParser.ConfigParser()
        try:
            if os.path.isfile("user.conf"):
                conf.read("user.conf")
            else:
                conf.read("default.conf")

            # Style
            self.bgcolor = conf.get("Style", "BackgroundColor")

            # Function
            self.updateInterval = conf.get("Function", "UpdateInterval")
            self.hpAdd = int(conf.get("Function", "hpAddress"), 16)
        except:
            tkMessageBox.showerror("Error", "Error reading config file.")
            root.destroy()
            sys.exit()

    def setup(self):
        root.wm_title("OOT Heart Piece Display")
        root.config(bg=self.bgcolor)
        icon = PhotoImage(file=res_path("img/icon.gif"))
        root.tk.call('wm', 'iconphoto', root._w, icon)
        self.photo = PhotoImage(file=res_path("img/0.gif"))
        self.w = Label(root, image=self.photo)
        self.w.photo = self.photo
        self.w.config(bg=self.bgcolor)

        self.w.pack()

        root.bind("<ButtonPress-1>", self.StartMove)
        root.bind("<ButtonRelease-1>", self.StopMove)
        root.bind("<B1-Motion>", self.OnMotion)

    def update(self):
        hp = readByte(self.hpAdd, processHandle)
        self.hpImg = PhotoImage(file=res_path("img/%s.gif" % readByte(
                                self.hpAdd, processHandle)))
        self.w.configure(image = self.hpImg)
        self.w.image = self.photo
        self.update_idletasks()
        self.after(self.updateInterval, self.update)

    def StartMove(self, event):
        self.x = event.x
        self.y = event.y

    def StopMove(self, event):
        self.x = None
        self.y = None

    def OnMotion(self, event):
        deltax = event.x - self.x
        deltay = event.y - self.y
        x = root.winfo_x() + deltax
        y = root.winfo_y() + deltay
        root.geometry("+%s+%s" % (x, y))

    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.getConf()
        self.setup()

root = Tk()
root.resizable(0, 0)
app = App(master=root)
app.update()
app.mainloop()
