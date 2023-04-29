import random
import copy

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

    print(10, end=" ")
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
        try:
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

        except ValueError:
            print("Les arguments ne sont pas bons, recommencez.")
            continue

    print("\n"*50)

    return grid

def hasDrowned(grid, num):
    for i in grid:
        if num in i:
            return False

    return True

def oneMove(grid, line, col):
    ships = {1:"Porte-avions", 2:"Croiseur", 3:"Contre-torpilleur", 4:"Sous-marin",
            5:"Torpilleur"}

    if grid[line][col]==0:
        print("A l'eau")

    else:
        print("Touche")
        value = grid[line][col]
        grid[line][col] = 6

        if hasDrowned(grid, value):
            print(ships.get(value)+" coule")

    return grid

def isOver(grid):
    for i in grid:
        for j in i:
            if j!=0 and j!=6:
                return False

    return True

def playComp():
    res = random.randint(0, 9), random.randint(0, 9)

    return list(res)

def playPlayer(grid1, grid2):
    letters = {"A":0, "B":1, "C":2, "D":3, "E":4, "F":5, "G":6, "H":7, "I":8, "J":9}

    rep = input("Sur quelle case voulez-vous tirer ? (ex : 'B1' ou 'D6'), tapez 'afficher' si vous voulez voir la grille adverse.\n").upper()

    if rep=="AFFICHER":
        res = copy.deepcopy(grid2)

        for i in range(len(res)):
            for j in range(len(res)):
                if res[i][j]!=0 and res[i][j]!=6:
                    res[i][j] = 0

        printGrid(res)
        return playPlayer(grid1, grid2)

    elif (len(rep)==2 or len(rep)==3) and "A">=rep[1]<="Z":
        try:
            if len(rep)==2:
                if rep[0]<"A" or rep[0]>"J" or int(rep[1])<1 or int(rep[1])>9:
                    print("La position n'est pas valide")
                    return playPlayer(grid1, grid2)

                return int(rep[1])-1, letters.get(rep[0])

            else:
                if rep[0]<"A" or rep[0]>"J" or int(rep[1]+rep[2])!=10:
                    print("La position n'est pas valide")
                    return playPlayer(grid1, grid2)

                return int(rep[1]+rep[2])-1, letters.get(rep[0])

        except ValueError:
            print("L'argument n'est pas valide")
            return playPlayer(grid1, grid2)

    else:
        print("L'argument n'est pas valide")
        return playPlayer(grid1, grid2)

def play():
    j1 = initGridPlay()
    j2 = initGridPlay()
    move1 = []
    move2 = []
    win = "Joueur 2"

    while not isOver(j1):
        print("Joueur 1 !", end=" ")
        move = playPlayer(j1, j2)
        while move in move1:
            print("Vous avez deja joue ce coup.")
            move = playPlayer(j1, j2)

        move1.append(move)
        j2 = oneMove(j2, move[0], move[1])

        if isOver(j2):
            win = "Joueur 1"
            break

        print("Joueur 2 !", end=" ")
        move = playPlayer(j2, j1)
        while move in move2:
            print("Vous avez deja joue ce coup.")
            move = playPlayer(j2, j1)

        move2.append(move)
        j1 = oneMove(j1, move[0], move[1])

    print(win+" a gagne !")
