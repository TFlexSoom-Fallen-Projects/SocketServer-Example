import socketserver

### Derived from Documentation
# https://docs.python.org/3.8/library/socketserver.html

import socket
import threading

import sqlite3
DB_NAME = "messages.db"

class ThreadedTCPRequestHandler(socketserver.BaseRequestHandler):

    def handle(self):
        try:
            self.request.setblocking(False)
            data = str(self.request.recv(1024), 'ascii')
            bufbuf = data
            counter = 0
            while "%" not in bufbuf:
                # This tries to be nice, but really it doesn't handle
                # more than 1024 characters.
                if len(bufbuf) >= 4000:
                    self.request.sendall(str.encode("ERRBuffer Overloaded%"))
                    break
                
                data = str(self.request.recv(1024), 'ascii')
                
                if counter > 10000:
                    self.request.sendall(str.encode("ERRTimeout!%"))
                    with open("log.txt", 'a') as f:
                        f.write("Counter Reached!\n")
                        f.close()
                    break
                else:
                    counter += 1

                bufbuf += data

            conn = sqlite3.connect(DB_NAME)
            c = conn.cursor()
            while "%" in bufbuf:
                # Get End of command
                end = bufbuf.index("%")
                
                # Do something with command
                if bufbuf[:len("POST")] == "POST":
                    self.request.sendall(str.encode("MSGPosting Message!%"))
                    
                    message = bufbuf[len("POST"):end]
                    c.execute('''INSERT INTO messages VALUES(NULL, ?);''', (message,))
                    conn.commit()

                elif bufbuf[:len("GET")] == "GET":
                    c.execute('''SELECT * FROM messages ORDER BY id;''')
                    self.request.sendall(str.encode("MSG" + repr(c.fetchall()) + "%"))
                
                else:
                    self.request.sendall(str.encode("ERRUnknown Command%"))
                
                # Go To Next Piece
                bufbuf = bufbuf[end+1:]
            
        except Exception as e:
            with open("log.txt", 'a') as f:
                f.write("Problem!\n")
                f.write(repr(e))
                f.write("\n\n")
                f.close()



        

class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass

if __name__ == "__main__":
    # Port 0 means to select an arbitrary unused port
    HOST, PORT = "localhost", 8080
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''DROP TABLE IF EXISTS messages''')
    c.execute('''CREATE TABLE messages (id INTEGER PRIMARY KEY AUTOINCREMENT, message text);''')
    c.execute('''INSERT INTO messages VALUES (NULL, "Server has Started");''')

    conn.commit()
    
    conn.close()

    with open("log.txt", "w+") as f:
        f.write("")
        f.close()

    server = ThreadedTCPServer((HOST, PORT), ThreadedTCPRequestHandler) with server:
        ip, port = server.server_address

        # Start a thread with the server -- that thread will then start one
        # more thread for each request
        server_thread = threading.Thread(target=server.serve_forever)
        # Exit the server thread when the main thread terminates
        server_thread.daemon = True
        server_thread.start()

        print("Server loop running in thread:", server_thread.name)

        input("Shutdown?")
        server.shutdown()