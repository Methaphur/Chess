import pygame 
import numpy as np

pygame.init()
width , height = 480 , 480 
screen = pygame.display.set_mode((width,height))
pygame.display.set_caption("Chess")

white_cell = (255, 255, 255)
black_cell = (0, 89, 179)
cell_size = width // 8
select_cell_color = (255 , 0, 0)
valid_spot_color = (79 ,121, 66)
grid_color = (150, 150 ,150)
black = (0, 0, 0)
check_color = (248, 110, 7)


king = 1
queen = 2
bishop= 3
knight = 4
rook = 5
pawn = 6

white = 8
black = 16

class ChessPiece:
    def __init__(self,color,position):
        self.color = color 
        self.position = position

    def move(self,position):
        if position in self.valid_spots():
            new_row , new_col = position        # Target
            old_row, old_col = self.position    # Current 
            game.board.board[old_row][old_col] = 0   
            game.board.board[new_row][new_col] = self
            self.position = new_row,new_col
            return True
        return False

class Pawn(ChessPiece):
    def valid_spots(self):
        valid_moves = []
            
        curr_row , curr_col = self.position

        if self.color == "white":
            direction = -1
            start_row = 6
            promotion_row = 0
        
        else:
            direction = 1
            start_row = 1
            promotion_row = 7
        
        final_row = curr_row + direction 
        rows = cols = len(game.board.board)

        if 0 <= final_row < rows and not game.board.board[final_row][curr_col]:
            valid_moves.append((final_row,curr_col))

            if curr_row == start_row:
                final_row = curr_row + direction*2
                if not game.board.board[final_row][curr_col]:
                    valid_moves.append((final_row,curr_col))

        # Checking if pawn can capture 
        capture_offset = [(direction,-1),(direction,1)]
        for row_offset , col_offset in capture_offset:
            final_row , final_col = curr_row + row_offset , curr_col + col_offset
            if 0 <= final_row < rows and 0 <= final_col < cols:
                dest_piece = game.board.board[final_row][final_col]
                if dest_piece and dest_piece.color != self.color:
                    valid_moves.append((final_row,final_col))
    
        return valid_moves
 
class King(ChessPiece): 
    
    def valid_spots(self):
        valid_moves = []

        curr_row , curr_col = self.position
        rows = cols = len(game.board.board)

            # Define all possible offsets for king's movements
        offsets = [
            (-1, -1),(-1, 0), (-1, 1),
            ( 0, -1),         (0, 1),
            ( 1, -1), (1, 0),  (1, 1)
        ]

        for offset in offsets:
            offset_row , offset_col = offset
            final_row , final_col = curr_row + offset_row , curr_col + offset_col

            if 0 <= final_row < rows and 0 <= final_col < cols:
                dest_piece = game.board.board[final_row][final_col]

                # Checking if square is empty or can be captured (opponent)
                if not dest_piece or dest_piece.color != self.color:
                    valid_moves.append((final_row,final_col))
        
        return valid_moves

class Queen(ChessPiece):
    def valid_spots(self):
        valid_moves = []
    
        curr_row , curr_col = self.position
        rows = cols = len(game.board.board)

        # 8 Moving directions of Queen
        offsets = [
         (-1, 0),    # Up
         (1, 0),     # Down
         (0, -1),    # Left
         (0, 1),     # Right
         (-1, -1),   # Up-Left
         (-1, 1),    # Up-Right
         (1, -1),    # Down-Left
         (1, 1)      # Down-Right
        
        ]

        for offset in offsets:
            offset_row , offset_col = offset
            final_row , final_col = curr_row + offset_row , curr_col + offset_col


            while 0 <= final_row < rows and 0 <= final_col < cols:
                dest_piece = game.board.board[final_row][final_col]

                if not dest_piece:
                    valid_moves.append((final_row,final_col))
                
                # Opponent in square then can be captured and not move further beyond
                elif dest_piece.color != self.color:
                    valid_moves.append((final_row,final_col))
                    break
            
                else:
                    break
                
                final_row += offset_row
                final_col += offset_col

        return valid_moves    
                

class Bishop(ChessPiece):
    def valid_spots(self):
        valid_moves = []
    
        curr_row , curr_col = self.position
        rows = cols = len(game.board.board)

        # Moving directions of Bishop
        offsets = [
         (-1, -1),   # Up-Left
         (-1, 1),    # Up-Right
         (1, -1),    # Down-Left
         (1, 1)      # Down-Right
        ]
        
        for offset in offsets:
            offset_row , offset_col = offset
            final_row , final_col = curr_row + offset_row , curr_col + offset_col


            while 0 <= final_row < rows and 0 <= final_col < cols:
                dest_piece = game.board.board[final_row][final_col]

                if not dest_piece:
                    valid_moves.append((final_row,final_col))
                
                # Opponent in square then can be captured and not move further beyond
                elif dest_piece.color != self.color:
                    valid_moves.append((final_row,final_col))
                    break
            
                else:
                    break
                
                final_row += offset_row
                final_col += offset_col

        return valid_moves

