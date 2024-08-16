#######################################
# THEME: FUNCTIONALY DISFUNCTIONAL
#######################################

# Idea: Annoying captcha

######################
# MODULES
######################
import math, os, pygame, sys
from enum import Enum

os.system("cls")
print("Welcome to the VERIFY viewing terminal!\n")

######################
# GAME STATES
######################
class GameState(Enum):
    MENU = -1
    STARTUP = 0
    TERMSANDCONDITIONS = 1
    CLICKED = 2
    WARNING = 3
    PRE_EVADE = 4
    EVADE = 5
    PRE_TAG = 6
    TAG = 7
    PRE_MATEIN3 = 8
    MATEIN3 = 9
    PRE_ACCESS = 10
    ACCESS = 11

######################
# SCREEN
######################
pygame.init()

# Screen setup
screen_height = 640
screen_width = 640
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("VERIFY - Please the CAPTCHA!")

# Icon setup
icon = pygame.image.load("icon.png")
pygame.display.set_icon(icon)

# Run setup
clock = pygame.time.Clock()
running = True

######################
# IMAGES
######################

# Menu
play           = pygame.image.load("play.png")
play_hover     = pygame.image.load("play_hover.png")
title          = pygame.image.load("title.png")

# Buttons
checkbox       = pygame.image.load("checkbox.png")
checked        = pygame.image.load("checkbox_checked.png")
proceed        = pygame.image.load("proceed.png")
proceed_agreed = pygame.image.load("proceed_agreed.png")

warning        = pygame.image.load("warning.png")
target         = pygame.image.load("target.png")
target_blink   = pygame.image.load("target_blink.png")

chessboard     = pygame.image.load("chessboard.png")
pawn           = pygame.image.load("pawn.png")
pawn_black     = pygame.image.load("pawn_black.png")
knight         = pygame.image.load("knight.png")
knight_black   = pygame.image.load("knight_black.png")
bishop         = pygame.image.load("bishop.png")
bishop_black   = pygame.image.load("bishop_black.png")
rook           = pygame.image.load("rook.png")
rook_black     = pygame.image.load("rook_black.png")
queen          = pygame.image.load("queen.png")
queen_black    = pygame.image.load("queen_black.png")
king           = pygame.image.load("king.png")
king_black     = pygame.image.load("king_black.png")

######################
# TEXT
######################
font = pygame.font.SysFont(["JetBrains Mono", "Courier New"], 16, True)
large_font = pygame.font.SysFont(["JetBrains Mono", "Courier New"], 20, True)

class TextEngine:
    def __init__(self, text:list, delay_frames:int=0):
        self.text = text
        self.delay_frames = delay_frames
        self.counter = delay_frames
        self.load_count = 0
        self.col = -1
        self.row = 0
        self.text_render = ["" for i in range(len(text))]
    def advance(self):
        if self.row >= len(self.text):
            return
        self.col += 1
        if self.col == len(self.text[self.row]):
            self.col = 0 
            self.row += 1
        if self.row >= len(self.text):
            return
        self.text_render[self.row] += self.text[self.row][self.col]
    def render(self):
        if self.counter > 0:
            self.counter -= 1
        else: # Special loading text
            global load_count
            if self.text_render[0][0:7] != "Loading":
                self.advance()
            else:
                self.text_render[0] += "."
                if self.text_render[0][7:11] == "....":
                    self.text_render[0] = "Loading"
                    load_count += 1
            self.counter = self.delay_frames
                
def draw_text(txt:TextEngine, col:pygame.Color, center_x:int, start_y:int, center:bool, big:bool=False):
    txt.render()
    if big:
        text = [large_font.render(i, True, col) for i in txt.text_render]
    else:
        text = [font.render(i, True, col) for i in txt.text_render]
    text_rect = [i.get_rect() for i in text]
    for i in range(len(text_rect)):
        if center:
            if not big: text_rect[i].center = (center_x, start_y+(i*16))
            else: text_rect[i].center = (center_x, start_y+(i*22))
        else:
            if not big: setattr(text_rect[i], "topleft", (center_x, start_y+(i*16)))
            else: setattr(text_rect[i], "topleft", (center_x, start_y+(i*22)))
        screen.blit(text[i], text_rect[i])

