import engine_main  
import engine  
import engine_io  
import engine_draw  
import engine_resources  
import random
from engine_nodes import Sprite2DNode, CameraNode, Text2DNode, Rectangle2DNode, EmptyNode  
from engine_math import Vector2  
from engine_draw import Color  

def RGB888to565(c):
    return ((c[0] >> 3) << 11) | ((c[1] >> 2) << 5) | c[2] >> 3

tA = False
direction = 1
doMovement = True
blocksTex = engine_resources.TextureResource("Images/blocks.bmp")
playerTex = engine_resources.TextureResource("Images/player.bmp")

def generateMap(image_path):
    TILE_WIDTH = 18   
    TILE_HEIGHT = 9   
    TILE_ROWS = 7     
    TILE_COLS = 7     
    
    texture_id = engine_resources.TextureResource(image_path)

    tilemap = EmptyNode()
    tilemap.layer = 0  
    tilemap.position = Vector2(0,0)
    
    start_x = -((TILE_COLS * TILE_WIDTH) // 2)
    start_y = -((TILE_ROWS * TILE_HEIGHT) // 2)
    
    for row in range(TILE_ROWS):
        for col in range(TILE_COLS):
            tile = Sprite2DNode()
            tile.texture = texture_id
            tile.layer = 0
            tile.playing = False
            tile.transparent_color = Color(1.0,0.0,1.0)
            
            tile.frame_count_x = TILE_ROWS
            tile.frame_count_y = TILE_COLS
            tile.frame_current_x = row
            tile.frame_current_y = col
            
            tile_x = start_x + (col - row) * (TILE_WIDTH // 2)
            tile_y = start_y + (col + row) * (TILE_HEIGHT // 2)

            tile.position.x = tile_x
            tile.position.y = tile_y
            
            tilemap.add_child(tile)
    
    rootMap = EmptyNode()
    rootMap.add_child(tilemap)

def createPlayer():
    TILE_WIDTH = 18
    TILE_HEIGHT = 9 
    
    player_texture = engine_resources.TextureResource("Images/player.bmp")
    
    player = Sprite2DNode()
    player.texture = player_texture
    player.layer = 1  
    player.playing = False
    player.transparent_color = Color(1.0,0.0,1.0)
    camera = CameraNode()
    player.add_child(camera)
    player.frame_count_x = 4
    player.frame_count_y = 3
    
    start_col, start_row = 0, 0  
    player.position.x = (start_col - start_row) * (TILE_WIDTH // 2) + 1
    player.position.y = (start_col + start_row) * (TILE_HEIGHT // 2) + 3
    
    global playercol 
    playercol = start_col
    global playerrow
    playerrow = start_row
    return player

def updatePlayer():
    if not doMovement:
        return
    global playercol
    global playerrow
    global direction
    TILE_WIDTH = 18   
    TILE_HEIGHT = 9
    move_col = 0
    move_row = 0

    if engine_io.UP.is_just_pressed:
        direction = 1
        move_row -= 1
        print(f"Direction: {direction}")
    if engine_io.DOWN.is_just_pressed:
        direction = 2
        move_row += 1
        print(f"Direction: {direction}")
    if engine_io.LEFT.is_just_pressed:
        direction = 3
        move_col -= 1
        print(f"Direction: {direction}")
    if engine_io.RIGHT.is_just_pressed:
        direction = 4
        move_col += 1
        print(f"Direction: {direction}")
    
    playercol += move_col
    playerrow += move_row
    
    player.position.x = (playercol - playerrow) * (TILE_WIDTH // 2) + 1
    player.position.y = (playercol + playerrow) * (TILE_HEIGHT // 2) + 3

def animate(node: Sprite2DNode, aNum: int):
    node.playing = True

def animStop(node):
    node.playing = False

player = createPlayer()
map = generateMap("Images/blocks.bmp")

while True:
    if engine.tick():
        updatePlayer()
        if engine_io.A.is_just_pressed:
            doMovement = not doMovement
        if engine_io.B.is_just_pressed:
            if tA: tA = not tA; animStop(player); print("Started animating")
            else: tA = not tA; animate(player, 1); print("Stopped animating")
            
