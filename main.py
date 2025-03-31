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

aFrame = 0
aFinished = True
incrementAFrame = False
frameDelayCounter = 0
frameDelayMax = 45
doMovement = True

direction = 1
blocksTex = engine_resources.TextureResource("Images/blocks.bmp")
playerTex = engine_resources.TextureResource("Images/player.bmp")

def generateMap(image_path):
    TILE_WIDTH = 16
    TILE_HEIGHT = 9   
    TILE_ROWS = 7     
    TILE_COLS = 7 
    TILEMAP_ROWS = 14
    TILEMAP_COLS = 14    
    
    texture_id = engine_resources.TextureResource(image_path)

    tilemap = EmptyNode()
    tilemap.layer = 0  
    tilemap.position = Vector2(0,0)
    
    start_x = -((TILEMAP_COLS * TILE_WIDTH) // 2)
    start_y = -((TILEMAP_ROWS * TILE_HEIGHT) // 2)
    
    for row in range(TILEMAP_ROWS):
        for col in range(TILEMAP_COLS):
            tile = Sprite2DNode()
            tile.texture = texture_id
            tile.layer = 0
            tile.playing = False
            tile.transparent_color = Color(1.0,0.0,1.0)
            
            tile.frame_count_x = TILE_ROWS
            tile.frame_count_y = TILE_COLS
            tile.frame_current_x = random.randint(0,7)
            tile.frame_current_y = random.randint(0,7)
            
            tile_x = start_x + (col - row) * (TILE_WIDTH // 2)
            tile_y = start_y + (col + row) * (TILE_HEIGHT // 2)

            tile.position.x = tile_x
            tile.position.y = tile_y
            
            tilemap.add_child(tile)
    
    rootMap = EmptyNode()
    rootMap.add_child(tilemap)

def createPlayer():
    TILE_WIDTH = 16
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
    player.position.y = (start_col + start_row) * (TILE_HEIGHT // 2) + 5
    global playercol 
    playercol = start_col
    global playerrow
    playerrow = start_row
    return player

def updatePlayer():
    global playercol, playerrow, direction, aFrame, aFinished, incrementAFrame, doMovement

    if not doMovement:  
        return

    TILE_WIDTH = 16
    TILE_HEIGHT = 9
    move_col = 0
    move_row = 0

    
    if engine_io.UP.is_just_pressed:
        direction = 0  
        move_row -= 1
    elif engine_io.DOWN.is_just_pressed:
        direction = 2  
        move_row += 1
    elif engine_io.LEFT.is_just_pressed:
        direction = 3  
        move_col -= 1
    elif engine_io.RIGHT.is_just_pressed:
        direction = 1  
        move_col += 1
    else:
        return  

    
    doMovement = False
    aFinished = False
    incrementAFrame = True

    
    playercol += move_col
    playerrow += move_row
    player.position.x = (playercol - playerrow) * (TILE_WIDTH // 2) + 1
    player.position.y = (playercol + playerrow) * (TILE_HEIGHT // 2) + 5

def animate(node: Sprite2DNode, animationNum: int, steps: int, framedelay: int):
    global aFrame, aFinished, incrementAFrame, frameDelayCounter, doMovement

    if aFinished:
        return  

    
    if frameDelayCounter < framedelay:
        frameDelayCounter += 1
        return
    frameDelayCounter = 0  

    
    if aFrame < steps:
        node.frame_current_x = animationNum  
        node.frame_current_y = aFrame - 1  
        aFrame += 1
    else:
        aFrame = 0
        aFinished = True
        incrementAFrame = False
        node.frame_current_x, node.frame_current_y = animationNum, aFrame+1  

        
        doMovement = True  


player = createPlayer()
map = generateMap("Images/blocks.bmp")

while True:
    if engine.tick():
        updatePlayer()
        animate(player, direction, 3, frameDelayMax)
        if engine_io.A.is_just_pressed:
            doMovement = not doMovement         
