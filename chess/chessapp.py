__author__ = "Kömen - Enes Bekdemir | 2024"

import pygame

pygame.init()

tnroman_boardletters = pygame.font.SysFont("timesnewroman", size=40)

pieceFont = pygame.font.SysFont("timesnewroman", size=40)

col1 = (238, 238, 213)
col2 = (125, 148, 93)
white_col = (255, 255, 255)
black_col = (0,0,0)
pieceCol1 = (255, 255, 255)
pieceCol2 = (0,0,0)
selected_piece_col = (255,0,0)
selected_sqr1 = (226, 81, 76)
selected_sqr2 = (215, 72, 64)

width, height = 1200, 800

pos_letter = ["A","B","C","D","E","F","G","H"]

# every square and their positions
def def_matrixes(rev=False):
    matrix = {}
    rmatrix= {}
    x_board = 200
    y_board = 100
    lng = 75
    for i in range(1,65):
            matrix[(x_board,y_board)] = f"{8 - i//8 if i%8 !=0 else 8 -i//8 +1}{pos_letter[i%8-1]}".lower()
            rmatrix[f"{8 - i//8 if i%8 !=0 else 8 -i//8 +1}{pos_letter[i%8-1]}".lower()] = (x_board,y_board)
            if i % 8 == 0:
                x_board = 200
                y_board += lng
            else:
                x_board += lng

    if rev: 
        return rmatrix
    return matrix

def piece_pos_match(pos, pieces_1, pieces_2):
    # white pieces
    if pos in [i for ind in pieces_1.values() for i in ind]:
        for key in pieces_1:
            if pos in pieces_1[key]:
                piece_name = key
                return (piece_name, True)
                

    # black pieces
    elif pos in [i for ind in pieces_2.values() for i in ind]:
        for key in pieces_2:
            if pos in pieces_2[key]:
                piece_name = key
                return (piece_name, False)

    return (False, None)

def is_sqr_empty(pos):
    if pos in [i for ind in pieces_1.values() for i in ind]:
        return (False, "p1")
    elif pos in [i for ind in pieces_2.values() for i in ind]:
        return (False, "p2")
    return (True, "")
   

