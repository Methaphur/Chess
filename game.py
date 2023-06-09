import pygame 

# Initializing pygame window
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
check_color = (255, 0 ,0)


class ChessPiece:
    def __init__(self,color,position):
        self.color = color 
        self.position = position
    
    def move(self, position , board):        
        new_row , new_col = position
        old_row , old_col = self.position
        # Moving character from current piece to new pos
        board[old_row][old_col] = 0
        board[new_row][new_col] = self
        self.position = new_row , new_col

        # Castling checks
        if isinstance(self, (King, Rook)) and not self.has_moved:
            self.has_moved = True

class Bishop(ChessPiece):
    def valid_moves(self, board):
        valid_moves = []
    
        curr_row , curr_col = self.position
        rows = cols = len(board)

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
                dest_piece = board[final_row][final_col]

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
    def valid_moves(self,board):
        valid_moves = []

        curr_row , curr_col = self.position
        rows = cols = len(board)

        # Define all possible offsets for knights movements
        offsets = [
        (-2, -1), (-2, 1),(-1, -2), (-1, 2),
        (1, -2), (1, 2),(2, -1), (2, 1)
        ]

        for offset in offsets:
            offset_row , offset_col = offset
            final_row , final_col = curr_row + offset_row , curr_col + offset_col

            if 0 <= final_row < rows and 0 <= final_col < cols:
                dest_piece = board[final_row][final_col]

                # Checking if square is empty or can be captured (opponent)
                if not dest_piece or dest_piece.color != self.color:
                    valid_moves.append((final_row,final_col))
        
        return valid_moves

class Rook(ChessPiece):
    def __init__(self,color,position):
        super().__init__(color,position)
        self.has_moved = False

    def valid_moves(self,board):
        valid_moves = []
    
        curr_row , curr_col = self.position
        rows = cols = len(board)

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
                dest_piece = board[final_row][final_col]

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

class Queen(ChessPiece):
    def valid_moves(self,board):
        valid_moves = []
    
        curr_row , curr_col = self.position
        rows = cols = len(board)

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
                dest_piece = board[final_row][final_col]

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

class King(ChessPiece):
    def __init__(self,color,position):
        super().__init__(color,position)
        self.has_moved = False

    def valid_moves(self,board):
        valid_moves = []
    
        curr_row , curr_col = self.position
        rows = cols = len(board)

        offsets = [
        (-1, -1), (-1, 0), (-1, 1),
        (0, -1),           (0, 1),
        (1, -1),  (1, 0),  (1, 1)
        ]

        for offset_row , offset_col in offsets:
            new_row = curr_row + offset_row
            new_col = curr_col + offset_col

            if 0 <= new_row < rows and 0 <= new_col < cols:
                piece = board[new_row][new_col]
                if not piece or piece.color != self.color:
                    # Temporarily make the move and check for check
                    temp = board[new_row][new_col]
                    board[new_row][new_col] = self
                    board[curr_row][curr_col] = 0

                    if not game.is_check(board,self.color):
                        valid_moves.append((new_row,new_col))

                    # Undo the move
                    board[new_row][new_col] = temp
                    board[curr_row][curr_col] = self
        
        # Castling possibility
            if not self.has_moved:
                curr_row , curr_col = self.position
                left_castle , right_castle = self.check_castling(board)

                if left_castle and isinstance(board[curr_row][curr_col - 4],Rook)\
                      and not board[curr_row][curr_col -4].has_moved:
                    valid_moves.append((curr_row , curr_col -2))
                if right_castle and isinstance(board[curr_row][curr_col +3],Rook)\
                      and not board[curr_row][curr_col +3].has_moved: 
                    valid_moves.append((curr_row, curr_col + 2))

        return valid_moves

    def check_castling(self,board):
        curr_row , curr_col = self.position
        left_castle = right_castle = False

        if not self.has_moved:
            if not board[curr_row][curr_col-1] and not board[curr_row][curr_col-2] and not board[curr_row][curr_col -3]:
                left_castle = True
            if not board[curr_row][curr_col + 1] and not board[curr_row][curr_col +2]:
                right_castle = True

        if left_castle:
            offsets = [ (0 ,-1),(0, -2)]
            for row_offset , col_offset in offsets:
                new_row = curr_row + row_offset
                new_col = curr_col + col_offset

                board[new_row][new_col] = self
                board[curr_row][curr_col] = 0
                if game.is_check(board,self.color):
                    board[new_row][new_col] = 0
                    board[curr_row][curr_col] = self
                    left_castle = False
                
                board[new_row][new_col] = 0
                board[curr_row][curr_col] = self

        if right_castle:
            offsets = [ (0 , 1),(0, 2)]
            for row_offset , col_offset in offsets:
                new_row = curr_row + row_offset
                new_col = curr_col + col_offset

                board[new_row][new_col] = self
                board[curr_row][curr_col] = 0
                if game.is_check(board,self.color):
                    board[new_row][new_col] = 0
                    board[curr_row][curr_col] = self
                    right_castle = False
                
                board[new_row][new_col] = 0
                board[curr_row][curr_col] = self

        # Returns a tuple of bool whether left or right castle
        return (left_castle, right_castle)

    def perform_castle(self,position,board):
        curr_row , curr_col = self.position
        final_row , final_col = position

        # Left Castle
        if curr_col - final_col > 0:
            board[curr_row][curr_col] = 0
            board[final_row][final_col] = self
            board[curr_row][curr_col-4].move((final_row,final_col+1),board)
            self.position = (final_row,final_col)
            self.has_moved = True
        # Right Castle 
        if curr_col - final_col < 0:
            board[curr_row][curr_col] = 0
            board[final_row][final_col] = self
            board[curr_row][curr_col +3].move((final_row,final_col-1),board)
            self.position = (final_row,final_col)
            self.has_moved = True

    def move(self,position,board):
        if abs(position[1] - self.position[1]) == 2:
            self.perform_castle(position,board)
            return

        new_row , new_col = position
        old_row , old_col = self.position
        board[old_row][old_col] = 0
        board[new_row][new_col] = self
        self.position = new_row , new_col    
        self.has_moved = True

