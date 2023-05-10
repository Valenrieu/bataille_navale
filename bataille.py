import random
import copy
import sys
import vernam
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

# Permet l'affichage a l'ecran des actions, et la modification de la grille
# a chaque tour. Renvoie la grille et le numero du bateau touche 0 sinon

def oneMove(grid, line, col):
    ships = {1:"Porte-avions", 2:"Croiseur", 3:"Contre-torpilleur", 4:"Sous-marin",
            5:"Torpilleur"}

    if grid[line][col]==0:
        print("A l'eau\n")
        value = 0

    else:
        print("Touche")

        value = grid[line][col]
        grid[line][col] = 6

        if hasDrowned(grid, value):
            print(ships.get(value)+" coule")

        print("")

    return grid, value

# Retourne True s'il n'y a plus de bateau non coules, False sinon

def isOver(grid):
    for i in grid:
        for j in i:
            if j!=0 and j!=6:
                return False

    return True

# Permet l'acharnement de l'IA sur un bateau, genere toutes les cases ou
# le bateau peut etre, en fonction de sa taille et eventuellement de son
# orientation, si on l'a touche plus d'une fois.

def drown(grid, move, index, last):
    ships_len = {1:5, 2:4, 3:3, 4:3, 5:2}
    possibilities = []

    try:
        # S'il y a le bateau en ligne 
        if index[0] not in (0, 10) and index[1] not in (0, 10) and grid[index[0]][index[1]+1]==last or grid[index[0]][index[1]-1]==last:
            if grid[index[0]][index[1]+1]==last and grid[move[-1][0]][move[-1][1]]==last:
                for k in range(1, ships_len.get(last)):
                    if (index[0], index[1]+k) not in move and index[1]+k<10:
                        possibilities.append((index[0], index[1]+k))
            
            else:
                for k in range(1, ships_len.get(last)):
                    if (index[0], index[1]-k) not in move and index[1]-k>=0:
                        possibilities.append((index[0], index[1]-k))

            if len(possibilities)==0:
                for k in range(1, ships_len.get(last)):
                    if (index[0], index[1]-k) not in move and index[1]-k>=0:
                        possibilities.append((index[0], index[1]-k))

                for k in range(1, ships_len.get(last)):
                    if (index[0], index[1]+k) not in move and index[1]+k<10:
                        possibilities.append((index[0], index[1]+k))

        # S'il est vertical
        elif grid[index[0]+1][index[1]]==last or grid[index[0]-1][index[1]]==last and index[0]!=0 and index[0]!=10:
            if grid[index[0]+1][index[1]]==last and grid[move[-1][0]][move[-1][1]]==last:
                for k in range(1, ships_len.get(last)):
                    if (index[0]+k, index[1]) not in move and index[0]+k<10:
                        possibilities.append((index[0]+k, index[1]))

            else:
                for k in range(1, ships_len.get(last)):
                    if (index[0]-k, index[1]) not in move and index[0]-k>=0:
                        possibilities.append((index[0]-k, index[1]))

            if len(possibilities)==0:
                for k in range(1, ships_len.get(last)):
                    if (index[0]-k, index[1]) not in move and index[0]-k>=0:
                        possibilities.append((index[0]-k, index[1]))

                for k in range(1, ships_len.get(last)):
                    if (index[0]+k, index[1]) not in move and index[0]+k<10:
                        possibilities.append((index[0]+k, index[1]))

        else:
            for k in range(1, ships_len.get(last)):
                if (index[0], index[1]+k) not in move and index[1]+k<10:
                    possibilities.append((index[0], index[1]+k))

                if (index[0], index[1]-k) not in move and index[1]-k>=0:
                    possibilities.append((index[0], index[1]-k))

                if (index[0]+k, index[1]) not in move and index[0]+k<10:
                    possibilities.append((index[0]+k, index[1]))

                if (index[0]-k, index[1]) not in move and index[0]-k>=0:
                    possibilities.append((index[0]-k, index[1]))

    except IndexError:
        for k in range(1, ships_len.get(last)):
            if (index[0], index[1]+k) not in move and index[1]+k<10:
                possibilities.append((index[0], index[1]+k))

            if (index[0], index[1]-k) not in move and index[1]-k>=0:
                possibilities.append((index[0], index[1]-k))

            if (index[0]+k, index[1]) not in move and index[0]+k<10:
                possibilities.append((index[0]+k, index[1]))

            if (index[0]-k, index[1]) not in move and index[0]-k>=0:
                possibilities.append((index[0]-k, index[1]))

    return possibilities[0]

