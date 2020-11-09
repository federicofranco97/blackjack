from mttkinter import mtTkinter as tk
from PIL import Image, ImageTk


class PantallaBase:

    def __init__(self):
        
        self.root = tk.Tk()
        self.root.withdraw()

    def getRoot(self):

        return self.root
    
    
class PantallaImagenes(tk.Frame):
    
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.master = master
        self.pack(fill=tk.BOTH, expand=1)
        self.img = []
        self.imgLabel = []

        return


    def agregar(self, imagen, x=0, y=0, width=0, height=0):
    
        print(imagen)
        load = Image.open(imagen)
        if width > 0 and height > 0:
            load = load.resize((width, height), Image.ANTIALIAS)
        render = ImageTk.PhotoImage(load)
        label = tk.Label(self.master, image=render)
        label.image = render
        label.place(x=x, y=y)
        
        self.imgLabel.append(label)
        self.img.append(imagen)        
        
        return

    
    def borrar(self):
        for widget in self.master.winfo_children():
            widget.destroy()
        self.img = []
        self.imgLabel = []
        
        return