class Pawn(ChessPiece):
    def __init__(self,color,position):
        super().__init__(color,position)
        self.en_passant_target = False

    def valid_moves(self,board):
        valid_moves = []
            
        curr_row , curr_col = self.position

        if self.color == "white":
            direction = -1
            start_row = 6
        
        else:
            direction = 1
            start_row = 1
        
        final_row = curr_row + direction 
        rows = cols = len(board)

        if 0 <= final_row < rows and not board[final_row][curr_col]:
            valid_moves.append((final_row,curr_col))

            if curr_row == start_row:
                final_row = curr_row + direction*2
                if not board[final_row][curr_col]:
                    valid_moves.append((final_row,curr_col))
                
                
        # Checking if pawn can capture 
        capture_offset = [(direction,-1),(direction,1)]
        for row_offset , col_offset in capture_offset:
            final_row , final_col = curr_row + row_offset , curr_col + col_offset
            if 0 <= final_row < rows and 0 <= final_col < cols:
                dest_piece = board[final_row][final_col]
                en_passant = board[curr_row][final_col]
                if dest_piece and dest_piece.color != self.color:
                    valid_moves.append((final_row,final_col))
                if en_passant and en_passant.color != self.color and isinstance(en_passant, Pawn)  and en_passant.en_passant_target and not game.en_passant_check and game.en_passant_check == self.color:
                    valid_moves.append((final_row,final_col))

        return valid_moves

    def perform_promotion(self,position,board):
        target_row , target_col = position
        curr_row , curr_col = self.position
        board[target_row][target_col] = Queen(self.color,position)
        board[curr_row][curr_col] = 0
        
    def move(self,position,board):
        if position[0] == 0 or position[0] == 7:
            self.perform_promotion(position,board)
            return
        
        new_row , new_col = position
        old_row , old_col = self.position
        
        # En passant move
        # sketchy code but pawn moves to empty square diagonally 
        if abs(old_col - new_col) == 1:
            if isinstance(board[old_row][old_col - (old_col - new_col)],Pawn):
                board[old_row][old_col - (old_col - new_col)] = 0

        # Moving character from current piece to new pos
        board[old_row][old_col] = 0
        board[new_row][new_col] = self
        self.position = new_row , new_col
        if abs(old_row - new_row) == 2 and game.en_passant_check != self.color:
            self.en_passant_target = True
            game.en_passant_check = self.color
        else:
            self.en_passant_target = False



