import pygame
import time

#TABLA
WINDOW_WIDTH = 540
WINDOW_HEIGHT = 600
BOARD_SIZE = 9
CELL_SIZE = WINDOW_WIDTH // BOARD_SIZE

#COLORES
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
LIGHT_BLUE = (204, 229, 255)
DARK_BLUE = (0, 102, 204)

#PYGAME
pygame.init()
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Sudoku")

# LISTA DE LOS VALORES DE CADA CASILLA DEL TABLERO
board_values = [[0] * BOARD_SIZE for _ in range(BOARD_SIZE)]
selected_cell = None

#DIBUJAR TABLERO
def draw_board():
    window.fill(WHITE)
    
    # Dibujar celdas y recuadros
    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            x = col * CELL_SIZE
            y = row * CELL_SIZE
            pygame.draw.rect(window, BLACK, (x, y, CELL_SIZE, CELL_SIZE), 1)
            
            # Dibujar recuadros resaltados
            if row % 3 == 0 and col % 3 == 0:
                pygame.draw.rect(window, DARK_BLUE, (x, y, CELL_SIZE*3, CELL_SIZE*3), 3)
            
            # Dibujar números
            number = str(board_values[row][col])
            if number != '0':
                font = pygame.font.Font(None, 36)
                text = font.render(number, True, BLACK)
                text_rect = text.get_rect(center=(x + CELL_SIZE // 2, y + CELL_SIZE // 2))
                window.blit(text, text_rect)
    
    # Dibujar celda seleccionada
    if selected_cell is not None:
        row, col = selected_cell
        x = col * CELL_SIZE
        y = row * CELL_SIZE
        pygame.draw.rect(window, DARK_BLUE, (x, y, CELL_SIZE, CELL_SIZE), 3)

#CAMBIAR VALOR DE CELDA
def update_cell_value(row, col, value):
    board_values[row][col] = value
def modify_cell_value(row, col, value):
    if selected_cell is not None:
        row, col = selected_cell
        update_cell_value(row, col, value)


#RESOLVER JUEGO
def solve_sudoku(board):
    #ENCONTRAR LA SIGUIENTE CELDA VACIA
    def find_empty_cell(board):
        for row in range(9):
            for col in range(9):
                if board[row][col] == 0:
                    return row, col
        return None

    #SI EL NUMERO ES VALIDO (1-9)
    def is_valid(board, row, col, num):
        #FILA
        for i in range(9):
            if board[row][i] == num:
                return False

        #COLUMNA
        for i in range(9):
            if board[i][col] == num:
                return False

        # VERIFICAR CADA BLOQUE (3X3)
        #CALCULAMOS LA ESQUINA SUP IZQ
        start_row = (row // 3) * 3
        start_col = (col // 3) * 3

        for i in range(start_row, start_row + 3):
            for j in range(start_col, start_col + 3):
                if board[i][j] == num:
                    return False #REGRESAMOS FALSE SI EL NUMERO NO ES VALIDO

        return True

    # FUNC RECURSIVA PARA RESOLVER
    def solve(board):
        # ENCONTRAR LA SIG CELDA VACIA
        cell = find_empty_cell(board)
        if cell is None:
            return True  # JUEGO RESUELTO

        row, col = cell

        # PROBAMOS VALORES DEL 1-9
        for num in range(1, 10):
            if is_valid(board, row, col, num):
                print(board_values)
                board[row][col] = num
                update_cell_value(row,col,num)
                #time.sleep(1)

                if solve(board):
                    return True

                # DESHACER EL CAMBIO SI NO SE ENCUENTRA SOLUCION
                board[row][col] = 0

        return False  # NO HAY SOLUCION

    # CREAMOS COPIA DEL TABLERO PARA MODIFICAR EL ORIGINAL
    board_copy = [row[:] for row in board]

    # RESOLVER JUEGO
    if solve(board_copy):
        return board_copy  # DEVOLVER SOLUCION ENCONTRADA
    else:
        return None  # NO HAY SOLUCION

# BUCLE DE JUEGO
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # CLICK IZQ
                x, y = event.pos
                col = x // CELL_SIZE
                row = y // CELL_SIZE
                selected_cell = (row, col)
            elif event.button == 3:  # CLICK DER
                selected_cell = None
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                selected_cell = None
            elif event.key == pygame.K_r:
                start_time = time.time()
                res = solve_sudoku(board_values)
                end_time = time.time()
                print("Resuelto en: ", end_time - start_time)
                #board_values = res
            elif selected_cell is not None:
                row, col = selected_cell
                if event.key == pygame.K_BACKSPACE or event.key == pygame.K_DELETE:
                    modify_cell_value(row, col, 0)
                elif event.unicode.isdigit() and int(event.unicode) in range(1, 10):
                    modify_cell_value(row, col, int(event.unicode))

    # DIBUJAR TABLERO
    draw_board()
    
    # ACTUALIZAR VENTANA
    pygame.display.flip()

# CERRAR JUEGO
pygame.quit()