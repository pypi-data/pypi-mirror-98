from SMRCBuilder import Exceptions
import socket
import time

class comms():
    """
    Communication Module
    """
    host = ""
    port = ""
    group = ""
    serversoc = ""
    clientsoc = ""
    connection = ""
    address = ""

    def __init__(self, host, port):
        comms.host = host
        comms.port = port
    
    def setgroup(self, group):
        """
        Sets The Type Of Self (Server Or Client)
        """
        if str(group.lower()) in ("server", "client"):
            comms.group = str(group)
        else:
            Exceptions.ArgError("Group Can Only Be Server Or Client")
    
    class server():
        """
        Server Part Of Communication Module
        """
        def check():
            if comms.group in ("client", ""): raise Exceptions.ArgError("Client Or Undefined Cannot Perform Server Actions")

        def start():
            """
            Starts The Host
            """
            comms.server.check()

            try:
                comms.serversoc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                comms.serversoc.bind((comms.host, comms.port))
                comms.serversoc.listen(1)
                print(f"Hosting Socket Connection Through {comms.host} On Port {comms.port}")
                comms.connection, comms.address = comms.serversoc.accept()
                print(f"Connected To Client")

            except:
                raise Exceptions.ServerHostingError("Error Hosting Connection. Incorrcect IP Or Port?")

        def sendmsg(message, encoding="utf8"):
            """
            Sends A Message To Client. Automatically Sent In Bytes
            """
            try:
                comms.connection.send(bytes(message, encoding))
            except:
                raise Exceptions.MessageError("Error Sending Message. Server Not Initialized?")
        
        def recvmsg(buffer=1024, encoding="utf8"):
            """
            Waits For A Message To Be Received. Message Is Decoded For You.
            """
            try:
                recv = comms.connection.recv(buffer)
                return recv.decode(encoding)
            
            except:
                raise Exceptions.MessageError("Error Reciving Message")
    
    class client():
        """
        Client Part Of Communication Module
        """
        def check():
            if comms.group in ("server", ""): raise Exceptions.ArgError("Server Or Undefined Cannot Perform Client Actions")

        def connect():
            """
            Attempts Connection To A Host
            """
            comms.client.check()

            try:
                comms.clientsoc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                comms.clientsoc.connect((comms.host, comms.port))
            
            except ConnectionRefusedError as error:
                raise Exceptions.ClientConnectionError("Error Connecting To Server. Connection May Have Timed Out. Make Sure Server Is Active")

            except:
                print(error)
                raise Exceptions.SocketError("Error Connecting To Server. Incorrect IP Or Port?")


        def sendmsg(message, encoding="utf8"):
            comms.clientsoc.sendall(bytes(message, encoding))
        
        def recvmsg(buffer=1024, encoding="utf8"):
            recv = comms.clientsoc.recv(buffer)
            return recv.decode(encoding)