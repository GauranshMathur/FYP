import sys

BOARD_SIZE = 19  # Updated to 19x19
board = [['.' for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
last_move = None

def mirror_move(move):
    x, y = move
    return (BOARD_SIZE - 1 - x, BOARD_SIZE - 1 - y)

def gtp_point_to_coords(point):
    col, row = ord(point[0].lower()) - ord('a'), int(point[1:]) - 1
    # Handle 'i' skip in GTP
    if ord(point[0].lower()) > ord('i'):
        col -= 1
    return row, col

def coords_to_gtp_point(x, y):
    col, row = chr(y + ord('a')), x + 1
    # Handle 'i' skip in GTP
    if y >= 8:
        col = chr(y + 1 + ord('a'))
    return f"{col}{row}"

def handle_gtp_command(command):
    global last_move
    
    tokens = command.strip().split()
    cmd = tokens[0]

    if cmd == "protocol_version":
        return "2"
    elif cmd == "name":
        return "MirroringBot"
    elif cmd == "version":
        return "1.0"
    elif cmd == "known_command":
        return "true" if tokens[1] in ["protocol_version", "name", "version", "known_command", "list_commands", "boardsize", "clear_board", "play", "genmove"] else "false"
    elif cmd == "list_commands":
        return "\n".join(["protocol_version", "name", "version", "known_command", "list_commands", "boardsize", "clear_board", "play", "genmove"])
    elif cmd == "boardsize":
        if int(tokens[1]) != BOARD_SIZE:
            return "? unacceptable size"
        return ""
    elif cmd == "clear_board":
        board = [['.' for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
        return ""
    elif cmd == "play":
        color, move = tokens[1], tokens[2]
        x, y = gtp_point_to_coords(move)
        board[x][y] = color[0].upper()
        last_move = (x, y)
        return ""
    elif cmd == "genmove":
        color = tokens[1]
        move = mirror_move(last_move) if last_move else None
        if move:
            x, y = move
            board[x][y] = color[0].upper()
            last_move = move
            return coords_to_gtp_point(x, y)
        else:
            return "pass"
    else:
        return "? unknown command"

if __name__ == "__main__":
    while True:
        try:
            command = sys.stdin.readline().strip()
            if command == "quit":
                break
            response = handle_gtp_command(command)
            sys.stdout.write(f"= {response}\n\n")
            sys.stdout.flush()
        except EOFError:
            break
