import matplotlib.pyplot as plt
import matplotlib.animation as animation
import random

#Radix sort
def radix_sort(data):
    def countingdigit_sort(data, exp):
        n = len(data) # n = 50
        count = [0] * 10 # ???

        for num in data:
            i = (num // exp) % 10
            # i = (0 // ???) % 10 = 
            count[i] += 1
            # count[i] += 1

        for i in range(1, 10):
            count[i] += count[i - 1]
            # count [1] += count[1 - 1] 

        output = [0] * n

        for i in range(n-1, -1, -1):
            a = data[i]
            d = (a // exp) % 10
            b = count[d] - 1

            output[b] = a
            count[d] -= 1

            temp = data.copy()
            for j in range(n):
                if output[j] != 0:
                    temp[j] = output[j]

            yield temp

        return output

    valor_max = max(data)
    exp = 1

    while valor_max // exp > 0:
        gen = countingdigit_sort(data, exp)

        for frame in gen:
            yield frame  

        data = list(gen)[-1] if False else sorted(data, key=lambda x: (x // exp) % 10)

        exp *= 10

    yield data


data = list(range(1, 51))
random.shuffle(data)


# Lo de la animacion
# Nota: Estas son funciones para la animacion
fig, ax = plt.subplots()
bars = ax.bar(range(len(data)), data)

ax.set_title("Radix Sort") # Titulo

# Update
def update(data):
    for bar, val in zip(bars, data):
        bar.set_height(val)

ani = animation.FuncAnimation(
    fig,
    update,
    frames = radix_sort(data),
    #frames=selection_sort(data),
    #frames=insertion_sort(data),
    #frames=quick_sort(data),
    repeat = False,
    interval = 100
)
 
plt.show()
