

from PyQt4.QtGui import *
from PyQt4.QtCore import *


TILE_WIDTH= 26.0
TILE_HEIGTH= 30.0
FADE_Z_LEVEL = 125.0
BACKGROUND_COLOR = Qt.black
ANIMATION_FRAMERATE = 45.0
ANIMATION_STEP_TIME = 200

#----------------------------------------------------------------------
def map_to_real(x,y):
    """"""
    return x*TILE_WIDTH, y*TILE_HEIGTH
    



#----------------------------------------------------------------------
def real_to_map(x,y):
    """"""
    return int(x/TILE_WIDTH), (y/TILE_HEIGTH)
    
class FadeItem(QGraphicsRectItem):
    def __init__ (self, x, y, fade=0.0):
        super(FadeItem,self).__init__()
        self.setZValue(FADE_Z_LEVEL)
        self.setPos(*map_to_real(x,y))
        self.setBrush(Qt.black)
        self.set_fade(fade)
        self.setRect(0,0,TILE_WIDTH,TILE_HEIGTH)
        c = QColor(BACKGROUND_COLOR)
        c.setAlpha(0)
        self.setPen(QPen(c))
    #----------------------------------------------------------------------
    def set_fade(self, fade):
        """"""
        self.setOpacity(fade)
        
    
class OneTimeItemAnimation(QGraphicsItemAnimation):
    #----------------------------------------------------------------------
    def afterAnimationStep(self, step):
        """"""
        if step==1:
            self.clear()
        

class MapItem(QGraphicsSimpleTextItem):
    
    #----------------------------------------------------------------------
    def __init__ (self, timer, x, y, z=0, symbol="?", color=Qt.white, click_callback=None):
        """"""
        super(MapItem,self).__init__()
        self.setFont(QFont("Consolas"))
        self.x, self.y, self.z = None, None, None
        self.__color, self.__symbol = None, None
        self.set_coords(x, y, z)
        
        self.__click_callback = click_callback
        self.set_symbol(symbol, color)
        self.__animation = OneTimeItemAnimation()
        self.__animation.setItem(self)
        self.__animation.setTimeLine(timer)
        
    
    def get_symbol(self):
        c = self.brush().color()
        return self.__symbol, c
        
        
    #----------------------------------------------------------------------
    def set_symbol (self, symbol, color):
        """"""
        self.__symbol, self.__color = symbol, color
        self.setText(self.__symbol)
        self.setBrush(self.__color)
        s = self.boundingRect().size()
        w,h = s.width(), s.height()
        
        self.resetTransform ()
        m11 = (TILE_WIDTH)/w
        m22 = TILE_HEIGTH/h
        t = QTransform()
        t.scale(m11,m22)
        self.setTransform(t)
        
        self.update()
        
        
    #----------------------------------------------------------------------
    def set_coords (self, x,y,z):
        """"""
        self.x, self.y, self.z = x,y,z
        self.setZValue(z)
        self.setPos(*map_to_real(x,y))
        self.update()
    
    #----------------------------------------------------------------------
    def move_to_coords(self, x, y):
        """"""
        """"""
        for i in range(int(ANIMATION_FRAMERATE)):
            ax = self.x + ((x-self.x)/ANIMATION_FRAMERATE)*i
            ay = self.y + ((y-self.y)/ANIMATION_FRAMERATE)*i
            self.__animation.setPosAt(i/ANIMATION_FRAMERATE, QPointF(*map_to_real(ax,ay)))
        self.x,self.y=x,y
        
    
    #----------------------------------------------------------------------
    def mousePressEvent (self, ev):
        """"""        
        if self.__click_callback is not None:
            self.__click_callback(self)
        else:
            print "%s clicked!"%self

    #----------------------------------------------------------------------
    def destroy (self):
        """"""
        self.scene().removeItem(self)
        
        
    #----------------------------------------------------------------------
    def __unicode__(self):
        """"""
        return "(%d,%d,%d)%s" %(self.x, self.y, self.z, self.__symbol)
        
        
        
        
        

