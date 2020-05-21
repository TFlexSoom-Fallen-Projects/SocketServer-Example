# SocketServer-Example
This project is an application of the socketserver library within python3.
It actually uses a lot of the code from the [documentation][1] examples.
It applies a simple messaging scheme in order to teach others how it works.

[1]: https://docs.python.org/3.8/library/socketserver.html

The project was geared towards some nooby Python Programmers. The idea
is to put this project with a lowered firewall into a online instance
and have the students write their own clients.

# Usage

## Warnings and Disclaimers
This is not a secure project... at least I would assume it's insecure.

1. It does not perform any encryption/decryption
2. It allows users to overload the SQL database freely
3. It does not record who submits messages to the database

I am trying to project that this server is made for simplicity. It is there
to teach students how to build their own application level for fun. It should
not be used for a messaging service (for obvious reasons). I could even
bet that there is a way to do Remote Code Execution (super scary) since someone
can freely commit to the sqlite database. In any case, please do not use this
for an enterprise solution!

## Dependencies
The only dependency is the Python3 language. Everything needed should be included
in there. I would also lower the firewall of any port used within the project. This
way foreign entities can submit messages freely.

## File Descriptions

### client.py
This represents a possible client that can interface with the server.py

### server.py
This is the example that uses socketserver. One downside to this implementation
is the lack of keeping sockets alive. Instead users/clients must create new sockets
for each online transaction with the server. This is a simple implementation, but it
might be better to handle the socket as long as possible for something like a game

## Running the code
`python server.py`


Yeah it's that simple. With `python` being your path variable to the Python3 executable.
If you are on windows you might have a better chance with `py server.py`. Alternatively,
you could also try: `python3 server.py`. All of which will run the server

## Changing options and configuratiosn
I do not have a CLI or config file for this program. Please change the global variables
inside of server.py

# Contributors
- Tristan Hilbert
- aka TFlexSoom