########################################################################
class GameObject(object):
    """
    Abstact game object class
    """

    #----------------------------------------------------------------------
    def __init__(self):
        """Constructor"""
        self.symbol = "X"
        self.color = (255,255,255,255)
        
        
    def tick(self):
        pass
        
        
        
########################################################################
class Message(GameObject):
    """"""

    #----------------------------------------------------------------------
    def __init__(self, text, color):
        """Constructor"""
        self.text = text
        self.color = color
        
        
########################################################################
class Effect(GameObject):
    """"""

    #----------------------------------------------------------------------
    def __init__(self, stx, sty, endx, endy, symbol="|", color=(255,255,255,255)):
        """Constructor"""
        self.stx, self.sty, self.endx, self.endy, self.symbol, self.color = \
            stx,sty, endx, endy, symbol, color
        
        
########################################################################
class CreatureMessage(GameObject):
    """"""

    #----------------------------------------------------------------------
    def __init__(self, creature, text):
        """Constructor"""
        self.creature = creature
        self.text = text
        
        
    
    
        
        
    
    