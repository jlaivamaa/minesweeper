import random, time

#Luo miinakentän ottamalla käyttäjän syöttämän pituuden ja leveyden
def generate_grid(width, height):
    field = []
    for row in range(width):
        field.append([])
        for column in range(height):
            field[-1].append("[ ]")
    return field

#Tulostaa miinakentän
def print_grid(field):
    grid = []
    for row in field:
        grid.append(" ".join(str(tile) for tile in row))
    print("\n".join(grid))

#Pyytää käyttäjältä x, y koordinaatit ja tarkistaa onko syöttö laillinen
def request_coordinates(width, height):
    while True:
        try:
            result = input("Give coordinates x,y: ")
            result = result.split(",")
            result[1] = int(result[1])
            result[0] = int(result[0])
            if result[1] > width or result[0] > height or result[1] < 0 or result[0] < 0:
                print("\nCoordinates are outside the grid\n")
                continue
        except ValueError:
            print("\nGive the coordinates as integers\n")
            continue
        except IndexError:
            print("\nGive two coordinates separated with a comma\n")
            continue
        return result[1], result[0]

#Luo käyttäjän määrittämän määrän miinoja miinakentän rajojen sisällä satunnaisiin paikkoihin ja tallentaa ne monikkolistaan
def plant_mines(mine_amount, grid):
    list_of_mines = []
    unmined = []
    for x in range(len(grid)):
        for y in range(len(grid[0])):
            unmined.append((x, y))

    while mine_amount > 0:
        x = random.randrange(len(grid))
        y = random.randrange(len(grid[0]))
        mines = (x, y)
        if mines in unmined:
                unmined.remove(mines)
                list_of_mines.append(mines)
                mine_amount -= 1
    return list_of_mines

#Tulva-algoritmi, joka käy läpi annettujen koordinaattien naapurit, avaa tyhjät ja pysähtyy kuin löytää miinan naapurin rajalla
#Otin väljästi esimerkkiä https://stackoverflow.com/questions/26711011/python-floodfill-algorithm-for-minesweeper siinä, miten tyhjien solujen läpi iteroidaan
def floodfill(grid, x, y, mines):
    if(x < 0 or y < 0 or x > len(grid) or y > len(grid[0])):
        return

    if (x, y) in mines:
        return

    if grid[x][y] == "[ ]":
        count = get_neighbors(grid, x, y, mines)

        grid[x][y] = "[{}]".format(count)
        if count == 0:
            grid[x][y] = "[E]"
            if x > 0:
                floodfill(grid, x - 1, y, mines)
            if x < len(grid) - 1:
                floodfill(grid, x + 1, y, mines)
            if y > 0:
                floodfill(grid, x, y - 1, mines)
            if y < len(grid[0]) - 1:
                floodfill(grid, x, y + 1, mines)
    return grid

#Käy läpi x,y koordinaattien naapurit, tarkistaa sisältävätkö ne miinoja ja palauttaa naapureista löydettyjen miinojen lukumäärän
#Otin väljästi esimerkkiä https://stackoverflow.com/questions/1620940/determining-neighbours-of-cell-two-dimensional-list ensimmäisestä ja kolmannesta vastauksesta funktion for-looppien luomisessa
def get_neighbors(grid, x, y, mines):
    neighbor_mine_count = 0
    for i in range(max(0, x - 1), min(len(grid), x + 2)):
        for j in range(max(0, y - 1), min(len(grid[0]), y + 2)):
            if(i != x or j != y):
                for mine in mines:
                    if mine == (i, j):
                        neighbor_mine_count += 1
    return neighbor_mine_count

#Paljastaa jäljelle jääneet miinat pelin päätyttyä
def reveal_mines(grid, mines):
    for mine in mines:
        x, y = mine
        grid[x][y] = "[x]"

