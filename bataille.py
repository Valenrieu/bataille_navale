import random
import copy
from time import sleep

# Renvoie une grille 10x10 sous forme de liste de listes

def creategrid():
    return [[0]*10 for i in range(10)]

# Renvoie True si le bateau rentre dans la grille et ne chevauche pas un autre bateau
# Renvoie False sinon

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

# Place le bateau sur la grille grid

def set_ships(grid, l, c, d, t, value):
    if d==1:
        for i in range(t):
            grid[l][c+i] = value

    else:
        for i in range(t):
            grid[l+i][c] = value

# Initialise la grille de l'ordi en placant les bateaux aleatoirement

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

# Permet d'afficher la grille

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

# Permet d'itinitialiser la grille du joueur

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

# Retourne True si le bateau dont le code est num a coule, False sinon

def hasDrowned(grid, num):
    for i in grid:
        if num in i:
            return False

    return True

# Permet l'affichage a l'ecran des actions, et la modification de la grille a chaque tour

def oneMove(grid, line, col):
    ships = {1:"Porte-avions", 2:"Croiseur", 3:"Contre-torpilleur", 4:"Sous-marin",
            5:"Torpilleur"}

    if grid[line][col]==0:
        print("A l'eau\n")

    else:
        print("Touche")
        value = grid[line][col]
        grid[line][col] = 6

        if hasDrowned(grid, value):
            print(ships.get(value)+" coule")

        print("")

    return grid

# Retourne True s'il n'y a plus de bateau non coules, False sinon

def isOver(grid):
    for i in grid:
        for j in i:
            if j!=0 and j!=6:
                return False

    return True

# Renvoie 2 entiers entre 0 et 9 compris pour que l'ordi joue aleatoirement

def playComp():
    res = random.randint(0, 9), random.randint(0, 9)

    return list(res)

# Permet l'affichage de la grille si le joueur le demande, renvoie les numeros de
# colonnes et lignes sur laquelle le joueur veut tirer

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
    
# Fonction qui implemente la partie

def play():
    letters = {0:"A", 1:"B", 2:"C", 3:"D", 4:"E", 5:"F", 6:"G", 7:"H", 8:"I", 9:"J"}
    mode = input("** Bienvenue, voulez-vous jouer joueur contre joueur (1), joueur contre IA (2) ou IA contre IA (3). **\n")

    # Mode joueur contre joueur

    if mode=="1":
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

    # Mode joueur contre IA

    elif mode=="2":
        j1 = initGridPlay()
        j2 = initGridComp()
        move1 = []
        move2 = []
        win = "IA"

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

            print("L'IA a joue :")
            move = playComp()
            while move in move2:
                move = playComp()

            print(move[0], letters.get(move[1]), sep="")
            move2.append(move)
            j1 = oneMove(j1, move[0], move[1])

        print(win+" a gagne !")

    # Mode IA contre IA

    elif mode=="3":
        try:
            time = float(input("Quel doit etre le temps en secondes entre chaque action de l'IA ?\n"))
        
        except ValueError:
            time = 0
            print("Par defaut, le temps sera de 0 sec.")

        j1 = initGridComp()
        j2 = initGridComp()
        move1 = []
        move2 = []
        win = "IA 2"

        while not isOver(j1):
            print("L'IA 1 a joue :")
            move = playComp()
            while move in move1:
                move = playComp()

            print(move[0], letters.get(move[1]), sep="")
            move1.append(move)
            j2 = oneMove(j2, move[0], move[1])

            if isOver(j2):
                win = "IA 1"
                break

            sleep(time)

            print("L'IA 2 a joue :")
            move = playComp()
            while move in move2:
                move = playComp()

            print(move[0], letters.get(move[1]), sep="")
            move2.append(move)
            j1 = oneMove(j1, move[0], move[1])
            sleep(time)

        print(win+" a gagne !")

    else:
        print("Le choix n'est pas bon !")
        return play()
