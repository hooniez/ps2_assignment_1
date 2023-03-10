from room import Room
import random

class Floor: #new class for floors
    def __init__(self,prop, floorColor): 
        self.prop = prop #the property that the house exists on
        self.rooms = [] #list of all the room locations in the house
        self.roomOrder = [] #order that rooms are place in the house
        #to imagine grid layout as array indexs
        ################ +
        #   2 | 5 | 8
        # x 1 | 4 | 7
        #   0 | 3 | 6
        #       z  -> +
        ################
        self.floorColor = floorColor

    def createEmptyFloor(self,propertyEdge,belowFloor,floorLevel,floorHeight,roomsizeX,roomsizeZ):
        self.floorLevel = floorLevel
        self.belowFloor = belowFloor
        self.aboveFloor = None
        self.floorHeight = floorHeight
        self.roomsperx = (self.prop.width_x - propertyEdge*2)//roomsizeX #calculates the number of rooms that will be created along the X direction
        self.roomsperz = (self.prop.width_z - propertyEdge*2)//roomsizeZ #calculates the number of rooms that will be created along the Z direction
        roomsizewidth = roomsizeX
        roomsizedepth = roomsizeZ
        count = 0
        for z in range(0,self.roomsperz): #following initalised empty rooms in an array. The rooms can later be filled with different types by calling functions in room class
            for x in range(0,self.roomsperx):
                newSpace = Room(
                                self.prop.start_vector.x+(roomsizewidth*x)+propertyEdge,
                                (self.prop.start_vector.y + 1)+(floorHeight*floorLevel),
                                self.prop.start_vector.z+(roomsizedepth*z)+propertyEdge,
                                self.prop.start_vector.x+(roomsizewidth*(x+1))+propertyEdge,
                                (self.prop.start_vector.y + 1)+self.floorHeight+(floorHeight*floorLevel),
                                self.prop.start_vector.z+(roomsizedepth*(z+1))+propertyEdge,
                                count, #Position of room in array room.roomPos
                                x,z,
                                self.floorColor #floor Color
                                ) #coordinates in the grid
                self.rooms.append(newSpace) #Coordinates of location in grid
                count+=1

        self.setConnectedRooms(self.rooms) #new connected rooms setup
        if(self.belowFloor == None): #Base case, ground floor
            pass
        else:
            self.belowFloor.aboveFloor = self
    def addRoom(self,mc,roomtype='basic'):
        empty = True
        builtRooms = []
        avaliableRooms = []
        if len(self.roomOrder)>len(self.rooms):
            print('Already Max rooms at this level, room not added')
            return
        if (roomtype == 'pool' or roomtype == 'garden') and self.floorLevel != 0:
            print('Can only add pool to ground floor, room not added')
            return
        #first check if we are the ground Floor
        if self.belowFloor == None: #we are at the ground floor
            avaliableRooms = self.rooms #All rooms are avaliable
        else: #if there is a below floor, then we need to ask that floor for a list of builable locations
            for room in self.belowFloor.rooms:
                if room.buildUpAvaliablity == True: #A room can be built up from
                    avaliableRooms.append(self.rooms[room.roomPos]) #add to the avaliableRooms array
        if len(avaliableRooms) == 0: #No avaliable rooms
            print('No avaliable room positions at level:',self.floorLevel)
        else:
            for room in avaliableRooms: #search through all rooms
                if room.full == True: #if a room exists (anything that isn't air. Pool is a room Room is a room etc)
                    empty = False
                    builtRooms.append(room) #add the room to the builtrooms working array
            if empty:
                currentRoom = avaliableRooms[random.randint(0,len(avaliableRooms)-1)] #If there are not yet any rooms select a random room as the starting room.
                currentRoom.createRoom(mc,roomtype)
                self.roomOrder.append((currentRoom.roomPos,None))
            else:
                roomIndex = random.randint(0,len(builtRooms)-1)
                fromRoom = builtRooms[roomIndex] #Select a room at random from the built rooms
                builtRooms.pop(roomIndex) #Remove this room from the builtRooms array
                builable = self.checkAvailableRooms(fromRoom) #List of avaliable rooms
                while len(builable)==0: #while there are no avaliable room spaces select a new room to start search from
                    if(len(builtRooms)==0): #No more rooms to build From
                        print('No more room space avaliable')
                        return None
                    else:
                        roomIndex = random.randint(0,len(builtRooms)-1) #select another room at random
                        fromRoom = builtRooms[roomIndex]
                        builtRooms.pop(roomIndex)
                        builable = self.checkAvailableRooms(fromRoom) #List of avaliable rooms
                randNum = random.randint(0,len(builable)-1) #room select to create that connects to the current Room
                currentRoom = builable[randNum] #Select a room from avaliable Rooms at random
                currentRoom.createRoom(mc,roomtype)
                self.roomOrder.append((currentRoom.roomPos,fromRoom.roomPos))
            
    def addDoors(self, mc):
        doorTypes = ['fullwidthDoor','singleDoor'] #Add new door types here to insert them into random selector

        for index in range(len(self.roomOrder)): #the position of the first room in rooms list
            if(self.roomOrder[index][1]!=None): #if its not the first room
                self.rooms[self.roomOrder[index][0]].createDoor(mc,self.rooms[self.roomOrder[index][1]]) #create a door between this room
            else: #its the first room, send in None
                self.rooms[self.roomOrder[index][0]].createDoor(mc,None)



