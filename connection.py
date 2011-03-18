import inspect

########################################################################
class Connection(object):
    """"""

    #----------------------------------------------------------------------
    def __init__(self, hero, world):
        """Constructor"""
        self.hero, self.world = hero, world
        
    #----------------------------------------------------------------------
    def get_actions(self, for_internal_use=False):
        """"""
        actions = {}
        for obj in self.hero.get_map_view():
            for name,member in inspect.getmembers(obj):
                if inspect.ismethod(member):
                    try:
                        actions[name] = member.action
                        if for_internal_use:
                            actions[name].append(member)
                    except AttributeError:
                        pass
                    
        
        
    
    #----------------------------------------------------------------------
    def get_world_state(self):
        """"""
        map_state = self.hero.get_map_view()
        
        return {"map_state":map_state,
                "actions": self.get_actions()}
        
        
        
    #----------------------------------------------------------------------
    def action(self, *args):
        """"""
        {"move_up":self.hero.move_up,
         "move_down":self.hero.move_down,
         "move_left":self.hero.move_left,
         "move_right":self.hero.move_right,
         
         }[args[0]]()
        
        self.world.tick()
        
    