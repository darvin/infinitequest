from qmapwidget import MapView, MiniMapView
from statuswidgets import StatusHeroWidget
from world import World
from connection import Connection

from creatures import Hero

from PyQt4.QtGui import *
from PyQt4.QtCore import *

class InfiniteQuestWindow(QMainWindow):
    #----------------------------------------------------------------------
    def __init__(self):
        """"""
        super(InfiniteQuestWindow, self).__init__()
        self.setWindowTitle('Infinite Quest')
        self.mapview = MapView()
        #self.mapview = QGraphicsView()
        #self.sc = MapScene()
        #self.mapview.setScene(self.sc)
        self.mapview.installEventFilter(self)
        
        self.setCentralWidget(self.mapview)
        
        
        self.minimap = MiniMapView(self.mapview)
        minimap_dw = QDockWidget()
        minimap_dw.setWidget(self.minimap)
        self.addDockWidget(Qt.LeftDockWidgetArea, minimap_dw)
        
        
        self.statushero = StatusHeroWidget()
        statushero_dw = QDockWidget()
        statushero_dw.setWidget(self.statushero)
        self.addDockWidget(Qt.LeftDockWidgetArea, statushero_dw)
        
        #self.mapview.setSizePolicy(QSizePolicy(QSizePolicy.MinimumExpanding,QSizePolicy.MinimumExpanding))
        
        self.world = World()
        
        
        
        
        
        self.hero = Hero(self.world.map(), *self.world.map().find_passable_landscape_coords())
        
        self.connection = Connection(self.hero,self.world)
        
        
        self.game_state_update()
        
        
        
        
    #----------------------------------------------------------------------
    def game_state_update(self):
        """"""
        st = self.connection.get_world_state()
        self.mapview.scene.mapstate_update(st["map_state"])
        
    #----------------------------------------------------------------------
    def eventFilter(self, obj, ev):
        """"""
        if ev.type()==QEvent.KeyPress:
            try: 
                self.connection.action({
                Qt.Key_Up:"move_up",
                Qt.Key_Down:"move_down",
                Qt.Key_Right:"move_right",
                Qt.Key_Left:"move_left",
                }[ev.key()])
                self.game_state_update()
                return True
            except KeyError:
                pass
        else:
            pass
        return super(InfiniteQuestWindow, self).eventFilter(obj, ev)
        
        
if __name__=="__main__":
    import sys
    from PyQt4 import QtGui
    
    app = QtGui.QApplication(sys.argv)
    
    widget = InfiniteQuestWindow()
    widget.resize(800, 600)
    
    widget.show()
    sys.exit(app.exec_())
        