#Luo tai lisää päättyneen pelin tiedot tekstitiedostoon
def record_statistics(date, end_time, turn_count, win_flag, mine_amount):
    with open("statistics.txt", "a+") as f:
        f.write("DATE: " + date + "\n")
        f.write("ELAPSED TIME: {:.2f} seconds".format(end_time) + "\n")
        f.write("TURN COUNT: " + str(turn_count) + "\n")
        f.write("VICTORY: " + str(win_flag) + "\n")
        f.write("MINES: " + str(mine_amount) + "\n\n")
        f.close()

#Avaa tilaston ja näyttää edellisien pelien tiedot
def show_statistics():
    with open("statistics.txt", "r") as q:
        stats = q.read()
        print(stats)
        q.close()

#Tarkastaa onko pelaaja voittanut pelin vertaamalla jäljellä olevia avaamattomia soluja miinojen sisältävän listan määrään
def winstate(grid, x, y, mines):
    unrevealed = 0
    for row in grid:
        for tile in row:
            if tile == "[ ]":
                unrevealed += 1
    if unrevealed == len(mines):
        return True
    return False

#Funktio jonka sisällä itse peli pelataan, luomalla aluksi miinakentän, miinat, aloittamalla pelin tietojen tallentamisen ja tarkastamalla onko peli hävitty tai voitettu jokaisen uuden solun avaamisen jälkeen
def play():
    flag = True
    turn_count = 0
    win_flag = False
    grid = generate_grid(width, height)
    print_grid(grid)
    mines = plant_mines(mine_amount, grid)
    date = time.strftime("%d/%m/%Y %H:%M:%S")
    start_time = time.time()
    while flag == True:
        x, y = request_coordinates(len(grid), len(grid[0]))
        turn_count += 1
        for mine in mines:
            if mine == (x, y):
                grid[x][y] = "[x]"
                print_grid(grid)
                print("\n******************\n*****YOU LOST*****\n******************\n")
                flag = False
                break
        if flag == True:
            grid = floodfill(grid, x, y, mines)
            print_grid(grid)
            win_flag = winstate(grid, x, y, mines)
            if win_flag == True:
                print("\n******************\n*****YOU WON******\n******************\n")
                flag = False
                break
    end_time = time.time() - start_time
    reveal_mines(grid, mines)
    print_grid(grid)
    record_statistics(date, end_time, turn_count, win_flag, mine_amount)

#Main -funktio, joka toimii valikkona jossa voidaan tarkastaa edellisten pelikertojen tiedot, aloittaa uusi peli tai lopettaa ohjelma
if __name__=="__main__":
    user_input = ""
    max_space = 0
    mine_amount = 0
    unmined_amount = 0
    while user_input != "n":
        user_input = input("y - Play minesweeper \nn - Quit \ns - Show statistics \n")
        if user_input == "y":
            try:
                user_input = input("\nInput the dimensions of the field in the format x,y: ")
                user_input = user_input.split(",")
                width, height = int(user_input[0]), int(user_input[1])
                if width <= 0 or height <= 0:
                    print("\nThe dimensions are too small\n")
                    continue
                max_space = width * height
            except ValueError:
                print("\nThe dimensions must be integers and seperated by a comma\n")
                continue
            except IndexError:
                print("\nThe dimensions must be integers and seperated by a comma\n")
                continue
            try:
                mine_amount = int(input("Input the amount of mines in the field (Available space: {}): ".format(max_space)))
                unmined_amount = max_space - mine_amount
                if mine_amount < 0:
                    print("\nInteger must be positive\n")
                    continue
                elif mine_amount > max_space:
                    print("\nToo many mines to fit the dimensions of the field\n")
                    continue
            except ValueError:
                print("\nAmount of mines must be an integer\n")
                continue

            play()

        elif user_input == "s":
            try:
                show_statistics()
            except FileNotFoundError:
                print("\nFile containing the statistics doesn't exist!\n")
        elif user_input != "n":
            print("\nIncorrect input!\n")
