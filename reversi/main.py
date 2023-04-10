import numpy as np
import pygame
import sys
import math
import random

#CONSTANTS
#COLORS
BLACK = (0,0,0)
WHITE = (255,255,255)
LIGHT_GREEN = (122, 255, 122)
RED = (255, 0, 0)
GREEN = (0, 122,0)
GREY = (122,122,122)
LIGHT_GREY = (166,166,166)


#POSITIONS
CORNERS = [[0,0],[0,7],[7,0],[7,7]]

BUFFERS = [[1,0],[1,1],[0,1],
           [6,0],[6,1],[7,1],
           [1,7],[1,6],[0,6],
           [7,6],[6,6],[6,7]]

EDGES   = [[0,2],[0,3],[0,4],[0,5],
           [7,2],[7,3],[7,4],[7,5],
           [2,0],[3,0],[4,0],[5,0],
           [2,7],[3,7],[4,7],[5,7],]

game = True # the game will run while it is True

col = 0 # X axis
row = 0 # Y axis

#SIZE OF GAME'S FIELD
FIELD_SIZE = 8

#Creates game's board
def create_field():
    field = np.zeros((FIELD_SIZE, FIELD_SIZE))
    return field

#transfer click coordinates into field's square positions if not clicked on menu
def turn():
    global col, row
    if event.pos[0] > 800 and event.pos[1] < 100:
        restart(field)
    if event.pos[0] < 800:
        col = int(math.floor((event.pos[0] / SQUARE_SIZE)))
        row = int(math.floor((event.pos[1] / SQUARE_SIZE)))

#before the game starts let you choose your turn (1st or 2nd)
def pick_turn(field):
    global step
    global game_started
    x = int(math.floor((event.pos[0])))
    y = int(math.floor((event.pos[1])))
    if 810 < x < 1090 and y > 580 and y < 890:
        if y < 670:
            step = 1
            game_start_setup(field, step)
            game_started = True
        else:
            step = 2
            game_start_setup(field, step)
            game_started = True


# set up table on game start and updates menu on right
def game_start_setup(field, step):
    field[3][3] = 1
    field[4][4] = 1
    field[3][4] = 2
    field[4][3] = 2

    pygame.draw.circle(SCREEN, WHITE, (875, 300), RADIUS)
    pygame.draw.circle(SCREEN, BLACK, (875, 400), RADIUS)
    pygame.draw.rect(SCREEN, GREY, (800, 560, 300, 300))

    find_number(field, step)
    side_menu(field, step)
    screen_from_field(field)

#check if point placed in avaible and place and if it is puts a point in there
def place_point(field, playerNumber):
    if field[row][col] == 3:
        field[row][col] = playerNumber
        return True
    else:
        return False



#searching for all numbers of player
def find_number(field, playerNumber):
    for r in range(FIELD_SIZE):
        for c in range(FIELD_SIZE):
            if field[r][c] == playerNumber:
                surround_with_threes(field, playerNumber, r, c)

