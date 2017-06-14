#!/usr/bin/env python3
from ev3dev.ev3 import *
from time import sleep, time
import datetime
import traceback
import math
import socket
import threading
import sys


# Function to test socket function of EV3Dev
# Test this function only when the EV3Dev is connected to an Android Mobile Phone using BlueTooth
def funTestSocket():
    global lcd, sock, gintLastCommand, gintTotalCommand, glstCommand, bolReConnect, gbolHeartBeat

    # timLastHB is the last time that we receive HeartBeat from the socket server
    global gtimLastHB


    # Initialize lcd screen of EV3 Brick
    lcd = Screen()

    # The following code set the ip address and port of the socket server
    # If you connect the EV3 to the PC using USB Cable or bluetooth, the ip address should be 169.254.?.?
    # If you connect the EV3 to the internet using Mobile Phone network via bluetooth, you should replace the ip address with the dns or your socket server,
    # in this case, remember to redirect the port (here we use 8070) of the router connecting your socket server, to the internal ip address of your socket server.
    HOST, PORT = "169.254.132.182", 8070
    # HOST, PORT = "lhcdims.kmdns.net", 8070


    try:
        bolProgramEnd = False
        bolReConnect = False

        while not bolProgramEnd:
            # First Time Display is Slow, so display First
            lcd.clear()
            lcd.draw.text((10,5),  'Connecting to Server ...')
            lcd.update()

            # Connect to server
            try:
                # Create a socket (SOCK_STREAM means a TCP socket)
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(10)
                sock.connect((HOST, PORT))
                sock.settimeout(None)
            except socket.timeout:
                # Here unable to connect server, may be the connection is permanently lost
                # Exit app, fix connection problem and run client again!!!
                sys.exit()

            try:
                # Login
                # Here assume sock.send will be ok for the first time, otherwise program stops here
                # ********** PROGRAM MIGHT STOP AT THE FOLLOWING CODES, WE DEAL WITH THIS LATER ********
                lcd.clear()
                lcd.draw.text((10,5),  'Before Send Login')
                lcd.update()
                sleep(1)
                sock.sendall(":Login".encode())

                lcd.clear()
                lcd.draw.text((10,5),  'After Login Sent')
                lcd.update()

                # Get ":LoginOK" from Server
                received = str(sock.recv(1024).decode())

                if received == ":LoginOK":
                    # Display Login Successful
                    lcd.clear()
                    lcd.draw.text((10,5),  'Server Connected')
                    lcd.update()

                # ********** PROGRAM MIGHT STOP ends here **********
            except:
                # Display Login Successful
                lcd.clear()
                lcd.draw.text((10,5),  'Login Failed, Exiting')
                lcd.update()
                sys.exit()



            # To avoid the EV3 Brick stops at sock.recv (here we use blocking mode),
            # Here we start the sock.recv in another thread
            client_thread = threading.Thread(target=StartClientReceive)
            client_thread.daemon = True
            client_thread.start()


            # Initialize gtimeLastHB
            gtimLastHB = time()


            # Start Sending HB to server
            gbolHeartBeat = True
            funHBStart()

            bolEnd = False
 
            while not bolEnd:
                # Check if socket disconnected
                if time() - gtimLastHB > 10:
                    # Here means for more than 10 seconds, NO heartbeat is received from socket server, we assume the connection is lost

                    # Below want to stop the thread but with error, may be thread is not stopped like that!!!
                    # client_thread.stop()

                    # Stop Sending HeartBeat to server
                    gbolHeartBeat = False

                    # First Time Display is Slow, so display First
                    lcd.clear()
                    lcd.draw.text((10,5),  'No HeartBeat received')
                    lcd.draw.text((10,15),  'Reconnect Later')
                    lcd.update()

                    # Try to tell server to close socket and wait for another connection
                    try:
                        data = ":End"
                        sock.sendall(data.encode())
                    except:
                        pass

                    # Close socket, wait for a few seconds and reconnect
                    sock.shutdown(socket.SHUT_RDWR)
                    sock.close()

                    sleep(3)

                    bolReConnect = True
                    bolEnd = True
                else:
                    if bolReConnect:
                        # This is true to received = "", means socket lost, need to reconnect
                        sock.close
                        bolEnd = True
                    else:
                        # Check if new command arrived from server
                        if gintLastCommand < gintTotalCommand:
                            gintLastCommand += 1

                            received = glstCommand[gintLastCommand-1]

                            if received == ":Disconnect":
                                bolEnd = True

                                # Stop Sending HeartBeat to server
                                gbolHeartBeat = False
                            else:
                                # Display result on the brick
                                # Or do other stuff according to command received from socket server
                                lcd.clear()
                                lcd.draw.text((10,5),  'Message received from Server:')
                                lcd.draw.text((10,20), received + " " + str(gintLastCommand))
                                lcd.draw.text((10,30), datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
                                lcd.update()

            if not bolReConnect:
                # Tell the server to close connection and wait for another client
                data = ":End"
                try:
                    sock.sendall(data.encode())
                except:
                    pass
                sock.close

                # Disconnected Normally by server, so client end program
                bolProgramEnd = True
            else:
                bolReConnect = False
    finally:
        pass



# Start HeartBeat
def funHBStart():
    thrHB = threading.Timer(2, funHeartBeat)
    thrHB.start()

def funHeartBeat():
    global sock
    try:
        sock.sendall(":HB:".encode())
    except:
        pass

    if gbolHeartBeat:
        funHBStart()



# Function to receive data from Socket Server, this function is to be started in another thread
def StartClientReceive():
    global sock, gintTotalCommand, glstCommand, bolReConnect, gtimLastHB

    bolEnd = False

    while not bolEnd:
        # Receive Data From Server and store it inside the list glstCommand
        received = str(sock.recv(1024).decode())

        if received == "":
            # Socket disconnected, may be due to mobile phone connection lost
            # There are 2 situations to determine whether the connection is lost
            # 1. received = ""
            # 2. We need to use the heartbit technique, if there is no response from the socket server for a particular time, say 5 seconds, then the connectio is assumed to be lost
            # The following codes deal with situation 1
            bolEnd = True
            bolReConnect = True
        elif received == ":HB:":
            # Got HeartBeat from socket server, reset gtimLastHB
            gtimLastHB = time()
        else:
            # Normal Receive
            gintTotalCommand += 1
            glstCommand.append(received)

            if received == ":Disconnect":
                bolEnd = True




# The Main program starts here ***********************************************************************************


try:
    # Create Global Variables
    
    # gintLastCommand is the last command number already processed
    gintLastCommand = 0

    # gintTotalCommand is the total number of command received from the socket server
    gintTotalCommand = 0

    # Create List storing all commands received from socket server
    glstCommand = []

    # Start Main Program
    funTestSocket()
except:
    # If there is any error, it will be stored in the log file in the same directory
    logtime = str(time())
    f=open("log" + logtime + ".txt",'a')  
    traceback.print_exc(file=f)  
    f.flush()  
    f.close()



# End Of Pard F - This is the end of the program ****************************************************************************


