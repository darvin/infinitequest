from mapobject import MapObject


########################################################################
class Landscape(MapObject):
    """
    Landscape element. Rock, tree, wall, floor
    """

    #----------------------------------------------------------------------
    def __init__(self, map, x, y):
        """Constructor"""
        super(Landscape, self).__init__(map, x, y)
        self.landscape = True
        
    

########################################################################
class Wall(Landscape):
    """
    Wall
    """

    #----------------------------------------------------------------------
    def __init__(self, map, x, y):
        """Constructor"""
        super(Wall, self).__init__(map, x, y)
        self.symbol = "#"
        self.passable = False
        self.view_passable = False
        self.update()
        

########################################################################
class Door(Landscape):
    """
    Door
    """

    #----------------------------------------------------------------------
    def __init__(self, map, x, y, closed=False):
        """Constructor"""
        super(Door, self).__init__(map, x, y)
        self.closed = None
        self.set_closed(closed)
        
        
    #----------------------------------------------------------------------
    def open(self):
        """"""
        self.set_closed(False)
        

        
    #----------------------------------------------------------------------
    def set_closed(self, closed):
        """
        """
        self.closed = closed
        self.passable = not closed
        self.view_passable = not closed
        if closed:
            self.symbol = "+"
        else:
            self.symbol = "/"
        self.update()
        

########################################################################
class SecretDoor(Door):
    """
    Secret Door
    """

    #----------------------------------------------------------------------
    def __init__(self, map, x, y):
        """Constructor"""
        super(SecretDoor, self).__init__(map, x, y, True)
        self.symbol = "#"
        self.update()
        

########################################################################
class Stairs(Landscape):
    """
    Stairs: up or down
    """

    #----------------------------------------------------------------------
    def __init__(self, map, x, y, down=True):
        """Constructor"""
        super(Stairs, self).__init__(map, x, y)
        self.passable = True
        self.view_passable = True
        self.connected_stairs = None
        if down:
            self.symbol = ">"
        else:
            self.symbol = "<"
        self.update()
        
    #----------------------------------------------------------------------
    def connect_to(self, stairs):
        """"""
        self.connected_stairs = stairs
        
        
########################################################################
class Floor(Landscape):
    """
    Floor
    """

    #----------------------------------------------------------------------
    def __init__(self, map, x, y):
        """Constructor"""
        super(Floor, self).__init__(map, x, y)
        self.symbol = "."
        self.passable = True
        self.view_passable = True
        self.update()  