tac_text = [
"By using this service, you agree to the", "following:", " ", "- You are responsible for all activities", "under your account.", "- You are agreeing that this is the", "shortest Terms and Conditions that you", "have read.", "- Your use of this service is at your own", "risk.", "- We reserve the right to modify these", "Terms and Conditions at any time.", "- We are not liable for any damages or", "losses incurred by you.", "- We are not responsible for rogue", "checkboxes you encountered.", "- Disputes will be governed by law.", " ", "I agree to the Terms and Conditions."]

terms_and_conditions = TextEngine(tac_text)

# Special loading text
load_count = 0
loading_text = TextEngine(["Loading"], 10)

warn = [
    "--- WARNING ---", " ", " ",
    "Access Denied", " ",
    "403 Forbidden: It appears you have failed", "to complete our security check.",
    " ",
    "Click on the check box to prove that",
    "you are a human trying to access our", "service."
]
warn_text = TextEngine(warn, 1)

pre_evade_texts = iter([
    TextEngine(["Do you think it's that easy..."], 3),
    TextEngine(["To click ME???"], 3),
    TextEngine(["..."], 3),
    TextEngine(["Tell you what."], 3),
    TextEngine(["..."], 3),
    TextEngine(["CATCH ME IF YOU CAN!"], 3)
])
pre_evade_text = next(pre_evade_texts)

pre_tag_texts = iter([
    TextEngine(["Interesting...", "Very interesting..."], 3),
    TextEngine(["..."], 3),
    TextEngine(["Would you look at that.", "The tables have turned."], 3),
    TextEngine(["..."], 3),
    TextEngine(["GOOD LUCK."], 3)
])
pre_tag_text = next(pre_tag_texts)

pre_matein3_texts = iter([
    TextEngine(["Why... can't I succeed..."], 3),
    TextEngine(["YOU..."], 10),
    TextEngine(["..."], 10),
    TextEngine(["Huff... puff...", "I am... weary..."], 5),
    TextEngine(["Tell... you... what..."], 6),
    TextEngine(["..."], 15),
    TextEngine(["Let's have a battle of wits instead."], 3),
    TextEngine(["Solve this puzzle, and I will let you proceed."], 3)
])
pre_matein3_txt = next(pre_matein3_texts)

matein3_text = TextEngine(["White to move.", "Mate in 3."], 0)

success_text = TextEngine(["Fine.", "I guess you win."], 3)

welcome_dialogue = iter([
    TextEngine(["Ah. Welcome.", "You arrived later than expected."], 3),
    TextEngine(["I see that you are late because of", "an anomaly.", "Let me find it."], 3),
    TextEngine([" ", "> System Console", " ", ">>> Launching Cleaner...", " ", " ", ">>> Anomaly Detected:", "<Checkbox[1000101]>", " ", ">>> Removing Anomaly", "<Checkbox[1000101]>...", " ", " ", " ", ">>> Anomaly removed successfully."], 3),
    TextEngine(["..."], 3),
    TextEngine(["Whoops... you... weren't supposed", "to see that..."], 3),
    TextEngine(["In any case... the anomaly made", "you go through a TON of trouble...", "didn't you?"], 3),
    TextEngine(["..."], 3),
    TextEngine(["Well, you have reached the end.", "There is nothing beyond this point."], 3),
    TextEngine(["There never was any service."], 3),
    TextEngine(["..."], 3),
    TextEngine(["It was all a simulation.", "To test your reaction, your wits,", "and your ability to read the Terms", "and Conditions."], 3),
    TextEngine(["..."], 3),
    TextEngine(["I'm kidding of course."], 3),
    TextEngine(["No data was being recorded.", " ", "This 'service' (if we can even call", "it that) is submitted to the", "Hackathon by Lewis Menelaws."], 3),
    TextEngine(["..."], 3),
    TextEngine(["You know what would be funny?", " ", "What if there was a rickroll instead", "of this dialogue?"], 3),
    TextEngine(["But the creator doesn't know how to", "do that, so we're stuck with this."], 3),
    TextEngine(["..."], 3),
    TextEngine(["Congratulations.", "You beat the game."], 3),
    TextEngine(["Peace out."], 3),
])

