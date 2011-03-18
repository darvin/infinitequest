from dungeon_generator import generate_map
from landscape import *
import random

########################################################################
class World(object):
    """
    Defines several connected pregenered maps
    """

    #----------------------------------------------------------------------
    def __init__(self, number_of_maps=2):
        """Constructor"""
        self.maps = []
        for i in range(number_of_maps):
            self.maps.append(Map.empty_random())
            
        for i in range(number_of_maps-1):
            stairs = self.maps[i].new_random_stairs(down=True)
            stairs.connect_to(self.maps[i+1].new_random_stairs(down=False))
            
            
    
    
    def tick(self):
        for map in self.maps:
            map.tick()
            
        
        
    def map(self):
        #FIXME!
        try:
            return self.maps[0]
        except IndexError:
            return None
        
 
            
CLOSED_DOOR = 4
OPEN_DOOR = 3
SECRET_DOOR = 5
WALL = 2
FLOOR = 0
VOID = 1

class Map(object):
    
    #----------------------------------------------------------------------
    def __init__(self, size_x, size_y):
        """"""
        self.size_x = size_x
        self.size_y = size_y
        self.objects_to_update = set()
        self.objects = set()
        self.objects_map = [[ set()  for i in range(self.size_y+1)] for x in range(self.size_x+1)]
        
        pass
        
    #----------------------------------------------------------------------
    def add_object(self, x, y, obj):
        """"""
        self.objects_map[x][y].add(obj)
        self.objects.add(obj)
        
    def move_object(self, oldx, oldy, newx, newy, obj):
        self.objects_map[oldx][oldy].remove(obj)
        self.objects_map[newx][newy].add(obj)
        
    #----------------------------------------------------------------------
    def update(self,obj):
        """"""
        self.objects_to_update.add(obj)


        
    #----------------------------------------------------------------------
    def tick(self):
        """"""
        self.objects_to_update.clear()
        for obj in self.objects:
            obj.tick()
        
    
        
    #----------------------------------------------------------------------
    def get_objects_at(self,x, y):
        """"""
        return self.objects_map[x][y]
        
        
    #----------------------------------------------------------------------
    def get_landscape_at(self):
        """"""
        return [obj for obj in self.objects_map[x][y] if obj.landscape]
        
        
    #----------------------------------------------------------------------
    def find_passable_landscape_coords(self):
        """"""
        while True:
            x = random.randint(0,self.size_x)
            y = random.randint(0,self.size_y)
            if self.is_passable(x, y):
                return x,y
    
    #----------------------------------------------------------------------
    def is_passable(self, x,y):
        """"""
        if len(self.objects_map[x][y])==0:
            return False
        
        for obj in self.objects_map[x][y]:
            if not obj.passable:
                return False
        return True
    
    #----------------------------------------------------------------------
    def is_view_passable(self, x,y):
        """"""
        if len(self.objects_map[x][y])==0:
            return False
        for obj in self.objects_map[x][y]:
            if not obj.view_passable:
                return False
        return True
    
    #----------------------------------------------------------------------
    def new_random_stairs(self, down=True):
        """"""
        x,y = self.find_passable_landscape_coords()
        return Stairs(self,x,y,down)
        
    
    
    @classmethod
    #----------------------------------------------------------------------
    def empty_random(cls):
        """"""
        nm = cls(35,68)
        arr = generate_map(nm.size_x,nm.size_y,110,50,60)
        
        #nm.size_x = sizex = 130
        #nm.size_y = sizey = 130
        #arr = generate_map(nm.size_x,nm.size_y,11,3,2)
        
        number = 0
        for y in range(nm.size_y):
            for x in range(nm.size_x):
                tile = arr[y][x]
                if tile==OPEN_DOOR:
                    Door(nm, x, y, closed=False)
                if tile==CLOSED_DOOR:
                    Door(nm, x, y, closed=True)
                if tile==SECRET_DOOR:
                    SecretDoor(nm, x, y)
                if tile==WALL:
                    Wall(nm, x, y)
                if tile==FLOOR:
                    Floor(nm, x, y)
                if tile==VOID:
                    pass
        return nm

                
        
if __name__=="__main__":
    def s(lst):
        #from pprint import pprint
        
        #pprint (lst)
        print len(lst)
    m = World()
    print len(m.map().objects_to_update)
    for i,obj in enumerate(m.map().objects_to_update):
        print i
        
        
    
    