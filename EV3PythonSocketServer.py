import clr
clr.AddReference('System.Drawing')
clr.AddReference('System.Windows.Forms')
clr.AddReference('IronPython')

import socket
import threading
from time import sleep, time
import datetime

from System.Drawing import *
from System.Windows.Forms import *

from IronPython.Compiler import CallTarget0


class MyForm(Form):
    global gstrTemp
    def __init__(self):
        # Create child controls and initialize form

        # Set Forms Attribute
        self.Text = "EV3 Python Socket Server"
        self.Width = 800
        self.Height = 600

        # Add Multi-Line TextBox Output
        self.setupTextBoxOutput()

        # Add a button to start server
        self.btnStart = Button()
        self.btnStart.Width = 120
        self.btnStart.Text = 'Start Server'
        self.btnStart.Location = Point(40, 450)
        self.btnStart.Click += self.btnStartClicked
        self.btnStart.Enabled = True

        # Add a button to stop server
        self.btnStop = Button()
        self.btnStop.Width = 120
        self.btnStop.Text = 'Quit Server'
        self.btnStop.Location = Point(40, 510)
        self.btnStop.Click += self.btnStopClicked
        self.btnStop.Enabled = False

        # Add Left Button
        self.btnLeft = Button()
        self.btnLeft.Text = 'Left'
        self.btnLeft.Location = Point(200, 480)
        self.btnLeft.Click += self.btnLeftClicked
        self.btnLeft.Enabled = False

        # Add Right Button
        self.btnRight = Button()
        self.btnRight.Text = 'Right'
        self.btnRight.Location = Point(400, 480)
        self.btnRight.Click += self.btnRightClicked
        self.btnRight.Enabled = False

        # Add Forward Button
        self.btnForward = Button()
        self.btnForward.Text = 'Forward'
        self.btnForward.Location = Point(300, 450)
        self.btnForward.Click += self.btnForwardClicked
        self.btnForward.Enabled = False

        # Add Backward Button
        self.btnBackward = Button()
        self.btnBackward.Text = 'Backward'
        self.btnBackward.Location = Point(300, 510)
        self.btnBackward.Click += self.btnBackwardClicked
        self.btnBackward.Enabled = False

        # Add Stop Motor Button
        self.btnStopMotor = Button()
        self.btnStopMotor.Width = 120
        self.btnStopMotor.Text = 'Stop Motor'
        self.btnStopMotor.Location = Point(520, 450)
        self.btnStopMotor.Click += self.btnStopMotorClicked
        self.btnStopMotor.Enabled = False

        # Add Disconnect Button
        self.btnDisconnect = Button()
        self.btnDisconnect.Width = 120
        self.btnDisconnect.Text = 'Disconnect'
        self.btnDisconnect.Location = Point(520, 510)
        self.btnDisconnect.Click += self.btnDisconnectClicked
        self.btnDisconnect.Enabled = False

        # Add all the controls
        self.Controls.Add(self.mtbOutput)
        self.Controls.Add(self.btnStart)
        self.Controls.Add(self.btnStop)
        self.Controls.Add(self.btnLeft)
        self.Controls.Add(self.btnRight)
        self.Controls.Add(self.btnForward)
        self.Controls.Add(self.btnBackward)
        self.Controls.Add(self.btnStopMotor)
        self.Controls.Add(self.btnDisconnect)
        
    # Create a multiline text box
    def setupTextBoxOutput(self):
        textbox = TextBox()
        textbox.Text = ""
        textbox.Location = Point(40, 20)
        textbox.Width = 700
        textbox.Height = 400
        textbox.Multiline = True
        textbox.ScrollBars = ScrollBars.Vertical
        textbox.AcceptsTab = False
        textbox.AcceptsReturn = False
        textbox.WordWrap = True
        textbox.ReadOnly = True
        self.mtbOutput = textbox





    # GUI Programming Starts Here

    

    # Create btnStartClicked Event            
    def btnStartClicked(self, sender, event):
        global server_thread

        #Disable the start button
        self.btnStart.Enabled = False
        self.btnStop.Enabled = True
        
        #Start Server Socket in another thread
        server_thread = threading.Thread(target=StartServerSocket)
        server_thread.daemon = True
        server_thread.start()
        funUpdateOutput("Starting Socket Server, waiting for EV3 Brick to login")



    # Create btnStopClicked Event            
    def btnStopClicked(self, sender, event):
        global server_thread

        #Stop thread and Quit program
        server_thread.stop()
        Application.Exit()



    # Create btnLeftClicked Event
    def btnLeftClicked(self, sender, event):
        global gstrSend
        gstrSend = 'Left'
        server_threadsend = threading.Thread(target=StartServerSend)
        server_threadsend.daemon = True
        server_threadsend.start()
        funUpdateOutput("Left")



    # Create btnRightClicked Event
    def btnRightClicked(self, sender, event):
        global gstrSend
        gstrSend = 'Right'
        server_threadsend = threading.Thread(target=StartServerSend)
        server_threadsend.daemon = True
        server_threadsend.start()
        funUpdateOutput("Right")



    # Create btnForwardClicked Event
    def btnForwardClicked(self, sender, event):
        global gstrSend
        gstrSend = 'Forward'
        server_threadsend = threading.Thread(target=StartServerSend)
        server_threadsend.daemon = True
        server_threadsend.start()
        funUpdateOutput("Forward")



    # Create btnBackwardClicked Event
    def btnBackwardClicked(self, sender, event):
        global gstrSend
        gstrSend = 'Backward'
        server_threadsend = threading.Thread(target=StartServerSend)
        server_threadsend.daemon = True
        server_threadsend.start()
        funUpdateOutput("Backward")


    # Create btnStopMotorClicked Event
    def btnStopMotorClicked(self, sender, event):
        global gstrSend
        gstrSend = 'Stop'
        server_threadsend = threading.Thread(target=StartServerSend)
        server_threadsend.daemon = True
        server_threadsend.start()
        funUpdateOutput("Stop Motor")


    # Create btnDisconnectClicked Event
    def btnDisconnectClicked(self, sender, event):
        global gstrSend
        gstrSend = ':Disconnect'
        server_threadsend = threading.Thread(target=StartServerSend)
        server_threadsend.daemon = True
        server_threadsend.start()




    # This function allows updating the Multiline Text Box from ANOTHER Thread
    def funUpdate(self):
        global gstrTemp
        def SetText():
            global gstrTemp
            text = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ": " + gstrTemp + "\r\n"
            self.mtbOutput.Text = text + self.mtbOutput.Text
            
        self.mtbOutput.Invoke(CallTarget0(SetText))



    # This login function enables all the buttons after client connect, "INVOKE" is being used in order to allow it can be called from another thread
    def funLogin(self):
        def EnableLeft():
            self.btnLeft.Enabled = True
        def EnableRight():
            self.btnRight.Enabled = True
        def EnableForward():
            self.btnForward.Enabled = True
        def EnableBackward():
            self.btnBackward.Enabled = True
        def EnableStopMotor():
            self.btnStopMotor.Enabled = True
        def EnableDisconnect():
            self.btnDisconnect.Enabled = True
            
        self.btnLeft.Invoke(CallTarget0(EnableLeft))
        self.btnRight.Invoke(CallTarget0(EnableRight))
        self.btnForward.Invoke(CallTarget0(EnableForward))
        self.btnBackward.Invoke(CallTarget0(EnableBackward))
        self.btnStopMotor.Invoke(CallTarget0(EnableStopMotor))
        self.btnDisconnect.Invoke(CallTarget0(EnableDisconnect))



    # This logout function disables all the buttons after client disconnect, "INVOKE" is being used in order to allow it can be called from another thread
    def funLogout(self):
        def DisableLeft():
            self.btnLeft.Enabled = False
        def DisableRight():
            self.btnRight.Enabled = False
        def DisableForward():
            self.btnForward.Enabled = False
        def DisableBackward():
            self.btnBackward.Enabled = False
        def DisableStopMotor():
            self.btnStopMotor.Enabled = False
        def DisableDisconnect():
            self.btnDisconnect.Enabled = False
            
        self.btnLeft.Invoke(CallTarget0(DisableLeft))
        self.btnRight.Invoke(CallTarget0(DisableRight))
        self.btnForward.Invoke(CallTarget0(DisableForward))
        self.btnBackward.Invoke(CallTarget0(DisableBackward))
        self.btnStopMotor.Invoke(CallTarget0(DisableStopMotor))
        self.btnDisconnect.Invoke(CallTarget0(DisableDisconnect))
        




