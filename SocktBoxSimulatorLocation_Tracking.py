from bluepy.btle import Scanner, DefaultDelegate, BTLEException, Peripheral, UUID
import socket
import xml.etree.ElementTree as ET
import datetime
from threading import Thread
import threading
import math




        
        
 
class clTracker:
    def __init__(self, paName):
        self.meName = paName
        self.meRssiToBeacon = []
        
class clPoint:
    def __init__(self, x: float, y: float, z: float = 0.0):
        self.x = x
        self.y = y
        self.z = z

    def distance_to(self, other: 'Point') -> float:
        return math.sqrt((self.x - other.x)**2 + (self.y - other.y)**2 + (self.z - other.z)**2)        
       
class clBeacon:
    def __init__(self, paName, paPoint: clPoint):
        self.meName = paName
        self.mePoint = paPoint




#####################################
#Fill in the classname of the object#
#####################################
class clSocketBoxSimulator:
    #####################################
    #Constructor class (stay's this way)#
    #####################################
    def __init__(self):
            print ('clSocketBoxSimulator::__init__->start')
            self.commandID = ""
            self.timerSendFile = 0
            self.timerRecieveFile = 0
            self.timerRunFile = 0
            self.paused = 0
            self.error = ''
            self.TrackerIDs = []
            self.counter = 50
            
            #Set up the interface communication
            try:
                self.commandID = ""
                self.timerSendFile = 0
                self.timerRecieveFile = 0
                self.timerRunFile = 0
                self.error = ''
            except:
                traceback.print_exc()
    ####################################
    #Destructor class (stay's this way)#
    ####################################
    def __del__(self):
            print ('clSocketBoxSimulator::__del__->start')

    ###########
    #Functions#
    ###########
    def run_server(self):
        # create a socket object
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        server_ip = "192.168.1.231"
        port = 4001

        # bind the socket to a specific address and port
        server.bind((server_ip, port))
        #server.close()
        # listen for incoming connections
        server.listen(10)
        print('Listening on ' + server_ip + ':' + str(port))

        try:
            while True:
                client_socket, addr = server.accept()
                print('Accepted connection from ' + str(addr))
                client_handler = Thread(target=self.handle_client, args=(client_socket,))
                client_handler.start()
                
                #client_scanner = Thread(target=self.handle_scan_for_ble,args=())
                #client_scanner.start()
                # close server socket
        except: 
            server.close()
        
    def handle_client(self,client_socket):
        while True:
            try:
                message = client_socket.recv(1024).decode('utf-8')
                if not message:
                    print('Nothing received')
                else:    
                    #print('Received: ' + message)
                    ######################### parse the input #######################################
                    self.parseXML(message)
                    ######################### send the response #######################################
                    #W0R0D0P0C0T5648779879
                    #Waiting
                    #Running
                    #DataTransfer
                    #Pauzed
                    #Connected
                    #Timestamp
                    returnState = ""
                    
                    if self.timerRunFile > 0:
                        returnState = returnState + 'W0R1'
                    else:
                        returnState = returnState + 'W1R0'
                    if self.paused == 0:
                        returnState = returnState + 'P0'
                    else:
                        returnState = returnState + 'P1'
                    if self.timerSendFile == 0 and self.timerRecieveFile == 0:
                        returnState = returnState + 'D0'
                    else:
                        returnState = returnState + 'D1'
                    #Connected
                    returnState = returnState + 'C1'
                    loTimeStamp = datetime.datetime.now()
                    returnState = returnState + 'T' + loTimeStamp.strftime("%f")
                    
                    loObjects = ''
                    for i, loTracker in enumerate(self.TrackerIDs):
                        loObjects = loObjects + '<object name=\"' + str(loTracker[0]) + '\"><x value=\"' + str(loTracker[1]) + '\"/><y value=\"' + str(loTracker[2]) + '\"/><z value=\"' + str(loTracker[3]) + '\"/></object>'
                    #<object name=\"Magazijn_1001\"><x value=\"30.5\"/><y value=\"30.5\"/><z value=\"1.0\"/></object><object name=\"Employee_200\"><x value=\"60.5\"/><y value=\"50.5\"/><z value=\"0.5\"/></object>
                    returnString = ('<returnHardwareDevice><id>' + self.commandID + '</id><state>' + returnState + '</state><datas>' + loObjects + '</datas><error>' + self.error + '</error></returnHardwareDevice>')

                    #print('Response: ' + returnString)
                    #print('sendall start')
                    client_socket.sendall(returnString.encode('utf-8'))
                    #print('sendall not handeled')
            except:
                print('Exception')
                break
        client_socket.close()
        
    def parseXML(self,request):
        #print('START parseXML(requestXML)')
        loRoot = ET.fromstring(request)
        loSelectedChild = None
        loSelectedChildren = []
        for loChild in loRoot:
            #print(loChild.tag, loChild.attrib)
            if loChild.tag == 'id':
                self.commandID = loChild.text
                
            loPerform = loChild.get('do')
            if (loPerform == 'true'):
                loSelectedChild = loChild
                for loChildParams in loSelectedChild:
                    loSelectedChildren.append(loChildParams.text)
                break
        
        if loSelectedChild.tag == "connect":
            self.commandConnect(loSelectedChildren)
        elif loSelectedChild.tag == "disconnect":
            self.commandDisconnect(loSelectedChildren)
        elif loSelectedChild.tag == "state":
            self.commandState(loSelectedChildren)
        elif loSelectedChild.tag == "run":
            self.commandRun(loSelectedChildren)
        elif loSelectedChild.tag == "abort":
            self.commandAbort(loSelectedChildren)
        elif loSelectedChild.tag == "hold":
            self.commandHold(loSelectedChildren)
        elif loSelectedChild.tag == "continue":
            self.commandContinue(loSelectedChildren)
        elif loSelectedChild.tag == "sendFile":
            self.commandSendFile(loSelectedChildren)
        elif loSelectedChild.tag == "recieveFile":
            self.commandRecieveFile(loSelectedChildren)
        elif loSelectedChild.tag == "scriptCommand":
            self.commandScriptCommand(loSelectedChildren)
        elif loSelectedChild.tag == "optionalCommand":
            self.commandOptionalCommand(loSelectedChildren)
        #print('STOP parseXML(requestXML)')

    def commandConnect(self,paParams):
        print('START commandConnect(paParams')
        print('STOP commandConnect(paParams')
        
    def commandDisconnect(self,paParams):
        print('START commandDisconnect(paParams)')
        print('STOP commandDisconnect(paParams)')
        
    def commandState(self,paParams):
        #print('START commandState(paParams)')
        
        ##################################################
        #Moving of 2 objects into the field
        ##################################################
        self.counter = self.counter - 5
        if self.counter < 1:
            self.counter = 50
            
        #if self.counter >= 40:
        #    self.objectID = '<object name=\"Magazijn_1001\"><x value=\"70.5\"/><y value=\"70.5\"/><z value=\"1.0\"/></object><object name=\"Employee_200\"><x value=\"80.5\"/><y value=\"50.5\"/><z value=\"0.5\"/></object>'
        #elif self.counter >= 30:
        #    self.objectID = '<object name=\"Magazijn_1001\"><x value=\"60.5\"/><y value=\"60.5\"/><z value=\"1.0\"/></object><object name=\"Employee_200\"><x value=\"65.5\"/><y value=\"40.5\"/><z value=\"0.5\"/></object>'
        #elif self.counter >= 20:
        #    self.objectID = '<object name=\"Magazijn_1001\"><x value=\"40.5\"/><y value=\"40.5\"/><z value=\"1.0\"/></object><object name=\"Employee_200\"><x value=\"50.5\"/><y value=\"30.5\"/><z value=\"0.5\"/></object>'
        #elif self.counter >= 10:
        #    self.objectID = '<object name=\"Magazijn_1001\"><x value=\"30.5\"/><y value=\"30.5\"/><z value=\"1.0\"/></object><object name=\"Employee_200\"><x value=\"35.5\"/><y value=\"20.5\"/><z value=\"0.5\"/></object>'
        #elif self.counter >= 0:
        #    self.objectID = '<object name=\"Magazijn_1001\"><x value=\"15.5\"/><y value=\"15.5\"/><z value=\"1.0\"/></object><object name=\"Employee_200\"><x value=\"10.5\"/><y value=\"10.5\"/><z value=\"0.5\"/></object>'
        ##################################################
        
        if self.timerRecieveFile > 0:
            self.timerRecieveFile = self.timerRecieveFile - 1
        
        if self.timerRunFile > 0:
            self.timerRunFile = self.timerRunFile - 1
        
        if self.timerRunFile < 5:
            self.error = ''
        
        if self.timerSendFile > 0:
            self.timerSendFile = self.timerSendFile -1
        
        #print('STOP commandState(paParams)')
        
    def commandRun(self,paParams):
        print('START commandRun(paParams)')
        self.timerRunFile = 10
        self.error = 'approx 10 seconds running'
        print('STOP commandRun(paParams)')
        
    def commandAbort(self,paParams):
        print('START commandAbort(paParams)')
        print('STOP commandAbort(paParams)')
        
    def commandHold(self,paParams):
        print('START commandHold(paParams)')
        self.paused = 1
        print('STOP commandHold(paParams)')
        
    def commandContinue(self,paParams):
        print('START commandContinue(paParams)')
        self.paused = 0
        print('STOP commandContinue(paParams)')
        
    def commandSendFile(self,paParams):
        print('START commandSendFile(paParams)')
        self.timerSendFile = 10
        print('STOP commandSendFile(paParams)')
        
    def commandRecieveFile(self,paParams):
        print('START commandRecieveFile(paParams)')
        self.timerReceiveFile = 10
        print('STOP commandRecieveFile(paParams)')
        
    def commandScriptCommand(self,paParams):
        print('START commandScriptCommand(paParams)')
        print('STOP commandScriptCommand(paParams)')
        
    def commandOptionalCommand(self,paParams):
        print('START optionalCommand(paParams)')
        print('STOP optionalCommand(paParams)')
        
