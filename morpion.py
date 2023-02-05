import pickle
from copy import deepcopy
from random import choice

import pygame


def verification_of_victory():
    """
    Verify all of the victory possibilities.
    If run is False, the game stop.
    If winner is 1, the winner is the player 1. Same for 2.
    If winner is None, all the squares are full and nobody win.
    """
    run = True
    winner = None
    full = True
    for i in range(3):
        if board[i][i] != 0 and board[i][0] == board[i][1] and board[i][0] == board[i][2]: # vertical
            run = False
            winner = board[i][i]
        if board[i][i] != 0 and board[0][i] == board[1][i] and board[0][i] == board[2][i]: # horizontal
            run = False
            winner = board[i][i]
        if 0 in board[i]: # check if a square is empty
            full = False
    if board[0][0] != 0 and board[0][0] == board[1][1] and board[0][0] == board[2][2]: # diagonal up-left -> down-right
        run = False
        winner = board[0][0]
    if board[2][0] != 0 and board[2][0] == board[1][1] and board[2][0] == board[0][2]: # diagonal down-left -> up-right
        run = False
        winner = board[2][0]
    if full: # if all squares are full, stop the game
        run = False
    return run, winner


def circle(x, y):
    """
    Draw a circle (form of player)
    """
    x = x*absciss+absciss/2
    y = y*ordonned+ordonned/2
    pygame.draw.circle(screen, (0, 0, 0), (x, y), 100, 5)


def cross(x, y):
    """
    Draw a cross (form of player)
    """
    x = x*absciss
    y = y*ordonned
    pygame.draw.line(screen, (0, 0, 0), (x, y), (x+absciss, y+ordonned), 5)
    pygame.draw.line(screen, (0, 0, 0), (x, y+ordonned), (x+absciss, y), 5)


def placement(position, player):
    """
    Place the good player form in the good place
    """
    x, y = position
    if player:
        board[y][x] = 1
        if display:
            circle(x, y)
    else:
        board[y][x] = 2
        if display:
            cross(x, y)

def lines():
    """
    Draw the lines of the morpion game (tic-tac-toe)
    """
    pygame.draw.line(screen, (0, 0, 0), (0, ordonned), (absciss*3, ordonned), 1)
    pygame.draw.line(screen, (0, 0, 0), (0, ordonned*2),
                     (absciss*3, ordonned*2), 1)
    pygame.draw.line(screen, (0, 0, 0), (absciss, 0), (absciss, ordonned*3), 1)
    pygame.draw.line(screen, (0, 0, 0), (absciss*2, 0),
                     (absciss*2, ordonned*3), 1)

def load_data(number):
    with open("data_"+str(number)+".bin", "rb") as d:
        data = pickle.load(d)
        return data

def save_data(number, data):
    with open("data_"+str(number)+".bin", "wb") as d:
        pickle.dump(data, d)

def ai(data):
    """
    The main function of the AI who search or add values in the dictionnary "data" where
    is stocked all the results of the precedents games
    """
    
    if board in data['boards']:
        index_board = data["boards"].index(board)
        importance = data["importance"][index_board]
    else:
        index_board = len(data["boards"])
        data["boards"].append(deepcopy(board))
        importance = new_importance
        data["importance"].append(importance)


    coords = None
    max = None
    # check the nine squares in the importance list corresponding to the game who is played
    for i in range(len(importance)):
        for j in range(len(importance[i])):
            if board[i][j]==0 and (max is None or importance[i][j]>max):
                max = importance[i][j]
                coords = (j, i)
    return coords, index_board, importance

def change_values():
    if not winner: # if AI won add 10 points of importance on the square where the AI played
        for index in range(len(indexs)):
            data["importance"][indexs[index]][coords_ai[index][1]][coords_ai[index][0]] += 8-2*(len(indexs)-index)
    else: # else remove 10 points of importance on the square where the AI played
        for index in range(len(indexs)):
            data["importance"][indexs[index]][coords_ai[index][1]][coords_ai[index][0]] -= 8+2*(len(indexs)-index)

def random_square():
    squares = []
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] == 0:
                squares.append((j,i))
    return choice(squares)


absciss = 200
ordonned = 200

self_ia = False

auto = False
print("""
Players :
0 : AI VS AI
1 : AI VS HERSELF
2 : AI VS PLAYER
else : PLAYER VS AI""")
match = input("player ? ")
if match == "0":
    auto = True
elif match == "1":
    self_ia = True

try:
    if auto:
        data_2 = load_data(2)
    data = load_data(1)
except EOFError:
    print("Save not valid")
    from reset import *
    print("Save reset")
    if auto:
        data_2 = load_data(2)
    data = load_data(1)

display = True
if auto or self_ia:
    display = input("0 : display\nelse : don't display\ndisplay ?")=="0"

if display:
    screen = pygame.display.set_mode((absciss*3, ordonned*3))

end = False
i=0
while not end:
    if display:
        screen.fill((255, 255, 255))
        lines()
    new_importance = ([10,10,10],[10,10,10],[10,10,10])
    board = ([0, 0, 0], [0, 0, 0], [0, 0, 0])
    coords_ai = []
    indexs = []
    if auto:
        coords_ai_2 = []
        indexs_2 = []
    run = True
    winner = None
    player = (True if match in ["0","1","2"] else False) # True : player, False : AI
    if display:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                end = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    end = True
    i+=1
    while run:
        if not self_ia and player:
            if auto:
                coords, index_board, importance = ai(data_2)
                coords_ai_2.append(coords)
                indexs_2.append(index_board)
                placement(coords, player)
                player = not player
                run, winner = verification_of_victory()
            else:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        run = False
                        end = True
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if pygame.mouse.get_pressed() == (1, 0, 0):
                            pos = pygame.mouse.get_pos()
                            x, y = pos
                            x2 = x//absciss
                            y2 = y//ordonned
                            if board[y2][x2] == 0:
                                placement((x2,y2), player)
                                player = not player
                                run, winner = verification_of_victory()
        else:
            coords, index_board, importance = ai(data)
            coords_ai.append(coords)
            indexs.append(index_board)
            placement(coords, player)
            player = not player
            run, winner = verification_of_victory()
        if display:
            pygame.display.flip()
    

    change_values() # change the tab
    if auto:
        save_data(2,data_2)
    else:
        save_data(1,data)
    print("number of played games :",i)
if display:
    pygame.quit()
