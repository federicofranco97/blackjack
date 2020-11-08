import tkinter as tk
import os
import playsound
from pantalla import MostrarImagenes
from PIL import Image, ImageTk
from guiViewModel import GuiViewModel
from tkinter.scrolledtext import ScrolledText
from _thread import *
import time


class PantallaBase:

    def __init__(self):
        
        self.root = tk.Tk()
        self.root.withdraw()
        
    def getRoot(self):
        
        return self.root


class PantallaIngreso:

    def __init__(self, model, tkroot):
        
        self.dobleroot = tkroot
        #self.dobleroot.withdraw()
        #self.dobleroot.hide()
        self.root = tk.Toplevel(self.dobleroot)
        self.model = model
        self.botones = ['direccion', 'puerto', 'conectar']
        self.error = tk.StringVar()

        self.inicializarFrames()
        self.inicializarBotones()
        self.cargarImagen()
        self.configurarEventos()
        self.cargarBotones()

        return
    

    def inicializarFrames(self):
                
        color = 'medium blue'        
        self.root.wm_title("Blackjac UB version Betal Alfa Centauri v1.0.1")
        self.root.geometry("1024x768")
        self.root['bg']=color
 
        self.framePanelTitulo = tk.Frame(self.root, width = 1024, height = 120)
        self.framePanelTitulo.pack(side=tk.TOP)
        self.framePanelTitulo['bg']=color
        self.framePanelTitulo.pack_propagate(0)
        
        self.framePanelPrincipal = tk.Frame(self.root, width = 1024, height = 638)
        self.framePanelPrincipal.pack(side=tk.BOTTOM)
        self.framePanelPrincipal['bg']=color
        self.framePanelPrincipal.pack_propagate(0)

        self.framePanelAuxiliar = tk.Frame(self.framePanelPrincipal, width = 50, height = 638)
        self.framePanelAuxiliar.pack(side=tk.LEFT)
        self.framePanelAuxiliar['bg']=color
        self.framePanelAuxiliar.pack_propagate(0)
                
        self.framePanelConexion = tk.Frame(self.framePanelPrincipal, width = 974, height = 638)
        self.framePanelConexion.pack(side=tk.RIGHT)
        self.framePanelConexion['bg']=color
        self.framePanelConexion.pack_propagate(0)
    
    
        self.framePanelDatos = tk.Frame(self.framePanelConexion, width = 264, height = 638)
        self.framePanelDatos.pack(side=tk.LEFT)
        self.framePanelDatos['bg']=color
        self.framePanelDatos.pack_propagate(0)
        
        self.framePanelImagen = tk.Frame(self.framePanelConexion, width = 700, height = 638)
        self.framePanelImagen.pack(side=tk.RIGHT)
        self.framePanelImagen['bg']=color
        self.framePanelImagen.pack_propagate(0)

        self.frameConexion = tk.Frame(self.framePanelDatos, width = 264, height = 350)
        self.frameConexion.pack(side=tk.TOP)
        self.frameConexion['bg']=color
        self.frameConexion.pack_propagate(0)

        self.frameIngreso = tk.Frame(self.framePanelDatos, width = 264, height = 220)
        self.frameIngreso.pack(side=tk.TOP)
        self.frameIngreso['bg']=color
        self.frameIngreso.pack_propagate(0) 


        self.frameConexionDatos = tk.Frame(self.frameConexion, width = 264, height = 200)
        self.frameConexionDatos.pack(side=tk.TOP)
        self.frameConexionDatos['bg']=color
        self.frameConexionDatos.pack_propagate(0)

        self.frameConexionBotonInfo = tk.Frame(self.frameConexion, width = 264, height = 150)
        self.frameConexionBotonInfo.pack(side=tk.BOTTOM)
        self.frameConexionBotonInfo['bg']=color
        self.frameConexionBotonInfo.pack_propagate(0)


        self.frameServidorInfo = tk.Frame(self.frameConexionDatos, width = 264, height = 100)
        self.frameServidorInfo.pack(side=tk.TOP)
        self.frameServidorInfo['bg']="blue"
        self.frameServidorInfo.pack_propagate(0)

        self.framePuertoInfo = tk.Frame(self.frameConexionDatos, width = 264, height = 100)
        self.framePuertoInfo.pack(side=tk.BOTTOM)
        self.framePuertoInfo['bg']="blue"
        self.framePuertoInfo.pack_propagate(0)


        self.frameConexionBoton = tk.Frame(self.frameConexionBotonInfo, width = 264, height = 50)
        self.frameConexionBoton.pack(side=tk.TOP)
        self.frameConexionBoton['bg']=color
        self.frameConexionBoton.pack_propagate(0)

        self.frameConexionAuxiliar = tk.Frame(self.frameConexionBotonInfo, width = 264, height = 100)
        self.frameConexionAuxiliar.pack(side=tk.BOTTOM)
        self.frameConexionAuxiliar['bg']=color
        self.frameConexionAuxiliar.pack_propagate(0)


        self.frameErrorAuxiliar = tk.Frame(self.frameConexionAuxiliar, width = 264, height = 25)
        self.frameErrorAuxiliar.pack(side=tk.TOP)
        self.frameErrorAuxiliar['bg']=color
        self.frameErrorAuxiliar.pack_propagate(0)

        self.frameError = tk.Frame(self.frameConexionAuxiliar, width = 264, height = 75)
        self.frameError.pack(side=tk.BOTTOM)
        self.frameError['bg']=color
        self.frameError.pack_propagate(0)

        
        self.frameJugarInfo = tk.Frame(self.frameIngreso, width = 264, height = 100)
        self.frameJugarInfo.pack(side=tk.TOP)
        self.frameJugarInfo['bg']=color
        self.frameJugarInfo.pack_propagate(0)


        self.frameJugarSalir = tk.Frame(self.frameIngreso, width = 264, height = 120)
        self.frameJugarSalir.pack(side=tk.BOTTOM)
        self.frameJugarSalir['bg']=color
        self.frameJugarSalir.pack_propagate(0)

        
        self.frameJugarBoton = tk.Frame(self.frameJugarSalir, width = 264, height = 50)
        self.frameJugarBoton.pack(side=tk.TOP)
        self.frameJugarBoton['bg']=color
        self.frameJugarBoton.pack_propagate(0)

        self.frameSalir = tk.Frame(self.frameJugarSalir, width = 264, height = 70)
        self.frameSalir.pack(side=tk.BOTTOM)
        self.frameSalir['bg']=color
        self.frameSalir.pack_propagate(0)


        self.frameSalirAuxiliar = tk.Frame(self.frameSalir, width = 264, height = 20)
        self.frameSalirAuxiliar.pack(side=tk.TOP)
        self.frameSalirAuxiliar['bg']=color
        self.frameSalirAuxiliar.pack_propagate(0)

        self.frameSalirBoton = tk.Frame(self.frameSalir, width = 264, height = 50)
        self.frameSalirBoton.pack(side=tk.BOTTOM)
        self.frameSalirBoton['bg']=color
        self.frameSalirBoton.pack_propagate(0)

        
        self.frameServidorTitulo = tk.Frame(self.frameServidorInfo, width = 264, height = 50)
        self.frameServidorTitulo.pack(side=tk.TOP)
        self.frameServidorTitulo['bg']=color
        self.frameServidorTitulo.pack_propagate(0)

        self.frameServidorIP = tk.Frame(self.frameServidorInfo, width = 264, height = 50)
        self.frameServidorIP.pack(side=tk.BOTTOM)
        self.frameServidorIP['bg']=color
        self.frameServidorIP.pack_propagate(0)

        self.framePuertoTitulo = tk.Frame(self.framePuertoInfo, width = 264, height = 50)
        self.framePuertoTitulo.pack(side=tk.TOP)
        self.framePuertoTitulo['bg']=color
        self.framePuertoTitulo.pack_propagate(0)

        self.framePuertoNumero = tk.Frame(self.framePuertoInfo, width = 264, height = 50)
        self.framePuertoNumero.pack(side=tk.BOTTOM)
        self.framePuertoNumero['bg']=color
        self.framePuertoNumero.pack_propagate(0)

        
        self.frameUsuarioInfo = tk.Frame(self.frameJugarInfo, width = 264, height = 100)
        self.frameUsuarioInfo.pack(side=tk.TOP)
        self.frameUsuarioInfo['bg']=color
        self.frameUsuarioInfo.pack_propagate(0)

        self.frameJugar = tk.Frame(self.frameJugarInfo, width = 264, height = 50)
        self.frameJugar.pack(side=tk.BOTTOM)
        self.frameJugar['bg']=color
        self.frameJugar.pack_propagate(0)

        self.frameUsuarioTitulo = tk.Frame(self.frameUsuarioInfo, width = 264, height = 50)
        self.frameUsuarioTitulo.pack(side=tk.TOP)
        self.frameUsuarioTitulo['bg']=color
        self.frameUsuarioTitulo.pack_propagate(0)

        self.frameUsuarioNombre = tk.Frame(self.frameUsuarioInfo, width = 264, height = 50)
        self.frameUsuarioNombre.pack(side=tk.BOTTOM)
        self.frameUsuarioNombre['bg']=color
        self.frameUsuarioNombre.pack_propagate(0)
        
        return

    
    def cargarBotones(self):
        
        self.habilitarBotones()
        #self.modificarEstado(self.estadoStr)
        
        return
    

    def habilitarBotones(self):

        self.botonesActivados = {'direccion': False,
                                 'puerto': False,
                                 'conectar': False,
                                 'usuario': False,
                                 'jugar': False}
        
        
        for boton in self.botones:
            
            self.botonesActivados[boton] = True
        
        for boton in self.botonesActivados:
            
            self.habilitarBoton(boton, self.botonesActivados[boton])
        
        return
    

    def habilitarBoton(self, boton, activar):
       
        estado = "disabled"
        if activar:
            estado = "normal"

        if boton == 'direccion':
            self.textlDireccionIP.config(state=estado)
        elif boton == 'puerto':
            self.textPuerto.config(state=estado)
        elif boton == 'conectar':
            self.buttonConectar.config(state=estado)
        elif boton == 'usuario':
            self.textUsuario.config(state=estado)
        elif boton == 'jugar':
            self.buttonJugar.config(state=estado)
        
        return
    

    def configurarEventos(self):

        self.model.ee.on("connectedEvent", self.onConnectEvent)
        self.model.ee.on("connectErrorEvent", self.onConnectErrorEvent)
        self.model.ee.on("soyAceptadoEvent", self.onSoyAceptadoEvent)
        self.model.ee.on("soyRechazadoEvent", self.onSoyRechazadoEvent)
        #self.model.ee.on("cierreEvent", self.btSalirOnDemand)

        return
    
    def modificarError(self, error):
        
        #self.jugadores.set(jugadores)
        self.textError.delete("0.0", tk.END)
        self.textError.insert(tk.END, error)
        self.textError.see(tk.END)
                
        return

    #def modificarError(self, error):
        
    #    self.error.set(error)

    #    return
    

    def onConnectEvent(self):
        
        print("Conectado")
        self.botones= ['usuario', 'jugar']
        self.habilitarBotones()
        
        return


    def onConnectErrorEvent(self, mensaje):
                
        print("Error Conectando")
        self.botones= ['direccion', 'puerto', 'conectar']
        self.habilitarBotones()
        print(mensaje)
        self.modificarError(mensaje)
        
        return

    
    def onSoyRechazadoEvent(self, mensaje):
        
        #Error
        print("Rechazado")
        self.botones= ['usuario', 'jugar']
        self.habilitarBotones()
        self.modificarError(mensaje)
        
        return


    def onSoyAceptadoEvent(self):
        
        print("Aceptado")
        self.model.Validado = True
        self.btSalirOnDemand()
        #self.model.onEntered()
        #self.root.update_idletasks()
        #self.root.update()
        #self.root.destroy()
        
        #self.root.quit()
        #for widget in self.root.winfo_children():
           #widget.destroy()
        #self.root.hide()
        #self.root.update()
        #self.root.deiconify()
        #self.root.destroy()
        #exit()
        #sys.exit()
        
        return


    def limpiarTexto(self, texto):
        
        i = 0
        for char in texto:
            if char not in "abcdefghijglmnopqrstuvwqyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890_.-":
                break
            i = i + 1
            
        return texto[0:i]

    def btConectar(self):
        
        print("Conectar")
        self.botones=[]
        self.habilitarBotones()
        self.direccionIP = self.limpiarTexto(self.textlDireccionIP.get("1.0", tk.END))
        #self.textlDireccionIP.delete("0.0", tk.END)
        self.puerto = self.limpiarTexto(self.textPuerto.get("1.0", tk.END).replace("\n ", ""))
        #self.puerto = self.textPuerto.delete("0.0", tk.END)
        print('Direccion: ' + self.direccionIP + ' Puerto: ' + self.puerto)
        self.model.onRequestConnection(self.direccionIP, self.puerto)
        #self.model.onRequestConnection('190.55.116.66', '3039')
       
        return
    
        
    def btJugar(self):
        
        print("Jugar")
        self.botones=[]
        self.habilitarBotones()
        self.usuario = self.limpiarTexto(self.textUsuario.get("1.0", tk.END))
        #self.textUsuario.delete("0.0", tk.END)
        self.model.onSoy(self.usuario)
       
        return


    def btSalir(self):

        self.root.quit()
    
        return  
    
    
    def btSalirOnDemand(self):

        self.buttonSalir.invoke()
        #os._exit(0)
    
        return  

    
    def notificacion(self, usuario):
        
        start_new_thread(self.play, ())
        
        return


    def play(self):
        
        soundurl = os.path.join("sounds", "messageEntered.mp3")
        playsound.playsound(soundurl)
        
        return


    def cargarImagen(self):

        self.app = MostrarImagenes(self.framePanelImagen)
        self.app['bg']='medium blue'
        self.imagen = 'blackjack'
        self.cwd = os.getcwd()
        images = 'images'
        x = 0
        y = 0
        
        self.imagen = os.path.join(os.path.join(self.cwd, images), self.imagen + '.jpg')
        self.app.agregar(self.imagen, x = x, y = y, width = 650, height = 568)
 
        return

    def focus_next_window(self, event):
        
        event.widget.tk_focusNext().focus()
         
        return("break")
     

    def inicializarBotones(self):

        ancho = 100
        colorFront = "white"
        colorBack = "medium blue"
        tamLetraLabel = 20
        tamLetraText = 25
        tamMonto = 15

        self.labelTitulo = tk.Label(self.framePanelTitulo, text="Blackjack UB",width = 100, height = 50,
                           fg=colorFront,
                           bg=colorBack,
                           font=("Arial Bold", 70, "bold"))
        self.labelTitulo.bind("<Tab>", self.focus_next_window)
        self.labelTitulo.pack(side=tk.TOP)

        self.labelDireccionIP = tk.Label(self.frameServidorTitulo, text="Direccion IP Servidor",width = 100, height = 50,
                           fg=colorFront,
                           bg=colorBack,
                           font=("Arial Bold", tamLetraLabel))
        self.labelDireccionIP.pack(side=tk.TOP)
        self.textlDireccionIP = tk.Text(self.frameServidorIP, width = 100, height = 50, 
                           fg="black",
                           bg="white",
                           font=("Arial Bold", tamLetraText))
        #self.textlDireccionIP.bind('<Tab>', self.procesarMonto)
        self.textlDireccionIP.bind("<Tab>", self.focus_next_window)
        self.textlDireccionIP.pack(side=tk.TOP)
        #self.textlDireccionIP = tk.Text(self.frameDireccionIP, width = 100, height = 50,
        #                        font=("Arial Bold", 15), fg="black", bg="white")
        #self.textlDireccionIP.pack(side=tk.BOTTOM)

        self.labelPuerto = tk.Label(self.framePuertoTitulo, text="Puerto",width = 100, height = 50,
                           fg=colorFront,
                           bg=colorBack,
                           font=("Arial Bold", tamLetraLabel))
        self.labelPuerto.bind("<Tab>", self.focus_next_window)
        self.labelPuerto.pack(side=tk.TOP)
        self.textPuerto = tk.Text(self.framePuertoNumero, width = 100, height = 50,
                           fg="black",
                           bg="white",
                           font=("Arial Bold", tamLetraText))
        self.textPuerto.bind("<Tab>", self.focus_next_window)
        self.textPuerto.pack(side=tk.TOP)

        self.buttonConectar = tk.Button(self.frameConexionBoton, width = ancho, height = 50,
                           text="CONECTAR", 
                           fg=colorFront,
                           bg=colorBack,
                           font=("Arial Bold", tamLetraLabel),
                           command=self.btConectar)
        self.buttonConectar.bind("<Tab>", self.focus_next_window)
        self.buttonConectar.pack(side=tk.TOP)

        self.scrollbarError = tk.Scrollbar(self.frameError)
        self.textError = tk.Text(self.frameError,
                                font=("Arial Bold", 10), bg="medium blue", fg="white")
        self.scrollbarError.pack(side=tk.RIGHT, fill=tk.Y)
        self.textError.pack(side=tk.LEFT, fill=tk.Y)
        self.scrollbarError.config(command=self.textError.yview)
        self.textError.config(yscrollcommand=self.scrollbarError.set)

        self.modificarError("")
        self.textError.pack(side=tk.LEFT)

        
        #self.labelError = tk.Label(self.frameError, textvariable=self.error, 
        #                           font=("Arial Bold", 15), bg="medium blue", fg="white")
        #self.labelError.bind("<Tab>", self.focus_next_window)
        #self.labelError.pack(side=tk.BOTTOM)


        self.labelUsuario = tk.Label(self.frameUsuarioTitulo, text="Usuario",width = 100, height = 50,
                           fg=colorFront,
                           bg=colorBack,
                           font=("Arial Bold", tamLetraLabel))
        self.labelUsuario.bind("<Tab>", self.focus_next_window)
        self.labelUsuario.pack(side=tk.TOP)
        self.textUsuario = tk.Text(self.frameUsuarioNombre, width = 100, height = 50,
                           fg="black",
                           bg="white",
                           font=("Arial Bold", tamLetraText))
        self.textUsuario.bind("<Tab>", self.focus_next_window)
        self.textUsuario.pack(side=tk.TOP)

        self.buttonJugar = tk.Button(self.frameJugarBoton, width = ancho, height = 50,
                           text="JUGAR", 
                           fg=colorFront,
                           bg=colorBack,
                           font=("Arial Bold", tamLetraLabel),
                           command=self.btJugar)
        self.buttonJugar.bind("<Tab>", self.focus_next_window)
        self.buttonJugar.pack(side=tk.TOP)

        self.buttonSalir = tk.Button(self.frameSalirBoton, width = ancho, height = 50,
                           text="SALIR", 
                           fg=colorFront,
                           bg=colorBack,
                           font=("Arial Bold", tamLetraLabel),
                           command=self.btSalir)
        self.buttonSalir.bind("<Tab>", self.focus_next_window)
        self.buttonSalir.pack(side=tk.TOP)

                
        return

    
    def mostrar(self):
        
        self.root.mainloop()
        #while True:
        #    if self.model.Validado:
        #        break
        #    self.root.update_idletasks()
        #    self.root.update()
        #    time.sleep(0.01)

        # or whatever your login check looks like
        #self.root.destroy()
        
        return



def testPantallaInicializadorIngreso():

    model = GuiViewModel()
    #model.MiSaldo = 3000
    #model.ee.on("pedirCartaEvent", testPantallaPedirCarta)
    bjbase = PantallaBase()
    bjScreen = PantallaIngreso(model, bjbase.getRoot())
    bjScreen.mostrar()

    '''    
    bjScreen.cargarCartas(listaCartas)
    bjScreen.cargarScore("12")
    bjScreen.cargarEstado("Jugar")
    bjScreen.cargarJugadores("Quique: Esperando\nSeba: Esperando\nFede G: Esperando\nFede F: Jugando\nRichard: Esperando")
    bjScreen.cargarMensajes("Quique: Esperando...\n")
    bjScreen.mostrar()
    
    test=input("prueba")
    '''


if __name__ == "__main__":

    #testPantallaInicializador()
    testPantallaInicializadorIngreso()
    
    