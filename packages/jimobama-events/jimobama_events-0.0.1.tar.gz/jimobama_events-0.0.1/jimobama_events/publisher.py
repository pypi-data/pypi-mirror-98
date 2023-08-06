from jimobama_events  import BaseObject, Event;


"""
  @Publisher : event listener and propagate the events to all the listing objects.
"""
class Publisher(BaseObject):

    def __init__(self, name:str = "untitled"):
        super().__init__();
        self.Name          =  name;
        self.__subscribers = list();
        
    @property
    def Count(self):
        return len(self.__subscribers);
    

    def Publish(self ,event:Event):
        nitems =   0;        
        if(isinstance(event , Event)):
            for sub in self.__subscribers:
                if(sub != None):
                    if(event.StopPropagation == True):
                        break;
                    sub(event);
                    nitems = nitems + 1;
        return nitems;


    def Subscribe(self, callableObj):
        status  = False;
        
        if(callable(callableObj) != True):
            raise ValueError("@Subscriber->Subscribe: parameter 1 must be a callable object or type of Subscriber");

        if(self.__Exists(callableObj) != True):
            self.__subscribers.append(callableObj);
            status  = True;
            
        return status;

    def UnSubscribe(self,callableObj):
          status = False;
          for sub in self.__subscribers:
              if(sub == callableObj):
                  self.__subscribers.remove(callableObj);
                  status  = True;
                  break;
                
          return status;

    def __Exists(self , callableObj):
        status  = False;
        
        if(callable( callableObj)):
            for sub in self.__subscribers:
                if(sub  == callableObj):
                    status  = True;
                    break;

        return status;

    def __call__(self, event):
        return self.Publish(event);

    def __del__(self):
        self.__subscribers = None;

if(__name__== "__main__"):
    def OnTest(event):
        print("Event Testing id = {0}", event.Type);
    p = Publisher();
    p.Subscribe(OnTest);
    p.Publish(Event(89));
    print(p.Count);
    
