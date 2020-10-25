# Blackjack - Universidad de Belgrano

## Requerimientos

Tener instalado Python >= 3.7 y tener el CLI de git configurado con su usuario.

## Instalación

Clonar el repositorio con el comando git clone. 

```
git clone git@github.com:federicofranco97/blackjack.git
```

Luego moverse al branch **feature/entregable-uno**

```
git checkout feature/entregable-uno
```

Las dependencias necesarias para correr ya vienen instaladas con python

## Iniciar el servidor

Para iniciar el servidor, pararse en el directorio raíz del proyecto y ejecutar:

````
python server.py
````

El servidor comenzará a escuchar conexiones en el puerto 3030.

## Conexión al servidor

Para conectarse al servidor se puede utilizar un cliente como Putty, Telnet o Netcat. El siguiente ejemplo utiliza Netcat. 
Entonces, para conectarse:

```
nc localhost 3030
```

Una vez conectado, el servidor pedirá que te identifiques. Lo puedes hacer con el comando:

```
soy <nombre>
```

Luego de identificarte puedes realizar las siguientes acciones:

**Ingresar dinero**
```
ingresar <monto>
```

**Enviar un mensaje a todos los conectados**
```
mensaje <mensaje>
```

**Pedir estadisticas**
```
estadisticas
```