######################
    def addFrontDoor(self, mc, priority):
        # print('got a priority of',priority)
        #             #south-east final array element
        
        #             #north-east #highest x value

        #             #north-west first element in the array

        #             #south-west #highest z value
        markers = False #set True for location markers

        maxmin = -1
        minimum = (self.roomsperx-1)*(self.roomsperz-1)

        maxRoom = None
        total = -1
        direction = None
        for room in self.rooms:
            if markers == True: #Marks location of 0,0
                if room.gridCoord[0] == 0 and room.gridCoord[1] == 0:
                    mc.setBlocks(room.xstart,room.ystart,room.zstart,room.xstart+4,room.ystart+40,room.zstart+4,125,4)

            if(room.full == True):
                # print('house is slots self.rooms = ', len(self.rooms))
                # print('found a room full room priority was,',priority)
                if(priority == 'southEast'):
                    direction = 3
                    if room.roomType == 'pool' or room.roomType == 'garden':
                        continue
                    else:

                        #Choose largest x and largest y
                        x = room.gridCoord[0]
                        z = room.gridCoord[1]
                        total = x+z
                        if(total>maxmin):
                            # print('set new maxmin with array element',room.roomPos)
                            # print('arrayelement was :', room.roomPos)
                            maxmin = total
                            maxRoom = room

                if(priority == 'northEast'):
                    direction = 2
                    if room.roomType == 'pool' or room.roomType == 'garden':
                        continue
                    else:
                        #choose largest x and smallest z
                        x = room.gridCoord[0]
                        z = room.gridCoord[1]
                        if(x>maxmin):
                            # print('set new maxmin with array coords',room.gridCoord)
                            # print('arrayelement was :', room.roomPos)
                            maxmin = x
                            maxRoom = room

                if(priority == 'northWest'):
                    direction = 2
                    if room.roomType == 'pool' or room.roomType == 'garden':
                        continue
                    else:
                        x = room.gridCoord[0]
                        z = room.gridCoord[1]
                        total = x+z
                        if(total<=minimum): #speical case use minimum
                            # print('set new minimum with array element',room.roomPos)
                            # print('arrayelement was :', room.roomPos)
                            minimum = total
                            maxRoom = room

                if(priority == 'southWest'):
                    direction = 3
                    if room.roomType == 'pool' or room.roomType == 'garden':
                        continue
                    else:
                        x = room.gridCoord[0]
                        z = room.gridCoord[1]
                        if(z>maxmin):
                            # print('set new maxmin with array element',room.roomPos)
                            # print('arrayelement was :', room.roomPos)
                            maxmin = z
                            maxRoom = room

        if(direction == None or maxRoom == None):
            print('error drawing the front door direction was,',direction,'maxRoom was,',maxRoom)
        else:
            # print('maxRoom is at',maxRoom.gridCoord)
            # print('built in direction,',direction)
            if(markers == True): #Marks location of maxRoom
                mc.setBlocks(maxRoom.xstart,maxRoom.ystart,maxRoom.zstart,maxRoom.xstart+2,maxRoom.ystart+30,maxRoom.zstart+2,87)
            maxRoom.drawDoor(mc,direction,'frontDoor')
            print('------------')

    def addStairs(self,mc):
        if(self.belowFloor == None): #If we are at the ground level
            #don't build any stairs
            pass
        else: #We at a level 1->
            avaliableRooms = []
            for room in self.rooms:
                if room.full==True: #The room is full
                    avaliableRooms.append(room.roomPos) #add to list of avaliable Rooms
            randIndex = random.randint(0,len(avaliableRooms)-1) #select a random index from the avaliableRooms array
            currentRoom = self.rooms[avaliableRooms[randIndex]] #set the current room to the value at this index
            belowRoom = self.belowFloor.rooms[avaliableRooms[randIndex]]
            avaliableRooms.pop(randIndex) #remove this value from the avaliable Rooms
            avaliableSpace = currentRoom.findStairSpaceOnRoomWalls(belowRoom)
            while len(avaliableSpace) == 0: #while their is no avaliable space
                if(len(avaliableRooms) == 0): #check if their is any more possible rooms
                    return
                else:
                    randIndex = random.randint(0,len(avaliableRooms)-1) #select a random index from the avaliableRooms array
                    currentRoom = self.rooms[avaliableRooms[randIndex]] #set the current room to the value at this index
                    belowRoom = self.belowFloor.rooms[avaliableRooms[randIndex]]
                    avaliableRooms.pop(randIndex) #remove this value from the avaliable Rooms
                    avaliableSpace = currentRoom.findStairSpaceOnRoomWalls(belowRoom)
            else:
                randSpace = random.randint(0,len(avaliableSpace)-1) #select a space at random
                currentRoom.createStaircase(mc,belowRoom,avaliableSpace[randSpace])

    def addWindows(self,mc):
        for currentRoom in self.rooms: #Search through all the rooms
            if (currentRoom.full == True) and currentRoom.buildUpAvaliablity == True : #The room is filled
                for index, conRoom in enumerate(currentRoom.connectedRooms): #look at the connected rooms:
                    if conRoom != None: #If there is no room there potential window Location
                        if (conRoom.full == False) or (conRoom.roomType == 'pool') or (conRoom.roomType == 'garden'):
                            if(currentRoom.walls[index] == None) or (currentRoom.walls[index] == 'stairsUpper'):
                                currentRoom.createWindow(mc,index)
                    else: # Its a None room, so on the edge.
                        if(currentRoom.walls[index] == None) or (currentRoom.walls[index] == 'stairsUpper'):
                            currentRoom.createWindow(mc,index)

    def addRoof(self,mc):
        infoArrays = ([0,0,0,0],[0,0,0,0])
        for currentRoom in self.rooms: #Search through all the rooms
            if (currentRoom.full == True) and currentRoom.buildUpAvaliablity == True: #The room is filled, and its a build up type (not a pool)
                #Look above
                above = self.aboveFloor
                if self.aboveFloor == None: #if there is no above floor
                    currentRoom.createRoof(mc,infoArrays[0],infoArrays[1]) #create a roof
                else:
                    if self.aboveFloor.rooms[currentRoom.roomPos].full == False: #There is a floor above, but nothing above this room
                        aboveRoom = self.aboveFloor.rooms[currentRoom.roomPos]
                        infoArrays = self.roofAdjustments(aboveRoom)
                        currentRoom.createRoof(mc,infoArrays[0],infoArrays[1])  
                    #build a roof over this floor.
                    
                #Look at the room index in the above room.
    def roofAdjustments(self,aboveRoom):
        adjustmentsArray = [0,0,0,0]
        overlapArray = [0,0,0,0]
        for index, connected in enumerate(aboveRoom.connectedRooms):
            if connected == None:
                pass
                #the room is on the edge do nothing
            else:
                if connected.full == True:
                    adjustmentsArray[index] = 1
                    if self.aboveFloor.rooms[connected.roomPos].full == False:
                        overlapArray[index] = 1
                    #its empty
        return adjustmentsArray,overlapArray

    #################
    def setConnectedRooms(self,roomArray):
        for emptyRoom in roomArray:
            arrayLocationX = emptyRoom.gridCoord[0]
            arrayLocationZ = emptyRoom.gridCoord[1]
            bot = True
            top = True
            left = True
            right = True
            if(arrayLocationX == 0): #On bot edge
                bot = False
            if(arrayLocationX == self.roomsperx-1): #On top edge
                top = False
            if(arrayLocationZ == 0): #On the left edge
                left = False
            if(arrayLocationZ == self.roomsperz-1): #On right edge
                right = False
            if(bot):
                emptyRoom.connectedRooms[0] = roomArray[emptyRoom.roomPos - 1]
            if(top):
                emptyRoom.connectedRooms[1] = roomArray[emptyRoom.roomPos + 1]
            if(left):
                emptyRoom.connectedRooms[2] = roomArray[emptyRoom.roomPos - self.roomsperx]
            if(right):
                emptyRoom.connectedRooms[3] = roomArray[emptyRoom.roomPos + self.roomsperx]

    def connectPools(self,mc):
        for room in self.rooms:
            if room.roomType == 'pool':
                room.createPoolConnections(mc)

    def fillGardens(self,mc):
        for room in self.rooms:
            if room.roomType == None: #Finally add gardens to all lower level emptys
                room.createGarden(mc)

    def checkAvailableRooms(self,currentRoom): #Used when adding a new floor. Makes sure that rooms are only built over a pre existing room (but not an unbuilable type e.g. pool)
        arrayLocationX = currentRoom.gridCoord[0]
        arrayLocationZ = currentRoom.gridCoord[1]
        availableRooms = []
        bot = True
        top = True
        left = True
        right = True
        if(arrayLocationX == 0): #On bot edge
            bot = False
        if(arrayLocationX == self.roomsperx-1): #On top edge
            top = False
        if(arrayLocationZ == 0): #On the left edge
            left = False
        if(arrayLocationZ == self.roomsperz-1): #On right edge
            right = False
        #Checking if rooms exist in other locations in array
        if bot: #Location is not on the left edge so can -1 from location
            if self.belowFloor==None: #If its the ground floor                
                if self.rooms[currentRoom.roomPos - 1].full == False:
                    availableRooms.append(self.rooms[currentRoom.roomPos - 1])
            elif self.belowFloor.rooms[currentRoom.roomPos - 1].buildUpAvaliablity == True: #if its not the ground floor, but it can be built on
                if self.rooms[currentRoom.roomPos - 1].full == False:
                    availableRooms.append(self.rooms[currentRoom.roomPos - 1])
        if top:
            if self.belowFloor==None: #If its the ground floor                
                if self.rooms[currentRoom.roomPos + 1].full == False:
                    availableRooms.append(self.rooms[currentRoom.roomPos + 1])
            elif self.belowFloor.rooms[currentRoom.roomPos + 1].buildUpAvaliablity == True: #if its not the ground floor, but it can be built on
                if self.rooms[currentRoom.roomPos + 1].full == False:
                    availableRooms.append(self.rooms[currentRoom.roomPos + 1])
        if left:
            if self.belowFloor==None: #If its the ground floor                
                if self.rooms[currentRoom.roomPos - self.roomsperx].full == False:
                    availableRooms.append(self.rooms[currentRoom.roomPos - self.roomsperx])
            elif self.belowFloor.rooms[currentRoom.roomPos - self.roomsperx].buildUpAvaliablity == True: #if its not the ground floor, but it can be built on
                if self.rooms[currentRoom.roomPos - self.roomsperx].full == False:
                    availableRooms.append(self.rooms[currentRoom.roomPos - self.roomsperx])
        if right:
            if self.belowFloor==None: #If its the ground floor                
                if self.rooms[currentRoom.roomPos + self.roomsperx].full == False:
                    availableRooms.append(self.rooms[currentRoom.roomPos + self.roomsperx])
            elif self.belowFloor.rooms[currentRoom.roomPos + self.roomsperx].buildUpAvaliablity == True: #if its not the ground floor, but it can be built on
                if self.rooms[currentRoom.roomPos + self.roomsperx].full == False:                    
                    availableRooms.append(self.rooms[currentRoom.roomPos + self.roomsperx])
        return availableRooms #list of avaliable indexs

    def addFurniture(self, mc):
        for room in self.rooms:
            if room.full:
                room.scanRoom(mc)

    def addFurnitureCal(self,mc):
        for room in self.rooms:
            if room.full:
                room.calsAddfurn(mc)
                