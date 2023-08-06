import os;
import ctypes;
from threading import Thread;
from events import Event,EventHandler;




class LoggerLevel(int):
    ALL          = 0x01;
    INFORMATION  = 0x02;

class Logger:
    DebugMode  = True;
    Level      = LoggerLevel.ALL;

    @staticmethod
    def Debug(message, **kwargs):
        level =  kwargs['level'] if ("level" in kwargs) else LoggerLevel.ALL;
        if(Logger.Level == level):
            if(level == LoggerLevel.ALL):
                if(Logger.DebugMode == True):
                     print("Debug ALL :{0} ".format(message));
            elif(level  == LoggerLevel.INFORMATION):
                print("Debug {0}: {0}".format("INFO", message));

    @staticmethod
    def Except(message):
        if(Logger.DebugMode == True):
            self.Debug(message);
            raise ValueError(message);


if (__name__ == "__main__"):

    Logger.Debug("Hello World");



