from SMRCBuilder import Exceptions
from pynput import keyboard, mouse

class input_():
    """
    Input Module. Detects Keypresses and Mouse Movements
    """
    group = ""

    def __init__(self):
        return

    def setgroup(self, group):
        """
        Sets Type Of Self (Keyboard Or Mouse)
        """
        if str(group.lower()) in ("keyboard", "mouse"):
            input_.group = group.lower()
        else:
            raise Exceptions.ArgError("Group Can Only Be Keyboard Or Mouse")

    class keyboard():
        def check():
            if input_.group in ("mouse", ""): raise Exceptions.ArgError("Mouse Or Undefined Cannot Perform Keyboard Actions")
        
        def null(key):
            pass
        
        def start(on_press=null, on_release=null):
            """
            Starts Detecting Keyboard Input
            """
            input_.keyboard.check()
            print("Now Detecting Keyboard Input")
            with keyboard.Listener(
                on_press = on_press,
                on_release = on_release) as listener:
                listener.join()
    
    class mouse():
        def check():
            if input_.group in ("keyboard", ""): raise Exceptions.ArgError("Keyboard Or Undefined Cannot Perform Mouse Actions")

        def null(w="",x="",y="",z=""):
            pass
            
        def start(on_move=null, on_click=null, on_scroll=null):
            print("Now Detecting Mouse Input")
            with mouse.Listener(
                on_move=on_move,
                on_click=on_click,
                on_scroll=on_scroll
            ) as listener:
                listener.join()
        