class Knight(ChessPiece):
    def valid_spots(self):
        valid_moves = []

        curr_row , curr_col = self.position
        rows = cols = len(game.board.board)

        # Define all possible offsets for knights movements
        offsets = [
        (-2, -1), (-2, 1),(-1, -2), (-1, 2),
        (1, -2), (1, 2),(2, -1), (2, 1)
        ]

        for offset in offsets:
            offset_row , offset_col = offset
            final_row , final_col = curr_row + offset_row , curr_col + offset_col

            if 0 <= final_row < rows and 0 <= final_col < cols:
                dest_piece = game.board.board[final_row][final_col]

                # Checking if square is empty or can be captured (opponent)
                if not dest_piece or dest_piece.color != self.color:
                    valid_moves.append((final_row,final_col))
        
        return valid_moves

class Rook(ChessPiece):
    def valid_spots(self):
        valid_moves = []
    
        curr_row , curr_col = self.position
        rows = cols = len(game.board.board)

        # 8 Moving directions of Rook
        offsets = [
         (-1, 0),    # Up
         (1, 0),     # Down
         (0, -1),    # Left
         (0, 1),     # Right
        ]
        
        for offset in offsets:
            offset_row , offset_col = offset
            final_row , final_col = curr_row + offset_row , curr_col + offset_col


            while 0 <= final_row < rows and 0 <= final_col < cols:
                dest_piece = game.board.board[final_row][final_col]

                if not dest_piece:
                    valid_moves.append((final_row,final_col))
                
                # Opponent in square then can be captured and not move further beyond
                elif dest_piece.color != self.color:
                    valid_moves.append((final_row,final_col))
                    break
            
                else:
                    break
                
                final_row += offset_row
                final_col += offset_col

        return valid_moves


pieces = {
    (King,'white')  : pygame.image.load("Assets/w_king.jpg"),
    (Queen,'white') : pygame.image.load("Assets/w_queen.jpg"),
    (Bishop,'white'): pygame.image.load("Assets/w_bishop.jpg"),
    (Knight,'white'): pygame.image.load("Assets/w_knight.jpg"),
    (Rook,'white')  : pygame.image.load("Assets/w_rook.jpg"),
    (Pawn,'white')  : pygame.image.load("Assets/w_pawn.jpg"),

    (King,'black')  : pygame.image.load("Assets/b_king.jpg"),
    (Queen,'black') : pygame.image.load("Assets/b_queen.jpg"),
    (Bishop,'black'): pygame.image.load("Assets/b_bishop.jpg"),
    (Knight,'black'): pygame.image.load("Assets/b_knight.jpg"),
    (Rook,'black')  : pygame.image.load("Assets/b_rook.jpg"),
    (Pawn,'black')  : pygame.image.load("Assets/b_pawn.jpg"),
}

piece_fen = {"r":Rook,"n":Knight,"b":Bishop,"q":Queen,"k":King,"p":Pawn 
             }

class Board:
    def __init__(self):
        self.board = [[0]*8 for _ in range(8)]

    def load_board(self,fen):

        fen = fen.split()   # splitting into board state and active color 

        board_state = fen[0]
        game.current_player = "white" if fen[1] == "w" else "black"

        rows = board_state.split("/")
        for row , fen_row in enumerate(rows):
            
            col = 0
            for char in fen_row:
                if char.isdigit():
                    col += int(char)
                else:
                    if char.isupper():
                        self.board[row][col] = piece_fen[char.lower()]('white',(row,col))
                    else:
                        self.board[row][col] = piece_fen[char]('black',(row,col))
                    
                    col += 1


starting_fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w"

