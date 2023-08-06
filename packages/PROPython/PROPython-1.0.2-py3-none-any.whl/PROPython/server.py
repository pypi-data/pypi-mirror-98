import socket
from _thread import *
from PROPython.Objects import Player
from PROPython.Settings import *
import pickle

class Server():
    def __init__(self, port, max_connections, players_server, players_instance):
        if max_connections > 2:
            print("[ERROR] You cannot make max_connections greater than 2")
            max_connections = 2
        # Server addres
        server = 'localhost'  # Not recommended to change it to public addres

        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.bind((server, port))

        # Max connections (players)
        self.s.listen(max_connections)
        print("[SERVER] Waiting for a connection, Server Started")

        # Players that can created
        if players_server:
            for player_instance in players_instance:
                players.append(player_instance)

    def threaded_client(self, conn, player):
        conn.send(pickle.dumps(players[player]))
        reply = ""
        while True:
            try:
                data = pickle.loads(conn.recv(2048))
                players[player] = data

                if not data:
                    print("[SERVER] Disconnected")
                    break
                else:
                    if player == 1:
                        reply = players[0]
                    else:
                        reply = players[1]

                    print("[SERVER] Received: ", data)
                    print("[SERVER] Sending : ", reply)

                conn.sendall(pickle.dumps(reply))
            except:
                break

        print("[SERVER] Lost connection")
        conn.close()

    def start(self):
        self.currentPlayer = 0
        while True:
            conn, addr = self.s.accept()
            print("[SERVER] Connected to:", addr)

            start_new_thread(self.threaded_client, (conn, self.currentPlayer))
            self.currentPlayer += 1