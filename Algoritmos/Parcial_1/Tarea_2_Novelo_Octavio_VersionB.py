#**********VERSIÓN B****************************************
class Student:
      def __init__(self, name, lastname, age, id, year):   
         self.name = name  
         self.lastname = lastname            
         self.age = age
         self.id = id
         self.year = year
    
      def __str__(self):
         return f'{self.name}, {self.lastname}, {self.age}, {self.id}, {self.year}'
    
people = [
   Student('Martha', 'Alvarez', 20, '816505', '2006'),
   Student('Erick', 'Perez', 32, '563188', '1992'),
   Student('Pedro', 'Montejo', 45, '235474', '1987'),
   Student('Laura', 'Cisneros', 37, '937125', '1990'),
   Student('Juan', 'Parra', 18, '754638', '2009'),
]

class Movies:
    def __init__(self, name, type, year, id):   
         self.name = name  
         self.type = type           
         self.year = year
         self.id = id
    
    def __str__(self):
         return f'{self.name}, {self.type}, {self.year}, {self.id}'
    
movies3 = [
   Movies('IronMan', 'Accion', 2006, 634128),
   Movies('Nueve', 'Terror', 2009, 999999),
   Movies('It', 'Terror', 2016, 852346),
   Movies('La la land', 'Romance', 1994, 567942),
   Movies('Lupin', 'Misterio', 1989, 365429),
   Movies('Interestelar', 'Ciencia ficcion', 2014, 397524),
]

#BUBLE SORT --------------------------------------------------------------------------------------------------------
def bubble_sort(data, cmp, reverse = True):
   n = len(data)
   for i in range( n - 1):
      sorted = True
      for j in range(n - 1 - i):
         if reverse:
            if cmp(data[j], data[j + 1]) > 0:
               data[j], data[j + 1] = data[j + 1], data[j]
               sorted = False

         else:
            if cmp(data[j], data[j + 1]) < 0:
               data[j], data[j + 1] = data[j + 1], data[j]
               sorted = False

      if sorted:
         return data

   return data

print('\n >>> Atributo numerico \n')
bubble_sort(people, lambda a, b: a.age - b.age)
for i in people:
   print(i)

print('\n >>> Atributo tipo texto \n')
bubble_sort(people, lambda a, b: (a.name > b.name) - (a.name < b.name)) #Compara alfabeticamente, siendo mayor la letra que va despues
for i in people:
   print(i)


#SELECTION SORT---------------------------------------------------------------------------------------------------
print('\n ********** Selection sort **********\n')

def selection_sort(data, cmp, reverse = True):    
   n = len(data)
   for i in range(n - 1):
      mini = i
      for j in range(i + 1, n):
         if reverse:
          if cmp((data[j]), (data[mini])) < 0:
             mini = j
         else:
           if cmp((data[j]), (data[mini])) > 0:
             mini = j 

      data[i], data[mini] = data[mini], data[i]

   return data

print('\n >>> Atributo numerico \n')
selection_sort(movies3, lambda a, b: a.year - b.year)
for i in movies3:
   print(i)

print('\n >>> Atributo tipo texto\ n')
selection_sort(movies3, lambda a, b: (a.type > b.type)- (a.type < b.type ),False)
for i in movies3:
   print(i)


#INSERTION SORT---------------------------------------------------------------------------------------------------
print('\n ********** Insertion sort **********\n')

def insertion_sort(data, cmp, reverse = True):  
   n = len(data)
   for i in range(1, n):
      e = data[i]
      j = i - 1
      if reverse:
         while j >= 0 and cmp((data[j]), e) > 0:
            data[j + 1] = data[j]
            j -= 1
      else:
         while j >= 0 and cmp((data[j]), e) < 0:
            data[j + 1] = data[j]
            j -= 1

      data[j + 1] = e
   return data

print('\n >>> Atributo numerico \n')
insertion_sort(movies3, lambda a, b: a.id - b.id, False)
for i in movies3:
   print(i)

print('\n >>> Atributo tipo texto \n')
insertion_sort(people, lambda a, b: (a.lastname > b.lastname)-(a.lastname < b.lastname))
for i in people:
   print(i)