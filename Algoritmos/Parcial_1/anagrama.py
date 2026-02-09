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
print(anagrama(palabra1 = "rat", palabra2 = "car"))
print(anagrama(palabra1 = "anagram", palabra2 = "nagaram"))
print(anagrama(palabra1 = "awesome", palabra2 = "awesom"))
print(anagrama(palabra1 = "qwerty", palabra2 = "qeywrt"))
print(anagrama(palabra1 = "texttwisstime", palabra2 = "timetwisttext"))