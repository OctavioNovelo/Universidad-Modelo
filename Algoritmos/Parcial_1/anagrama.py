def anagrama(palabra1, palabra2):

    resultado1 = 0
    resultado2 = 0

    resultado1 += sum(ord(char) for char in palabra1)
    resultado2 += sum(ord(char) for char in palabra2)

    if resultado1 == resultado2:
        return True
    else:
        return False


print(anagrama(palabra1 = ", ", palabra2 = ", "))
