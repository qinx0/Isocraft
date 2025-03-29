import engine_main  # type: ignore
import engine  # type: ignore
import engine_io  # type: ignore
import engine_draw  # type: ignore
import engine_resources  # type: ignore
import random
from engine_nodes import Sprite2DNode, CameraNode, Text2DNode, Rectangle2DNode  # type: ignore
from engine_math import Vector2  # type: ignore
from engine_draw import Color  # type: ignore

def RGB888to565(c):
    return ((c[0] >> 3) << 11) | ((c[1] >> 2) << 5) | c[2] >> 3

doMovement = True
# buttons = ["UP","DOWN","LEFT","RIGHT","B","A","LB","RB","MENU"]

blocksTex = engine_resources.TextureResource("Images/blocks.bmp")
playerTex = engine_resources.TextureResource("Images/player.bmp")
player = Sprite2DNode(Vector2(0, -10), playerTex, Color(1.0, 0.0, 1.0), frame_count_x=4, frame_count_y=3, layer=1)
player.playing = False
# map = Sprite2DNode(Vector2(0,0), blocksTex, Color(1.0,0.0,1.0), frame_count_x=7, frame_count_y=7, layer=0)
# map.playing = False
camera = CameraNode()
player.add_child(camera)


def generateMap():
    for x in range(7):
        for y in range(7):            
            if x < 4 and y < 4:
                bTp = [random.randint(0, 7), random.randint(0, 7)]
                bp = Vector2(int(x * -18), int(y * -18))
                b = Sprite2DNode(bp, blocksTex, Color(1.0, 0.0, 1.0), frame_count_x=7, frame_count_y=7, layer=0)
                b.playing = False
                b.frame_current_x = bTp[0]
                b.frame_current_y = bTp[1]
                print(f"Block created: position: ({bp.x},{bp.y}) ; block: ({bTp[0]},{bTp[1]})")
            elif x < 4 and y >= 4:
                bTp = [random.randint(0, 7), random.randint(0, 7)]
                bp = Vector2(int(x * -18), int(y * 18 // 2))
                b = Sprite2DNode(bp, blocksTex, Color(1.0, 0.0, 1.0), frame_count_x=7, frame_count_y=7, layer=0)
                b.playing = False
                b.frame_current_x = bTp[0]
                b.frame_current_y = bTp[1]
                print(f"Block created: position: ({bp.x},{bp.y}) ; block: ({bTp[0]},{bTp[1]})")
            elif y < 4 and x >= 4:
                bTp = [random.randint(0, 7), random.randint(0, 7)]
                bp = Vector2(int(x * 18 // 2), int(y * -18))
                b = Sprite2DNode(bp, blocksTex, Color(1.0, 0.0, 1.0), frame_count_x=7, frame_count_y=7, layer=0)
                b.playing = False
                b.frame_current_x = bTp[0]
                b.frame_current_y = bTp[1]
                print(f"Block created: position: ({bp.x},{bp.y}) ; block: ({bTp[0]},{bTp[1]})")


map = generateMap()

def movement():
    if engine_io.UP.is_just_pressed:
        player.position.y -= 18
    elif engine_io.DOWN.is_just_pressed:
        player.position.y += 18
    elif engine_io.LEFT.is_just_pressed:
        player.position.x -= 18
    elif engine_io.RIGHT.is_just_pressed:
        player.position.x += 18

while True:
    if engine.tick():
        movement()