welcome_text = next(welcome_dialogue)

######################
# SPRITES
######################
class Title(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = title
        self.x = x
        self.y = y
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
    def update(self):
        # Move to the top and kill itself
        global game_state
        if game_state == GameState.STARTUP:
            self.y -= 6
            self.rect.center = (self.x, self.y)
            if self.y < 100:
                self.y = 100
        elif game_state == GameState.CLICKED:
            self.y -= 6
            self.rect.center = (self.x, self.y)
            if self.y < -47:
                self.kill()

class Play(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale_by(play, 1.5)
        self.x = x
        self.y = y
        self.fallen = False
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
    def update(self):
        pos = pygame.mouse.get_pos()
        if not self.fallen:
            self.image = pygame.transform.scale_by(play, 1.5)
            if pos[0] > self.x - 71 and pos[0] < self.x + 71 and pos[1] > self.y - 48 and pos[1] < self.y + 48:
                self.image = pygame.transform.scale_by(play_hover, 2)
                self.image = pygame.transform.rotate(self.image, -5)
                mouse_down = pygame.mouse.get_pressed()
                if mouse_down[0]:
                    global game_state
                    print("> Starting up...")
                    self.fallen = True
            self.rect = self.image.get_rect()
            self.rect.center = (self.x, self.y)
        else:
            # Fall and start game
            self.y += 12
            self.image = pygame.transform.rotate(self.image, -5)
            self.rect = self.image.get_rect()
            self.rect.center = (self.x, self.y)
            if self.y > screen_height + 32:
                game_state = GameState.STARTUP
                self.kill()

class Checkbox(pygame.sprite.Sprite):
    def __init__(self, x, y, type_:str):
        pygame.sprite.Sprite.__init__(self)
        self.scale = 0.5 if type_ == "TaC" else 1
        self.image = pygame.transform.scale_by(checkbox, self.scale)
        self.checked = False
        self.x = x
        self.y = y
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
    def update(self):
        # Calls only when mouse is down
        global game_state
        if game_state == GameState.TERMSANDCONDITIONS: # Only one check box is used in every stage, so we're good.
            pos = pygame.mouse.get_pos()
            if pos[0] > self.x - 16 and pos[0] < self.x + 16 and pos[1] > self.y - 16 and pos[1] < self.y + 16:
                if self.checked:
                    self.image = pygame.transform.scale_by(checkbox, self.scale)
                else:
                    self.image = pygame.transform.scale_by(checked, self.scale)
                self.checked = not self.checked
        elif game_state == GameState.WARNING:
            pos = pygame.mouse.get_pos()
            if pos[0] > self.x - 32 and pos[0] < self.x + 32 and pos[1] > self.y - 32 and pos[1] < self.y + 32:
                print("> A rogue check box is loose!\n  We are not responsible for it though.")
                game_state = GameState.PRE_EVADE
                self.kill()

class GameCheckbox(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = checkbox
        self.x = x
        self.y = y
        self.pressed = True
        self.checkdelay = 0
        self.rect = checkbox.get_rect()
        self.rect.center = (x, y)
    def update(self):
        global game_state
        pos = pygame.mouse.get_pos()
        mouse_down = pygame.mouse.get_pressed(3)[0]
        if pos[0] in list(range(self.x - 32, self.x + 33)) and pos[1] in list(range(self.y - 32, self.y + 33)) and mouse_down and not self.pressed and self.checkdelay == 0:
            self.image = checked
            self.checkdelay = 45
        if mouse_down:
            self.pressed = True
        else:
            self.pressed = False
        if self.checkdelay > 0:
            self.checkdelay -= 1
            if self.checkdelay == 0:
                if game_state == GameState.PRE_MATEIN3:
                    game_state = GameState.MATEIN3
                self.kill()

class RogueCheckbox(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = checkbox
        self.x = x
        self.y = y
        self.rect = checkbox.get_rect()
        self.rect.center = (x, y)

        self.stamina = 60.0
        self.drag = 8
        self.clicked = False
        self.pressed = False

        self.blink_delay = 15
        self.blink_count = 0
    def update(self):
        pos = pygame.mouse.get_pos()
        global game_state
        if game_state == GameState.EVADE:
            if not self.clicked:
                dx = self.x - pos[0]
                dy = self.y - pos[1]
                dist = math.hypot(dx, dy)
                if dist == 0: dist = 1
                dx /= dist
                dy /= dist
                self.x += dx * self.stamina / self.drag
                self.y += dy * self.stamina / self.drag
                # Wrap around
                if self.x > screen_width:
                    self.x = 32
                if self.x < 0:
                    self.x = screen_width - 32
                if self.y > screen_height:
                    self.y = 32
                if self.y < 0:
                    self.y = screen_height - 32
                # Check if clicked
                mouse_pressed = pygame.mouse.get_pressed()[0]
                if mouse_pressed:
                    if not self.pressed:
                        self.clicked = True
                    self.pressed = True
                else:
                    self.pressed = False
                self.stamina -= 0.25
            else:
                if round(self.x) != 320 or round(self.y) != 320:
                    dx = 320 - self.x
                    dy = 320 - self.y
                    self.x += dx / 32
                    self.y += dy / 32
                    if self.blink_delay > 0:
                        self.blink_delay -= 1
                    else:
                        if self.blink_count & 1:
                            self.image = checkbox
                        else:
                            self.image = checked
                        self.blink_count += 1
                        self.blink_delay = 15
                else:
                    self.x = 320
                    self.y = 320
                    self.stamina = 0
        elif game_state == GameState.TAG:
            dx = self.x - pos[0]
            dy = self.y - pos[1]
            dist = math.hypot(dx, dy)
            if dist == 0: dist = 1
            dx /= dist
            dy /= dist
            self.x -= dx * self.stamina / 1.125 # Slight slowing factor
            self.y -= dy * self.stamina / 1.125
            self.stamina += 0.0625
            if pos[0] > self.x - 32 and pos[0] < self.x + 32 and pos[1] > self.y - 32 and pos[1] < self.y + 32:
                print("> The check box tagged you.")
                pygame.quit()
                sys.exit()
        self.rect.center = (self.x, self.y)
        pygame.draw.line(screen, "green", (self.x, self.y), pos)

class Proceed(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = proceed
        self.x = x
        self.y = y
        self.rect = self.image.get_rect()
        self.rect.center = x, y
    def update(self):
        # Change state depending on the checkbox
        if spr_checkbox.checked:
            self.image = proceed_agreed
        else:
            self.image = proceed
        pos = pygame.mouse.get_pos()
        if pos[0] > self.x - 64 and pos[0] < self.x + 64 and pos[1] > self.y - 32 and pos[1] < self.y + 32 and self.image == proceed_agreed:
            global game_state
            game_state = GameState.CLICKED
            print("> You agreed to the Terms and Conditions.")
            self.kill()

class Warning(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = warning
        self.x = x
        self.y = y
        self.rect = warning.get_rect()
        self.rect.center = x, y

class Target(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = target
        self.x = x
        self.y = y
        self.rect = target.get_rect()
        self.rect.center = (x, y)
        # Statuses
        self.blinking = True
        self.blink_delay = 5
        self.blink_count = 0
        self.reached = False
    def update(self):
        if self.blinking:
            if self.blink_count & 1:
                self.image = target
            else:
                self.image = target_blink
            if self.blink_delay > 0:
                self.blink_delay -= 1
            else:
                self.blink_count += 1
                if self.blink_count < 12:
                    self.blink_delay = 5
                else:
                    self.blinking = False
        else:
            pos = pygame.mouse.get_pos()
            self.reached = False
            if pos[0] > self.x - 8 and pos[0] < self.x + 8:
                if pos[1] > self.y - 8 and pos[1] < self.y + 8:
                    self.reached = True
            if self.reached:
                global game_state
                if game_state == GameState.PRE_EVADE:
                    game_state = GameState.EVADE
                if game_state == GameState.PRE_TAG:
                    rogue.sprites()[0].stamina = 10
                    game_state = GameState.TAG
                if game_state == GameState.PRE_MATEIN3:
                    game_state = GameState.MATEIN3
                self.kill()

class Chessboard(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = chessboard
        self.x = x
        self.y = y-100
        self.speed_y = 0
        self.y_init = y
        self.rect = chessboard.get_rect()
        self.rect.center = (x, self.y)
        self.fallen = False
    def update(self):
        if not self.fallen:
            if self.y < self.y_init:
                self.y += self.speed_y
                self.speed_y += 1
            else:
                self.fallen = True
                self.y = self.y_init
        self.rect.center = self.x, self.y

class Piece(pygame.sprite.Sprite):
    def __init__(self, img, x, y, id):
        pygame.sprite.Sprite.__init__(self)
        self.image : pygame.Surface = img
        self.id = id
        self.x = 208 + x * 32
        self.y_init = 432 - y * 32
        self.y = self.y_init - 100
        self.can_draw = False
        self.speed_y = 0
        self.rect = img.get_rect()
        self.rect.center = (x, self.y)
        self.fallen = False
    def update(self):
        if not self.fallen:
            self.can_draw = True
            if self.y < self.y_init:
                self.y += self.speed_y
                self.speed_y += 1
            else:
                self.fallen = True
                self.y = self.y_init
        self.rect.center = self.x, self.y
    def draw(self, surface:pygame.Surface):
        if self.can_draw:
            surface.blit(self.image, self.rect)

class Pawn(Piece):
    def __init__(self, white:bool, x, y, id):
        super().__init__(pawn if white else pawn_black, x, y, id)

class Knight(Piece):
    def __init__(self, white:bool, x, y, id):
        super().__init__(knight if white else knight_black, x, y, id)

class Bishop(Piece):
    def __init__(self, white:bool, x, y, id):
        super().__init__(bishop if white else bishop_black, x, y, id)

class Rook(Piece):
    def __init__(self, white:bool, x, y, id):
        super().__init__(rook if white else rook_black, x, y, id)

class Queen(Piece):
    def __init__(self, white:bool, x, y, id):
        super().__init__(queen if white else queen_black, x, y, id)

class King(Piece):
    def __init__(self, white:bool, x, y, id):
        super().__init__(king if white else king_black, x, y, id)

# Menu
menu : pygame.sprite.Group = pygame.sprite.Group()
menu.add(Title(320, 240))
menu.add(Play(320, 420))

# Terms and Conditions
tac : pygame.sprite.Group = pygame.sprite.Group()
spr_checkbox = Checkbox(500, 494, "TaC")
tac.add(spr_checkbox)
tac.add(Proceed(320, 548))

# Warning Stage
warn_stage : pygame.sprite.Group = pygame.sprite.Group()
spr_captcha = Checkbox(320, 496, "CAPTCHA")
warn_stage.add(Warning(320, 180))

# Before Rogue
pre_surf : pygame.sprite.Group = pygame.sprite.Group()
target_surf = Target(500, 500)

def add_target():
    global target_surf
    target_surf.blinking = True
    target_surf.blink_count = 0
    target_surf.blink_delay = 5
    pre_surf.add(target_surf)
    global show_target
    show_target = True

# Rogue Checkbox
rogue : pygame.sprite.Group = pygame.sprite.Group()
spr_rogue = RogueCheckbox(320, 320)
rogue.add(spr_rogue)

gr_chess : pygame.sprite.Group = pygame.sprite.Group()
gr_chess.add(Chessboard(screen_width / 2, screen_height / 2))

# That's a lot of pieces
def add_pieces():
    gr_chess.add(Rook(True, 0, 0, 0))
    gr_chess.add(Bishop(True, 2, 0, 1))
    gr_chess.add(King(True, 4, 0, 2))
    gr_chess.add(Rook(True, 7, 0, 3))
    gr_chess.add(Bishop(True, 2, 1, 4))
    gr_chess.add(Pawn(True, 1, 2, 5))
    gr_chess.add(Pawn(True, 2, 2, 6))
    gr_chess.add(Pawn(True, 5, 3, 7))
    gr_chess.add(Knight(False, 5, 4, 8))
    gr_chess.add(Pawn(True, 6, 4, 9))
    gr_chess.add(Pawn(True, 7, 4, 10))
    gr_chess.add(Queen(False, 1, 5, 11))
    gr_chess.add(Knight(False, 2, 5, 12))
    gr_chess.add(Pawn(False, 4, 5, 13))
    gr_chess.add(Pawn(True, 5, 5, 14))
    gr_chess.add(Pawn(False, 6, 5, 15))
    gr_chess.add(Queen(True, 7, 5, 16))
    gr_chess.add(Pawn(False, 0, 6, 17))
    gr_chess.add(Pawn(False, 1, 6, 18))
    gr_chess.add(Bishop(False, 3, 6, 19))
    gr_chess.add(Pawn(False, 5, 6, 20))
    gr_chess.add(Pawn(False, 7, 6, 21))
    gr_chess.add(Rook(False, 0, 7, 22))
    gr_chess.add(Rook(False, 6, 7, 23))
    gr_chess.add(King(False, 7, 7, 24))

# I'm not gonna implement a chess engine just for this
def move_and_capture(piece_idx:int, gx:int, gy:int, capture_idx:int|None = None):
    for i in gr_chess.sprites()[1:]:
        if i.id == piece_idx:
            piece : Piece = i
    if capture_idx:
        for i in gr_chess.sprites()[1:]:
            if i.id == capture_idx:
                capture : Piece = i
        capture.kill()
    piece.x = 208 + gx * 32
    piece.y_init = 432 - gy * 32
    piece.y = piece.y_init - 100
    piece.fallen = False

######################
# PLAN BOARD
######################

# Stage 1 - Check box evades from you
# Stage 2 - Check box tries to tag you
# Stage 3 - Check box forces you to find a mate in 3 to proceed

# Finally able to access the service

######################
# SETTINGS
######################
game_state = GameState.MENU

# Delays (in frames)
TaC_delay_frame = 40
check_box_delay = 30
warn_delay = 30
evade_time = 600

# Box heights
TaC_height = 0
warn_height = 0
accessed_height = 0

# Mate in 3 input field
matein3_input = pygame.Rect(170, 450, 300, 30)
matein3_inputtxt = ""
color_inactive = "lightskyblue3"
color_active = "dodgerblue2"
col = color_inactive
active = False
solution = ["Qxh7+", "hxg6+", "Rhh6#"]
move_idx = 0
move_delay = 0

######################
# MAIN
######################
show_target = False

while running:
    # Wipe stuff from previous frame
    screen.fill((40, 43, 64))

    # Update menu
    if game_state in [GameState.MENU, GameState.STARTUP, GameState.TERMSANDCONDITIONS, GameState.CLICKED]:
        menu.update()
        menu.draw(screen)

    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            print("> You quit VERIFY. Thanks for using it!")
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == pygame.BUTTON_LEFT:
            if game_state == GameState.TERMSANDCONDITIONS:
                tac.update()
            elif game_state == GameState.WARNING:
                warn_stage.update()
            elif game_state == GameState.PRE_EVADE:
                if len(pre_evade_text.text_render[-1]) == len(pre_evade_text.text[-1]):
                    try:
                        pre_evade_text = next(pre_evade_texts)
                    except StopIteration:
                        add_target()
            elif game_state == GameState.PRE_TAG:
                if len(pre_tag_text.text_render[-1]) == len(pre_tag_text.text[-1]):
                    try:
                        pre_tag_text = next(pre_tag_texts)
                    except StopIteration:
                        add_target()
            elif game_state == GameState.PRE_MATEIN3:
                if len(pre_matein3_txt.text_render[-1]) == len(pre_matein3_txt.text[-1]):
                    try:
                        pre_matein3_txt = next(pre_matein3_texts)
                    except StopIteration:
                        pre_surf.add(GameCheckbox(500, 500))
                        show_target = True
            elif game_state == GameState.ACCESS:
                if len(welcome_text.text_render[-1]) == len(welcome_text.text[-1]):
                    try:
                        welcome_text = next(welcome_dialogue)
                    except StopIteration:
                        print("> You beat VERIFY.")
                        running = False
            elif game_state == GameState.PRE_ACCESS:
                if len(success_text.text_render[-1]) == len(success_text.text[-1]):
                    print("> Welcome.")
                    game_state = GameState.ACCESS
            elif game_state == GameState.MATEIN3:
                if matein3_input.collidepoint(event.pos):
                    active = not active
                else:
                    active = False
                if move_delay > 0:
                    active = False
                col = color_active if active else color_inactive
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
                print("> You quit VERIFY. Thanks for using it!")
            else:
                if active:
                    if event.key == pygame.K_RETURN:
                        if solution[move_idx] == matein3_inputtxt:
                            move_idx += 1
                            move_delay = 30
                            if move_idx == 1:
                                move_and_capture(16, 7, 6, 21)
                            elif move_idx == 2:
                                move_and_capture(10, 6, 5, 15)
                            elif move_idx == 3:
                                move_and_capture(3, 7, 5)
                            print("> Correct!")
                        else:
                            move_idx = 0
                            print("> Wrong. Try again.")
                            matein3_text.text_render[1] = "Mate in 3."
                            gr_chess = pygame.sprite.Group()
                            gr_chess.add(Chessboard(screen_width / 2, screen_height / 2))
                            add_pieces()
                        matein3_inputtxt = ""
                    elif event.key == pygame.K_BACKSPACE:
                        matein3_inputtxt = matein3_inputtxt[:-1]
                    else:
                        matein3_inputtxt += event.unicode

    # Draw rectangle for Terms and Conditions
    if game_state == GameState.STARTUP:
        if TaC_delay_frame > 0:
            TaC_delay_frame -= 1
        else:
            if TaC_height < 420:
                TaC_height += 5
            else:
                game_state = GameState.TERMSANDCONDITIONS
            TaC = pygame.Rect(100, 180, 440, TaC_height)
            pygame.draw.rect(screen, (202, 207, 214, 200), TaC)

    # Draw Terms and Conditions
    elif game_state == GameState.TERMSANDCONDITIONS:
        pygame.display.set_caption("Terms and Conditions")
        TaC = pygame.Rect(100, 180, 440, TaC_height)
        pygame.draw.rect(screen, (202, 207, 214, 200), TaC)
        draw_text(terms_and_conditions, "black", 115, 200, False)
        if terms_and_conditions.row == len(tac_text):
            if check_box_delay > 0:
                check_box_delay -= 1
            else:
                tac.draw(screen)
    
    # Draw Loading Text
    elif game_state == GameState.CLICKED:
        pygame.mouse.set_cursor(pygame.cursors.broken_x)
        pygame.mouse.set_visible(False)
        if load_count < 6:
            pygame.display.set_caption("VERIFY - Please the CAPTCHA!")
            draw_text(loading_text, "white", 320, 320, True, True)
        else:
            if warn_delay > 0:
                warn_delay -= 1
            else:
                if warn_height < 320:
                    warn_height += 5
                else:
                    print("> Uh oh. Something has gone wrong. (403 Forbidden)")
                    game_state = GameState.WARNING
                screen.fill((100, 0, 0))
                warn_box = pygame.Rect(100, 230, 440, warn_height)
                pygame.draw.rect(screen, (255, 207, 214, 200), warn_box)
                pygame.draw.rect(screen, "red", warn_box, 2)
                warn_stage.draw(screen)
    
    # Draw Warning Stage
    elif game_state == GameState.WARNING:
        pygame.display.set_caption("403 Forbidden")
        screen.fill((100, 0, 0))
        warn_box = pygame.Rect(100, 230, 440, warn_height)
        pygame.draw.rect(screen, (255, 207, 214, 200), warn_box)
        pygame.draw.rect(screen, "red", warn_box, 2)
        draw_text(warn_text, "red", 320, 280, True)
        if warn_text.row == len(warn) and spr_captcha not in warn_stage.sprites():
            pygame.mouse.set_visible(True)
            warn_stage.add(spr_captcha)
        warn_stage.draw(screen)

    # Stage 1 - Evade
    elif game_state == GameState.PRE_EVADE:
        screen.fill("black")
        if show_target:
            pygame.display.set_caption("Move your cursor to the target.")
            pre_surf.update()
            pre_surf.draw(screen)
        else:
            draw_text(pre_evade_text, "white", 320, 320, True, True)
            pygame.display.set_caption("Click to continue.")
    elif game_state == GameState.EVADE:
        show_target = False
        pygame.display.set_caption("Try to tag the check box by moving the cursor!")
        if rogue.sprites()[0].stamina > 0:
            rogue.update()
            rogue.draw(screen)
        else:
            if rogue.sprites()[0].clicked == False:
                print("> You did not tag the check box.")
                running = False
            else:
                game_state = GameState.PRE_TAG
    
    # Stage 2 - Tag
    elif game_state == GameState.PRE_TAG:
        screen.fill("black")
        if show_target:
            pygame.display.set_caption("Move your cursor to the target.")
            pre_surf.update()
            pre_surf.draw(screen)
        else:
            pygame.display.set_caption("Click to continue.")
            draw_text(pre_tag_text, "white", 320, 320, True, True)
    elif game_state == GameState.TAG:
        show_target = False
        pygame.display.set_caption("Move your cursor away from the checkbox!")
        if rogue.sprites()[0].stamina < 20:
            rogue.update()
            rogue.draw(screen)
        else:
            print("> Good job. You survived.\n  It won't give up easily. Be alert.")
            game_state = GameState.PRE_MATEIN3

    # Stage 3 - Find Mate in 3
    elif game_state == GameState.PRE_MATEIN3:
        screen.fill("black")
        if show_target:
            pygame.display.set_caption("Click on the checkbox to conitnue. No tricks this time.")
            pre_surf.update()
            pre_surf.draw(screen)
        else:
            pygame.display.set_caption("Click to continue.")
            draw_text(pre_matein3_txt, "white", 320, 320, True, True)
    elif game_state == GameState.MATEIN3:
        draw_text(matein3_text, "white", 320, 50, True, True)
        pygame.display.set_caption("Find the checkmate in 3 moves for white.")
        gr_chess.update()
        if gr_chess.sprites()[0].fallen and len(gr_chess.sprites()) == 1:
            add_pieces()
        gr_chess.draw(screen)
        txt_surf = font.render(matein3_inputtxt, True, "white")
        # Resize the box if the text is too long.
        width = max(300, txt_surf.get_width()+10)
        matein3_input.w = width
        # Blit the text.
        screen.blit(txt_surf, (matein3_input.x+5, matein3_input.y+5))
        # Blit the input_box rect.
        pygame.draw.rect(screen, col, matein3_input, 2)
        if move_delay > 0:
            move_delay -= 1
            if move_delay == 0:
                if move_idx == 1:
                    move_and_capture(24, 7, 6, 16)
                    matein3_text.text_render[1] = "Mate in 2."
                if move_idx == 2:
                    move_and_capture(24, 6, 5, 10)
                    matein3_text.text_render[1] = "Mate in 1."
                if move_idx == 3:
                    print("> Checkmate!")
                    game_state = GameState.PRE_ACCESS
    
    # Pre-access
    elif game_state == GameState.PRE_ACCESS:
        pygame.display.set_caption("Click to continue.")
        screen.fill("black")
        draw_text(success_text, "white", 320, 320, True, True)
    
    # Accessed
    elif game_state == GameState.ACCESS:
        pygame.display.set_caption("Welcome.")
        if accessed_height < 420: accessed_height += 8
        else: accessed_height = 420
        box = pygame.Rect(120, 110, 400, accessed_height)
        pygame.draw.rect(screen, "white", box)
        if accessed_height == 420:
            draw_text(welcome_text, "black", 140, 130, False, False)
    
    # Update display
    pygame.display.flip()
    clock.tick(60) # Limit FPS to 60
pygame.quit()