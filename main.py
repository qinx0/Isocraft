import engine_main
import engine
import engine_io
import engine_draw
from engine_draw import Color
import engine_resources

blockTex = engine_resources.TextureResource("Images/Tiny Blocks_1.0/tinyBlocks_NoLine.bmp")
playerTex = engine_resources.TextureResource("Images/Small-8-Direction-Characters_by_AxulArt.bmp")

while True:
    if engine.tick():
        pass