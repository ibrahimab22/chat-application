Chat Application README

Usage Instructions:
1.Start the Server
Run the server script first to start listening for incoming client connections.
2.Run the Client
Open a new terminal window and run the client script to connect to the server.
3.Connect Multiple Clients
For multiple users, open additional terminal windows and run the client script in each.


Commands and Inputs

Registration
Command: REGISTER <username> <password>
Purpose: Registers a new user with a unique username and password.
Server Response:
Success: "Registration Successful."
Failure: "Username is already taken."

Login
Command: LOGIN <username> <password>
Purpose: Authenticates the user, allowing them to participate in the chat.
Server Response:
Success: Confirms successful login and sets the user's nickname.
Failure: Indicates incorrect username or password.


Logout
Command: LOGOUT
Purpose: Logs the user out.
Server Response:  Informs other users that the user has left the chat.

Sending a Public Message
Command: MSG <message>
Purpose: Broadcasts a message to all connected clients.
Example: MSG Hello!

Sending a Private Message
Command: PRIVMSG <target-username> <message>
Purpose: Sends a private message to a specific user.
Example: PRIVMSG  Hi, BOB!

Listing Online Users
Command: LIST
Purpose: Lists the usernames of all users connected to the server
p