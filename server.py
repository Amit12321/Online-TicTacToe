import socket
import struct
from pickle import dumps, loads

from _thread import start_new_thread
from game import Game
from player import Player

server = "192.168.1.33"
port = 6654
BOARD_SIZE = 3


def prepare_to_send(data):  # padding packet with its length
    packet = dumps(data)
    length = struct.pack('!I', len(packet))
    packet = length + packet
    return packet


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))
except socket.error as e:
    print(e)

s.listen()
print("[Server] Waiting for connections")

games = {}
players_count = 0


def client(con, p, game_id):
    global players_count

    # Sending the client his player
    con.sendall(prepare_to_send(p))

    while True:
        try:
            data = con.recv(1024).decode()
            if game_id in games:
                game = games[game_id]

                if not data:
                    break
                else:
                    if data == "reset":
                        game.reset()
                    elif data != "get" and game.current_turn == p.get_id():
                        pos = data.split(",")
                        game.make_move(p, int(pos[0]), int(pos[1]))
                        game.current_turn = 1 - p.get_id()
                        if game.board.check_for_winner(p, int(pos[0]), int(pos[1])):
                            game.add_win(p.get_id())
                            game.done = True
                        if game.is_draw():
                            game.done = True
                    con.sendall(prepare_to_send(game))
            else:
                break
        except Exception as e:
            print(e)
            break

    print("[SERVER] Lost connection")
    con.sendall(prepare_to_send("Q"))
    try:
        del games[game_id]
        print("[SERVER] Closing game ", game_id)
    except:
        pass
    players_count -= 1
    con.close()


while True:
    con, addr = s.accept()
    print("[SERVER] Connected to: ", addr)

    players_count += 1
    p = Player("O", 0)
    game_id = (players_count - 1) // 2
    if players_count % 2 == 1:
        games[game_id] = Game(game_id, BOARD_SIZE)
        print("[SERVER] Creating new game with id ", game_id)
    else:
        games[game_id].ready = True
        games[game_id].current_turn = 0
        p = Player("X", 1)

    start_new_thread(client, (con, p, game_id))
