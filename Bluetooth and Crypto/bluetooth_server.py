from bluedot.btcomm import BluetoothServer
import time
import Crypto
import hashlib

global end_program
end_program = False  # Indicates to end the program when True
INTERVAL = 3  # Time between sending messages to the client

def data_received(data):  # Function called when the client sends data to the server
    global end_program
    print(f"Data received from client: {repr(data)}")

    if data == "close":  # Close the connection and end the program if the client sends "close"
        s.send("Server ending connection per client's request\n")
        print("Ending Connection")
        s.disconnect_client()
        end_program = True  # Set to True to exit the infinite loop
    else:
        s.send("\nmessage from server")  # Server replies to client message if it is not "close"


sha = hashlib.sha256()
sha.update(b"My key")  # Create a 32 byte key to create the confidentiality and integrity keys
crypt = Crypto.Crypto_Cipher(sha.digest())

send_time = 0.0  # Time to send the message to the client
connection_made = False  # Indicates if a connection has been previously made
i = 1  # Message index
s = BluetoothServer(data_received)  # Creates the object for bluetooth connection
print("Program started, waiting for connection")

while True:
    if s.client_connected and not connection_made:  # If client is connected and no other connection has been made
        print(f"Server connected to {s.client_address}")  # Client connected to
        connection_made = True
        send_time = time.time() + INTERVAL  # Initialize when to send the message
    elif not s.client_connected and connection_made:  # If client disconnected and connection was previously made
        connection_made = False

    if end_program:  # End the program if the client specified to do so
        break

    if time.time() >= send_time and s.client_connected:  # When connected and the specified time passed
        msg = f"Server sending message {i}\n"  # Data to send to client
        s.send(msg)  # Sending data as plaintext
        ct = crypt.encrypt(msg.encode())  # Creating ciphertext
        s.send(ct.decode() + "\n")  # Turn ciphertext into string then send
        i += 1
        send_time = time.time() + INTERVAL