# Supporting Functions Start Here



# Update mtbOutput
def funUpdateOutput(strTemp1):
    global form
    form.mtbOutput.Text = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ": " + strTemp1 + "\r\n" + form.mtbOutput.Text
    


# This function start socket server
def StartServerSocket():
    global sock, connection, gstrTemp, gstrSend, gbolHeartBeat, gintTotalCommand, gintLastCommand, glstCommand, gbolConnect

    global gtimLastHB

    #sock.bind(('169.254.132.182', 8070))
    sock.bind(('', 8070))

    # Allow only ONE client connection
    sock.listen(1)

    # Accept Connection Again if the previous connection is closed
    while True:
        # Accept from Client
        connection,address = sock.accept()
        connection.settimeout(3600)
        gbolConnect = True

        # Init Vars
        gintTotalCommand = 0
        gintLastCommand = 0
        glstCommand = []

        # To avoid the Socket Server stops at sock.recv (here we use blocking mode),
        # Here we start the sock.recv in another thread
        server_thread_receive = threading.Thread(target=StartServerReceive)
        server_thread_receive.daemon = True
        server_thread_receive.start()

        gtimLastHB = time()

        while gbolConnect:
            if time() - gtimLastHB > 10:
                # Here client may lose connection

                # Try to disconnect client if it is still there
                gstrSend = ":Disconnect"
                server_threadsend = threading.Thread(target=StartServerSend)
                server_threadsend.daemon = True
                server_threadsend.start()

                # Reset and accept another connection
                gbolHeartBeat = False
                gbolConnect = False
                form.funLogout()
                gstrTemp = "EV3 Brick Lose Connection"
                form.funUpdate()
            else:
                if gintLastCommand < gintTotalCommand:
                    gintLastCommand += 1
                    received = glstCommand[gintLastCommand-1]

                    if received == ":End":
                        # Stop HeartBeat
                        gbolHeartBeat = False
                        gbolConnect = False
                        form.funLogout()
                        gstrTemp = "EV3 Brick Logout"
                        form.funUpdate()
                    elif received == ":Login":
                        # Tell client Login OK
                        gstrSend = ":LoginOK"
                        server_threadsend = threading.Thread(target=StartServerSend)
                        server_threadsend.daemon = True
                        server_threadsend.start()
                    
                        # Enable all buttons
                        form.funLogin()
                        gstrTemp = "EV3 Brick Login"
                        form.funUpdate()

                        # Start Send HeartBeat to client
                        gbolHeartBeat = True
                        funHBStart()

                        # Record gtimLastHB
                        gtimLastHB = time()
                    else:
                        pass

            # This sleep(0.1) is VERY IMPORTANT
            # Without it, this loop will be running too fast
            # And may LOCK resources => Unexpected Behaviour    
            sleep(0.1)

        connection.close()



