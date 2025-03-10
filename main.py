import engine_main
import engine
import engine_io
import engine_draw
from engine_draw import Color
import engine_nodes 
import engine_resources

blockTex = engine_resources.TextureResource("Images/Tiny Blocks_1.0/tinyBlocks_NoLine.bmp")
playerTex = engine_resources.TextureResource("Images/Small-8-Direction-Characters_by_AxulArt.bmp")
playerNode = engine_nodes.Sprite2DNode(texture = playerTex, transparent_color = engine_draw.Color(1.0,0.0,1.0), frame_count_x = 4, frame_count_y = 3)

while True:
    if engine.tick():
        pass