########################################################################
class MapScene(QGraphicsScene):
    """"""
    

    #----------------------------------------------------------------------
    def __init__(self):
        """Constructor"""
        self.__fade = {}
        self.__objects__table = {}
        super(MapScene,self).__init__()
        self.br = QBrush(BACKGROUND_COLOR)
        self.setBackgroundBrush(self.br)
        
        
        
        #moving timer
        self.__timer = QTimeLine(ANIMATION_STEP_TIME)
        self.__timer.setFrameRange(1,ANIMATION_FRAMERATE)
        self.__timer.finished.connect(self.timer_finished)
        self.__timer.frameChanged.connect(self.timer_frame)
        self.__timer.start()
        
    
    #----------------------------------------------------------------------
    def timer_finished(self):
        """"""
        self.__timer.start()
    #----------------------------------------------------------------------
    def timer_frame(self):
        """"""
        pass
        
    #----------------------------------------------------------------------
    def get_items_at(self, x, y, z=None):
        """"""
        res = []
        for item in self.items():
            if item.x==x and item.y==y and (item.z==z or z is None):
                res.append(item)
                
        return res
    
    
    def get_top_item_at(self, x, y):
        items = self.get_items_at(x,y)
        
        
        return sorted(items, key=lambda a: a.z)[0]
    
    #----------------------------------------------------------------------
    def set_fade_at(self, x,y, fade=0.0):
        """"""
        fi = self.__fade[(x,y)]
        fi.set_fade(fade)
   
    def new_mapitem(self, x, y, z, symbol, color=Qt.white):
        
        fade = FadeItem(x,y)
        self.addItem(fade)
        self.__fade[(x,y)] = fade
        
        item = MapItem(self.__timer, x, y, z, symbol, color)
        self.addItem(item)
        
        
        return item  
    
    #----------------------------------------------------------------------
    def __map_item_from_game_object(self, obj):
        """"""
        if obj.landscape:
            z = 0
        else:
            z = 30
        x,y  = obj.get_coords()
        return self.new_mapitem(x,y,z, obj.symbol, QColor(*obj.color))
        
        
    def mapstate_update(self, objs):
        for obj in objs:
            if obj in self.__objects__table.keys():
                mi = self.__objects__table[obj]
                if obj.x!= mi.x or obj.y != mi.y:
                    mi.move_to_coords(obj.x,obj.y)
                sym, c = mi.get_symbol()
                ct = (c.red(),c.green(),c.blue(),c.alpha())
                if obj.color!=ct or obj.symbol!=sym:
                    mi.set_symbol(obj.symbol, QColor(*obj.color))
            else:
                self.__objects__table[obj] = self.__map_item_from_game_object(obj)
                
        
                
                
class MapView(QGraphicsView):
    def __init__(self):
        super(MapView,self).__init__()
        self.scene = MapScene()
        self.setScene(self.scene)  
        
    def mapstate_update(self, objs):
        self.scene.mapstate_update(objs)
        
        
    
    def wheelEvent(self,event):
        """
        use mouse wheel to scale the screen.
        """
        factor = 1.41 ** (-event.delta()/240.0)
        self.scale(factor,factor)


class MiniMapInnerView(QGraphicsView):
    def __init__(self, mapview):
        super(MiniMapInnerView,self).__init__()
        self.setScene(mapview.scene)
        self.scene = mapview.scene
        
    def resizeEvent(self, ev):
        self.fitInView(self.scene.sceneRect(), Qt.KeepAspectRatio)
        super(MiniMapInnerView, self).resizeEvent(ev)
        
        
class MiniMapScene(QGraphicsScene):
    def __init__(self, mapview):
        super(MiniMapScene,self).__init__()
        gv = MiniMapInnerView(mapview)
        self.addWidget(gv)
        
        self.mapview = mapview
        
        self.rect = QGraphicsRectItem(mapview.sceneRect())
        self.rect.setBrush(Qt.white);
        
        self.addItem(self.rect)
        
        self.setSceneRect(self.itemsBoundingRect())
        
        
        
    def mousePressEvent (self, ev):
        """"""        
        
        self.mapview.centerOn( ev.pos())
        print ev.pos().x()

class MiniMapView(QGraphicsView):
    def __init__(self, mapview):
        super(MiniMapView,self).__init__()
        self.scene = MiniMapScene(mapview)
        self.setScene(self.scene)
    def sizeHint(self):
        return QSize(200,100)
    def resizeEvent(self, ev):
        self.fitInView(self.scene.sceneRect(), Qt.KeepAspectRatio)
        super(MiniMapView, self).resizeEvent(ev)
    
    
