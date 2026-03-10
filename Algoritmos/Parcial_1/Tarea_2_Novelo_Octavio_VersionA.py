# **********VERSIÓN A****************************************

# Nota: Struct no existe en python. Lo que se hace es emular un struct usando clases (class)
# sin embargo se considera struct al tipo de dato que agrupa datos relacionados como lo es
# edad, nombre, etc. Se considera class cuando el tipo de dato tambien almacena metodos (funciones).
# Por si pregunta edson

# Estructura == struct

# Estructura de los estudiantes 
# Todos los estudiantes tienen un nombre, un apellido, edad. un id y fecha de registro
class Student:
   def __init__(self, name, lastname, age, id, year):   
      self.name = name  
      self.lastname = lastname            
      self.age = age
      self.id = id
      self.year = year
    
   def __str__(self):
      return f'{self.name}, {self.lastname}, {self.age}, {self.id}, {self.year}'

#  Listas 
people = [
   Student('Martha', 'Alvarez', 20, '816505', '2006'),
   Student('Erick', 'Perez', 32, '563188', '1992'),
   Student('Pedro', 'Montejo', 45, '235474', '1987'),
   Student('Laura', 'Cisneros', 37, '937125', '1990'),
   Student('Juan', 'Parra', 18, '754638', '2009'),
]
people2 = [
   Student('Martha', 'Alvarez', 20, '816505', '2006'),
   Student('Erick', 'Perez', 32, '563188', '1992'),
   Student('Pedro', 'Perez', 45, '235474', '1992'),
   Student('Laura', 'Cisneros', 37, '937125', '1990'),
   Student('Juan', 'Parra', 37, '754638', '2009'),
   Student('Cesar', 'Lara', 25, '122476', '1999'),
]

# Estrucutra de los estudiantes
# Todas las peliculas tienen nombre, genero, fecha de estreno e id
class Movies:
   def __init__(self, name, genre, year, id):   
      self.name = name  
      self.genre = genre           
      self.year = year
      self.id = id
    
   def __str__(self):
      return f'{self.name}, {self.genre}, {self.year}, {self.id}'

# Lista de peliculas
movies = [
   Movies('IronMan', 'Accion', 2006, 634128),
   Movies('Nueve', 'Terror', 2009, 999999),
   Movies('It', 'Terror', 2016, 852346),
   Movies('La la land', 'Romance', 1994, 567942),
   Movies('Lupin', 'Misterio', 1989, 365429),
   Movies('Interestelar', 'Ciencia ficcion', 2014, 397524),
]


# Nota: El valor de n puse 10 solo como ejemplo

#BUBLE SORT --------------------------------------------------------------------------------------------------------
print('\n ********** Buble sort ********** \n')

# La funcion recibe un data (cualquiera dato pero en este caso nuestras listas), una key
# que basicamente es el PARAMETRO que usara para la comparacion (edad, apellido, genero, id, etc)
# y el parametro de reverse = True que explicare despues
def bubble_sort(data, key, reverse = True):      
   n = len(data) 
   for i in range(n - 1): # Recorre el tamano de data
      sorted = True 
      for j in range(n - 1 - i): # Sirve para comparar de izquierda a derecha !! REVISAR 
         # n = 10 
         # i = 0 j = 0
         # i <= 9 j <= 9 - i 
         if reverse: # True
            # 0 > 1 = Si true se intercambia
            if key(data[j]) > key(data[j + 1]):
               data[j], data[j + 1] = data[j + 1], data[j]  #intercambio de tuplas
               sorted = False
         else: # False
            # 0 < 1 = Si true se intercambia
            if key(data[j]) < key(data[j + 1]):
               data[j], data[j + 1] = data[j + 1], data[j]  #intercambio de tuplas
               sorted = False
         
         # Si el codigo no entra ninguno de los condicionales significa que la lista esta ordenada (sorted = True)
      if sorted:
         return data


print('\n >>> Atributo numerico \n')
bubble_sort(people, lambda s: s.age) # reverse = True 
for i in people: 
   print(i)


print('\n >>> Atributo tipo texto \n')
bubble_sort(people, lambda s: s.name, False) # reverse = False
for i in people:
   print(i)


print('\n >>> Tupla \n')
bubble_sort(people2, lambda s: (s.lastname, s.name))
for i in people2:
    print(i)



#SELECTION SORT---------------------------------------------------------------------------------------------------
print('\n ********** Selection sort ********** \n')
# COMPROBAR ESTABILIDAD

# Mismo asunto, data, key, reverse
def selection_sort(data, key, reverse = True):    
   n = len(data)
   for i in range(n - 1):
      # n = 10 i = 0 i <= 9
      # mini = 0
      mini = i
      for j in range(i + 1, n):
         # j = 1
         # 1 <= j <= 10
         if reverse:
            if key(data[j]) < key(data[mini]):
               mini = j
         else:
            if key(data[j]) > key(data[mini]):
               mini = j 

      data[i], data[mini] = data[mini], data[i] # intercambio de tuplas ya tu sabe

   return data


# Ordenar usando un valor numerico, en este caso por id
print('\n >>> Atributo numerico \n')
# REVISAR, estoy seguro que debe recibir una variable para que tenga chiste el lambda, pero implicaria que no esten todos los ejemplos en el mismo doc
selection_sort(movies, lambda s: s.id, False) # reverse = False 
for i in movies: # Imprimir la lista
   print(i)


# Ordenar usando un valor string, en este caso por genero
print('\n >>> Atributo tipo texto \n')
selection_sort(movies, lambda s: s.genre) # reverse = True 
for i in movies:
   print(i)


# Creo que era para comparar por un segundo atributo
print('\n >>> Tupla \n')
selection_sort(people2, lambda s: (s.age, s.id))
for i in people2:
    print(i)



#INSERTION SORT---------------------------------------------------------------------------------------------------
print('\n ********** Insertion sort ********** \n')

def insertion_sort(data, key, reverse = True):  
   n = len(data)
   for i in range(1, n):
      e = key(data[i])
      save = data[i]
      j = i - 1
      # i = 1 ; n = 10
      # e = id(data[1])
      # save = data[1]
      # j = 1 - 1 
      if reverse:
       # 0 >= 0 and id(data[0]) > id(data[1])
       while j >= 0 and key(data[j]) > e:
            # data[1] = data[0]
            data[j + 1] = data[j]
            j -= 1
      else:
         while j >= 0 and key(data[j]) < e:
            data[j + 1] = data[j]
            j -= 1

      data[j + 1] = save
   return data


print('\n >>> Atributo numerico \n')
insertion_sort(movies, lambda s: s.year,False)
for i in movies:
   print(i)


print('\n >>> Atributo tipo texto \n')
insertion_sort(movies, lambda s: s.name)
for i in movies:
   print(i)


print('\n >>> Tupla \n')
insertion_sort(people2, lambda s: (s.year, s.name))
for i in people2:
    print(i)