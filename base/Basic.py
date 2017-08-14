import ConfigParser
import os

cf = ConfigParser.ConfigParser()
cf.read("./conf/config.ini")

class Basic:
    def getAtpHost(self):
        atpHost = cf.get("host_conf", "host")
        return atpHost

    def getAtpHeaders(self):
        atpHeaders = cf.get("headers_conf","headers")
        return atpHeaders