class Game:
    def __init__(self,screen):
        self.screen = screen
        self.board = Board()
        self.selected_piece = None
        self.selected_piece_pos = None
        self.current_player = "white" # True = White , False = Black 

    def load_board(self,fen = starting_fen):
        self.board.load_board(fen)

    def display(self):
        running = True
        while running:
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1: # left click  
                        if self.selected_piece:
                            pos = pygame.mouse.get_pos()
                            row = pos[1] // cell_size
                            col = pos[0] // cell_size
                            cell = self.board.board[row][col]

                            if self.selected_piece.move((row,col)):                                
                                self.current_player = "white" if self.current_player != "white" else "black"
                                if self.is_in_check(self.current_player):
                                    self.display_check()
                                # if self.is_checkmate(self.current_player):
                                #     self.display_checkmate()

                            self.selected_piece = None
                            self.selected_piece_pos = None
                        else:
                            self.handle_click(pos=pygame.mouse.get_pos())


                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
            
            # Coloring all the tiles 
            rows , cols  = 8,8
            for row in range(rows):
                for col in range(cols):
                    color = white_cell if (row + col) % 2 == 0 else black_cell
                    pygame.draw.rect(screen,color,(col * cell_size, row * cell_size, cell_size, cell_size))

                    piece = self.board.board[row][col]
                    
                    if self.selected_piece:
                        select_row,select_col = self.selected_piece_pos
                        if self.board.board[select_row][select_col]:
                            selected_cell = self.board.board[self.selected_piece_pos[0]][self.selected_piece_pos[1]]
                            valid_spots = selected_cell.valid_spots()

                            for x,y in valid_spots:
                                pygame.draw.rect(screen,valid_spot_color,(y * cell_size , x * cell_size , cell_size ,cell_size))

                        if self.selected_piece_pos == (row , col):        
                            # Selected cell
                            pygame.draw.rect(screen,select_cell_color,(col * cell_size , row * cell_size , cell_size ,cell_size))
                      

            # Loading all the pieces on top of the tiles (funky fix ofc)
            for row in range(rows):
                for col in range(cols):
                    piece = self.board.board[row][col]

                    if piece:
                        screen.blit(pieces[type(piece),piece.color], (col*cell_size , row * cell_size))


            for x in range(0, width, cell_size):
                pygame.draw.line(screen, grid_color, (x, 0), (x, height))
            for y in range(0, height, cell_size):
                pygame.draw.line(screen, grid_color, (0, y), (width, y))

            pygame.display.flip()

        pygame.quit()

    def load_game(self,fen):
        self.board = Board()
        self.board.load_board()


    def handle_click(self,pos):
        row = pos[1] // cell_size
        col = pos[0] // cell_size
        cell = self.board.board[row][col]
    
        if cell:
            if self.current_player == cell.color:
                self.selected_piece = cell
                self.selected_piece_pos = (row,col)

    def king_pos(self,color):
        rows = cols = 8
        # Finding king pos
        king_pos = None
        for row in range(rows):
            for col in range(cols):
                piece = self.board.board[row][col] 
                if isinstance(piece, King) and piece.color == color:
                    king_pos = (row,col)
                    break
        return king_pos

    def is_in_check(self,color):
        king_pos = self.king_pos(color)
        # Checking threat from opponent pieces 
        rows = cols = 8
        # Possible directional threats
        directions = {
        'rook': [(1, 0), (-1, 0), (0, 1), (0, -1)],
        'bishop': [(1, 1), (1, -1), (-1, 1), (-1, -1)],
        'queen': [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (1, -1), (-1, 1), (-1, -1)]
        
        }

        def check_direction(piece_direction):
            row_dir , col_dir = piece_direction
            row , col = king_pos
            not_check = True
            
            while not_check:

                row += row_dir
                col += col_dir

                if 0 <= row < rows and 0 <= col < cols:
                    piece = self.board.board[row][col]

                    if piece:
                        if isinstance(piece , (Rook, Bishop, Queen)) and piece.color != color:
                            return True
                        else:
                            break

                else:
                    break
            
            return False
    
        # Check condition for Rook , Bishop , Queen
        for piece_type , piece_direction in directions.items():
            for direction in piece_direction:
                if check_direction(direction):
                    return True
            
        # Check condition for Knight 
        knight_offsets = [(-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1)]
        curr_row , curr_col = king_pos
        for row_offset,col_offset in knight_offsets:
            row = curr_row + row_offset
            col = curr_col + col_offset
        
            if 0 <= row < rows and 0 <= col < cols:
                piece = self.board.board[row][col]
                if isinstance(piece, Knight) and piece.color != color:
                    return True
        

        # Checking condition for Pawns

        pawn_offsets = [(-1, -1), (-1, 1)] if color == "white" else [(1, -1), (1, 1)]
        for row_offset , col_offset in pawn_offsets:
            row = curr_row + row_offset
            col = curr_col + col_offset
        
            if 0 <= row < rows and 0 <= col < cols:
                piece = self.board.board[row][col]
                if isinstance(piece, Pawn) and piece.color != color:
                    return True
        
        king_offsets =  [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (1, -1), (-1, 1), (-1, -1)]
        for row_offset , col_offset in king_offsets:
            row = curr_row + row_offset
            col = curr_col + col_offset
        
            if 0 <= row < rows and 0 <= col < cols:
                piece = self.board.board[row][col]
                if isinstance(piece, King) and piece.color != color:
                    return True
    
        return False
    
    def display_check(self):
        message = pygame.font.Font(None, 40).render("Check !!", True, check_color)
        message_rect = message.get_rect(center=(width/2, height/2))
        screen.blit(message, message_rect)
        pygame.display.flip()
        pygame.time.wait(1000)

test_fen1 = "8/Np1P1PP1/1P2Q2r/1r5p/1Pp1n3/5k2/5B2/3K4 w"
test_fen2 = "b2n2N1/qp1QnRp1/2p5/8/4k2N/1p2P3/6P1/1K6 b"
test_fen3 = "8/3p1P2/2npP2R/P3k1p1/P5p1/5rp1/K4Nb1/8 b"

test_mate = "r2qk2r/pb4pp/1n2Pb2/2B2Q2/p1p5/2P5/2B2PPP/RN2R1K1 w"

game = Game(screen)
# game.load_board() Starting game        
game.load_board(test_mate)  # Testing different game states
game.display()
