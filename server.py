import socket
from _thread import start_new_thread
import pickle
from player import Player
from game import Game

server = "192.168.1.36"
port = 8820
BOARD_SIZE = 3

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind( (server, port) )
except socket.error as e:
    print(e)

s.listen()
print("[Server] Waiting for connections")

connected = set()
games = {}
players_count = 0

def client(con, p, game_id):
    global players_count
    con.send(pickle.dumps(p)) #send the client his player
    
    while True:
        try:
            data = con.recv(4096).decode()

            if game_id in games:
                game = games[game_id]

                if not data:
                    break
                else:
                    if data == "reset":
                        game.reset()
                    elif data != "get" and game.current_turn == p.id:
                        pos = data.split(",")
                        game.make_move(p, pos[0], pos[1])
                        game.current_turn = 1 - p.id
                        if game.board.check_for_winner(p, pos[0], pos[1]):
                            game.done = True
                        elif game.is_draw():
                            game.done = True

                con.sendall(pickle.dumps(game))
            else:
                break
        except:
            break
        
    print("[SERVER] Lost connection")
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
        print("[SERVER] Creating new game...")
    else:
        games[game_id].ready = True
        games[game_id].current_turn = 0
        p = Player("X", 1)
    
    start_new_thread(client, (con, p, game_id))
