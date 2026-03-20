import matplotlib.pyplot as plt
import matplotlib.animation as animation
import random
 
def bubble_sort(data):
    n = len(data)
 
    for i in range(n-1): # pasadas
        for j in range(n-1-i): # recorrido de intercambios
            if (data[j] > data[j+1]):
                data[j], data[j+1] = data[j+1], data[j] # intercambio basado en tuplas
                yield data
 
data = list(range(1, 51))
random.shuffle(data)
 
fig, ax = plt.subplots()
bars = ax.bar(range(len(data)), data)
 
ax.set_title("Sort Visualization")
 
def update(data):
    for bar, val in zip(bars, data):
        bar.set_height(val)
 
ani = animation.FuncAnimation(
    fig,
    update,
    frames=bubble_sort(data),
    #frames=selection_sort(data),
    #frames=insertion_sort(data),
    #frames=quick_sort(data),
    repeat=False,
    interval=100
)
 
plt.show()