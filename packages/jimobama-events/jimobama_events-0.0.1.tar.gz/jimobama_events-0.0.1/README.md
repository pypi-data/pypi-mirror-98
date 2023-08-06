# messaging
A simple event handling package.

Almost all application are event driven, for instead , when a serial port is open you want to notify other objects that want to use it.
The module provide a clear interface like C# event handlers.
```
from events.event import Event;
from events.eventhandler import EventHandler;
def OnClicked(event):
    print(event.Type);
    
handler  = EventHandler();
handler += OnClicked;
handler(Event('SERIAL_OPEN');

```