if __name__=="__main__":
    import sys
    from PyQt4 import QtGui
    
    app = QtGui.QApplication(sys.argv)
    
    mw = widget = MapView()
    widget.resize(250, 150)
    widget.setWindowTitle('simple')
    widget.show()
    
    w2 = MiniMapView(mw)
    w2.show()
    
    
    
    dungeon = [
 '                                                            ###                 ',
 '     #####################         ####################     #.#                 ',
 '     #...................#         #.#................#     #.#                 ',
 '     #.#=###=#############         #.#=##############.#######.#                 ',
 '     #...# #........#              #.=......................=.#                 ',
 '     #...# ##########              ###=##.#######=#####.#####=#####             ',
 '     #...#                          #.....#   #.....=.#.#.........#             ',
 '     #...#    ###############       #.....#   #.....#.#.#.......#.#             ',
 '     #...#    #.............#########.....#   #.....#.#.#.......#.#        ###  ',
 '     #...######=##########=###......#.....#   #.....#.#.#.......#.#        #.#  ',
 '     #...=...................=......#.....#   #.....=...........#.#        #.#  ',
 ' ######.######################............#   #.....###.#.......=.#  #######.#  ',
 ' #......#         ###################=#=#=#   ####### #.........###  #....##.#  ',
 ' ###.##.####      #...................#.#.#           #.........#########.##.#  ',
 ' #.......=.#      ###########=#=#=#####.#.#           #.##########......=.##.#  ',
 ' #.......#.############## #.......=.# #...#           #.##########==#####.##.#  ',
 ' #.......#..............# #.##.=#=#.# #.#.#           #.................=.##.#  ',
 ' #.......#.#######.##.### #.##....#.# #.=.##################.############=##.#  ',
 ' #.......=.#    #......#  #########.# #.#.##...............#...#      #....#.#  ',
 ' ##.######.#  ###......#          #.# #.#.##=###############...#  #####....#.#  ',
 '  #.#    #.#  #.=......#          #.# #.#.#...# ###        #...#  #...=....#.#  ',
 '  #.#    #.#  #.#......#          #.# #.#.#...# #.#        #...# ##.###....#.#  ',
 '  #.###  #.#  #.#......#          #.# #.#.#...# #.#        #...# #...##....#.#  ',
 '  #.#.#  #.#  #.#......#          #.# #.#.....# #.#        #...# #...##....#.#  ',
 '  #.#.#  #.#  #.#......#          ### #.#.##### #.#        #...# #...##....#.#  ',
 '  #.#.#  #.#  #.#......#              #.#.#     #.#        #...# #...##......#  ',
 '  #.#.#  #.#  #.########              ###.#     #.#        #...# #...##....###  ',
 '  #.#.#  #.#  #.#                  ######.##    #.#        #...# #...##....#    ',
 '  #.#.#  #.#  #.#        ###########.=.....#    #.####     ##### #...#######    ',
 '  #.#.#  #.#  ###        #...........#.....######.##.#           #...#          ',
 '  #.#.#  #.#################=#=#####.=.....=.......#.#           #...#          ',
 '  #.#.#  #.##.=.........=......#   #.#######.......=.#       ################## ',
 '  #.#.#  #.##.###########......#   #.#....##.......###########................# ',
 '  #.#.####.##.#         #......#   #.#....##.......#.........#=####=######=#### ',
 '  #.#.=....##.#         #......#   #.#....##.......=.........#.#  #.##......#   ',
 '  #.###....##.#         #......#   #......##.......#.........#.#  #.##......#   ',
 '  ### #....##.#         ########   #########.......#...........#  #.##......#   ',
 '      #######.#                            #.......#.........###  #.##......#   ',
 '            #.#                            ###################    #.##......#   ',
 '            ###                                                   ###########   ']
    from random import random
    
    for y,line in enumerate(dungeon):
        for x,char in enumerate(line):
            mw.scene.new_mapitem(x,y,0,char, Qt.white)
            #mw.set_fade_at(x,y,random())
            
            
    
    
    
    
    
    sys.exit(app.exec_())
