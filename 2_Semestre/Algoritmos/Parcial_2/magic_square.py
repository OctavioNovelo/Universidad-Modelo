import numpy as np

def validate_magic_square(n,M,square):
    #validate rows
    for i in range(n):
        suma = 0
        for j in range(n):
            suma += square[i,j]

        if suma != M:
            return False    

    #validate cols
    for i in range(n):
        suma = 0
        for j in range(n):
            suma += square[j,i]

        if suma != M:
            return False  
    #validate diags I-D
    suma = 0
    for i in range(n):
        suma+= square[i,i]

    if suma != M:
        return False    

    #validate diags D-I
    suma = 0
    for i in range(n):
        suma+= square[i,n-1-i]

    if suma != M:
        return False  


    return True

def print_magic_square_impl(n, M, square, pos, used):
    #calculate row & col
    row = pos // n
    col = pos % n

#we will try every digit
    for num in range(1,n*n+1):
        #if current digit has been used jump to next iteration
        if used[num]:
            continue

        #if digit has not been used, set current digit as being used
        square[row,col]=num
        used[num]=True

        #Validate on-road  


        #If square has been filled
        if pos==n*n-1:
            #validate magic square
           # if (validate_magic_square(n,M,square)): ----------------------------
                print(f'{square}\n')
        else:
            print_magic_square_impl(n,M,square,pos+1,used)

        #backtrack
        used[num]=False



        

def print_magic_square(n):
    M=n*(n*n+1)//2
    square=np.zeros((n,n), dtype=int)
    used=np.zeros(n*n+1, dtype=bool)

    print_magic_square_impl(n,M,square,0,used)




n=3
print_magic_square(n)