# Implemente l'IA, renvoie un tuple de deux entiers entre 0 et 9
# Prend en argument l'historique des mouvements (liste) et les resultats
# correspondants, aussi une liste et la difficulte ("1", "2", ou "3").
# Difficulte 1 : totalement aleatoire
# Difficulte 2 : L'IA reconstruit la grille ennemie grace a son historique
# de tirs et de resultats, elle tire au hasard jusqu'a qu'elle touche un bateau
# puis elle s'acharne ensuite dessus, etc..
# Difficulte 3 : Elle reconstruit aussi la grille adverse, puis utilise une
# fonction d'evaluation pour choisir ses coups, des qu'elle touche un
# bateau, elle s'acharne.

def playComp(move, res1, difficulty):
    ships_len = {1:5, 2:4, 3:3, 4:3, 5:2}
    last = None
    grid = creategrid()

    if difficulty=="1":
        res = random.randint(0, 9), random.randint(0, 9)

        while res in move:
            res = random.randint(0, 9), random.randint(0, 9)

        return res

    elif difficulty=="2":
        for i in range(len(res1)):
            if res1[i]!=0:
                grid[move[i][0]][move[i][1]] = res1[i]

            else:
                grid[move[i][0]][move[i][1]] = 7

        for i in range(len(res1)):
            if res1[i]!=0:
                last = res1[i]
                index = move[i]

                if res1.count(last)!=ships_len.get(last):
                    return drown(grid, move, index, last)

        if last is None or res1.count(last)==ships_len.get(last):
            res = random.randint(0, 9), random.randint(0, 9)

            while res in move:
                res = random.randint(0, 9), random.randint(0, 9)

        return res
    
    elif difficulty=="3":
        for i in range(len(res1)):
            if res1[i]!=0:
                grid[move[i][0]][move[i][1]] = res1[i]

            else:
                # On met un 7, pour les coups rates, quand il va verifier
                # si la position est valide ou non, et qu'il y a un 7,
                # il saura que non
                grid[move[i][0]][move[i][1]] = 7

        for i in range(len(res1)):
            if res1[i]!=0:
                last = res1[i]
                index = move[i]

                if res1.count(last)!=ships_len.get(last):
                    return drown(grid, move, index, last)

        if last is None or res1.count(last)==ships_len.get(last):
            score = creategrid()

            for i in range(len(score)):
                for j in range(len(score)):
                    for k in [2, 3, 3, 4, 5]:
                        if validPosition(grid, i, j, 1, k):
                            for l in range(k):
                                score[i][j+l] += 1

                        if validPosition(grid, i, j, 2, k):
                            for l in range(k):
                                score[i+l][j] += 1

            max = float('-inf')
            index = (0, 0)

            for i in range(len(score)):
                for j in range(len(score)):
                    if score[i][j]>max and (i, j) not in move:
                        max = score[i][j]
                        index = (i, j)

            return index

# Permet l'affichage de la grille si le joueur le demande, renvoie les numeros de
# colonnes et lignes sur laquelle le joueur veut tirer, si le joueur a tire
# sur une case, une croix sera affichee.

def playPlayer(grid1, grid2, move1):
    letters = {"A":0, "B":1, "C":2, "D":3, "E":4, "F":5, "G":6, "H":7, "I":8, "J":9}

    rep = input("Sur quelle case voulez-vous tirer ? (ex : 'B1' ou 'D6'), tapez 'afficher' si vous voulez voir la grille adverse.\n").upper()

    if rep=="AFFICHER":
        res = copy.deepcopy(grid2)

        for i in range(len(res)):
            for j in range(len(res)):
                if res[i][j]!=0 and res[i][j]!=6:
                    res[i][j] = 0

                elif (i, j) in move1 and res[i][j]!=6:
                    res[i][j] = "x"

        printGrid(res)
        return playPlayer(grid1, grid2, move1)

    elif (len(rep)==2 or len(rep)==3) and "A">=rep[1]<="Z":
        try:
            if len(rep)==2:
                if rep[0]<"A" or rep[0]>"J" or int(rep[1])<1 or int(rep[1])>9:
                    print("La position n'est pas valide")
                    return playPlayer(grid1, grid2, move1)

                return int(rep[1])-1, letters.get(rep[0])

            else:
                if rep[0]<"A" or rep[0]>"J" or int(rep[1]+rep[2])!=10:
                    print("La position n'est pas valide")
                    return playPlayer(grid1, grid2, move1)

                return int(rep[1]+rep[2])-1, letters.get(rep[0])

        except ValueError:
            print("L'argument n'est pas valide")
            return playPlayer(grid1, grid2, move1)

    else:
        print("L'argument n'est pas valide")
        return playPlayer(grid1, grid2, move1)

