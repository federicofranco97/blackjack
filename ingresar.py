import tkinter as tk
import os
import playsound
from pantalla import MostrarImagenes
#from PIL import Image, ImageTk
from guiViewModel import GuiViewModel
#from tkinter.scrolledtext import ScrolledText
#from _thread import *

class PantallaIngreso:

    def __init__(self, model):
        
        self.root = tk.Tk()
        self.model = model
        self.botones = ['conectar']

        self.inicializarFrames()
        self.inicializarBotones()
        #self.cargarImagen()
        self.configurarEventos()
        self.cargarBotones()

        return
    

    def inicializarFrames(self):
                
        color = 'medium blue'        
        self.root.wm_title("Blackjac UB version Betal Alfa Centauri v1.0.1")
        self.root.geometry("1024x768")
        self.root['bg']="green"
 
        self.framePanelTitulo = tk.Frame(self.root, width = 1024, height = 150)
        self.framePanelTitulo.pack(side=tk.TOP)
        self.framePanelTitulo['bg']="white"
        self.framePanelTitulo.pack_propagate(0)
        
        self.framePanelConexion = tk.Frame(self.root, width = 1024, height = 618)
        self.framePanelConexion.pack(side=tk.BOTTOM)
        self.framePanelConexion['bg']="white"
        self.framePanelConexion.pack_propagate(0)
    
    
        self.framePanelDatos = tk.Frame(self.framePanelConexion, width = 324, height = 618)
        self.framePanelDatos.pack(side=tk.LEFT)
        self.framePanelDatos['bg']=color
        self.framePanelDatos.pack_propagate(0)
        
        self.framePanelImagen = tk.Frame(self.framePanelConexion, width = 700, height = 618)
        self.framePanelImagen.pack(side=tk.RIGHT)
        self.framePanelImagen['bg']=color
        self.framePanelImagen.pack_propagate(0)

        self.frameConexion = tk.Frame(self.framePanelDatos, width = 324, height = 250)
        self.frameConexion.pack(side=tk.TOP)
        self.frameConexion['bg']=color
        self.frameConexion.pack_propagate(0)

        self.frameIngreso = tk.Frame(self.framePanelDatos, width = 324, height = 150)
        self.frameIngreso.pack(side=tk.TOP)
        self.frameIngreso['bg']=color
        self.frameIngreso.pack_propagate(0) 


        self.frameConexionDatos = tk.Frame(self.frameConexion, width = 324, height = 200)
        self.frameConexionDatos.pack(side=tk.TOP)
        self.frameConexionDatos['bg']=color
        self.frameConexionDatos.pack_propagate(0)

        self.frameConexionBoton = tk.Frame(self.frameConexion, width = 324, height = 50)
        self.frameConexionBoton.pack(side=tk.BOTTOM)
        self.frameConexionBoton['bg']=color
        self.frameConexionBoton.pack_propagate(0)


        self.frameServidorInfo = tk.Frame(self.frameConexionDatos, width = 324, height = 100)
        self.frameServidorInfo.pack(side=tk.TOP)
        self.frameServidorInfo['bg']=color
        self.frameServidorInfo.pack_propagate(0)

        self.framePuertoInfo = tk.Frame(self.frameConexionDatos, width = 324, height = 100)
        self.framePuertoInfo.pack(side=tk.BOTTOM)
        self.framePuertoInfo['bg']=color
        self.framePuertoInfo.pack_propagate(0)


        self.frameJugarInfo = tk.Frame(self.frameIngreso, width = 324, height = 100)
        self.frameJugarInfo.pack(side=tk.TOP)
        self.frameJugarInfo['bg']=color
        self.frameJugarInfo.pack_propagate(0)

        self.frameJugarBoton = tk.Frame(self.frameIngreso, width = 324, height = 50)
        self.frameJugarBoton.pack(side=tk.BOTTOM)
        self.frameJugarBoton['bg']=color
        self.frameJugarBoton.pack_propagate(0)


        self.frameDireccionIP = tk.Frame(self.frameServidorInfo, width = 324, height = 50)
        self.frameDireccionIP.pack(side=tk.TOP)
        self.frameDireccionIP['bg']=color
        self.frameDireccionIP.pack_propagate(0)

        self.framePuerto = tk.Frame(self.frameServidorInfo, width = 324, height = 50)
        self.framePuerto.pack(side=tk.BOTTOM)
        self.framePuerto['bg']=color
        self.framePuerto.pack_propagate(0)

        
        self.frameUsuario = tk.Frame(self.frameJugarInfo, width = 324, height = 50)
        self.frameUsuario.pack(side=tk.TOP)
        self.frameUsuario['bg']=color
        self.frameUsuario.pack_propagate(0)

        self.frameJugar = tk.Frame(self.frameJugarInfo, width = 324, height = 50)
        self.frameJugar.pack(side=tk.BOTTOM)
        self.frameJugar['bg']=color
        self.frameJugar.pack_propagate(0)
        
        return

    
    def cargarBotones(self):
        
        self.habilitarBotones()
        #self.modificarEstado(self.estadoStr)
        
        return
    

    def habilitarBotones(self):

        self.botonesActivados = {"conectar": False,
                                 "jugar": False}
        
        
        for boton in self.botones:
            
            self.botonesActivados[boton] = True
        
        for boton in self.botonesActivados:
            
            self.habilitarBoton(boton, self.botonesActivados[boton])
        
        return
    

    def habilitarBoton(self, boton, activar):
       
        estado = "disabled"
        if activar:
            estado = "normal"

        if boton == "conectar":
            self.buttonConectar.config(state=estado)
        elif boton == "jugar":
            self.buttonJugar.config(state=estado)
        
        return
    

    def configurarEventos(self):

        self.model.ee.on("connectedEvent", self.onConnectEvent)
        self.model.ee.on("connectErrorEvent", self.onConnectErrorEvent)
        self.model.ee.on("soyAceptadoEvent", self.onSoyAceptadoEvent)
        self.model.ee.on("soyRechazadoEvent", self.onSoyRechazadoEvent)

        return
    
    
    def onConnectEvent(self):
        
        print("Conectado")
        self.botones= ['jugar']
        self.habilitarBotones()
        
        return


    def onConnectErrorEvent(self, mensaje):
                
        print("Error Conectando")
        self.botones= ['conectar']
        self.habilitarBotones()
        print(mensaje)
        
        return

    
    def onSoyRechazadoEvent(self):
        
        #Error
        print("Rechazado")
        self.botones= ['jugar']
        self.habilitarBotones()
        
        return


    def onSoyAceptadoEvent(self):
        
        print("Aceptado")
        self.model.onEntered()
        #self.root.quit()
        self.root.destroy()
        #exit()
        #sys.exit()
        
        return


    def btConectar(self):
        
        print("Conectar")
        self.botones=[]
        self.habilitarBotones()
        self.model.onRequestConnection('190.55.116.66', '3039')
       
        return
    
    
    def btJugar(self):
        
        print("Jugar")
        self.botones=[]
        self.habilitarBotones()
        self.model.onSoy('quique')
       
        return

    
    def notificacion(self, usuario):
        
        if (usuario == self.usuario):
            start_new_thread(self.play, ())
        
        return


    def play(self):
        
        soundurl = os.path.join("sounds", "messageEntered.mp3")
        playsound.playsound(soundurl)
        
        return


    def cargarImagen(self):

        self.app = MostrarImagenes(self.framePanelImagen)
        self.app['bg']='green'
        self.imagen = 'blackjack'
        self.cwd = os.getcwd()
        images = 'images'
        x = 400
        y = 400
        
        self.imagen = os.path.join(os.path.join(self.cwd, images), self.imagen + '.jpg')
        self.app.agregar(self.imagen, x, y)
 
        return


    def inicializarBotones(self):

        ancho = 100
        colorFront = "white"
        colorBack = "medium blue"
        tamLetra = 13
        tamMonto = 15

        self.labelTitulo = tk.Label(self.framePanelTitulo, text="Blackjack UB",width = 100, height = 50,
                           fg=colorFront,
                           bg=colorBack,
                           font=("Arial Bold", 80))
        self.labelTitulo.pack(side=tk.TOP)

        self.labelDireccionIP = tk.Label(self.frameDireccionIP, text="Direccion IP Servidor",width = 100, height = 50,
                           fg=colorFront,
                           bg=colorBack,
                           font=("Arial Bold", tamLetra))
        self.labelDireccionIP.pack(side=tk.TOP)
        self.textlDireccionIP = tk.Text(self.frameDireccionIP, width = 100, height = 50, 
                           fg=colorFront,
                           bg=colorBack,
                           font=("Arial Bold", 15))
        #self.textlDireccionIP.bind('<Return>', self.procesarMonto)
        self.textlDireccionIP.pack(side=tk.BOTTOM)
        #self.textlDireccionIP = tk.Text(self.frameDireccionIP, width = 100, height = 50,
        #                        font=("Arial Bold", 15), fg="black", bg="white")
        #self.textlDireccionIP.pack(side=tk.BOTTOM)

        self.labelPuerto = tk.Label(self.framePuerto, text="Puerto",width = 100, height = 50,
                           fg=colorFront,
                           bg=colorBack,
                           font=("Arial Bold", tamLetra))
        self.labelPuerto.pack(side=tk.TOP)
        self.textPuerto = tk.Text(self.framePuerto, width = 100, height = 50,
                                font=("Arial Bold", 15), fg="black", bg="white")
        self.textPuerto.pack(side=tk.BOTTOM)

        self.buttonConectar = tk.Button(self.frameConexionBoton, width = ancho, height = 50,
                           text="CONECTAR", 
                           fg=colorFront,
                           bg=colorBack,
                           font=("Arial Bold", tamLetra),
                           command=self.btConectar)
        self.buttonConectar.pack(side=tk.RIGHT)


        self.labelUsuario = tk.Label(self.frameUsuario, text="Usuario",width = 100, height = 50,
                           fg=colorFront,
                           bg=colorBack,
                           font=("Arial Bold", tamLetra))
        self.labelUsuario.pack(side=tk.TOP)
        self.textUsuario = tk.Text(self.frameUsuario, width = 100, height = 50,
                                font=("Arial Bold", 15), fg="black", bg="white")
        self.textUsuario.pack(side=tk.BOTTOM)

        self.buttonJugar = tk.Button(self.frameJugarBoton, width = ancho, height = 50,
                           text="JUGAR", 
                           fg=colorFront,
                           bg=colorBack,
                           font=("Arial Bold", tamLetra),
                           command=self.btJugar)
        self.buttonJugar.pack(side=tk.RIGHT)
                
        return

    
    def mostrar(self):
        
        self.root.mainloop()
        
        return


def testPantallaInicializadorIngreso():

    model = GuiViewModel()
    #model.MiSaldo = 3000
    #model.ee.on("pedirCartaEvent", testPantallaPedirCarta)
    bjScreen = PantallaIngreso(model)
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
    
    