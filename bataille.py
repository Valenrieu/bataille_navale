import random

def creategrid():
    return [[0]*10 for i in range(10)]

def validPosition(array, l, c, d, t):
    if d==1:
        for i in range(t):
            try:
                if array[l][c+i]!=0:
                    return False

            except IndexError:
                return False

        return True

    elif d==2:
        for i in range(t):
            try:
                if array[l+i][c]!=0:
                    return False

            except IndexError:
                return False

        return True

    else:
        raise ValueError(f"d={d} is not a valid argument.")

def set_ships(grid, l, c, d, t, value):
    if d==1:
        for i in range(t):
            grid[l][c+i] = value

    else:
        for i in range(t):
            grid[l+i][c] = value

def initGridComp():
    gridComp = creategrid()
    ships_len = [5, 4, 3, 3, 2]
    code = [1, 2, 3, 4, 5]

    while len(ships_len)!=0:
        d = random.randint(1, 2)
        l, c = random.randint(0, 10), random.randint(0, 10)

        if validPosition(gridComp, l, c, d, ships_len[0]):
            set_ships(gridComp, l, c, d, ships_len[0], code[0])

            del ships_len[0]
            del code[0]

    return gridComp

def printGrid(grid):
    print("   A B C D E F G H I J")

    for i in range(9):
        print(str(i+1)+"  ", end="")

        for j in grid[i]:
            print(j, end=" ")

        print("")
    
    print(i+2, end=" ")
    for j in grid[i+1]:
        print(j, end=" ")

    print("")

def initGridPlay():
    grid = creategrid()
    letters = {"A":0, "B":1, "C":2, "D":3, "E":4, "F":5, "G":6, "H":7, "I":8, "J":9}
    ships = ["porte-avions", "croiseur", "contre-torpilleur", "sous-marin",
            "torpilleur"]
    code = [1, 2, 3, 4, 5]
    ships_len = [5, 4, 3, 3, 2]

    print("** Placement des bateaux : **")

    while len(code)!=0:
        letter = input("Donnez la lettre pour le "+ships[0]+" :\n").upper()
        number = int(input("Donnez le nombre pour le "+ships[0]+" :\n"))
        d = int(input("Voulez-vous qu'il soit horizontal (1) ou vertical (2) ?\n"))

        if letter not in letters or number>=11 or number<0 or d not in (1, 2) or type(number)!=int:
            print("Erreur : Les arguments passes ne sont pas bons, recommencez.")
            continue

        elif not validPosition(grid, number-1, letters.get(letter), d, ships_len[0]):
            print("Erreur : Le "+ships[0]+" ne rentre pas dans la grille.")
            continue

        set_ships(grid, number-1, letters.get(letter), d, ships_len[0], code[0])
        del ships[0]
        del ships_len[0]
        del code[0]
