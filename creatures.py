from mapobject import MapObject
from landscape import *
from fov import fieldOfView

class Creature(MapObject):
    def __init__(self, map, x, y):
        """Constructor"""
        super(Creature, self).__init__(map, x, y)
        self.fov = []
        self.passable = False
        self.view_passable = True
        self.view_distance = 6
        self.symbol = "C"
        self.update()
        
    def update_fov(self):
        self.fov = []
        fieldOfView(self.x,self.y, self.map.size_x, self.map.size_y,
                          self.view_distance, lambda x,y: self.fov.append((x,y)), 
                          lambda x,y: not self.map.is_view_passable(x,y))
        print len(self.fov)
           
    
    
    def get_map_view(self):
        self.update_fov()
        lst = []
        for x,y in self.fov:
            lst += self.map.objects_map[x][y]
        return lst
    
    
    
    def get_map_view_update(self):
        self.update_fov()
        print "m v u", self.fov
        print [(obj.x,obj.y) for obj in self.map.objects_to_update]
        return [obj for obj in self.map.objects_to_update \
                if (obj.x, obj.y) in self.fov]
    
    def tick(self):
        pass
    
    
    #----------------------------------------------------------------------
    def move(self, x,y):
        """"""
        if self.map.is_passable(x,y):
            self.set_coords(x,y)
            self.update()
        else:
            for obj in self.map.get_objects_at(x,y):
                self.kick(obj)
    #----------------------------------------------------------------------
    def kick(self, obj):
        """"""
        if isinstance(obj, (Door, SecretDoor)):
            obj.open()
            
        

class Hero(Creature):
    
    def __init__(self, map, x, y):
        """Constructor"""
        super(Hero, self).__init__(map, x, y)
        self.symbol = "@"
        self.color = (232,33,52,255)
        self.update()
    
    #----------------------------------------------------------------------
    def move_right(self):
        """"""
        self.move(self.x+1, self.y)
        
    
    #----------------------------------------------------------------------
    def move_left(self):
        """"""
        self.move(self.x-1, self.y)
    
    #----------------------------------------------------------------------
    def move_up(self):
        """"""
        self.move(self.x, self.y-1)
    
    #----------------------------------------------------------------------
    def move_down(self):
        """"""
        self.move(self.x, self.y+1)
        