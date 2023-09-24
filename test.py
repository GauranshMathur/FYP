import random

# Global variables
played_moves = set()
last_opponent_move = ""

def convert_gtp_to_coords(gtp_coords):
    column, row = gtp_coords[0], gtp_coords[1:]
    x = ord(column) - ord('A')
    if x >= 8:  # GTP lettering skips 'I'
        x -= 1
    y = 19 - int(row)
    return x, y

def play(color, move):
    global played_moves, last_opponent_move
    played_moves.add(move)
    last_opponent_move = move
    return "="

def genmove(color):
    # Try mirrored move first
    mirrored_move = mirror_move(last_opponent_move)
    if mirrored_move not in played_moves:
        played_moves.add(mirrored_move)
        return f"= {mirrored_move}"
    
    # If mirrored move is occupied, generate random move
    all_moves = [chr(x + ord('A')) + str(19 - y) for x in range(19) for y in range(19)]
    random.shuffle(all_moves)
    for move in all_moves:
        if move not in played_moves:
            played_moves.add(move)
            return f"= {move}"
    
    # If all intersections are occupied, pass
    return "= pass"

def mirror_move(move):
    x, y = convert_gtp_to_coords(move)
    mirror_x = 18 - x
    mirror_y = 18 - y
    mirrored_move = chr(mirror_x + ord('A')) + str(19 - mirror_y)
    return mirrored_move

def handle_command(command):
    tokens = command.strip().split()

    if not tokens:
        return ''

    if tokens[0] == "name":
        return "= MirroringBot"
    elif tokens[0] == "version":
        return "= 1.0"
    elif tokens[0] == "protocol_version":
        return "= 2"
    elif tokens[0] == "known_command":
        known_commands = ["name", "version", "protocol_version", "list_commands",
                          "boardsize", "clear_board", "play", "genmove", "quit", "komi"]
        return f"= {'true' if tokens[1] in known_commands else 'false'}"
    elif tokens[0] == "list_commands":
        return "= name\nversion\nprotocol_version\nlist_commands\nboardsize\nclear_board\nplay\ngenmove\nquit\nkomi"
    elif tokens[0] == "boardsize":
        if int(tokens[1]) != 19:
            return "? unacceptable size"
        return "="
    elif tokens[0] == "clear_board":
        global played_moves
        played_moves = set()
        return "="
    elif tokens[0] == "play":
        return play(tokens[1], tokens[2])
    elif tokens[0] == "genmove":
        return genmove(tokens[1])
    elif tokens[0] == "komi":
        return "="
    elif tokens[0] == "quit":
        return "="

    return "? unknown command"

if __name__ == "__main__":
    while True:
        try:
            command = input().strip()
            response = handle_command(command)
            print(response)
            print()  # GTP requires two newlines
            if command == "quit":
                break
        except EOFError:
            break
