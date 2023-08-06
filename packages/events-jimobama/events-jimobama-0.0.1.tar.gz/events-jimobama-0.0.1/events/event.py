import os;
from  events import BaseObject;

"""
 The base class of all the event objects.
"""
class Event(BaseObject):

    def __init__(self, typeid ):
        super().__init__();
        self.__typeid  = typeid;
        self.__stopPropagation = False;

    @property
    def Type(self):
        return self.__typeid;

    @property
    def StopPropagation(self):
        return self.__stopPropagation;

    @StopPropagation.setter
    def StopPropagation(self, stopStatus):
        if(type(stopStatus)  == bool):
            self.__stopPropagation = stopStatus;


"""
 Test the event class.
"""
if(__name__ =="__main__"):
    event  = Event(89);
    event2 = Event(81);
    print(event.Type);
    print(event.StopPropagation);
    event.StopPropagation = True;
    print(event.StopPropagation);
    print(event.ID);
    print(event2.ID);