#####################################
#Fill in the classname of the object#
#####################################
class clSocketBoxBeaconServer:
    #####################################
    #Constructor class (stay's this way)#
    #####################################
    def __init__(self, paSocketBoxSimulator: clSocketBoxSimulator, paBeacons):
            print ('clSocketBoxBeaconServer::__init__->start')
            self.myMac = ""
            self.trackerX = []
            self.trackerY = []
            self.trackerZ = []
            self.meSocketBoxSimulator = paSocketBoxSimulator
            self.meBeacons = paBeacons
            self.meTrackers = []

    ####################################
    #Destructor class (stay's this way)#
    ####################################
    def __del__(self):
            print ('clSocketBoxBeaconServer::__del__->start')

    ###########
    #Functions#
    ###########
    def run_server(self):
        # create a socket object
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        server_ip = "192.168.1.231"
        port = 4000

        # bind the socket to a specific address and port
        server.bind((server_ip, port))
        #server.close()
        # listen for incoming connections
        server.listen(10)
        print('Listening on ' + server_ip + ':' + str(port))

        try:
            while True:
                client_socket, addr = server.accept()
                print('Accepted connection from ' + str(addr))
                client_handler = Thread(target=self.handle_client, args=(client_socket,))
                client_handler.start()
                
                #client_scanner = Thread(target=self.handle_scan_for_ble,args=())
                #client_scanner.start()
                # close server socket
        except: 
            server.close()
        
    def handle_client(self,client_socket):
        while True:
            try:
                message = client_socket.recv(1024).decode('utf-8')
                if not message:
                    print('Nothing received')
                else:    
                    #print('Received: ' + message)
                    ######################### parse the input #######################################
                    self.parseXML(message)
                    self.calculatePoints()
                    print ('Received from Beacon:' + message)
                    client_socket.close()
                    break
            except:
                print('Exception')
                break
        client_socket.close()
        

    def parseXML(self,xmlStringForObject):
        try:
            loName = ""
            loDistanceToObject = ""
            
            #Parse xml from the beacon
            xml_string = xmlStringForObject
            print(xml_string)
            root = ET.fromstring(xml_string)
            #<root><master>" + glDeviceName + "</master><devices>somedevice</devices></root>
            
            #Find beacon name
            for master in root.iter(tag='master'):
                
                
                loBeaconFound = False    
                for n, loBeacon in enumerate(self.meBeacons):
                    
                    if loBeacon.meName == master.text:
                        print ('Beacon found: ' +  master.text)    
                        loBeaconFound = True
                        
                        #Find tracker name
                        for device in root.iter(tag = 'device'):
                            for loTrackerToFind in device.iter(tag = 'name'):
                                
                                #Check Tracker already in list
                                loTrackerFound = False
                                for l, loTracker in enumerate(self.meTrackers):
                                    if loTracker.meName == loTrackerToFind.text:
                                        loTrackerFound = True
                                        
                                        #Update rssi value too
                                        for devRSSI in device.iter(tag = 'rssi'):
                                            loDistanceToObject = devRSSI.text
                                        
                                        #Check if beacon alredy in the tracker
                                        loBeaconInTrackerFound = False
                                        for m, loObjectBeaconInTrackerAndRssi in enumerate(loTracker.meRssiToBeacon):
                                            loObjectBeaconInTracker = loObjectBeaconInTrackerAndRssi[0]
                                            loObjectRssiInTracker = loObjectBeaconInTrackerAndRssi[1]
                                            if loObjectBeaconInTracker.meName == loBeacon.meName:
                                                loBeaconInTrackerFound = True
                                                loObjectBeaconInTrackerAndRssi[1] = loDistanceToObject
                                                
                                        #Beacon not in tracker list add    
                                        if not loBeaconInTrackerFound:
                                            loTracker.meRssiToBeacon.append([loBeacon,loDistanceToObject])   
                                            
                                          
                                #Tracker not in list so add to list    
                                if not loTrackerFound:
                                    #Add rssi value too
                                    for devRSSI in device.iter(tag = 'rssi'):
                                        loDistanceToObject = devRSSI.text
                                    loTrackerNew = clTracker(loTrackerToFind.text)
                                    loTrackerNew.meRssiToBeacon.append([loBeacon,loDistanceToObject])
                                    self.meTrackers.append(loTrackerNew)
                #For a specific master
                #Loop all tarcker devices and check if this master (beacon) has this tracker device
                for p, loTracker in enumerate(self.meTrackers):
                    loTrackerFoundToResetBeaconValue = True
                    for r, loBeaconToCheck in enumerate(loTracker.meRssiToBeacon):
                        #Beacon has the same name as in the list
                        if(loBeaconToCheck[0].meName == master):    
                            for device in root.iter(tag = 'device'):
                                for loTrackerToFind in device.iter(tag = 'name'):
                                    if (loTracker.meName == loTrackerToFind.text):
                                        loTrackerFoundToResetBeaconValue = False
                    if loTrackerFoundToResetBeaconValue:
                        for r, loBeaconToCheck in enumerate(loTracker.meRssiToBeacon):
                            #Beacon has the same name as in the list
                            if(loBeaconToCheck[0].meName == master):
                                loBeaconToCheck[1] = str(-1000)
                if not loBeaconFound:
                    print('Beacon not found in list error ....')
                                       
        except Exception as e:
            print("Error parseXML:", e)        
                 
    ##########################################################
    #Created for manual testing of the methods on the class  #
    ##########################################################
    def sortDesc(self, paTracker: clTracker):
        try:
            loTracker = paTracker
            for i, loBeaconAndRssi in enumerate(loTracker.meRssiToBeacon):
                j = i + 1
                while j < len(loTracker.meRssiToBeacon):
                    if (int(loTracker.meRssiToBeacon[i][1]) < int(loTracker.meRssiToBeacon[j][1])):
                            temp = loTracker.meRssiToBeacon[i]
                            loTracker.meRssiToBeacon[i] = loTracker.meRssiToBeacon[j]
                            loTracker.meRssiToBeacon[j] = temp
                    j = j + 1
                    
            return loTracker                
        except Exception as e:                
            print("clSocketBoxBeaconServer::sortDesc -> Error:", e)
            return None
            
    def calculatePoints(self):
        try:
            #Set the trackerIDs to zero
            self.meSocketBoxSimulator.TrackerIDs = []
            
            for p, listTracker in enumerate(self.meTrackers):
                loTracker = self.sortDesc(listTracker)
                #If there are more than one beacons to detect the tracker
                if len(loTracker.meRssiToBeacon) == 2:
                    if (int(loTracker.meRssiToBeacon[0][1]) != -1000) and (int(loTracker.meRssiToBeacon[1][1]) != -1000):
                        #Distance calculation
                        loFirstBeacon = loTracker.meRssiToBeacon[0][0]
                        loSecondBeacon = loTracker.meRssiToBeacon[1][0]
                        loFirstBeaconDistance = self.distanceCalculation(int(loTracker.meRssiToBeacon[0][1]))
                        loSecondBeaconDistance = self.distanceCalculation(int(loTracker.meRssiToBeacon[1][1]))
                        print ("The %s has distance %.2f" % (loFirstBeacon.meName,loFirstBeaconDistance))
                        print ("The %s has distance %.2f" % (loSecondBeacon.meName,loSecondBeaconDistance))
                        
                        #Base calculation
                        loBaseDistance = loFirstBeacon.mePoint.distance_to(loSecondBeacon.mePoint)
                        print("The base distance %.2f" % (loBaseDistance))
                        
                        #Level Distance 1 and 2
                        if (loFirstBeaconDistance + loSecondBeaconDistance) < loBaseDistance:
                            loTemp = loBaseDistance - (loFirstBeaconDistance + loSecondBeaconDistance)
                            #+1 to create a triangle
                            loFirstBeaconDistance = loFirstBeaconDistance + (loTemp/2) + 1
                            loSecondBeaconDistance = loSecondBeaconDistance + (loTemp/2) + 1
                            print("Leveled distance %s: %.2f" % (loFirstBeacon.meName,loFirstBeaconDistance))
                            print("Leveled distance %s: %.2f" % (loSecondBeacon.meName,loSecondBeaconDistance))
                        

                        #Calculate coord
                        result = self.coordCalc(abs(loBaseDistance),loFirstBeaconDistance,loSecondBeaconDistance,loFirstBeacon.mePoint,loSecondBeacon.mePoint,clPoint(170.0,-965.0,0.0))
                        if result:
                            print(f"Calculated location: {result}")
                            self.meSocketBoxSimulator.TrackerIDs.append([listTracker.meName,result[0],result[1],0.05])
                        else:
                            print(f"Result could not be caluclated ... ")
                        
                    else:
                        print ("The Tracker has id: %s with beaconID_1 %s values Rssi: %.2f beaconID_2 %s Rssi: %.2f" % (loTracker.meName,loTracker.meRssiToBeacon[0][0].meName, float(loTracker.meRssiToBeacon[0][1]), loTracker.meRssiToBeacon[1][0].meName, float(loTracker.meRssiToBeacon[1][1])))
                elif len(loTracker.meRssiToBeacon) > 2:
                    if (int(loTracker.meRssiToBeacon[0][1]) != -1000) and (int(loTracker.meRssiToBeacon[1][1]) != -1000):
                        #Distance calculation
                        loFirstBeacon = loTracker.meRssiToBeacon[0][0]
                        loSecondBeacon = loTracker.meRssiToBeacon[1][0]
                        loThirdBeacon = loTracker.meRssiToBeacon[2][0]
                        loFirstBeaconDistance = self.distanceCalculation(int(loTracker.meRssiToBeacon[0][1]))
                        loSecondBeaconDistance = self.distanceCalculation(int(loTracker.meRssiToBeacon[1][1]))
                        loThirdBeaconDistance = self.distanceCalculation(int(loTracker.meRssiToBeacon[2][1]))
                        print ("The %s has distance %.2f" % (loFirstBeacon.meName,loFirstBeaconDistance))
                        print ("The %s has distance %.2f" % (loSecondBeacon.meName,loSecondBeaconDistance))
                        print ("The %s has distance %.2f" % (loThirdBeacon.meName,loThirdBeaconDistance))
                        
                        #Base calculation
                        loBaseDistance = loFirstBeacon.mePoint.distance_to(loSecondBeacon.mePoint)
                        print("The base distance %.2f" % (loBaseDistance))
                        
                        #Level Distance 1 and 2
                        if (loFirstBeaconDistance + loSecondBeaconDistance) < loBaseDistance:
                            loTemp = loBaseDistance - (loFirstBeaconDistance + loSecondBeaconDistance)
                            #+1 to create a triangle
                            loFirstBeaconDistance = loFirstBeaconDistance + (loTemp/2) + 1
                            loSecondBeaconDistance = loSecondBeaconDistance + (loTemp/2) + 1
                            print("Leveled distance %s: %.2f" % (loFirstBeacon.meName,loFirstBeaconDistance))
                            print("Leveled distance %s: %.2f" % (loSecondBeacon.meName,loSecondBeaconDistance))

                        #Calculate coord
                        result = self.coordCalc(loBaseDistance,loFirstBeaconDistance,loSecondBeaconDistance,loFirstBeacon.mePoint,loSecondBeacon.mePoint,loThirdBeacon.mePoint)
                        if result:
                            print(f"Calculated location: {result}")
                            self.meSocketBoxSimulator.TrackerIDs.append([listTracker.meName,result[0],result[1],0.05])
                        else:
                            print(f"Result could not be caluclated ... ")
                        


                            
                    else:
                        print ("The Tracker has id: %s with beaconID_1 %s values Rssi: %.2f beaconID_2 %s Rssi: %.2f beaconID_3 %s values Rssi: %.2f" % (loTracker.meName,loTracker.meRssiToBeacon[0][0].meName, float(loTracker.meRssiToBeacon[0][1]), loTracker.meRssiToBeacon[1][0].meName, float(loTracker.meRssiToBeacon[1][1]), loTracker.meRssiToBeacon[2][0].meName, float(loTracker.meRssiToBeacon[2][1])))
                else:
                    print ("The Tracker has id: %s has not more than 1 detection Beacon" % (loTracker.meName))
            
            
        except Exception as e:
            print("Error calculatePoints:", e)

    def distanceCalculation(self,rssiValue) -> float:
        powerAtOneMeter = -49
         #3.2 to short
         #2.6 good
         
         
         #WROOM -49 and 2.3
         #Mini Esp32 -57 and 2
        scaleFactor = 2.5
        return (pow(10,((powerAtOneMeter-(rssiValue))/(10*scaleFactor))) * 100)

    def coordCalc (self,paDistanceBase,paDistance1,paDistance2, paPoint1: clPoint, paPoint2: clPoint, paPoint3: clPoint) -> list[float, float]:        
        try:
            #Calculate the area
            perimeter = paDistanceBase + paDistance1 + paDistance2
            s = perimeter/2
            area = math.sqrt(s*(s-paDistanceBase)*(s-paDistance1)*(s-paDistance2))
            #area = base * height/2
            height = (2*area)/paDistanceBase
            
            
            #Get point length on the Base
            #c²=x²+y² => c = sqrt(x²+y²)
            pointLenghtOnBase = 0
            if height <= paDistance1:
                pointLenghtOnBase = math.sqrt(pow(paDistance1,2) - pow(height,2))
            else:
                pointLenghtOnBase = math.sqrt(pow(height,2) - pow(paDistance1,2))
            print("The distance to the point is: %.2f and height is: %.2f" % (pointLenghtOnBase, height))
            
            
            cosAlfa = (paPoint1.x - paPoint2.x)/paDistanceBase
            radians = math.acos(cosAlfa)
            sinAlfa = math.sin(radians)
            degrees = radians * (180.0 / math.pi)
            print("The Angle of the base is: %.2f in radians is: %.2f" % (degrees, radians))
            pointLenghtOnBase_X = cosAlfa * pointLenghtOnBase
            pointLenghtOnBase_Y = sinAlfa * pointLenghtOnBase
            print("The pointLenghtOnBase_X: %.2f" % (pointLenghtOnBase_X))
            print("The pointLenghtOnBase_Y: %.2f" % (pointLenghtOnBase_Y))
            
            pointlenghtOnBase_OrigCoord_X = 0
            pointlenghtOnBase_OrigCoord_Y = 0
            #Quadtrant 3
            if (paPoint1.x > paPoint2.x) and (paPoint1.y > paPoint2.y) and (paPoint1.y < paPoint3.y):
                print ("Quadtrant 3 A")
                pointlenghtOnBase_OrigCoord_X = paPoint1.x - abs(pointLenghtOnBase_X)
                pointlenghtOnBase_OrigCoord_Y = paPoint1.y + abs(pointLenghtOnBase_Y)
            elif (paPoint1.x > paPoint2.x) and (paPoint1.y >= paPoint2.y) and (paPoint1.y > paPoint3.y):
                print ("Quadtrant 3 B")
                pointlenghtOnBase_OrigCoord_X = paPoint1.x - abs(pointLenghtOnBase_X)
                pointlenghtOnBase_OrigCoord_Y = paPoint1.y - abs(pointLenghtOnBase_Y)                
            #Quadtrant 1
            elif (paPoint1.x < paPoint2.x) and (paPoint1.y <= paPoint2.y) and (paPoint1.y < paPoint3.y):
                print ("Quadtrant 1 A")
                pointlenghtOnBase_OrigCoord_X = paPoint1.x + abs(pointLenghtOnBase_X)
                pointlenghtOnBase_OrigCoord_Y = paPoint1.y + abs(pointLenghtOnBase_Y)
            elif (paPoint1.x < paPoint2.x) and (paPoint1.y <= paPoint2.y) and (paPoint1.y > paPoint3.y):
                print ("Quadtrant 1 B")
                pointlenghtOnBase_OrigCoord_X = paPoint1.x + abs(pointLenghtOnBase_X)
                pointlenghtOnBase_OrigCoord_Y = paPoint1.y - abs(pointLenghtOnBase_Y)                
            #Quadtrant 2        
            elif (paPoint1.x >= paPoint2.x) and (paPoint1.y < paPoint2.y) and (paPoint1.x < paPoint3.x):
                print ("Quadtrant 2 A")
                pointlenghtOnBase_OrigCoord_X = paPoint1.x + abs(pointLenghtOnBase_X)
                pointlenghtOnBase_OrigCoord_Y = paPoint1.y + abs(pointLenghtOnBase_Y)
            elif (paPoint1.x >= paPoint2.x) and (paPoint1.y < paPoint2.y) and (paPoint1.x > paPoint3.x):
                print ("Quadtrant 2 B")                
                pointlenghtOnBase_OrigCoord_X = paPoint1.x - abs(pointLenghtOnBase_X)
                pointlenghtOnBase_OrigCoord_Y = paPoint1.y + abs(pointLenghtOnBase_Y)                
            #Quadtrant 4
            elif (paPoint1.x <= paPoint2.x) and (paPoint1.y > paPoint2.y) and (paPoint1.x < paPoint3.x):
                print ("Quadtrant 4 A")
                pointlenghtOnBase_OrigCoord_X = paPoint1.x + abs(pointLenghtOnBase_X)
                pointlenghtOnBase_OrigCoord_Y = paPoint1.y - abs(pointLenghtOnBase_Y)
            elif (paPoint1.x <= paPoint2.x) and (paPoint1.y > paPoint2.y) and (paPoint1.x > paPoint3.x):
                print ("Quadtrant 4 B")                
                pointlenghtOnBase_OrigCoord_X = paPoint1.x - abs(pointLenghtOnBase_X)
                pointlenghtOnBase_OrigCoord_Y = paPoint1.y - abs(pointLenghtOnBase_Y)                
            
            
            print("pointlenghtOnBase_OrigCoord_X = %.2f" %(pointlenghtOnBase_OrigCoord_X))
            print("pointlenghtOnBase_OrigCoord_Y = %.2f" %(pointlenghtOnBase_OrigCoord_Y))
            
            #Check the direction of the hight
            loLeftOrRight = ""
            loUpperOrLower = ""
            
            if (degrees == 0.0 or degrees == 360.0):
                if (pointlenghtOnBase_OrigCoord_Y <= paPoint3.y):
                    print ("Degrees 0 = LE")
                    loLeftOrRight = "LE"
                elif (pointlenghtOnBase_OrigCoord_Y >= paPoint3.y):
                    print ("Degrees 0 = RI")
                    loLeftOrRight = "RI"                
            elif (degrees == 90.0):
                if (pointlenghtOnBase_OrigCoord_X <= paPoint3.x):
                    print ("Degrees 90 = RI")
                    loLeftOrRight = "RI"
                elif (pointlenghtOnBase_OrigCoord_X >= paPoint3.x):
                    print ("Degrees 90 = LE")
                    loLeftOrRight = "LE"
            elif (degrees == 180.0):
                if (pointlenghtOnBase_OrigCoord_Y <= paPoint3.y):
                    print ("Degrees 180 = LE")
                    loLeftOrRight = "LE"
                elif (pointlenghtOnBase_OrigCoord_Y >= paPoint3.y):
                    print ("Degrees 180 = RI")
                    loLeftOrRight = "RI" 
            elif (degrees == 270.0):
                if (pointlenghtOnBase_OrigCoord_X <= paPoint3.x):
                    print ("Degrees 270 = LE")
                    loLeftOrRight = "LE"
                elif (pointlenghtOnBase_OrigCoord_X >= paPoint3.x):
                    print ("Degrees 270 = RI")
                    loLeftOrRight = "RI"                    
            elif (pointlenghtOnBase_OrigCoord_X <= paPoint3.x):
                print ("corner RI")
                loLeftOrRight = "RI"
            elif (pointlenghtOnBase_OrigCoord_X >= paPoint3.x):
                print ("corner LE")
                loLeftOrRight = "LE"
                
            pointOfLocation_X = 0.0
            pointOfLocation_Y = 0.0
            pointOfLocation_OrigCoord_X = 0.0
            pointOfLocation_OrigCoord_Y = 0.0
            
            #coord of the point pointLenghtOnBase
            #Select quadrant 3
            if (paPoint1.x > paPoint2.x) and (paPoint1.y >= paPoint2.y):
                    print("Entering quadrant 3")
                    #Triangle goes right
                    if loLeftOrRight == "RI":
                        pointOfLocation_Y = cosAlfa * height
                        pointOfLocation_X = sinAlfa * height
                        pointOfLocation_OrigCoord_X = pointlenghtOnBase_OrigCoord_X - abs(pointOfLocation_X)
                        pointOfLocation_OrigCoord_Y = pointlenghtOnBase_OrigCoord_Y - abs(pointOfLocation_Y)
                    #Triangle goes left    
                    elif loLeftOrRight == "LE":
                        pointOfLocation_Y = cosAlfa * height
                        pointOfLocation_X = sinAlfa * height
                        pointOfLocation_OrigCoord_X = pointlenghtOnBase_OrigCoord_X - abs(pointOfLocation_X)
                        pointOfLocation_OrigCoord_Y = pointlenghtOnBase_OrigCoord_Y + abs(pointOfLocation_Y) 
            #Select quadrant 1
            elif (paPoint1.x < paPoint2.x) and (paPoint1.y <= paPoint2.y):
                #degreesHelp = 180 - degrees
                #radiansHelp = degreesHelp * (math.pi / 180)
                #if ((degreesHelp >= 0) and (degreesHelp <= 90)):
                    print("Entering quadrant 1")
                    #Triangle goes right
                    if loLeftOrRight == "RI":
                        pointOfLocation_Y = cosAlfa * height
                        pointOfLocation_X = sinAlfa * height
                        pointOfLocation_OrigCoord_X = pointlenghtOnBase_OrigCoord_X + abs(pointOfLocation_X)
                        pointOfLocation_OrigCoord_Y = pointlenghtOnBase_OrigCoord_Y - abs(pointOfLocation_Y)
                    #Triangle goes left    
                    elif loLeftOrRight == "LE":
                        pointOfLocation_Y = cosAlfa * height
                        pointOfLocation_X = sinAlfa * height
                        pointOfLocation_OrigCoord_X = pointlenghtOnBase_OrigCoord_X + abs(pointOfLocation_X)
                        pointOfLocation_OrigCoord_Y = pointlenghtOnBase_OrigCoord_Y + abs(pointOfLocation_Y)             
            #Select quadrant 2            
            elif (paPoint1.x >= paPoint2.x) and (paPoint1.y < paPoint2.y):
                    print("Entering quadrant 2")
                    #Triangle goes right
                    if loLeftOrRight == "RI":
                        pointOfLocation_Y = cosAlfa * height
                        pointOfLocation_X = sinAlfa * height
                        pointOfLocation_OrigCoord_X = pointlenghtOnBase_OrigCoord_X + abs(pointOfLocation_X)
                        pointOfLocation_OrigCoord_Y = pointlenghtOnBase_OrigCoord_Y + abs(pointOfLocation_Y)
                    #Triangle goes left    
                    elif loLeftOrRight == "LE":
                        pointOfLocation_Y = cosAlfa * height
                        pointOfLocation_X = sinAlfa * height
                        pointOfLocation_OrigCoord_X = pointlenghtOnBase_OrigCoord_X - abs(pointOfLocation_X)
                        pointOfLocation_OrigCoord_Y = pointlenghtOnBase_OrigCoord_Y + abs(pointOfLocation_Y)
                       
            #Select quadrant 4        
            elif (paPoint1.x <= paPoint2.x) and (paPoint1.y > paPoint2.y):
                    print("Entering quadrant 4")
                    #Triangle goes right
                    if loLeftOrRight == "RI":
                        pointOfLocation_Y = cosAlfa * height
                        pointOfLocation_X = sinAlfa * height
                        pointOfLocation_OrigCoord_X = pointlenghtOnBase_OrigCoord_X + abs(pointOfLocation_X)
                        pointOfLocation_OrigCoord_Y = pointlenghtOnBase_OrigCoord_Y - abs(pointOfLocation_Y)
                    #Triangle goes left    
                    elif loLeftOrRight == "LE":
                        pointOfLocation_Y = cosAlfa * height
                        pointOfLocation_X = sinAlfa * height
                        pointOfLocation_OrigCoord_X = pointlenghtOnBase_OrigCoord_X - abs(pointOfLocation_X)
                        pointOfLocation_OrigCoord_Y = pointlenghtOnBase_OrigCoord_Y - abs(pointOfLocation_Y)
           
            return (pointOfLocation_OrigCoord_X,pointOfLocation_OrigCoord_Y)
        except Exception as e:
            print("Error coordCalc:", e)
            return None
           
def main():
    print('Start SocketBoxLocationBeacon')
    
    #Define the beacons with name and location
    loBeacons = []
    loBeacons.append(clBeacon("2UVBEACON_001_X",clPoint(170.0,-310.0,0.0)))
    loBeacons.append(clBeacon("2UVBEACON_001_Y",clPoint(895.0,-310.0,0.0)))
    loBeacons.append(clBeacon("2UVBEACON_001_Z",clPoint(170.0,-965.0,0.0)))
    
    
    #Create the socket communicator
    meSocketBoxSimulator = clSocketBoxSimulator()
    meSocketBoxBeaconServer = clSocketBoxBeaconServer(meSocketBoxSimulator, loBeacons)
    #Start the BLE threading
    x = threading.Thread(target=meSocketBoxBeaconServer.run_server, args=())
    x.start()

    #Test the function manually
    #while True:
    #    try:
    meSocketBoxSimulator.run_server()
    #    except:
    #        print('Exception') 
            

if __name__ == "__main__":
    main()