# Permet de sauver les donnees du jeu dans 'game_data.txt' de la maniere suivante :
# 1ere ligne, le mode de jeu, 1, 2 ou 3 (JcJ, JcIA, IAcIA)
# 2e ligne : le nom du prochain joueur, 3e : le nom du joueur 1
# 4e : tous les coups joues par j1, 5e les resultats des coups 6 a 15 :
# la grille de j1, 16e : le nom du joueur 2, 17e : les coups du j2
# 18 les resultats du joueur 2 19 a 28 : la grille de j2, eventuellement 28, 29
# la difficulte et le temps de reponse des IA

def save(next, grid1, move1, res1, player1, grid2, move2, res2, player2, mode, difficulty=None, time=None):
    key = vernam.random_key()

    open("game_data.txt", "w").close()

    data = next+"\n"+player1+"\n"

    for i in move1:
        data += str(i[0])+str(i[1])+" "

    data += "\n"

    for i in res1:
        data += str(i)+" "

    data += "\n"

    for i in grid1:
        for j in i:
            data += str(j)

        data += "\n"

    data += player2+"\n"

    for i in move2:
        data += str(i[0])+str(i[1])+" "

    data += "\n"

    for i in res2:
        data += str(i)+" "

    data += "\n"

    for i in grid2:
        for j in i:
            data += str(j)

        data += "\n"

    if difficulty is not None:
        data += difficulty

    data += "\n"

    if time is not None:
        data += str(time)+"\n"

    with open("game_data.txt", "a") as file:
        file.write(vernam.cipher((mode+"\n"+data).upper(), key))

# Charge les donnes du fichier pour une reprise de jeu, renvoie un tuple
# du mode de partie, le nom du prochain joueur qui doit jouer , le nom du
# joueur1, les coups du joueur1, les resultats des coups, la grille du
# joueur 1, la meme chose pour le joueur 2 ensuite, la difficulte, et le temps :
# None ou float

def load():
    grid1, grid2 = [], []
    move1, move2 = [], []
    res1, res2 = [], []
    time = None
    difficulty = None

    with open("game_data.txt", "r") as file:
        res = file.read()

    data = vernam.decipher(res)
    data = data.split("\n")

    player1, player2 = data[2], data[15]
    mode = data[0]
    next = data[1]

    for i in range(0, len(data[3]), 3):
        move1.append((int(data[3][i]), int(data[3][i+1])))

    for i in range(0, len(data[16]), 3):
        move2.append((int(data[16][i]), int(data[16][i+1])))

    for i in range(0, len(data[4]), 2):
        res1.append(int(data[4][i]))

    for i in range(0, len(data[17]), 2):
        res2.append(int(data[17][i]))

    for i in range(5, 15):
        res = []
        for j in data[i]:
            res.append(int(j))

        grid1.append(res)

    for i in range(18, 28):
        res = []
        for j in data[i]:
            res.append(int(j))

        grid2.append(res)

    try:
        difficulty = data[28]
        time = float(data[29])

    except ValueError:
        pass

    except IndexError:
        pass

    return mode, next, player1, move1, res1, grid1, player2, move2, res2, grid2, difficulty, time

# Fonction qui permet le deroulement de la partie, permet de sauvegarder 
# automatiquement la partie si l'utilisateur fait CTRL+C, s'il quitte
# sans faire CTRL+C, il n'y aura pas de sauvegarde