#check for avaiable positions where a new points can be placed (marks it as 3)
def surround_with_threes(field, playerNumber, row_temp, col_temp):
    # checks on right
    place = False
    for c in range(col_temp+1, FIELD_SIZE):
        if field[row_temp][c] == 0 or field[row_temp][c] == playerNumber or field[row_temp][c] == 3:
            break
        else:
            place = True
    if place:
        for c in range(col_temp+1, FIELD_SIZE):
            if field[row_temp][c] == playerNumber or field[row_temp][c] == 3:
                break
            if field[row_temp][c] == 0:
                field[row_temp][c] = 3
                break

    # checks on left
    place = False
    for c in range(col_temp - 1, -1, -1):
        if field[row_temp][c] == 0 or field[row_temp][c] == playerNumber or field[row_temp][c] == 3:
            break
        else:
            place = True
    if place:
        for c in range(col_temp - 1, -1, -1):
            if field[row_temp][c] == playerNumber or field[row_temp][c] == 3:
                break
            if field[row_temp][c] == 0:
                field[row_temp][c] = 3
                break

    # checks on down
    place = False
    for r in range(row_temp + 1, FIELD_SIZE):
        if field[r][col_temp] == 0 or field[r][col_temp] == playerNumber or field[r][col_temp] == 3:
            break
        else:
            place = True
    if place:
        for r in range(row_temp + 1, FIELD_SIZE):
            if field[r][col_temp] == playerNumber or field[r][col_temp] == 3:
                break
            if field[r][col_temp] == 0:
                field[r][col_temp] = 3
                break

    # checks on top
    place = False
    for r in range(row_temp - 1, -1, -1):
        if field[r][col_temp] == 0 or field[r][col_temp] == playerNumber or field[r][col_temp] == 3:
            break
        else:
            place = True
    if place:
        for r in range(row_temp - 1, -1, -1):
            if field[r][col_temp] == playerNumber or field[r][col_temp] == 3:
                break
            if field[r][col_temp] == 0:
                field[r][col_temp] = 3
                break

    # diagonal top right
    place = False
    i, j = row_temp-1, col_temp+1
    while i >= 0 and j < FIELD_SIZE:
        if field[i][j] == 0 or field[i][j] == playerNumber or field[i][j] == 3:
            break
        else:
            place = True
        i -= 1
        j += 1
    if place:
        i, j = row_temp - 1, col_temp + 1
        while i >= 0 and j < FIELD_SIZE:
            if field[i][j] == 0:
                field[i][j] = 3
                break
            elif field[i][j] == 3 or field[i][j] == playerNumber:
                break
            i -= 1
            j += 1

    # diagonal top left
    place = False
    i, j = row_temp - 1, col_temp - 1
    while i >= 0 and j >= 0:
        if field[i][j] == 0 or field[i][j] == playerNumber or field[i][j] == 3:
            break
        else:
            place = True
        i -= 1
        j -= 1
    if place:
        i, j = row_temp - 1, col_temp - 1
        while i >= 0 and j >= 0:
            if field[i][j] == 0:
                field[i][j] = 3
                break
            elif field[i][j] == 3 or field[i][j] == playerNumber:
                break
            i -= 1
            j -= 1

    # diagonal bot right
    place = False
    i, j = row_temp + 1, col_temp + 1
    while i < FIELD_SIZE and j < FIELD_SIZE:
        if field[i][j] == 0 or field[i][j] == playerNumber or field[i][j] == 3:
            break
        else:
            place = True
        i += 1
        j += 1
    if place:
        i, j = row_temp + 1, col_temp + 1
        while i < FIELD_SIZE and j < FIELD_SIZE:
            if field[i][j] == 0:
                field[i][j] = 3
                break
            elif field[i][j] == 3 or field[i][j] == playerNumber:
                break
            i += 1
            j += 1

    # diagonal bot left
    place = False
    i, j = row_temp + 1, col_temp - 1
    while i < FIELD_SIZE and j >= 0:
        if field[i][j] == 0 or field[i][j] == playerNumber or field[i][j] == 3:
            break
        else:
            place = True
        i += 1
        j -= 1
    if place:
        i, j = row_temp + 1, col_temp - 1
        while i < FIELD_SIZE and j >= 0:
            if field[i][j] == 0:
                field[i][j] = 3
                break
            elif field[i][j] == 3 or field[i][j] == playerNumber:
                break
            i += 1
            j -= 1

# removes all of the threes on the field
def get_rid_of_three(field):
    for i in range(FIELD_SIZE):
        for j in range(FIELD_SIZE):
            pass
            if field[i][j] == 3:
                field[i][j] = 0

