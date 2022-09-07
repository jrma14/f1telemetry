import code
import socket
import struct
import json

class telemetry:
    
    numParticipants = -1
    
    headerCodec = '<HBBBBQfIBB'
    headerSize = 24
    
    
    lapHistoryCodec = 'IHHHB'
    tyreStintCodec = 'BBB'
    sessionHistoryCodec = 'BBBBBBB' #11
    
    damageCodec = 'ffffBBBBBBBBBBBBBBBBBBBBBBBBBB'
    carDamageCodec = '<' # 10
    
    
    lobbyCodec = 'BBB' + 'c' * 48 + 'BB'
    lobbyInfoCodec = '<B'  # 9
    
    classificationCodec = 'BBBBBBIdBBBBBBBBBBBBBBBBBBBBBBBBBBB'
    finalClassificationCodec = '<B'  # 8
    
    
    statusCodec = 'BBBBBfffHHBBHBBBbfBfffB'
    carStatusCodec = '<'  # 7
    

    telemetryCodec = 'HfffBbHBBHHHHHBBBBBBBBHffffBBBB'
    carTelemetryEndCodec = 'BBb'
    carTelemetryCodec = '<'  # 6
    

    setupCodec = 'BBBBffffBBBBBBBBffffBf'
    carSetupsCodec = '<'  # 5
    
    
    participantDataCodec = 'BBBBBBB' + 'c' * 48 + 'B'
    participantsCodec = '<B'  # 4
    
    
    fastestLapCodec = '<Bf'
    retirementCodec = '<B'
    teammateInPitsCodec = '<B'
    raceWinnerCodec = '<B'
    penaltyCodec = '<BBBBBBB'
    speedTrapCodec = '<BfBBBf'
    startLightsCodec = '<B'
    driveThroughPenaltyServedCodec = '<B'
    stopGoPenaltyServedCodec = '<B'
    flashbackCodec = '<If'
    buttonsCodec = '<B'
    eventCodec = '<BBBB'  # 3 BfBBBBBBBBBBBfBBBfBBBIfI
    

    lapCodec = 'IIHHfffBBBBBBBBBBBBBBHHB'
    lapDataEndCodec = 'BB'
    lapDataCodec = '<'  # 2
    

    weatherForecastSampleCodec = 'BBBbbbbB'
    marshalZoneCodec = 'fb'#num defined in the packet
    sessionCodecAfterWeather = 'BBIIIBBBBBBBBBBBBBBIB'
    sessionCodecAfterMarshal = 'BBB'
    sessionCodec = '<BbbBHBbBHHBBBBBB'  # 1


    extraPlayercarCodec = 'ffffffffffffffffffffffffffffff'
    carMotionCodec = 'ffffffhhhhhhffffff' 
    motionCodec = '<'  # 0



    dataPacks = [
    ['worldPositionX', 'worldPositionY', 'worldPositionZ', 'worldVelocityX', 'worldVelocityY', 'worldVelocityZ',
     'worldForwardDirX', 'worldForwardDirY', 'worldForwardDirZ', 'worldRightDirX', 'worldRightDirY', 'worldRightDirZ',
     'gForceLateral', 'gForceLongitudinal', 'gForceVertical', 'yaw', 'pitch', 'roll'],
    [],
    ['lastLapTime', 'currentLapTime', 'sector1TimeInMS', 'sector2TimeInMS', 'bestLapTime', 'bestLapNum',
     'bestLapSector1TimeInMS', 'bestLapSector2TimeInMS', 'bestLapSector3TimeInMS', 'bestOverallSector1TimeInMS',
     'bestOverallSector1LapNum', 'bestOverallSector2TimeInMS', 'bestOverallSector2LapNum', 'bestOverallSector3TimeInMS',
     'bestOverallSector3LapNum', 'lapDistance', 'totalDistance', 'safetycarDelta', 'carPosition', 'currentLapNum',
     'pitStatus', 'sector', 'currentLapInvalid', 'penalties', 'gridPosition', 'driverStatus', 'resultStatus'],
    [],
    [],
    ['frontWing', 'rearWing', 'onThrottle', 'offThrottle', 'frontCamber', 'rearCamber', 'frontToe', 'rearToe',
     'frontSuspension', 'rearSuspension', 'frontAntiRollBar', 'rearAntiRollBar', 'frontSuspensionHeight',
     'rearSuspensionHeight', 'brakePressure', 'brakeBias', 'rearLeftTyrePressure', 'rearRightTyrePressure',
     'frontLeftTyrePressure', 'frontRightTyrePressure', 'ballast', 'fuelLoad'],
    ['speed', 'throttle', 'steer', 'brake', 'clutch', 'gear', 'engineRPM', 'drs', 'revLightsPercent',
     'brakesTemperature', 'tyresSurfaceTemperature', 'tyresInnerTemperature', 'engineTemperature', 'tyresPressure',
     'surfaceType'],
    ['tractionControl', 'antiLockBrakes', 'fuelMix', 'frontBrakeBias', 'pitLimiterStatus', 'fuelInTank',
     'fuelCapacaity', 'fuelRemainingLaps', 'maxRPM', 'idleRPM', 'maxGears', 'drsAllowed', 'drsAvtivationDistance',
     'tyresWear', 'actualTyreCompound', 'visualTyreCompound', 'tyresAgeLaps', 'tyresDamage', 'frontLeftWingDamage',
     'frontRightWingDamage', 'rearWingDamage', 'drsFault', 'engineDamage', 'gearBoxDamage', 'vehicleFiaFlags',
     'ersStoreEnergy', 'ersDeployMode', 'ersHarvestedThisLapMGUK', 'ersHarvestedThisLapMGUH', 'ersDeployedThisLap'],
    ['position', 'numLaps', 'gridPosition', 'points', 'numPitStops', 'resultStatus', 'bestLapTime', 'totalRaceTime',
     'penaltiesTime', 'numPenalties', 'numTyreStints', 'tyreStintsActual', 'tyreStintsVisual'],
    ['aiControlled', 'teamId', 'nationality', 'name', 'readyStatus']]

    
    
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
        return struct.unpack(codec, data[self.headerSize:self.headerSize + struct.calcsize(codec)])

    def unpackEvent(self, eventCode, data):
        match eventCode:
            case 'SSTA':
                return 'Session Started'
            case 'SEND':
                return 'Session Ended'
            case 'FTLP':
                return self.unpack(self.fastestLapCodec,data)
            case 'RTMT':
                return self.unpack(self.retirementCodec,data)
            case 'DRSE':
                return 'DRS Enabled'
            case 'DRSD':
                return 'DRS Disabled'
            case 'TMPT':
                return self.unpack(self.teammateInPitsCodec,data)
            case 'CHQF':
                return 'Chequered Flag'
            case 'RCWN':
                return self.unpack(self.raceWinnerCodec,data)
            case 'PENA':
                return self.unpack(self.penaltyCodec,data)
            case 'SPTP':
                return self.unpack(self.speedTrapCodec,data)
            case 'STLG':
                return self.unpack(self.startLightsCodec,data)
            case 'LGOT':
                return 'Lights out and away we go!'
            case 'DTSV':
                return self.unpack(self.driveThroughPenaltyServedCodec,data)
            case 'SGSV':
                return self.unpack(self.stopGoPenaltyServedCodec,data)
            case 'FLBK':
                return self.unpack(self.flashbackCodec,data)
            case 'BUTN':
                return self.unpack(self.buttonsCodec,data)
            case _:
                print('unknown event code')
                

    def decodePacket(self, data, packetID):
        match packetID:
            case 0: #motion
                codec = self.motionCodec + ((self.carMotionCodec)*self.numParticipants)
                if self.secondPlayerCarIndex != 255: codec += self.extraPlayercarCodec
                return self.unpack(codec,data)
            case 1: #session
                sessionData = self.unpack(self.sessionCodec,data)
                numMarshalZones = sessionData[len(sessionData) - 1]
                codec = self.sessionCodec + (self.marshalZoneCodec) * numMarshalZones + self.sessionCodecAfterMarshal
                sessionData = self.unpack(codec, data)
                numWeatherForecastSamples = sessionData[len(sessionData) - 1]
                codec += (self.weatherForecastSampleCodec) * numWeatherForecastSamples + self.sessionCodecAfterWeather
                return self.unpack(codec,data)
            case 2: #lap data
                codec = self.lapDataCodec + (self.lapCodec) * self.numParticipants + self.lapDataEndCodec
                return self.unpack(codec,data)
            case 3: #Event
                eventCode = ''.join(list(map(lambda i: chr(i),struct.unpack(self.eventCodec,data))))
                return self.unpackEvent(eventCode, data[4:])
            case 4: #participants
                self.numParticipants = self.unpack(self.participantsCodec,data)
                codec = self.participantsCodec + (self.participantDataCodec) * self.numParticipants
                return self.unpack(codec, data)
            case 5: #setups
                codec = self.carSetupsCodec + (self.setupCodec) * self.numParticipants
                return self.unpack(codec,data)
            case 6: #telemetry
                codec = self.carTelemetryCodec + (self.telemetryCodec) * self.numParticipants + self.carTelemetryEndCodec
                return self.unpack(codec,data)
            case 7: #status
                return self.unpack(self.carSetupsCodec + self.statusCodec * self.numParticipants,data)
            case 8: #final classification
                codec = self.finalClassificationCodec + (self.classificationCodec) * self.numParticipants
                return self.unpack(codec,data)
            case 9: #lobby
                codec = self.lobbyInfoCodec + (self.lobbyCodec) * self.numParticipants
                return self.unpack(codec,data)
            case 10: #damage
                return self.unpack(self.carDamageCodec + self.damageCodec * self.numParticipants,data)
            case 11: #session history
                temp = self.unpack(self.sessionHistoryCodec,data)
                numLaps = temp[1]
                numTyrestints = temp[2]
                return self.unpack(self.sessionHistoryCodec + self.lapHistoryCodec * numLaps + self.tyreStintCodec * numTyrestints,data)
            case _:
                print('unknown packet id')

    def zipPacket(self, data, packetID):
        try:
            zipped = list(zip(self.dataPacks[packetID],list(data)))
            return zipped
        except:
            print('Could not zip, returning unpacked data')
            return data

    def listen(self):
        data = self.sock.recvfrom(2048)[0]
        header = struct.unpack(self.headerCodec, data[:self.headerSize])
        self.playerCarIndex = header[8]
        self.secondPlayerCarIndex = header[9]
        packetID = header[4]
        data = data[self.headerSize:]

        res = self.zipPacket(self.decodePacket(data, packetID),packetID)
        res_dict = dict(res)
        res_dict.update({"packetType":self.packetNames[codecInd]})
        res_json = json.dumps(res_dict)
        return res_json
            
if __name__ == "__main__":
    tel = telemetry("127.0.0.1",20777)
    while True:
        tel.test()
