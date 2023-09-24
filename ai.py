class MirrorGoAI:
    def __init__(self):
        self.board = GoBoard()
        self.color = None

    def handle_gtp_command(self, command):
        parts = command.split()
        if parts[0] == "boardsize":
            self.board = GoBoard(int(parts[1]))
            return "=\n"
        elif parts[0] == "play":
            row, col = self.convert_gtp_coords(parts[2])
            self.board.board[row][col] = parts[1]
            return "=\n"
        elif parts[0] == "genmove":
            # Implement your move generation logic here
            ai_move = self.make_move(self.board.board)
            row, col = self.convert_gtp_coords(ai_move)
            self.board.board[row][col] = self.color
            return f"= {ai_move}\n"
        elif parts[0] == "showboard":
            return f"=\n{self.show_board()}\n"
        else:
            return "? Unknown command\n"

    def convert_gtp_coords(self, gtp_coord):
        row = BoardSize - int(gtp_coord[1:])
        col = ord(gtp_coord[0].upper()) - ord('A')
        return row, col

    # ... Other methods ...

ai = MirrorGoAI()

while True:
    command = input()
    if command == "quit":
        break
    response = ai.handle_gtp_command(command)
    print(response)
