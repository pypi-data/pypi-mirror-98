"""************************************************************
* @brief
*   The base object of the system.
* 
************************************************************"""
import sys;
import time;
import uuid;


class BaseObject(object):
    
    __OBJECT_COUNTS__  =  0;
    def __init__(self):
        
        self.__OBJECT_COUNTS__  = self.__OBJECT_COUNTS__ + 1;
        self.__id               = "{0}{1}".format(uuid.uuid4(), self.__OBJECT_COUNTS__);
        self.__name             = self.__id;
        
    @property
    def Name(self):
        return self.__name;

    @Name.setter
    def Name(self, value):

        if(type(value) != str):
             raise ValueError("Unexpected value provided");
        self.__name  = value;
        
    @property
    def ID(self):
        return self.__id;
    
class ScopeTimer(object):

    def __init__(self, filename , funcName):
        if(sys.platform =="win32"):
            self.Clock  =  time.perf_counter;
        else:
            self.Clock     =  time.time();
        self.__starttimer  =  self.Clock();
        self.__funcName    =  funcName;
        self.__filename    = filename;

    @property
    def Elapse(self):
        self.__endtimer  =  self.Clock();
        elapse =  (self.__endtimer - self.__starttimer) ;
        return elapse;
    
    @property
    def StartTime(self):
        return elf.__starttimer;

    def __del__(self):
        print("@Filename = {0}, Function = {1}, Time elapse = {2} secs".format(self.__filename , self.__funcName, self.Elapse));





if(__name__ == "__main__"):
    obj1  =  BaseObject();
    obj2  =  BaseObject();
    obj1.Name= "Obaro I. Johnson";
    print(obj1.Name);
    print(obj2.ID);