# *** BUG ***
# If connection.send is sent in the StartSocketServer thread, that thread stopped at connection.send, this is a BUG
# So, we start another thread to do the connection.send
# Which is this function!!!
def StartServerSend():
    global connection, gstrSend
    connection.sendall(gstrSend).encode()




# Function to receive data from Client, this function is to be started in another thread
def StartServerReceive():
    global gintTotalCommand, glstCommand, gtimLastHB, connection, gbolConnect, gstrTemp, gbolHeartBeat

    bolEnd = False

    while not bolEnd:
        try:
            # Receive Data From Client and store it inside the list glstCommand
            received = connection.recv(1024).decode()

            gstrTemp = "Message Received from EV3 Brick: " + received
            form.funUpdate()

            if received == ":HB:":
                # Got HeartBeat from client, reset gtimLastHB
                gtimLastHB = time()
            else:
                # Normal Receive
                gintTotalCommand += 1
                glstCommand.append(received)

                # If got logout from client, end this thread
                if received == ":End":
                    bolEnd = True
        except socket.timeout:
            # print 'time out'
            gstrTemp = "EV3 Connection Timeout"
            form.funUpdate()
            gbolHeartBeat = False
            bolEnd = True
            gbolConnect = False
            form.funLogout()




# Start HeartBeat
def funHBStart():
    thrHB = threading.Timer(2, funHeartBeat)
    thrHB.start()

def funHeartBeat():
    global gstrSend, gbolHeartBeat
    gstrSend = ":HB:"
    server_threadsend = threading.Thread(target=StartServerSend)
    server_threadsend.daemon = True
    server_threadsend.start()

    if gbolHeartBeat:
        funHBStart()



#Main Program starts here
Application.EnableVisualStyles()
Application.SetCompatibleTextRenderingDefault(False)

#Create the socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  

#Run the form
form = MyForm()
Application.Run(form)

