import code
import socket
import struct
import json

class telemetry:
    
    numParticipants = -1
    
    headerCodec = 'HBBBBQfIBB'
    headerSize = 24
    
    
    lapHistoryCodec = 'IHHHB'
    tyreStintCodec = 'BBB'
    sessionHistoryCodec = 'BBBBBBB' #11
    
    damageCodec = 'ffffBBBBBBBBBBBBBBBBBBBBBBBBBB' # 10
    
    
    lobbyCodec = 'BBB' + 'c' * 48 + 'BB'
    lobbyInfoCodec = 'B'  # 9
    
    classificationCodec = 'BBBBBBIdBBBBBBBBBBBBBBBBBBBBBBBBBBB'
    finalClassificationCodec = 'B'  # 8
    
    
    statusCodec = 'BBBBBfffHHBBHBBBbfBfffB' # 7
    

    telemetryCodec = 'HfffBbHBBHHHHHBBBBBBBBHffffBBBB'
    carTelemetryEndCodec = 'BBb' # 6
    

    setupCodec = 'BBBBffffBBBBBBBBffffBf' # 5
    
    
    participantDataCodec = 'BBBBBBB' + 'c' * 48 + 'B'
    participantsCodec = 'B'  # 4
    
    
    fastestLapCodec = 'Bf'
    retirementCodec = 'B'
    teammateInPitsCodec = 'B'
    raceWinnerCodec = 'B'
    penaltyCodec = 'BBBBBBB'
    speedTrapCodec = 'BfBBBf'
    startLightsCodec = 'B'
    driveThroughPenaltyServedCodec = 'B'
    stopGoPenaltyServedCodec = 'B'
    flashbackCodec = 'If'
    buttonsCodec = 'B'
    eventCodec = 'BBBB'  # 3 BfBBBBBBBBBBBfBBBfBBBIfI
    

    lapCodec = 'IIHHfffBBBBBBBBBBBBBBHHB'
    lapDataEndCodec = 'BB' # 2
    

    weatherForecastSampleCodec = 'BBBbbbbB'
    marshalZoneCodec = 'fb'#num defined in the packet
    sessionCodecAfterWeather = 'BBIIIBBBBBBBBBBBBBBIB'
    sessionCodecAfterMarshal = 'BBB'
    sessionCodec = 'BbbBHBbBHHBBBBBB'  # 1


    extraPlayercarCodec = 'ffffffffffffffffffffffffffffff'
    carMotionCodec = 'ffffffhhhhhhffffff' # 0



    headerData = ['packetFormat','gameMajorVersion','gameMinorVersion','packetVersion','packetID','sessionUID','sessionTime','frameIdentifier','playerCarIndex','secondaryPlayerCarIndex']

    carMotionData = ['worldPositionX', 'worldPositionY', 'worldPositionZ', 'worldVelocityX', 'worldVelocityY', 'worldVelocityZ',
     'worldForwardDirX', 'worldForwardDirY', 'worldForwardDirZ', 'worldRightDirX', 'worldRightDirY', 'worldRightDirZ',
     'gForceLateral', 'gForceLongitudinal', 'gForceVertical', 'yaw', 'pitch', 'roll']
    packetMotionData = ['carMotionData',
    'suspensionPosition',
    'suspensionVelocity',
    'suspensionAcceleration',
    'wheelSpeed',
    'wheelSlip',
    'localVelocityX','localVelocityY','localVelocityZ',
    'angularVelocityX','angularVelocityY','angularVelocityZ',
    'angularAccelerationX','angularAccelerationY','angularAccelerationZ',
    'frontWheelsAngle']

    marshalZoneData = ['zoneStart','zoneFlag']
    weatherForecastSampleData = ['sessionType','timeOffset','weather','trackTemperature','trackTemperatureChange','airTemperature','airTemperatureChange',
    'rainPercentage']
    packetSessionData = ['weather','trackTemperature','airTemperature','totalLaps','trackLength','sessionType','trackID','formula','sessionTimeLeft','sessionDuration','pitSpeedLimit',
    'gamePaused','isSpectating','spectatorCarIndex','sliProNativeSupport','numMarshalZones','marshalZones','safetyCarStatus','networkGame','numWeatherForecastSamples',
    'weatherForecastSamples','forecastAccuracy','aiDifficulty','seasonLinkIdentifier','weekendLinkIdentifier','pitStopWindowIdealLap','pitStopLatestLap',
    'pitStopRejoinPosition','steeringAssist','brakingAssist','gearboxAssist','pitAssist','pitReleaseAssist','ersAssist','drsAssist','dynamicRacingLine','dynamicRacingLineType','gameMode','ruleSet','timeOfDay','sessionLength']

    lapData = ['lastLapTimeInMS','currentLapTimeInMS','sector1TimeInMS','sector2TimeInMS','lapDistance','totalDistance',
    'safetyCarDelta','carPosition','currentLapNum','pitStatus','numPitStops','sector','currentLapInvalid','penalties','warnings','numUnservedDriveThroughPenalties',
    'numUnservedStopGoPenalties','girdPosition','driverStatus','resultStatus','pitLaneTimerActive','pitLaneTimeInLaneInMS','pitStopTimerInMS','pitStopShouldServePenalties']
    packetLapData = ['lapData','timeTrialPBCarIndex','timeTrialRivalCarIndex']

    fastestLapData = ['vehicleIndex','lapTime']
    retirementData = ['vehicleIndex']
    teammateInPitsData = ['vehicleIndex']
    raceWinnerData = ['vehicleIndex']
    penalty = ['penaltyType','infringementType','vehicleIndex','otherVehicleIndex','time','lapNum','placesgained']
    speedTrapData = ['vehicleIndex','speed','isOverallFastestInSession','isDriverFastestInSession','fastestVehicleIndexInSession','fastestSpeedInSession']
    startLightsData = ['numLights']
    driveThroughPenaltyServedData = ['vehicleIndex']
    stopGoPenaltyServedData = ['vehicleIndex']
    flashbackData = ['flashbackFrameIdentifier','flashbackSessionTime']
    buttons = ['buttonStatus']
    packetEventData = ['eventStringCode','eventDetails']

    participantData = ['aiControlled','driverID','networkID','teamID','myTeam','raceNumber','nationality','name','yourTelemetry']
    packetParticipantData = ['numActiveCars','participants']

    carSetupData =     ['frontWing', 'rearWing', 'onThrottle', 'offThrottle', 'frontCamber', 'rearCamber', 'frontToe', 'rearToe',
     'frontSuspension', 'rearSuspension', 'frontAntiRollBar', 'rearAntiRollBar', 'frontSuspensionHeight',
     'rearSuspensionHeight', 'brakePressure', 'brakeBias', 'rearLeftTyrePressure', 'rearRightTyrePressure',
     'frontLeftTyrePressure', 'frontRightTyrePressure', 'ballast', 'fuelLoad']
    packetCarSetupData = ['carSetups']

    carTelemetryData = ['speed', 'throttle', 'steer', 'brake', 'clutch', 'gear', 'engineRPM', 'drs', 'revLightsPercent',
    'revLightsBitValue','brakesTemperature', 'tyresSurfaceTemperature', 'tyresInnerTemperature', 'engineTemperature', 'tyresPressure',
    'surfaceType']
    packetCarTelemetryData = ['carTelemetryData','mfdPanelIndex','mfdPanelIndexSecondaryPlayer','suggestedGear']

    carStatusData = ['tractionControl', 'antiLockBrakes', 'fuelMix', 'frontBrakeBias', 'pitLimiterStatus', 'fuelInTank',
     'fuelCapacaity', 'fuelRemainingLaps', 'maxRPM', 'idleRPM', 'maxGears', 'drsAllowed', 'drsAvtivationDistance',
     'tyresWear', 'actualTyreCompound', 'visualTyreCompound', 'tyresAgeLaps', 'vehicleFiaFlags', 'ersStoreEnergy', 'ersDeployMode',
     'ersHarvestedThisLapMGUK', 'ersHarvestedThisLapMGUH', 'ersDeployedThisLap', 'networkPaused']
    packetCarStatusData = ['carStatusData']
    
    finalClassificationData = ['position', 'numLaps', 'gridPosition', 'points', 'numPitStops', 'resultStatus', 'bestLapTimeInMS', 'totalRaceTime',
     'penaltiesTime', 'numPenalties', 'numTyreStints', 'tyreStintsActual', 'tyreStintsVisual', 'tyreStintsEndLaps']
    packetFinalClassificationData = ['numCars','classificationData']

    lobbyInfoData = ['aiControlled', 'teamId', 'nationality', 'name', 'readyStatus']
    packetLobbyInfoData = ['numPlayers','lobbyPlayers']

    carDamageData = ['tyresWear','tyresDamage','brakesDamage','frontLeftWingDamage','frontRightWingDamage','rearWingDamage','floorDamage','diffuserDamage','sidepodDamage','drsFault','ersFault','gearBoxDamage','engineDamage','engineMGUHWear','engineESWear','engineCEWear','engineICEWear','engineMGUKWear','engineTCWear','engineBlown','engineSeized']
    packetCarDamageData = ['carDamageData']

    lapHistoryData = ['lapTimeInMS','sector1TimeInMS','sector2TimeInMS','sector4TimeInMS','lapValidBitFlags']
    tyreStintHistoryData = ['endLap','tyreActualCompound','tyreVisualCompound']
    packetSessionHistoryData = ['carIndex','numLaps','numTyreStints','bestLapTimeLapNum','bestSector1LapNum','bestSector2LapNum','bestSector3LapNum','lapHistoryData','tyreStintsHistoryData']
    
    packetNames = ['Motion',
    'Session',
    'Lap data',
    'Event',
    'Participants',
    'Car setups',
    'Car Telemetry',
    'Car status',
    'Final classification',
    'Lobby info',
    'Car Damage',
    'Session History']

    def __init__(self,host,port):
        self.host = host
        self.port = port

        self.sock = socket.socket(socket.AF_INET,  # Internet
                            socket.SOCK_DGRAM)  # UDP
        self.sock.bind((self.host, self.port))


    def unpack(self, codec, data):
        codec = '<' + codec
        return struct.unpack(codec, data[:struct.calcsize(codec)])

    def unpackEvent(self, eventCode, data, packetID):
        match eventCode:
            case 'SSTA':
                return 'Session Started'
            case 'SEND':
                return 'Session Ended'
            case 'FTLP':
                unpacked = self.unpack(self.fastestLapCodec,data)
                res = list(unpacked)
                res.insert(0,eventCode)
                return self.json(self.fastestLapData,res,packetID)
            case 'RTMT':
                unpacked = self.unpack(self.retirementCodec,data)
                res = list(unpacked)
                res.insert(0, eventCode)
                return self.json(self.retirementData, res, packetID)
            case 'DRSE':
                return 'DRS Enabled'
            case 'DRSD':
                return 'DRS Disabled'
            case 'TMPT':
                unpacked = self.unpack(self.teammateInPitsCodec,data)
                res = list(unpacked)
                res.insert(0, eventCode)
                return self.json(self.teammateInPitsData, res, packetID)
            case 'CHQF':
                return 'Chequered Flag'
            case 'RCWN':
                unpacked = self.unpack(self.raceWinnerCodec,data)
                res = list(unpacked)
                res.insert(0, eventCode)
                return self.json(self.raceWinnerData, res, packetID)
            case 'PENA':
                unpacked = self.unpack(self.penaltyCodec,data)
                res = list(unpacked)
                res.insert(0, eventCode)
                return self.json(self.penalty, res, packetID)
            case 'SPTP':
                unpacked = self.unpack(self.speedTrapCodec,data)
                res = list(unpacked)
                res.insert(0, eventCode)
                return self.json(self.speedTrapData, res, packetID)
            case 'STLG':
                unpacked = self.unpack(self.startLightsCodec,data)
                res = list(unpacked)
                res.insert(0, eventCode)
                return self.json(self.startLightsData, res, packetID)
            case 'LGOT':
                return 'Lights out and away we go!'
            case 'DTSV':
                unpacked = self.unpack(self.driveThroughPenaltyServedCodec,data)
                res = list(unpacked)
                res.insert(0, eventCode)
                return self.json(self.driveThroughPenaltyServedData, res, packetID)
            case 'SGSV':
                unpacked = self.unpack(self.stopGoPenaltyServedCodec,data)
                res = list(unpacked)
                res.insert(0, eventCode)
                return self.json(self.stopGoPenaltyServedData, res, packetID)
            case 'FLBK':
                unpacked = self.unpack(self.flashbackCodec,data)
                res = list(unpacked)
                res.insert(0, eventCode)
                return self.json(self.flashbackData, res, packetID)
            case 'BUTN':
                unpacked = self.unpack(self.buttonsCodec,data)
                res = list(unpacked)
                res.insert(0,eventCode)
                return self.json(self.buttons,unpacked, packetID)
            case _:
                print('unknown event code')
                

    def decodePacket(self, data):
        self.header = struct.unpack('<' + self.headerCodec, data[:self.headerSize])
        self.header_dict = dict(list(zip(self.headerData,self.header)))
        self.playerCarIndex = self.header[8]
        self.secondPlayerCarIndex = self.header[9]
        packetID = self.header[4]
        data = data[self.headerSize:]
        match packetID:
            case 0: #motion ✓
                codec = self.carMotionCodec*22 + self.extraPlayercarCodec
                # if self.secondPlayerCarIndex != 255: codec += self.extraPlayercarCodec
                unpacked = self.unpack(codec,data)

                res = [self.createArray(self.carMotionCodec,unpacked,self.carMotionData,self.numParticipants)]
                for i in range(5):
                    res.append(unpacked[:4])
                    unpacked = unpacked[4:]
                res.extend(unpacked)
                return self.json(self.packetMotionData,res,packetID)
            case 1: #session
                sessionData = self.unpack(self.sessionCodec,data)
                numMarshalZones = sessionData[len(sessionData) - 1]
                codec = self.sessionCodec + self.marshalZoneCodec * numMarshalZones + self.sessionCodecAfterMarshal
                sessionData = self.unpack(codec, data)
                numWeatherForecastSamples = sessionData[len(sessionData) - 1]
                codec += self.weatherForecastSampleCodec * numWeatherForecastSamples + self.sessionCodecAfterWeather
                unpacked = self.unpack(codec,data)
                res = list(unpacked[:16])
                unpacked = unpacked[16:]
                res.append(self.createArray(self.marshalZoneCodec,unpacked,self.marshalZoneData,numMarshalZones))
                res.extend(unpacked[:3])
                res.append(self.createArray(self.weatherForecastSampleCodec,unpacked,self.weatherForecastSampleData,numWeatherForecastSamples))
                res.extend(unpacked)
                return self.json(self.packetSessionData,res,packetID)
            case 2: #lap data ✓
                codec = self.lapCodec * self.numParticipants + self.lapDataEndCodec
                unpacked = self.unpack(codec,data)
                res = [self.createArray(self.lapCodec, unpacked, self.lapData, self.numParticipants)]
                res.extend(unpacked)
                return self.json(self.packetLapData,res,packetID)
            case 3: #Event ✓
                eventCode = ''.join(list(map(lambda i: chr(i),self.unpack(self.eventCodec,data))))
                return self.unpackEvent(eventCode, data[4:], packetID)
            case 4: #participants ✓
                self.numParticipants = self.unpack(self.participantsCodec,data)[0]
                codec = self.participantsCodec + self.participantDataCodec * self.numParticipants
                unpacked = self.unpack(codec, data)
                res = list(unpacked[:1])
                unpacked = unpacked[1:]
                res.append(self.createArray(self.participantsCodec,unpacked,self.participantData,self.numParticipants))
                return self.json(self.packetParticipantData,res,packetID)
            case 5: #setups ✓
                codec = self.setupCodec * self.numParticipants
                unpacked = self.unpack(codec,data)
                return self.json(self.packetCarSetupData,self.createArray(self.setupCodec,unpacked,self.carSetupData,self.numParticipants),packetID)
            case 6: #telemetry ✓
                codec = self.telemetryCodec * self.numParticipants + self.carTelemetryEndCodec
                unpacked = self.unpack(codec,data)
                res = [self.createArray(self.telemetryCodec,unpacked,self.carTelemetryData,self.numParticipants)]
                res.extend(unpacked[:3])
                # print(self.json(self.packetCarTelemetryData,res,packetID))
                return self.json(self.packetCarTelemetryData,res,packetID)
            case 7: #status ✓
                unpacked = self.unpack(self.statusCodec * self.numParticipants,data)
                return self.json(self.packetCarStatusData,
                                 self.createArray(self.statusCodec, unpacked, self.carStatusData,
                                                  self.numParticipants), packetID)
            case 8: #final classification
                codec = self.finalClassificationCodec + self.classificationCodec * self.numParticipants
                unpacked = self.unpack(codec,data)
                res = list(unpacked[:1])
                unpacked = unpacked[1:]
                res.append(self.createArray(self.classificationCodec,unpacked,self.finalClassificationData,self.numParticipants))
                return self.json(self.packetFinalClassificationData,res, packetID)
            case 9: #lobby
                codec = self.lobbyInfoCodec + self.lobbyCodec * self.numParticipants
                unpacked = self.unpack(codec,data)
                res = list(unpacked[:1])
                unpacked = unpacked[1:]
                res.append(self.createArray(self.lobbyCodec,unpacked,self.lobbyInfoData,self.numParticipants))
                return self.json(self.packetLobbyInfoData, res, packetID)
            case 10: #damage ✓
                unpacked = self.unpack(self.damageCodec * self.numParticipants,data)
                return self.json(self.packetCarDamageData,
                                 self.createArray(self.damageCodec, unpacked, self.carDamageData,
                                                  self.numParticipants), packetID)
            case 11: #session history ✓
                temp = self.unpack(self.sessionHistoryCodec,data)
                numLaps = temp[1]
                numTyrestints = temp[2]
                unpacked = self.unpack(self.sessionHistoryCodec + self.lapHistoryCodec * numLaps + self.tyreStintCodec * numTyrestints,data)
                res = list(unpacked[:7])
                unpacked = unpacked[7:]
                res.append(self.createArray(self.lapHistoryCodec,unpacked,self.lapHistoryData,numLaps))
                res.append(self.createArray(self.tyreStintCodec,unpacked,self.tyreStintHistoryData,numTyrestints))
                return self.json(self.packetSessionHistoryData,res,packetID)
            case _:
                print('unknown packet id')

    def json(self,data,res, packetID):
        res_dict = dict(list(zip(data, res)))
        res_dict.update({"packetType": self.packetNames[packetID]})
        res_dict.update({"header":self.header_dict})
        return json.dumps(res_dict)

    def createArray(self, codec, unpacked, data, num):
        temp = []
        for i in range(num):
            temp.append(dict(list(zip(data,list(unpacked[i*len(codec):(i+1)*len(codec)])))))
        unpacked = unpacked[num*len(codec):]
        return temp

    def listen(self):
        # res = self.zipPacket(self.decodePacket(data, packetID),packetID)
        # res_dict = dict(res)
        # res_dict.update({"packetType":self.packetNames[packetInd]})
        # res_json = json.dumps(res_dict)
        data = self.sock.recvfrom(2048)[0]
        return self.decodePacket(data)
            
if __name__ == "__main__":
    tel = telemetry("127.0.0.1",20777)
    while True:
        tel.listen()
