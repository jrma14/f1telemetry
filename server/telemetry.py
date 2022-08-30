import socket
import struct
import json

class telemetry:
    
    headerCodec = '<HBBBBQfIBB'
    headerSize = 24
    lobbyInfoCodec = '<BBBcB'  # 9
    finalClassificationCodec = '<BBBBBBfdBBBBB'  # 8
    carStatusCodec = '<BBBBBfffHHBBHBBBBBBBBBBBifBfff'  # 7
    carTelemetryCodec = '<HfffBbHBBHBBHfB'  # 6
    carSetupsCodec = '<BBBBffffBBBBBBBBffffBf'  # 5
    participantsCodec = ''  # 4
    eventCodec = ''  # 3
    lapDataCodec = '<ffHHfBHHHHBHBHBfffBBBBBBBBB'  # 2
    sessionCodec = ''  # 1
    motionCodec = '<ffffffhhhhhhffffff'  # 0

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

    # Packet ids
    # 0 Motion
    # 1 Session
    # 2 Lap data
    # 3 Event
    # 4 Participants
    # 5 Car setups
    # 6 Car Telemetry
    # 7 Car status
    # 8 Final classification
    # 9 Lobby info

    codecs = {
        0: (motionCodec, struct.calcsize(motionCodec)),
        1: (sessionCodec, struct.calcsize(sessionCodec)),
        2: (lapDataCodec, struct.calcsize(lapDataCodec)),
        3: (eventCodec, struct.calcsize(eventCodec)),
        4: (participantsCodec, struct.calcsize(participantsCodec)),
        5: (carSetupsCodec, struct.calcsize(carSetupsCodec)),
        6: (carTelemetryCodec, struct.calcsize(carTelemetryCodec)),
        7: (carStatusCodec, struct.calcsize(carStatusCodec)),
        8: (finalClassificationCodec, struct.calcsize(finalClassificationCodec)),
        9: (lobbyInfoCodec, struct.calcsize(lobbyInfoCodec)),
        10: ('', struct.calcsize('')),
        11: ('', struct.calcsize(''))
    }

    packetNames = ['Motion',
    'Session',
    'Lap data',
    'Event',
    'Participants',
    'Car setups',
    'Car Telemetry',
    'Car status',
    'Final classification',
    'Lobby info']

    def __init__(self,host,port):
        self.host = host
        self.port = port

        self.sock = socket.socket(socket.AF_INET,  # Internet
                            socket.SOCK_DGRAM)  # UDP
        self.sock.bind((self.host, self.port))


    def unpack(self, codecInd, data):
        unpacked = struct.unpack(self.codecs[codecInd][0], data[self.headerSize:(self.headerSize + self.codecs[codecInd][1])])
        zipped = list(zip(self.dataPacks[codecInd],list(unpacked)))
        # print(zipped)
        return zipped


    def listen(self):
        data, addr = self.sock.recvfrom(2048)
        header = struct.unpack(self.headerCodec, data[:self.headerSize])
        codecInd = header[4]
        # print(header[6])
        # if codecInd == 6:
        #     print("Telemetry")
        if codecInd < 10:
            # print(header)
            try:
                res = self.unpack(codecInd, data)
                res_dict = dict(res)
                res_dict.update({"packetType":self.packetNames[codecInd]})
                res_json = json.dumps(res_dict)
                # if(self.packetNames[codecInd] == 'Car Telemetry'):
                #     print(res_dict['throttle'])
                # print(res_json)
                # res_json.append(self.packetNames[codecInd])
                # print(res)
                # if len(res) > 0:
                return res_json
                # else:
                #     temp = {'packetType':'invalid'}
                #     return json.dumps(temp)
            except Exception as e:
                # unpacked = struct.unpack(self.codecs[codecInd][0], data[self.headerSize:(self.headerSize + self.codecs[codecInd][1])])
                # print(data)
                print(self.codecs[codecInd][1])
                print(e)
        else:
            return json.dumps('{packetType:invalid}')
