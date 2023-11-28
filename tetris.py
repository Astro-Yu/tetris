import os
import random
import time 
import threading
import keyboard

tetris_shapes = [
    [[1, 1, 1, 1]],
    [[1, 1, 1], [0, 1, 0]],
    [[1, 1, 1], [0, 0, 1]],
    [[1, 1, 1], [1, 0, 0]],
    [[1, 1, 0], [0, 1, 1]],
]

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

class TetrisBoard:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.board = [[0] * self.width for _ in range(self.height)]
        self.current_block = None
        self.current_block_position = [0, 0] # 0번 인덱스 -> 위아래, 1번 인덱스 -> 좌우
        self.lock = threading.Lock()

    def new_block(self):
        self.current_block = random.choice(tetris_shapes)
        self.current_block_position = [0, self.width // 2 - len(self.current_block[0]) // 2]

    def is_valid_move(self, block, position):
        for i in range(len(block)):
            for j in range(len(block[0])):
                if block[i][j]:
                    row, col = position[0] + i, position[1] + j
                    if not (0 <= row < self.height and 0 <= col < self.width) or self.board[row][col]:
                        return False
                    
        return True

    def freeze_block(self):
        for i in range(len(self.current_block)):
            for j in range(len(self.current_block[0])):
                if self.current_block[i][j]:
                    row, col = self.current_block_position[0] + i, self.current_block_position[1] + j
                    self.board[row][col] = 1  # 2차원 리스트로 저장

        self.clear_lines()
        self.new_block() 
    
    
    def move_block(self, direction):
        new_position = list(self.current_block_position)
        if direction == "A":
            new_position[1] -= 1
        if direction == "D":
            new_position[1] += 1
        elif direction == "S":
            new_position[0] += 1
        elif direction == 'W':
            self.rotate_block()

        if self.is_valid_move(self.current_block, new_position):
            self.current_block_position = new_position
        else:
            if direction == "S":
                self.freeze_block()
            elif direction in ["D", "A"]:
                self.move_block("S")

    def rotate_block(self):
        rotated_block = list(zip(*reversed(self.current_block)))
        if self.is_valid_move(rotated_block, self.current_block_position):
            self.current_block = rotated_block

    def clear_lines(self):
        full_lines = [i for i, row in enumerate(self.board) if all(row)]
        for i in reversed(full_lines):
            del self.board[i]
            self.board.insert(0, [[0] for _ in range(self.width)])

    def __str__(self):
        # 초기화된 디스플레이 보드 생성
        display_board = [['  ' for _ in range(self.width)] for _ in range(self.height)]

        # 현재 블록을 디스플레이 보드에 표시
        for i in range(len(self.current_block)):
            for j in range(len(self.current_block[0])):
                row, col = self.current_block_position[0] + i, self.current_block_position[1] + j

                # 보드 내에 있는지 검사
                if 0 <= row < self.height and 0 <= col < self.width:
                    # 블록과 보드의 해당 위치에 있는 값이 1인지 확인
                    if self.current_block[i][j]:
                        display_board[row][col] = '[]'

        for i in range(self.height):
            for j in range(self.width):
                if self.board[i][j]:
                    display_board[i][j] = '[]'

        
        # 상단 경계
        display_board.insert(0, ['--'] * self.width)
        # 하단 경계
        display_board.append(['--'] * self.width)

        # 좌우 경계
        for row in display_board[1:-1]:  # Skip the first and last rows
            row.insert(0, '|')
            row.append('|')

        return '\n'.join([''.join(row) for row in display_board])



def run_game(board):
    while True:
        clear_screen()
        print(board)
        time.sleep(0.5)
        board.move_block('S')

def main():
    board = TetrisBoard(width=10, height=20)
    board.new_block()
    game_thread = threading.Thread(target=run_game, args=(board,))
    game_thread.start()

    keyboard.add_hotkey('a', lambda: board.move_block('A'))
    keyboard.add_hotkey('d', lambda: board.move_block('D'))
    keyboard.add_hotkey('s', lambda: board.move_block('S'))
    keyboard.add_hotkey('w', lambda: board.rotate_block())

if __name__ == "__main__":
    main()

