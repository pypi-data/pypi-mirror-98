from jimobama_events import BaseObject, Event, Publisher;



class EventHandler(BaseObject):
    
    def __init__(self, publisher = None):
        self.__publisher = publisher if (isinstance(publisher, Publisher)) else Publisher("EventHandler")
        
    def __call__(self, event):
        if(isinstance(event, Event) != True):
            raise TypeError("@Evenhandler: parameter must be an event type")
        return  self.__publisher.Publish(event);

    def __iadd__(self, other):
        if(callable(other)):
            self.__publisher.Subscribe(other)
        return self;
    
    def __isub__(self, other):
        if(callable(other)):
            self.__publisher.UnSubscribe(other)
        return self
    
    @property
    def Count(self):
        return self.__publisher.Count
    

if(__name__ == "__main__"):
    def OnTest(event):
        print("Handler event ={0}", event.Type);
    handler  = EventHandler()
    handler+= OnTest
    handler(Event(892))
    print(handler.Count)