def possible_mov_of_one(wanted, pos, rival, ):
    rules = {
        "Q":[[(0, 1), (0, 2), (0, 3), (0, 4), (0, 5), (0, 6), (0, 7)], [(1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (6, 0), (7, 0)], [(0, -1), (0, -2), (0, -3), (0, -4), (0, -5), (0, -6), (0, -7)],[(-1, 0), (-2, 0), (-3, 0), (-4, 0), (-5, 0), (-6, 0), (-7, 0)], [(1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7)], [(1, -1), (2, -2), (3, -3), (4, -4), (5, -5), (6, -6), (7, -7)], [(-1, -1), (-2, -2), (-3, -3), (-4, -4), (-5, -5), (-6, -6), (-7, -7)], [(-1, 1), (-2, 2), (-3, 3), (-4, 4), (-5, 5), (-6, 6), (-7, 7)]], # queen
        "R":[[(0, 1), (0, 2), (0, 3), (0, 4), (0, 5), (0, 6), (0, 7)], [(1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (6, 0), (7, 0)], [(0, -1), (0, -2), (0, -3), (0, -4), (0, -5), (0, -6), (0, -7)],[(-1, 0), (-2, 0), (-3, 0), (-4, 0), (-5, 0), (-6, 0), (-7, 0)]], # rook
        "K":[[(2, 1)], [(1, 2)], [(-1, 2)], [(-2, 1)], [(-2, -1)], [(-1, -2)], [(1, -2)], [(2, -1)]], # knight
        "B":[[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7)], [(1, -1), (2, -2), (3, -3), (4, -4), (5, -5), (6, -6), (7, -7)], [(-1, -1), (-2, -2), (-3, -3), (-4, -4), (-5, -5), (-6, -6), (-7, -7)], [(-1, 1), (-2, 2), (-3, 3), (-4, 4), (-5, 5), (-6, 6), (-7, 7)]], # bishop
        "+":[[(1, 0)], [(1, 1)], [(0, 1)], [(-1, 1)], [(-1, 0)], [(-1, -1)], [(0, -1)], [(1, -1)]]
    }
    leng = 75
    

    # def pawn movements
    if wanted == "P":
        if rival == "p2":
            lst = []
            if (pos[0], pos[1]-leng) in matrix:
                if is_sqr_empty(matrix[(pos[0], pos[1]-leng)])[0]:
                    lst.append((pos[0], pos[1]-leng))
            if (pos[0], pos[1]-leng*2) in matrix:
                if "2" in matrix[(pos[0],pos[1])] and is_sqr_empty(matrix[(pos[0], pos[1]-leng*2)])[0] and is_sqr_empty(matrix[(pos[0], pos[1]-leng)])[0]:
                    lst.append((pos[0], pos[1]-leng*2))
            if (pos[0]-leng, pos[1]-leng) in matrix:
                if is_sqr_empty(matrix[(pos[0]-leng, pos[1]-leng)])[1] == rival:
                    lst.append((pos[0]-leng, pos[1]-leng))
            if (pos[0]+leng, pos[1]-leng) in matrix:
                if is_sqr_empty(matrix[(pos[0]+leng, pos[1]-leng)])[1] == rival:
                    lst.append((pos[0]+leng, pos[1]-leng))
            movements = lst
        elif rival == "p1":
            lst = []
            if (pos[0], pos[1]+leng) in matrix:
                if is_sqr_empty(matrix[(pos[0], pos[1]+leng)])[0]:
                    lst.append((pos[0], pos[1]+leng))
            if (pos[0], pos[1]+leng*2) in matrix:
                if "7" in matrix[(pos[0],pos[1])] and is_sqr_empty(matrix[(pos[0], pos[1]+leng*2)])[0] and is_sqr_empty(matrix[(pos[0], pos[1]+leng)])[0]:
                    lst.append((pos[0], pos[1]+leng*2))
            if (pos[0]-leng, pos[1]+leng) in matrix:
                if is_sqr_empty(matrix[(pos[0]-leng, pos[1]+leng)])[1] == rival:
                    lst.append((pos[0]-leng, pos[1]+leng))
            if (pos[0]+leng, pos[1]+leng) in matrix:
                if is_sqr_empty(matrix[(pos[0]+leng, pos[1]+leng)])[1] == rival:
                    lst.append((pos[0]+leng, pos[1]+leng))
            movements = lst

        
    else:
        movements = []
        for line in rules[wanted]:
            for ps in line:
                if (pos[0]+leng*ps[0], pos[1]+leng*ps[1]) in matrix:
                    if is_sqr_empty(matrix[(pos[0]+leng*ps[0], pos[1]+leng*ps[1])])[0]:
                        movements.append((pos[0]+leng*ps[0], pos[1]+leng*ps[1]))
                    elif is_sqr_empty(matrix[(pos[0]+leng*ps[0], pos[1]+leng*ps[1])])[1] == rival:
                        movements.append((pos[0]+leng*ps[0], pos[1]+leng*ps[1]))
                        break
                    else:
                        break

    return movements


def possible_sqr(piece_name, pos, tr, res_type=True):

    rival = "p2" if tr%2 == 0 else "p1"

    # determinated piece's movements
    if res_type:
        return possible_mov_of_one(piece_name, pos, rival)
    
    # all pieces' movements
    else: 
        all_mov = []
        
        if rival == "p2":
            for name in pieces_2:
                for pie in pieces_2[name]:
                    all_mov += possible_mov_of_one(name, revmatrix[pie], rival)
        elif rival == "p1":
            for name in pieces_1:
                for pie in pieces_1[name]:
                    all_mov += possible_mov_of_one(name, revmatrix[pie], rival)

        return all_mov
    

def move(piece, curr_pos, mov_pos, tr):
    
    if tr %2 == 0:
        pieces_1[piece][pieces_1[piece].index(curr_pos)]=matrix[mov_pos]

    else: 
        pieces_2[piece][pieces_2[piece].index(curr_pos)]=matrix[mov_pos]


def app():
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Chess")

    clock = pygame.time.Clock()
    
    global matrix
    global revmatrix
    matrix = def_matrixes()
    revmatrix = def_matrixes(True)
    global pieces_1
    global pieces_2
    # player 1
    pieces_1 = {
        "+":["1e"], # king
        "Q":["1d"], # queen
        "R":["1a", "1h"], # rook
        "K":["1b", "1g"], # knight
        "B":["1c", "1f"], # bishop
        "P":["2a","2b","2c","2d","2e","2f","2g","2h"] # pawn
    }
    # player 2
    pieces_2 = {
        "+":["8e"], # king
        "Q":["8d"], # queen
        "R":["8a", "8h"], # rook
        "K":["8b", "8g"], # knight
        "B":["8c", "8f"], # bishop
        "P":["7a","7b","7c","7d","7e","7f","7g","7h"] # pawn
    }
    
    
    tour = 0
    procces = True
    selected_piece_pos = None
    selected_piece_n = False
    possible_movements = []
    while procces:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                procces = False

            # mouse click
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x_click, y_click = event.pos

                if 900 > x_click > 200 and 700 > y_click > 100:
                    for sqpos in matrix.keys():
                        if sqpos[0]<x_click<sqpos[0]+75 and sqpos[1]<y_click<sqpos[1]+75:
                            matrix[sqpos] # clicked square
                            if is_sqr_empty(matrix[sqpos])[0] and selected_piece_n:
                                if sqpos in possible_movements:
                                        
                                    move(selected_piece_n, selected_piece_pos, sqpos, tour)
                                    tour += 1
                                    possible_movements = []
                                    selected_piece_n = False
                                    selected_piece_pos = None
                                else: 
                                    selected_piece_n = False
                                    selected_piece_pos = None
                                    break
                            elif selected_piece_n:
                                if is_sqr_empty(matrix[sqpos])[1] == "p2" and player ==  (tour%2==0) and sqpos in possible_movements:
                                    pieces_2[piece_pos_match(matrix[sqpos], pieces_1, pieces_2)[0]].remove(matrix[sqpos])
                                    move(selected_piece_n, selected_piece_pos, sqpos, tour)
                                    tour += 1
                                    possible_movements = []
                                    selected_piece_n = False
                                    selected_piece_pos = None
                                elif is_sqr_empty(matrix[sqpos])[1] == "p1" and player ==  (tour%2==0) and sqpos in possible_movements:
                                    pieces_1[piece_pos_match(matrix[sqpos], pieces_1, pieces_2)[0]].remove(matrix[sqpos])
                                    move(selected_piece_n, selected_piece_pos, sqpos, tour)
                                    tour += 1
                                    possible_movements = []
                                    selected_piece_n = False
                                    selected_piece_pos = None
                                else:

                                    selected_piece_n, player = piece_pos_match(matrix[sqpos], pieces_1, pieces_2)
                                    
                                    if selected_piece_n and player == (tour%2 == 0):
                                        selected_piece_pos = matrix[sqpos]
                                        possible_movements = possible_sqr(selected_piece_n, revmatrix[selected_piece_pos], tour)
                                        break

                            else:

                                selected_piece_n, player = piece_pos_match(matrix[sqpos], pieces_1, pieces_2)
                                if selected_piece_n and player == (tour%2 == 0):
                                    selected_piece_pos = matrix[sqpos]
                                    possible_movements = possible_sqr(selected_piece_n, revmatrix[selected_piece_pos], tour)
                                    break
                                else:
                                    selected_piece_n = False
                                    selected_piece_pos= None
                                    possible_movements = []

        screen.fill(white_col)
        
        
        # # # board
        color = col1
        sel_col = selected_sqr1
        x_board = 200
        y_board = 100
        lng = 75 # side length of every square
        pygame.draw.rect(screen, black_col, (x_board-5,y_board-5,lng*8+10,lng*8+10)) # side-line
        for i in range(1,65):
            # squares
            if selected_piece_n and (x_board,y_board) in possible_movements and (piece_pos_match(matrix[(x_board,y_board)], pieces_1, pieces_2)[1] == None or piece_pos_match(matrix[(x_board,y_board)], pieces_1, pieces_2)[1] != (tour%2 == 0)):
                pygame.draw.rect(screen, sel_col, (x_board,y_board,lng,lng))
            else: pygame.draw.rect(screen, color, (x_board,y_board,lng,lng))

            # pieces
            piece_n, white = piece_pos_match(matrix[(x_board,y_board)], pieces_1, pieces_2)
            if piece_n:
                if selected_piece_pos == matrix[(x_board,y_board)] and selected_piece_n:
                    piece_color = selected_piece_col
                elif white:
                    piece_color = pieceCol1
                else:
                    piece_color = pieceCol2
                render_piece = pieceFont.render(f"{str(piece_n)}", False, piece_color)
                screen.blit(render_piece,(x_board+25,y_board+15))



            # new x and y
            if i % 8 == 0:
                x_board = 200
                y_board += lng
            else:
                x_board += lng
                color = col2 if color == col1 else col1
                sel_col = selected_sqr2 if sel_col == selected_sqr1 else selected_sqr1


        # letters and numbers
        render_char = tnroman_boardletters.render(f"{'WHITE' if tour%2==0 else 'BLACK'}", False, black_col) # who is the player

        screen.blit(render_char,(200,25))
        x_char = 200 - 40
        y_char = 100 + 15
        for i in range(8,0, -1):
            render_char = tnroman_boardletters.render(f"{i}", False, black_col)
            screen.blit(render_char,(x_char,y_char))
            y_char += 75
        x_char = 200 + 25
        y_char = 700 + 10
        for i in pos_letter:
            render_char = tnroman_boardletters.render(f"{i}", False, black_col)
            screen.blit(render_char,(x_char,y_char))
            x_char += 75
        
        

        # update
        pygame.display.flip()
        clock.tick(60)  # limits FPS to 60





if __name__ == "__main__":
    app()
    pygame.quit()
