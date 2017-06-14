# EV3Dev-Python-Socket-Connection
Control EV3 Brick installed with EV3Dev remotely using Client Server Socket Connection

1. Introduction

1.1 The Socket Server is a Windows Form running in Visual Studio 2017 Community, written by Python with IronPython 2.7 (32 bit)

1.2 The Socket Client is running in your EV3 Brick installed with EV3Dev

1.3 There are some buttons in the Windows Form, such as Left, Right, Forward, Backward, Stop Motor, etc.

1.4 When you press those buttons in your PC, the EV3 screen will show what you have pressed, you can then change those codes to control the motors, which means that initially, you don't need to add any motors to your EV3 brick.

1.5 The connection can be done in 2 ways, 1: Connect your EV3 Brick to the PC using the USB Cable.  2: Connect your EV3 Brick to the internet, using your Mobile Phone network via Bluetooth, and connect your PC to the internet using WIFI or LAN, which means that your PC can control the EV3 Brick over Internet.



2. Steps to establish Client Server Socket Connection between your PC and your EV3 Brick using USB cable:

2.1 Install Visual Studio 2017 Community with Python support in your PC.

2.2 Create a new IronPython Windows Form project.

2.3 Copy the contents from EV3PythonSocketServer.py to your .py file inside the new project.

2.4 Run the project in Visual Studio and click the "Start Server" button.

2.5 Connect your EV3 Brick (installed with EV3Dev) to your PC using the USB Cable, wait until you see the ip address appears in your EV3Dev, it should be something like 169.254.xxx.xxx

2.6 Open a command prompt in your PC, type: ipconfig

2.7 Check your PC's ip address of the USB Cable, it should be 169.254.132.182 or 169.254.yyy.yyy

2.8 Download and Open EV3PythonSocketClient.py

2.9 Change the host ip address of your PC inside EV3PythonSocketClient.py, if and only if your PC ip address of the USB Cable is not 169.254.132.182

2.10 Use the software WinSCP, copy this updated EV3PythonSocketClient.py to your EV3 Brick, remember to set the file executable during the upload process.

2.11 Select the File Explorer inside your EV3 Brick, then select and run EV3PhthonSocketClient.py

2.12 After a few seconds, you should see in your PC Windows Form that the EV3 Brick is connected to your PC.

2.13 Now click the "Left" button in your PC Windows Form, you should see the EV3 Screen display "Left" immediately after your press the Left button in your PC.

2.14 Try other buttons in your PC.

2.15 Click "Disconnect" in your PC, the socket client will stop.


