from gameobject import GameObject

########################################################################
class MapObject(GameObject):
    """
    Represents map object on map
    """

    #----------------------------------------------------------------------
    def __init__(self, map, x, y):
        """Constructor"""
        super(MapObject,self).__init__()
        self.__x, self.__y = x,y
        self.passable = None
        self.landscape = None
        self.view_passable = None
        self.map = map
        self.map.add_object(x, y, self)
    @property
    def x(self):
        return self.__x
    
    @property
    def y(self):
        return self.__y
        
    def get_coords(self):
        return self.__x, self.__y
    
    def set_coords(self, x,y):
        self.map.move_object(self.__x,self.__y, x,y, self)
        self.__x, self.__y = x,y
        
        
    def update(self):
        self.map.update(self)
        
    
    