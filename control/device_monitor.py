from pysnmp.hlapi import *
import sys, json

class managedDevice:
    def __init__(self, host, readString, writeString):
        self.host = host
        self.readString = readString
        self.writeString = writeString
    def memoryUsage(self):
        walkResult = {}
        for (errorIndication,
            errorStatus,
            errorIndex,
            varBinds) in nextCmd(SnmpEngine(),
                                CommunityData(self.readString),
                                UdpTransportTarget((self.host, 161)),
                                ContextData(),
                                ObjectType(ObjectIdentity('1.3.6.1.4.1.9.9.48.1.1.1')),
                                lookupMib=False,
                                lexicographicMode=False):

            if errorIndication:
                print(errorIndication, file=sys.stderr)
                break

            elif errorStatus:
                print('%s at %s' % (errorStatus.prettyPrint(),
                                    errorIndex and varBinds[int(errorIndex) - 1][0] or '?'), file=sys.stderr)
                break

            else:
                # print(varBinds)
                for varBind in varBinds:
                    a = '%s = %s' % varBind
                    walkResult[a.split(' = ')[0]] = a.split(' = ')[-1]
                    # for character in a.split('= ')[-1]:
                    # print(a)
        return walkResult


    def cpuUsage(self):
        walkResult = {}
        for (errorIndication,
            errorStatus,
            errorIndex,
            varBinds) in nextCmd(SnmpEngine(),
                                CommunityData(self.readString),
                                UdpTransportTarget((self.host, 161)),
                                ContextData(),
                                ObjectType(ObjectIdentity('1.3.6.1.4.1.9.9.109.1.1.1.1.6')),
                                lookupMib=False,
                                lexicographicMode=False):

            if errorIndication:
                print(errorIndication, file=sys.stderr)
                break

            elif errorStatus:
                print('%s at %s' % (errorStatus.prettyPrint(),
                                    errorIndex and varBinds[int(errorIndex) - 1][0] or '?'), file=sys.stderr)
                break

            else:
                # print(varBinds)
                for varBind in varBinds:
                    a = '%s = %s' % varBind
                    walkResult[a.split(' = ')[0]] = a.split(' = ')[-1]
                return walkResult


    def getHostName(self):
        walkResult = {}
        for (errorIndication,
             errorStatus,
             errorIndex,
             varBinds) in nextCmd(SnmpEngine(),
                                  CommunityData(self.readString),
                                  UdpTransportTarget((self.host, 161)),
                                  ContextData(),
                                  ObjectType(ObjectIdentity('1.3.6.1.4.1.9.2.1.3')),
                                  lookupMib=False,
                                  lexicographicMode=False):

            if errorIndication:
                print(errorIndication, file=sys.stderr)
                break

            elif errorStatus:
                print('%s at %s' % (errorStatus.prettyPrint(),
                                    errorIndex and varBinds[int(errorIndex) - 1][0] or '?'), file=sys.stderr)
                break

            else:
                # print(varBinds)
                for varBind in varBinds:
                    a = '%s = %s' % varBind
                    walkResult[a.split(' = ')[0]] = a.split(' = ')[-1]
                return walkResult


    def checkIpForwarding(self):
        walkResult = {}
        for (errorIndication,
             errorStatus,
             errorIndex,
             varBinds) in nextCmd(SnmpEngine(),
                                  CommunityData(self.readString),
                                  UdpTransportTarget((self.host, 161)),
                                  ContextData(),
                                  ObjectType(ObjectIdentity('1.3.6.1.2.1.4.1')),
                                  lookupMib=False,
                                  lexicographicMode=False):

            if errorIndication:
                print(errorIndication, file=sys.stderr)
                break

            elif errorStatus:
                print('%s at %s' % (errorStatus.prettyPrint(),
                                    errorIndex and varBinds[int(errorIndex) - 1][0] or '?'), file=sys.stderr)
                break

            else:
                # print(varBinds)
                for varBind in varBinds:
                    a = '%s = %s' % varBind
                    walkResult[a.split(' = ')[0]] = a.split(' = ')[-1]
                return walkResult