# "captures" enemy points after a turn
def flip_points(field, playerNumber):
    # check horizontal on left:
    flip = False
    until_point = 0
    for c in range(col-1, -1, -1):
        if field[row][c] == playerNumber:
            flip = True
            until_point = c - 1
            break
        if field[row][c] == 0 or field[row][c] == 3:
            break
    if flip:
        for c in range(col-1, until_point, -1):
            field[row][c] = playerNumber

    # check horizontal on right:
    flip = False
    until_point = 0
    for c in range(col+1, FIELD_SIZE):
        if field[row][c] == playerNumber:
            flip = True
            until_point = c + 1
            break
        if field[row][c] == 0 or field[row][c] == 3:
            break
    if flip:
        for c in range(col+1, until_point):
            field[row][c] = playerNumber

    #check vertical from down to top
    flip = False
    until_point = 0
    for r in range(row - 1, -1, -1):
        if field[r][col] == playerNumber:
            flip = True
            until_point = r - 1
            break
        if field[r][col] == 0 or field[r][col] == 3:
            break
    if flip:
        for r in range(row - 1, until_point, -1):
            field[r][col] = playerNumber

    # check horizontal on right:
    flip = False
    until_point = 0
    for r in range(row+1, FIELD_SIZE):
        if field[r][col] == playerNumber:
            flip = True
            until_point = r + 1
            break
        if field[r][col] == 0 or field[r][col] == 3:
            break
    if flip:
        for r in range(row+1, until_point):
            field[r][col] = playerNumber

    # diagonal: top right
    flip = False
    until_point_i = 0
    until_point_j = 0
    i, j = row-1, col+1
    while i >= 0 and j < FIELD_SIZE - 1:
        i -= 1
        j += 1
        if field[i][j] == 0 or field[i][j] == 3:
            break
        if field[i][j] == playerNumber:
            flip = True
            until_point_i = i
            until_point_j = j
            break
    if flip:
        i, j = row - 1, col + 1
        while i >= until_point_i and j < until_point_j:
            if field[i][j] == 0 or field[i][j] == 3:
                break
            field[i][j] = playerNumber
            i -= 1
            j += 1

    #diagonal top left
    flip = False
    until_point_i = 0
    until_point_j = 0
    i, j = row - 1, col - 1
    while i >= 0 and j >= 0:
        i -= 1
        j -= 1
        if field[i][j] == 0 or field[i][j] == 3:
            break
        if field[i][j] == playerNumber:
            flip = True
            until_point_i = i
            until_point_j = j
            break
    if flip:
        i, j = row - 1, col - 1
        while i >= until_point_i and j >= until_point_j:
            if field[i][j] == 0 or field[i][j] == 3:
                break
            field[i][j] = playerNumber
            i -= 1
            j -= 1

    # diagonal: bot right
    flip = False
    until_point_i = 0
    until_point_j = 0
    i, j = row + 1, col + 1
    while i < FIELD_SIZE-1 and j < FIELD_SIZE-1:
        i += 1
        j += 1
        if field[i][j] == 0 or field[i][j] == 3:
            break
        if field[i][j] == playerNumber:
            flip = True
            until_point_i = i
            until_point_j = j
            break
    if flip:
        i, j = row + 1, col + 1
        while i < until_point_i and j < until_point_j:
            if field[i][j] == 0 or field[i][j] == 3:
                break
            field[i][j] = playerNumber
            i += 1
            j += 1

    # diagonal: bot left
    flip = False
    until_point_i = 0
    until_point_j = 0
    i, j = row + 1, col - 1
    while i < FIELD_SIZE-1 and j >= 0:
        i += 1
        j -= 1
        if field[i][j] == 0 or field[i][j] == 3:
            break
        if field[i][j] == playerNumber:
            flip = True
            until_point_i = i
            until_point_j = j
            break
    if flip:
        i, j = row + 1, col - 1
        while i < until_point_i and j > until_point_j:
            if field[i][j] == 0 or field[i][j] == 3:
                break
            field[i][j] = playerNumber
            i += 1
            j -= 1

