import engine_main # type: ignore
import engine # type: ignore
import engine_io # type: ignore
import engine_resources # type: ignore
import random
import engine_audio # type: ignore
from engine_nodes import Sprite2DNode, CameraNode, Text2DNode, Rectangle2DNode, EmptyNode # type: ignore
from engine_math import Vector2 # type: ignore
from engine_draw import Color # type: ignore

def RGB888to565(c):
    return ((c[0] >> 3) << 11) | ((c[1] >> 2) << 5) | c[2] >> 3

aFrame = 0
aFinished = True
incrementAFrame = False
frameDelayCounter = 0
frameDelayMax = 5
doMovement = True

direction = 1
blocksTex = engine_resources.TextureResource("Images/blocks.bmp")
playerTex = engine_resources.TextureResource("Images/player.bmp")
pending_move_col = 0
pending_move_row = 0

Font5x7 = engine_resources.FontResource("Font/5x7Font.bmp")

# sfxChannel = AudioChannel()
# sfxChannel.loop = False
sfx = [engine_resources.WaveSoundResource("Audio/step-click.wav")]
engine_audio.set_volume(1.0)

class debug():
    def __init__(self, position, font):
        self.dText = Text2DNode(position = position, font = font)
        
    def Println(self, Text: str):
        if not len(str(self.dText.text)) > 32:
            self.dText.text = self.dText.text + Text
        else: return
    
    def Print(self, Text: str):
        if not len(str(self.dText.text)) > 32:
            self.dText.text = str(self.dText.text) + str('\n'+Text)
        else: return

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
    global direction, aFrame, aFinished, incrementAFrame
    global doMovement, pending_move_col, pending_move_row

    if not doMovement or not aFinished:
        return

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

    # Store intended movement
    pending_move_col = move_col
    pending_move_row = move_row


def animate(node: Sprite2DNode, animationNum: int, steps: int, framedelay: int):
    global aFrame, aFinished, incrementAFrame, frameDelayCounter, doMovement
    global playercol, playerrow, pending_move_col, pending_move_row

    if aFinished:
        return

    if frameDelayCounter < framedelay:
        frameDelayCounter += 1
        return
    frameDelayCounter = 0

    if aFrame < steps:
        node.frame_current_x = animationNum
        node.frame_current_y = aFrame
        engine_audio.play(sfx[0], 3, False)
        aFrame += 1
    else:
        aFrame = 0
        aFinished = True
        incrementAFrame = False
        engine_audio.stop(3)

        # Apply the movement now
        TILE_WIDTH = 16
        TILE_HEIGHT = 9
        playercol += pending_move_col
        playerrow += pending_move_row
        node.position.x = (playercol - playerrow) * (TILE_WIDTH // 2) + 1
        node.position.y = (playercol + playerrow) * (TILE_HEIGHT // 2) + 5

        # Reset movement state
        pending_move_col = 0
        pending_move_row = 0
        doMovement = True


player = createPlayer()
map = generateMap("Images/blocks.bmp")
debugText = debug(Vector2(-32,-32), Font5x7)

while True:
    if engine.tick():
        updatePlayer()
        animate(player, direction, 3, frameDelayMax)
        debugText.Print(f'Ppos: {player.position}')  
