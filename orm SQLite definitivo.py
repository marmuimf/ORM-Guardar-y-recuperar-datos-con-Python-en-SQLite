
#Guardar datos en un sistema ORM (SQLite)
#Recuperar datos desde ORM (SQLite)
#ORM: object relational mapping


import tkinter as tk
import random
import math
import sqlite3

# Declaración de variables globales
personas = []
numeropersonas = 5
class Persona:
    def __init__(self):
        self.posx = random.randint(0,700)
        self.posy = random.randint(0,700)
        self.radio = 30
        self.direccion = random.randint(0,360)
        self.color = random.choice(["pink", "violet", "purple"])
        self.entidad = ""
        self.energia = 100
        self.descanso = 100
        self.entidadenergia = ""
        self.entidaddescanso = ""
        self.cansancio = 1
        self.entidadcansancio = ""
        
    
    def dibuja(self):
        self.entidad = lienzo.create_oval(
            self.posx-self.radio/2,
            self.posy-self.radio/2,
            self.posx+self.radio/2,
            self.posy+self.radio/2,
            fill=self.color)
        
        self.entidadenergia = lienzo.create_rectangle(
            self.posx-self.radio/2,
            self.posy-self.radio/2-10,
            self.posx+self.radio/2,
            self.posy-self.radio/2-8,
            fill="green"
            )
        
        self.entidaddescanso = lienzo.create_rectangle(
            self.posx-self.radio/2,
            self.posy-self.radio/2-16,
            self.posx+self.radio/2,
            self.posy-self.radio/2-14,
            fill="blue"
            )
        
        self.entidadcansancio = lienzo.create_rectangle(
            self.posx-self.radio/2,
            self.posy-self.radio/2-22,
            self.posx+self.radio/2,
            self.posy-self.radio/2-20,
            fill="yellow"
            )
        
    
    def mueve(self):
        if self.energia > 0:
            self.energia -= 0.1  #pierden energia y descanso al moverse
        if self.descanso > 0:
            self.descanso -= 0.1
        
        if self.cansancio is None:
            print("¡Atención! self.cansancio es None. Asignando valor predeterminado.")
            self.cansancio = 1
            print("Valor de cansancio:", self.cansancio)
        
        if self.cansancio > 0:
            self.cansancio += 0.1
          
        self.colisiona()
        
        lienzo.move(
            self.entidad,
            math.cos(self.direccion),
            math.sin(self.direccion))
        
        #coordenadas para las barras
        anchuraenergia = (self.energia/100)*self.radio
        lienzo.coords(
            self.entidadenergia,
            self.posx - self.radio/2,
            self.posy - self.radio/2 - 10,
            self.posx - self.radio/2 + anchuraenergia,
            self.posy - self.radio/2 - 8
        )
        
        anchuradescanso = (self.descanso/100)*self.radio
        lienzo.coords(
            self.entidaddescanso,
            self.posx - self.radio/2,
            self.posy - self.radio/2 - 16,
            self.posx - self.radio/2 + anchuradescanso,
            self.posy - self.radio/2 - 14
        )
        
        anchuracansancio = (self.cansancio/100)*self.radio
        lienzo.coords(
            self.entidadcansancio,
            self.posx - self.radio/2,
            self.posy - self.radio/2 - 22,
            self.posx - self.radio/2 + anchuracansancio,
            self.posy - self.radio/2 - 20
        )

        raiz.update()

        self.posx += math.cos(self.direccion)
        self.posy += math.sin(self.direccion)
    
    def colisiona(self):
        if self.posx < 0 or self.posx > 700 or self.posy < 0 or self.posy > 700:
            self.direccion += math.pi
            
def guardarPersonas():
    print("guardo a los jugadores")
    # Guardo los personajes en SQL
    conexion = sqlite3.connect("jugadores.sqlite3") #abro una conexion
    cursor = conexion.cursor()
    #elimino la info de los jugadores antiguos
    cursor.execute('''
            DELETE FROM jugadores 
            ''')
    conexion.commit()
    for persona in personas:
        cursor.execute('''   
            INSERT INTO jugadores
            VALUES (
                NULL,   
                '''+str(persona.posx)+''',
                '''+str(persona.posy)+''',
                '''+str(persona.radio)+''',
                '''+str(persona.direccion)+''',
                "'''+str(persona.color)+'''",
                "'''+str(persona.entidad)+'''",
                '''+str(persona.energia)+''',
                '''+str(persona.descanso)+''',
                "'''+str(persona.entidadenergia)+'''",
                "'''+str(persona.entidaddescanso)+'''",
                '''+str(persona.cansancio)+''',
                "'''+str(persona.entidadcansancio)+'''"
            )
            ''')
    conexion.commit() #para que ejecute todos los comandos
    conexion.close()
    #al pulsar guardar, hace un mapeo directo y lo mismo q guardamos en el json, se guarda ahora en sql

# Creo una ventana
raiz = tk.Tk()
#En la ventana creo un lienzo
lienzo = tk.Canvas(raiz,width=700,height=700)
lienzo.pack()
#Boton de guardar
boton = tk.Button(raiz,text="Guarda",command=guardarPersonas)
boton.pack()

# cargar personas DESDE SQL
try:
    conexion = sqlite3.connect("jugadores.sqlite3") #me conecto a la base de datos
    cursor = conexion.cursor() #el cursor es necesario para establecer una peticion a la base de datos
    cursor.execute('''
            
            SELECT * FROM jugadores WHERE posx < 100;
            
            ''')
    while True:
        fila = cursor.fetchone() 
        if fila is None:
            break
        #print(fila)
        persona = Persona()
        persona.posx = fila[1]
        persona.posy = fila[2]
        persona.radio = fila[3]
        persona.direccion = fila[4]
        persona.color = fila[5]
        persona.entidad = fila[6]
        persona.energia = fila[7]
        persona.descanso = fila[8]
        persona.entidadenergia = fila[9]
        persona.entidaddescanso = fila[10]
        persona.cansancio = fila[11]
        persona.entidadcansancio = fila[12]
        
        personas.append(persona)
    conexion.close()
except:
    print("error al leer base de datos")

# En la colección introduzco instancias de personas en el caso de que no existan
print(len(personas))
if len(personas) == 0:
    numeropersonas = 10
    for i in range(0,numeropersonas):
        personas.append(Persona())

# Para cada una de las personas en la colección las pinto
for persona in personas:
    persona.dibuja()
    
# Creo un bucle repetitivo
def bucle():
    # Para cada persona en la colección
    for persona in personas:
        persona.mueve()
    raiz.after(10,bucle)
    
#Ejecuto el bucle
bucle()
raiz.mainloop()