def run_game(mode, j1, j2, player1, player2, move1, move2, res1, res2, difficulty=None, time=None):
    letters = {0:"A", 1:"B", 2:"C", 3:"D", 4:"E", 5:"F", 6:"G", 7:"H", 8:"I", 9:"J"}
    next = player1

    try:

        # Mode JcJ

        if mode=="1":
            win = player2

            while not isOver(j1):
                print(player1+" !", end=" ")
                move = playPlayer(j1, j2, move1)
                while move in move1:
                    print("Vous avez deja joue ce coup.")
                    move = playPlayer(j1, j2, move1)

                j2, last1 = oneMove(j2, move[0], move[1])
                move1.append(move)
                res1.append(last1)
                next = player2

                if isOver(j2):
                    win = player1
                    break

                print(player2+" !", end=" ")
                move = playPlayer(j2, j1, move2)
                while move in move2:
                    print("Vous avez deja joue ce coup.")
                    move = playPlayer(j2, j1, move1)

                j1, last2 = oneMove(j1, move[0], move[1])
                move2.append(move)
                res2.append(last2)
                next = player1

            print(win+" a gagne !")
            print("Au-revoir")
            sleep(1)

        # Mode JcIA

        elif mode=="2":
            win = player2

            while not isOver(j1):
                print(player1+" !", end=" ")
                move = playPlayer(j1, j2, move1)
                while move in move1:
                    print("Vous avez deja joue ce coup.")
                    move = playPlayer(j1, j2, move1)

                j2, last1 = oneMove(j2, move[0], move[1])
                move1.append(move)
                res1.append(last1)
                next = player2

                if isOver(j2):
                    win = player1
                    break

                next = player1
                print("L'IA a joue :")
                move = playComp(move2, res2, difficulty)

                print(letters.get(move[1]), move[0]+1, sep="")
                j1, last2 = oneMove(j1, move[0], move[1])
                move2.append(move)
                res2.append(last2)

            print(win+" a gagne !")
            print("Au-revoir")
            sleep(1)

        # Mode IAcIA

        elif mode=="3":
            win = player2

            while not isOver(j1):
                next = player2
                print("L'"+player1+" a joue :")
                move = playComp(move1, res1, difficulty)

                print(letters.get(move[1]), move[0]+1, sep="")
                j2, last1 = oneMove(j2, move[0], move[1])
                move1.append(move)
                res1.append(last1)
    
                if isOver(j2):
                    win = player1
                    break

                sleep(time)

                next = player1
                print("L'"+player2+" a joue :")
                move = playComp(move2, res2, difficulty)
                print(letters.get(move[1]), move[0]+1, sep="")
                j1, last2 = oneMove(j1, move[0], move[1])
                move2.append(move)
                res2.append(last2)
                sleep(time)

            print(win+" a gagne !")
            print("Au-revoir")
            sleep(1)

    except KeyboardInterrupt:
        save(next, j1, move1, res1, player1, j2, move2, res2, player2, mode, difficulty=difficulty, time=time)
        print("Au-revoir !")
        sys.exit()

# Fonction qui implemente la partie

def play():
    try:
        mode = input("** Bienvenue, choisissez votre mode de jeu : **\n1 : joueur contre joueur\n2 : Joueur contre IA\n3 : IA contre IA\n4 : Reprendre la partie precedente\n")

        # Mode joueur contre joueur

        if mode=="1":
            j1 = initGridPlay()
            j2 = initGridPlay()
            move1, move2 = [], []
            res1, res2 = [], []
            run_game(mode, j1, j2, "JOUEUR 1", "JOUEUR 2", move1, move2, res1, res2)

        # Mode joueur contre IA

        elif mode=="2":
            difficulty = input("Quel doit etre la difficulte de l'IA, facile (1), moyen (2) ou difficile (3) ?\n")
            j1 = initGridPlay()
            j2 = initGridComp()
            move1, move2 = [], []
            res1, res2 = [], []
            run_game(mode, j1, j2, "JOUEUR 1", "IA", move1, move2, res1, res2, difficulty=difficulty)

        # Mode IA contre IA

        elif mode=="3":
            try:
                time = float(input("Quel doit etre le temps en secondes entre chaque action de l'IA ?\n"))

            except ValueError:
                time = float(0)
                print("Par defaut, le temps sera de 0 sec.")

            difficulty = input("Quel doit etre la difficulte de l'IA, facile (1), moyen (2) ou difficile (3) ?\n")

            if difficulty not in ("1", "2", "3"):
                print("La difficulte choisie, n'existe pas.\n")
                return play()

            j1 = initGridComp()
            j2 = initGridComp()
            move1, move2 = [], []
            res1, res2 = [], []
            run_game(mode, j1, j2, "IA 1", "IA 2", move1, move2, res1, res2, difficulty=difficulty, time=time)

        # Reprise de partie

        elif mode=="4":
            try:
                data = load()
                player1 = data[1]

                if data[2]==player1:
                    player2 = data[6]
                    move1, move2 = data[3], data[7]
                    res1, res2 = data[4], data[8]
                    j1, j2 = data[5], data[9]

                else:
                    player2 = data[2]
                    move1, move2 = data[7], data[3]
                    res1, res2 = data[8], data[4]
                    j1, j2 = data[9], data[5]

                difficulty = data[10]
                time = data[11]
                mode = data[0]

            except IndexError:
                print("Il n'y a pas de partie a charger.\n")
                return play()

            if isOver(j1) or isOver(j2):
                print("La partie est finie, recommencez-en une.\n")
                return play()

            print("")
            run_game(mode, j1, j2, player1, player2, move1, move2, res1, res2, difficulty=difficulty, time=time)

        else:
            print("Le choix n'est pas bon.\n")
            return play()

    except KeyboardInterrupt:
        print("Au-revoir !")
        sys.exit()

play()