piece_fen = {"r":Rook,"n":Knight,"b":Bishop,"q":Queen,"k":King,"p":Pawn 
             }

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

class Game:
    def __init__(self,screen):
        self.screen = screen
        self.board = [[0]* 8 for _ in range(8)]
        self.current_player = "white" 
        self.selected_piece = None
        self.has_check = None
        self.has_mate = None
        self.en_passant_check = None

    def load_board(self,fen = "DEFAULT"):
        if fen == "DEFAULT":
            fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w" # Starting fen
        # Splitting fen into board state and active player
        fen = fen.split()   
        board_state = fen[0]
        self.current_player = "white" if fen[1] == "w" else "black"
    
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
                    
                    if isinstance(self.board[row][col], King):
                        if (row,col) not in ((0,4),(7,4)):
                            self.board[row][col].has_moved = True 
                    col += 1

    def handle_click(self,pos):
        row = pos[1] // cell_size
        col = pos[0] // cell_size

        cell = self.board[row][col]
        # Selecting an unselected square
        if not self.selected_piece:
            if cell:
                if cell.color != self.current_player:
                    return
                    
                self.selected_piece = cell
                return
            else:
                self.selected_piece = None

        # Square is already selected
        if self.selected_piece:
            if (row, col) in self.selected_piece.valid_moves(self.board):
                pos = self.selected_piece.position
                temp = self.board[row][col]
                self.selected_piece.move((row,col),self.board)
                # If check after move ... illegal move
                if self.is_check(self.board,self.current_player):
                    self.board[pos[0]][pos[1]] = self.selected_piece
                    self.board[row][col] = temp
                    self.selected_piece.position = (pos)
                    self.selected_piece = None
                    return
                
                # Changing the en passant target
                if self.en_passant_check == self.selected_piece.color:
                    self.en_passant_check = None

                self.current_player = "white" if self.current_player != "white" else "black"
                # Checkmate condition
                if self.check_mate(self.board,self.current_player):
                    self.has_mate = self.current_player
                
                # King in check
                if self.is_check(self.board,self.current_player):
                    self.has_check = self.current_player
                
                else:
                    self.has_check = None

            self.selected_piece = None

    def is_check(self,board,color):
        king_pos = None

        # Finding king position
        for row in range(8):
            for col in range(8):
                piece = board[row][col]
                if isinstance(piece, King) and piece.color == color:
                    king_pos = (row , col)
                    break
        
        # Checking for attac
        for row in range(8):
            for col in range(8):
                piece = board[row][col]
                if piece and piece.color != color and not isinstance(piece , King):
                    valid_moves = piece.valid_moves(board)
                    if king_pos in valid_moves:
                        return True
        
        for row in range(8):
            for col in range(8):
                piece = board[row][col]
                if piece and piece.color != color and isinstance(piece, King):
                    curr_row , curr_col = piece.position
                    king_offsets = [
                    (-1, -1), (-1, 0), (-1, 1),
                    (0, -1),           (0, 1),
                    (1, -1),  (1, 0),  (1, 1)
                    ]
                    for offset_row , offset_col in king_offsets:
                        new_row = curr_row + offset_row
                        new_col = curr_col + offset_col
                        if 0 <= new_row < 8 and 0 <= new_col < 8:
                            valid_moves.append((new_row,new_col))
                            # Minor optimization
                            if king_pos in valid_moves:
                                return True

        return False    

    def check_mate(self,board,color):
        # Check if player's king is in Check
        if self.is_check(board,color):
            # Check if any piece can make a valid move to get our of check
            for row in range(8):
                for col in range(8):
                    piece = board[row][col]
                    if piece and piece.color == color:
                        valid_moves = piece.valid_moves(board)
                        for move in valid_moves:
                            target_row , target_col = move
                            # Try making a move and see if still in check
                            temp = board[target_row][target_col]
                            board[target_row][target_col] = piece
                            board[row][col] = 0

                            # If not check , king can escape check
                            if not self.is_check(board,color):
                                board[row][col] = piece
                                board[target_row][target_col] = temp
                                return False
                        
                            # Undo the move
                            board[row][col] = piece
                            board[target_row][target_col] = temp
            
            # If no valid move can get king out of check , it's checkmate 
            return True
        # King not in check
        return False

    def display(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                # Quitting the game
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False

                # Selecting a tile
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        pos = pygame.mouse.get_pos()
                        self.handle_click(pos)
            

            # Coloring all the tiles
            for row in range(8):
                for col in range(8):
                    color = white_cell if (row + col) % 2 == 0 else black_cell
                    pygame.draw.rect(screen,color,(col * cell_size, row * cell_size, cell_size, cell_size))

                    # Selected piece
                    if self.selected_piece:
                        select_row,select_col = self.selected_piece.position
                        pygame.draw.rect(screen,select_cell_color,(select_col * cell_size, select_row * cell_size, cell_size, cell_size))

                        valid_moves = self.selected_piece.valid_moves(self.board)
                        for x , y in valid_moves:
                             pygame.draw.rect(screen,valid_spot_color,(y * cell_size, x * cell_size, cell_size, cell_size))

            # Rank and File Indexing
            label_font = pygame.font.Font(None ,22)

            rank_labels = ['8', '7', '6', '5', '4', '3', '2', '1']
            file_labels = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']

            for i in range(8):
                color = white_cell if i%2 != 0 else black_cell
                rank_text = label_font.render(rank_labels[i],True, color)
                rank_rect = rank_text.get_rect(x = 5 , y = i * cell_size + 5)
                screen.blit(rank_text,rank_rect)

                color = white_cell if i%2 == 0 else black_cell
                file_text = label_font.render(file_labels[i],True, color)
                file_rect = rank_text.get_rect(x = i * cell_size + cell_size - 17 , y = height - 15)
                screen.blit(file_text,file_rect)

            # Loading all the pieces into the game 
            for row in range(8):
                for col in range(8):
                    piece = self.board[row][col]

                    if piece:
                        screen.blit(pieces[type(piece),piece.color], (col*cell_size , row * cell_size))

            # Grid lines
            for x in range(0, width, cell_size):
                pygame.draw.line(screen, grid_color, (x, 0), (x, height))
            for y in range(0, height, cell_size):
                pygame.draw.line(screen, grid_color, (0, y), (width, y)) 


            # Updating the board
            pygame.display.flip()
        
            # Checkmate  message
            if self.has_mate:
                while running:
                    # Quitting 
                    for event in pygame.event.get():
                        if event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_ESCAPE:
                                running = False
                        if event.type == pygame.QUIT:
                            running = False

                    message = pygame.font.Font(None, 40).render("CHECK MATE" , True , check_color)
                    message_rect = message.get_rect(center = (width//2,height//2))
                    screen.blit(message,message_rect)
                    pygame.display.flip()
                
                pygame.quit()
                exit(1)

            if self.has_check:
                message = pygame.font.Font(None, 34).render("Check !!", True, check_color)
                message_rect = message.get_rect(center=(width//2, height//2))
                screen.blit(message, message_rect)
                pygame.display.flip()
                pygame.time.wait(2000)
                self.has_check = None

        pygame.quit()
        exit(1)

test_fen1 = "8/Np1P1PP1/1P2Q2r/1r5p/1Pp1n3/5k2/5B2/3K4 w"
test_fen2 = "b2n2N1/qp1QnRp1/2p5/8/4k2N/1p2P3/6P1/1K6 b"
test_fen3 = "8/3p1P2/2npP2R/P3k1p1/P5p1/5rp1/K4Nb1/8 b"
test_mate = "r2qk2r/pb4pp/1n2Pb2/2B2Q2/p1p5/2P5/2B2PPP/RN2R1K1 w"
mate_in_1 = "k7/ppp5/8/3q4/1P3RK1/7r/P4Q2/8 b"

final_test = "2nb2k1/3P4/p2p1Ppp/3P2p1/3QR3/1P6/3K2P1/8 w - - 0 1"
game = Game(screen)
game.load_board(test_fen1)
game.display()