# updates the screen with graphics based on field's matrix
# Where:
# 0 - free space
# 1 - white points
# 2 - black points
# 3 - place where a point can be placed
def screen_from_field(field):
    for c in range(FIELD_SIZE):
        for r in range(FIELD_SIZE):
            pygame.draw.rect(SCREEN, GREEN, (c * SQUARE_SIZE, r * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
            pygame.draw.rect(SCREEN, BLACK, (c * SQUARE_SIZE, r * SQUARE_SIZE , SQUARE_SIZE, SQUARE_SIZE), 1)

    for c in range(FIELD_SIZE):
        for r in range(FIELD_SIZE):
            if field[r][c] == 1:
                pygame.draw.circle(SCREEN, WHITE, (int(c * SQUARE_SIZE + SQUARE_SIZE / 2), int(r * SQUARE_SIZE + SQUARE_SIZE / 2)), RADIUS)
            elif field[r][c] == 2:
                pygame.draw.circle(SCREEN, BLACK, (int(c * SQUARE_SIZE + SQUARE_SIZE / 2), int(r * SQUARE_SIZE + SQUARE_SIZE / 2)), RADIUS)
            elif field[r][c] == 3:
                pygame.draw.rect(SCREEN, LIGHT_GREEN, (c * SQUARE_SIZE, r * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
                pygame.draw.rect(SCREEN, BLACK, (c * SQUARE_SIZE, r * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE), 1)

    pygame.display.update()

# updates side menu on right based on turn
def side_menu(field, playerNumber):
    pygame.draw.rect(SCREEN, GREY, (850, 75, 300, 300))
    if playerNumber == 1:
        draw_text("Your Turn", text_font, BLACK, 850, 75)
        pygame.draw.circle(SCREEN, WHITE, (950, 170), RADIUS*0.5)
    else:
        draw_text("AI's Turn", text_font, BLACK, 860, 75)
        pygame.draw.circle(SCREEN, BLACK, (950, 170), RADIUS * 0.5)

    pygame.draw.rect(SCREEN, GREY, (925, 260, 300, 300))
    draw_text((": " + str(count(field, 1))) , text_font, BLACK, 925, 260)
    draw_text((": " + str(count(field, 2))), text_font, BLACK, 925, 360)
    pygame.draw.circle(SCREEN, WHITE, (875, 300), RADIUS)
    pygame.draw.circle(SCREEN, BLACK, (875, 400), RADIUS)

    pygame.display.update()


def count(field, playerNumber):
    count = 0
    for r in range(FIELD_SIZE):
        for c in range(FIELD_SIZE):
            if field[r][c] == playerNumber:
                count += 1
    return count

#check if game is over
def check_win(field):
    game_finished = True
    for r in range(FIELD_SIZE):
        for c in range(FIELD_SIZE):
            if field[r][c] == 3:
                game_finished = False
                break

    if game_finished:
        if count(field, 1) > count(field, 2):
            draw_text("Wins: ", text_font, BLACK, 825, 600)
            pygame.draw.circle(SCREEN, WHITE, (1000, 635), RADIUS * 0.75)
        elif count(field, 1) == count(field, 2):
            draw_text("draw", text_font, BLACK, 825, 600)
        else:
            draw_text("wins:", text_font, BLACK, 825, 600)
            pygame.draw.circle(SCREEN, BLACK, (1000, 635), RADIUS * 0.75)
        return True
    return False

#set up to easily add text to a game
def draw_text(text, font, text_color, x, y):
    img = font.render(text, True, text_color)
    SCREEN.blit(img, (x, y))

#get all possible poistions on field (all 3's)
def get_possible_positions(field):
    possible_positions = []
    for r in range(FIELD_SIZE):
        for c in range(FIELD_SIZE):
            position = [0,0]
            if field[r][c] == 3:
                position[0] = r
                position[1] = c
                possible_positions.append(position)
    return possible_positions

#check if a point is a Frontier point (have at least 1 free space square around them)
def check_if_frontier(field, r, c):

    # check if there is a 0 in horizontal and vertical lines
    if r > 0 and field[r - 1][c] == 0:
        return True
    if r < FIELD_SIZE - 1 and field[r + 1][c] == 0:
        return True
    if c > 0 and field[r][c - 1] == 0:
        return True
    if c < FIELD_SIZE - 1 and field[r][c + 1] == 0:
        return True

    # check if there is a 0 in the diagonals
    if r > 0 and c > 0 and field[r - 1][c - 1] == 0:
        return True
    if r > 0 and c < FIELD_SIZE - 1 and field[r - 1][c + 1] == 0:
        return True
    if r < FIELD_SIZE - 1 and c > 0 and field[r + 1][c - 1] == 0:
        return True
    if r < FIELD_SIZE - 1 and c < FIELD_SIZE - 1 and field[r + 1][c + 1] == 0:
        return True

    return False

#count frontiers and Interiers (points that have no free spaces around the,)
def count_frontiers_and_Interiers(field, playerNumber):
    frontiers = 0
    interiers = 0

    for r in range(FIELD_SIZE):
        for c in range(FIELD_SIZE):
            if field[r][c] == playerNumber:
                if check_if_frontier(field, r, c):
                    frontiers += 1
                else:
                    interiers += 1

    return frontiers, interiers

#counts how many points on different type of position
def count_position_for_scroing(field, playerNumber):
    corners = 0
    buffers = 0
    edges = 0
    for r in range(FIELD_SIZE):
        for c in range(FIELD_SIZE):
            if field[r][c] == playerNumber:
                position = [r,c]

                if position in CORNERS:
                    corners += 1
                if position in BUFFERS:
                    buffers += 1
                if position in EDGES:
                    edges += 1

    return corners, buffers, edges

#same as above but counts what is the best position enemy can place point on its next step
def count_enemy_position_for_scoring(field, playerNumber):
    get_rid_of_three(field)
    find_number(field, playerNumber)
    corners = 0
    buffers = 0
    edges = 0
    for r in range(FIELD_SIZE):
        for c in range(FIELD_SIZE):
            if field[r][c] == 3:
                position = [r, c]

                if position in CORNERS:
                    corners += 1
                if position in BUFFERS:
                    buffers += 1
                if position in EDGES:
                    edges += 1

                if corners >= 1:
                    buffers = 0
                    edges = 0
                elif buffers >= 1:
                    edges = 0
    get_rid_of_three(field)
    return corners, buffers, edges

#counts score based on field
def score_calculation(field, playerNumber):
    FRONTIER_SCORE = 1
    INTERIER_SCORE = 2

    ENENMY_FRONTIER_SCORE = -1
    ENENMY_INTERIER_SCORE = -2

    CORNERS_SCORE = 20
    BUFFERS_SCORE = 12
    EDGES_SCORE   = 8


    if playerNumber == 1:
        enemyNumber = 2
    else:
        enemyNumber = 1

    frontiers, interiers = count_frontiers_and_Interiers(field, playerNumber)
    corners, buffers, edges = count_position_for_scroing(field, playerNumber)

    enemy_frontiers, enemy_interiers = count_frontiers_and_Interiers(field, enemyNumber)
    enemy_corners, enemy_buffers, enemy_edges = count_enemy_position_for_scoring(field, enemyNumber)


    FI_score = frontiers * FRONTIER_SCORE + interiers * INTERIER_SCORE
    ENEMY_FI_score = enemy_frontiers * ENENMY_FRONTIER_SCORE + enemy_interiers * ENENMY_INTERIER_SCORE
    POS_score = corners * CORNERS_SCORE + buffers * BUFFERS_SCORE + edges * EDGES_SCORE
    ENEMY_POS_score = -1 * (enemy_corners * CORNERS_SCORE + enemy_buffers * BUFFERS_SCORE + enemy_edges * EDGES_SCORE)

    score = FI_score + POS_score + ENEMY_FI_score + ENEMY_POS_score


    return score

#minimax algorithm
def minimax(field, depth, maximizing):
    global row, col
    if depth == 0:
        print("Score: " + str(score_calculation(field, 2)))
        return None, None, score_calculation(field, 2)

    if maximizing:
        find_number(field, 2)
        max_eval = -math.inf
        possible_positions = get_possible_positions(field)

        if len(possible_positions) == 0:
            return None, None, score_calculation(field, 2)

        best_row = random.choice(possible_positions)[0]
        best_col = random.choice(possible_positions)[1]

        for position in possible_positions:
            print("Max: ")
            test_field = field.copy()
            row = position[0]
            col = position[1]

            temp_col = col
            temp_row = row

            place_point(test_field, 2)
            get_rid_of_three(test_field)
            flip_points(test_field, 2)
            eval = minimax(test_field, depth - 1, False)[2]
            print("Is " + str(eval) + " (child) > then " + str(max_eval) + "?")
            if eval > max_eval:
                print("Yes! new max value is: " + str(eval))
                best_col = temp_col
                best_row = temp_row
                max_eval = eval
        col = best_col
        row = best_row
        return best_col, best_row, max_eval
    else:
        find_number(field, 1)
        min_eval = math.inf
        possible_positions = get_possible_positions(field)

        if len(possible_positions) == 0:
            return None, None, score_calculation(field, 2)

        best_row = random.choice(possible_positions)[0]
        best_col = random.choice(possible_positions)[1]

        for position in possible_positions:
            print("Min: ")
            test_field = field.copy()
            row = position[0]
            col = position[1]

            temp_col = col
            temp_row = row

            place_point(test_field, 1)
            get_rid_of_three(test_field)
            flip_points(test_field, 1)
            eval = minimax(test_field, depth - 1, True)[2]
            print("Is " + str(eval) + " (child) < then " + str(min_eval) + "?")
            if eval < min_eval:
                print("Yes! new min value is: " + str(eval))
                best_col = temp_col
                best_row = temp_row
                min_eval = eval
        col = best_col
        row = best_row
        return best_col, best_row, min_eval

#returns game to turn choosing section
def restart(field):
    global game_started
    for c in range(FIELD_SIZE):
        for r in range(FIELD_SIZE):
            field[r][c] = 0
    screen_from_field(field)
    game_started = False
    pygame.draw.rect(SCREEN, GREY, (800, 0, SQUARE_SIZE*3, SQUARE_SIZE*8))
    pygame.draw.rect(SCREEN, LIGHT_GREY, (810, 10, 280, 50))
    pygame.draw.rect(SCREEN, BLACK, (810, 10, 280, 50), 1)
    draw_text("Restart", text_font, BLACK, 880, 5)
    pygame.draw.rect(SCREEN, LIGHT_GREY, (810, 580, 280, SQUARE_SIZE))
    pygame.draw.rect(SCREEN, BLACK, (810, 580, 280, SQUARE_SIZE), 1)
    draw_text("Start 1st", text_font, BLACK, 825, 600)
    pygame.draw.rect(SCREEN, LIGHT_GREY, (810, 690, 280, SQUARE_SIZE))
    pygame.draw.rect(SCREEN, BLACK, (810, 690, 280, SQUARE_SIZE), 1)
    draw_text("Start 2nd", text_font, BLACK, 825, 710)
    pygame.display.update()

field = create_field()

pygame.init()
SQUARE_SIZE = 100
RADIUS = int(SQUARE_SIZE / 2 - 5)

SCREEN_SIZE = (SQUARE_SIZE * FIELD_SIZE + 300, SQUARE_SIZE * FIELD_SIZE)

SCREEN = pygame.display.set_mode(SCREEN_SIZE)
text_font = pygame.font.SysFont("Arial", 50)

SCREEN.fill(GREY)
step = 1
screen_from_field(field)

#side menu set up
pygame.draw.rect(SCREEN, LIGHT_GREY, (810,  10, 280, 50))
pygame.draw.rect(SCREEN, BLACK, (810,  10, 280, 50),1)
draw_text("Restart", text_font, BLACK, 880, 5)
pygame.draw.rect(SCREEN, LIGHT_GREY, (810, 580, 280, SQUARE_SIZE))
pygame.draw.rect(SCREEN, BLACK, (810, 580, 280, SQUARE_SIZE),1)
draw_text("Start 1st", text_font, BLACK, 825, 600)
pygame.draw.rect(SCREEN, LIGHT_GREY, (810, 690, 280, SQUARE_SIZE))
pygame.draw.rect(SCREEN, BLACK, (810, 690, 280, SQUARE_SIZE),1)
draw_text("Start 2nd", text_font, BLACK, 825, 710)
pygame.display.update()

game_started = False
while game:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if game_started:
                if step == 1:
                    find_number(field, 1)
                    screen_from_field(field)
                    turn()
                    if place_point(field, 1):
                        get_rid_of_three(field)
                        flip_points(field, 1)
                        find_number(field, 2)
                        check_win(field)
                        screen_from_field(field)
                        side_menu(field, 2)
                        step = 2
            else:
                pick_turn(field)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                restart(field)

    if step == 2:
        find_number(field, 2)
        screen_from_field(field)

        col, row, score = minimax(field, 2, True)
        print("\n")
        if col is not None and row is not None:
            place_point(field, 2)
            get_rid_of_three(field)
            flip_points(field, 2)
            find_number(field, 1)
            pygame.time.wait(600)
            check_win(field)
            side_menu(field, 2)
            screen_from_field(field)
            step = 1
            side_menu(field, 1)
        else:
            step = 1
            side_menu(field, 1)
