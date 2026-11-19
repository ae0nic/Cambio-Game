import pygame
import math
from cards import *
from player import Player
import random
from cambio import Cambio

screen = pygame.Surface((1,1))
mask_colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0), (255, 0, 255), (0, 255, 255)]

def create_masks(size):
    masks = {}
    line_thickness = 2
    line_density = [35, 20, 13, 10, 5, 3]
    for i,c in enumerate(mask_colors):
        m = pygame.Surface(size)
        m.fill((0,0,0))
        m.set_colorkey((0,0,0))
        for j in range(2 * math.ceil(size[0] / line_density[i])):
            pygame.draw.line(m, (255, 255, 255), (size[0] - j * line_density[i], 0), (size[0], j * line_density[i]), width=line_thickness)
            pygame.draw.line(m, (255, 255, 255), (size[0] - j * line_density[i], size[1]), (size[0], size[1] - j * line_density[i]), width=line_thickness)
        masks[c] = pygame.mask.from_surface(m)
    return masks

def apply_masks(surface, masks, offset, line_color=(0,0,0,160)):
    mask_surface = pygame.Surface(surface.size, flags=pygame.SRCALPHA)
    mask_surface.fill((127,127,127,0))
    for i,c in enumerate(mask_colors):
        m = pygame.mask.from_threshold(surface, c, threshold=(1,1,1,1))
        c_area = pygame.mask.from_surface(surface)
        c_area.fill()
        m2 = masks[c]
        overlap = m.overlap_mask(m2, offset=offset)
        c_surface = pygame.Surface(surface.size, flags=pygame.SRCALPHA)
        c_surface.blit(m2.overlap_mask(m, offset=offset).to_surface(unsetcolor=(0,0,0,0), setcolor=line_color), (-offset[0], -offset[1]))
        mask_surface.blit(c_surface)
    return mask_surface

CARD_SIZE = (80, 112)
def draw_card_back(masks, offset, using = None, rot=0):
    card_round = None
    card_base = None
    card_surface = None
    if using == None:
        card_round = pygame.Surface(CARD_SIZE, flags=pygame.SRCALPHA)
        card_base = pygame.Surface(CARD_SIZE, flags=pygame.SRCALPHA)
        card_surface = pygame.Surface(CARD_SIZE, flags=pygame.SRCALPHA)
    else:
        card_base = using[0]
        card_round = using[1]
        card_surface = using[2]
    card_base.fill((50, 70, 123, 255))
    card_round.fill((0,0,0,0))
    pygame.draw.rect(card_round, (255,255,255,255), pygame.Rect(0,0,CARD_SIZE[0],CARD_SIZE[1]), border_radius=7)
    card_surface.fill((0, 255, 255, 255))
    pygame.draw.rect(card_surface, (0, 0, 255, 255), pygame.Rect(5, 5, CARD_SIZE[0]-10, CARD_SIZE[1]-10))
    card_base = pygame.transform.rotate(card_base, rot)
    card_surface = pygame.transform.rotate(card_surface, rot)
    card_round = pygame.transform.rotate(card_round, rot)
    s = apply_masks(card_surface, masks, offset)
    card_base.blit(s)
    card_round.blit(card_base, special_flags=pygame.BLEND_RGBA_MULT)
    return card_round

suits={"Hearts": "♥", "Diamonds": "♦", "Clubs": "♣", "Spades": "♠"}
colors={"Hearts": (164, 40, 40, 255), "Diamonds": (163, 143, 21, 255), "Clubs": (24, 134, 34, 255), "Spades": (37, 21, 101, 255), "Joker": (0, 0, 0, 255)}
patterns = {"2":"020","3":"030","4":"202","5":"212","6":"303","7":"313","8":"323","9":"414","10":"424"}
font = None
small_font = None
large_font = None
small_text_font = None
text_font = None
def draw_card_front(card, masks, offset, using = None, rot=0):
    global suits
    global colors
    global patterns
    global font
    global small_text_font
    global small_font
    global text_font
    global large_text_font
    card_round = None
    card_base = None
    card_surface = None
    if using == None:
        card_round = pygame.Surface(CARD_SIZE, flags=pygame.SRCALPHA)
        card_base = pygame.Surface(CARD_SIZE, flags=pygame.SRCALPHA)
        card_surface = pygame.Surface(CARD_SIZE, flags=pygame.SRCALPHA)
    else:
        card_base = using[3]
        card_round = using[4]
        card_surface = using[5]
    card_base.fill((246, 236, 205, 255))
    card_round.fill((0,0,0,0))
    pygame.draw.rect(card_round, (255,255,255,255), pygame.Rect(0,0,CARD_SIZE[0],CARD_SIZE[1]), border_radius=7)

    if card.suit == "Joker":
        text = text_font.render("Joker!", False, (0, 255, 255, 255))
        card_surface.blit(text, (CARD_SIZE[0] / 2 - text.size[0] / 2, CARD_SIZE[1] / 2 - text.size[1] / 2))
    else:
        suit = suits[card.suit]
        rank = card.rank
        if rank in patterns: # Non-face card
            pattern = patterns[rank]
            left_spacing = int(pattern[0])
            mid_spacing = int(pattern[1])
            for i in range(left_spacing):
                up = i < (left_spacing + 1) // 2
                text = font.render(suit, False, (255,0,255,255))
                up_adjustment = 0
                if not up:
                    up_adjustment = -8
                    text = pygame.transform.flip(text, False, True)
                diamonds_adjustment = -2 if card.suit == "Diamonds" else 0
                card_surface.blit(text, (25 - text.size[0] / 2, i * ((CARD_SIZE[1] - 40) / (left_spacing - 1)) + text.size[1] / 2 + diamonds_adjustment + up_adjustment))
                card_surface.blit(text, (CARD_SIZE[0] - 25 - text.size[0] / 2, i * ((CARD_SIZE[1] - 40) / (left_spacing - 1)) + text.size[1] / 2 + diamonds_adjustment + up_adjustment))
                #pygame.draw.line(card_base, (0, 0, 255), (0, i * ((CARD_SIZE[1] - 40) / (left_spacing - 1)) + text.size[1] / 2 + diamonds_adjustment), (CARD_SIZE[0], i * ((CARD_SIZE[1] - 40) / (left_spacing - 1)) + text.size[1] / 2 + diamonds_adjustment), 2)
            for i in range(mid_spacing):
                up = i < (mid_spacing + 1) // 2
                text = font.render(suit, False, (255,0,255,255))
                up_adjustment = 0
                if not up:
                    up_adjustment = -8
                    text = pygame.transform.flip(text, False, True)
                diamonds_adjustment = -2 if card.suit == "Diamonds" else 0
                rows = 0
                start_row = 0
                row_step = 1
                match int(rank):
                    case 2:
                        rows = 3
                        row_step = 2
                    case 3:
                        rows = 3
                    case 5 | 9:
                        rows = 3
                        start_row = 1
                    case 7 | 8:
                        rows = 5
                        start_row = 1
                        row_step = 2
                    case 10:
                        rows = 7
                        start_row = 1
                        row_step = 4
                c_row = start_row + i * row_step
                card_surface.blit(text, (CARD_SIZE[0] / 2 - text.size[0] / 2, c_row * ((CARD_SIZE[1] - 40) / (rows - 1)) + text.size[1] / 2 + diamonds_adjustment + up_adjustment))

        else: # Face card
            if rank == "Ace":
                text = large_font.render(suit, False, (255, 0, 255, 255))
                card_surface.blit(text, (CARD_SIZE[0] / 2 - text.size[0] / 2, CARD_SIZE[1] / 2 - text.size[1] / 2 + 10))
            elif rank == "Joker":
                pass
            else:
                letter = rank[0]
                text = large_text_font.render(letter, False, (255, 0, 255, 255))
                card_surface.blit(text, (CARD_SIZE[0] / 2 - text.size[0] / 2, CARD_SIZE[1] / 2 - text.size[1] / 2))

        small_text_font.set_bold(True)
        card_surface.blit(small_text_font.render(rank[0] if len(rank) > 2 else rank, False, (0, 255, 255)), (6, 5))
        card_surface.blit(small_font.render(suit, False, (0, 255, 255)), (5, 17))
        card_surface.blit(pygame.transform.rotate(small_text_font.render(rank[0] if len(rank) > 2 else rank, False, (0, 255, 255)), 180), (CARD_SIZE[0] - 12, CARD_SIZE[1] - 17))
        card_surface.blit(pygame.transform.rotate(small_font.render(suit, False, (0, 255, 255)), 180), (CARD_SIZE[0] - 13, CARD_SIZE[1] - 29))
    
    card_base = pygame.transform.rotate(card_base, rot)
    card_surface = pygame.transform.rotate(card_surface, rot)
    card_round = pygame.transform.rotate(card_round, rot)
    small_text_font.set_bold(False)
    s = apply_masks(card_surface, masks, offset, line_color = colors[card.suit])
    card_base.blit(s)
    card_round.blit(card_base, special_flags=pygame.BLEND_RGBA_MULT)
    return card_round

def draw_card_inventory(screen, masks, cards, surfaces, pid=0):
    num = len(cards)
    boundary_1 = (screen.size[0] // 2 - 160, screen.size[1] - 220)
    boundary_2 = (screen.size[0] // 2 + 160, screen.size[1] - 220)
    if pid == 1: 
        boundary_1 = (220, screen.size[1] // 2 - 160)
        boundary_2 = (220, screen.size[1] // 2 + 160)
    elif pid == 2:
        boundary_1 = (screen.size[0] // 2 + 160, 220)
        boundary_2 = (screen.size[0] // 2 - 160, 220)
    elif pid == 3:
        boundary_1 = (screen.size[0] - 220, screen.size[1] // 2 + 160)
        boundary_2 = (screen.size[0] - 220, screen.size[1] // 2 - 160)
    size = abs((boundary_2[0] - boundary_1[0]) + (boundary_2[1] - boundary_1[1]))

    columns = math.ceil(num / 2)
    step = size / (columns + 1)
    direction = (step, 0)
    top_mod = (0, 140)
    rotation = 0
    if pid == 1:
        direction = (0, step)
        top_mod = (-140, 0)
        rotation = 270
    elif pid == 2:
        direction = (-step, 0)
        top_mod = (0, -140)
        rotation = 180
    elif pid == 3:
        direction = (0, -step)
        top_mod = (140, 0)
        rotation = 90

    card_adjustment = (-CARD_SIZE[0] / 2, -CARD_SIZE[1] / 2)

    for i in range(num):
        c, face_up = cards[i]
        column = (i // 2)
        pos = (boundary_1[0] + direction[0] * (column + 1), boundary_1[1] + direction[1] * (column + 1))
        if i == num - 1 and num % 2 != 0:
            pos = (pos[0] + top_mod[0] / 2, pos[1] + top_mod[1] / 2) 
            if face_up:
                card = draw_card_front(c, masks, (pos[0] + card_adjustment[0],pos[1] + card_adjustment[1]), rot=rotation)
            else:
                card = draw_card_back(masks, (pos[0] + card_adjustment[0],pos[1] + card_adjustment[1]), rot=rotation)
            pos = (pos[0] - card.size[0] / 2, pos[1] - card.size[1] / 2)
            screen.blit(card, pos)
        else:
            top = i % 2 == 0
            pos = (pos[0] + top_mod[0], pos[1] + top_mod[1]) if top else pos
            if face_up:
                card = draw_card_front(c, masks, (pos[0] + card_adjustment[0],pos[1] + card_adjustment[1]), rot=rotation)
            else:
                card = draw_card_back(masks, (pos[0] + card_adjustment[0],pos[1] + card_adjustment[1]), rot=rotation)
            pos = (pos[0] - card.size[0] / 2, pos[1] - card.size[1] / 2)
            screen.blit(card, pos)

def generate_card_surfaces(deck):
    card_to_surf = {}
    # Generate card surfaces
    for c in deck.cards:
        base = pygame.Surface(CARD_SIZE)
        rounded = pygame.Surface(CARD_SIZE, flags=pygame.SRCALPHA)
        surf = pygame.Surface(CARD_SIZE)
        
        base_front = pygame.Surface(CARD_SIZE)
        rounded_front = pygame.Surface(CARD_SIZE, flags=pygame.SRCALPHA)
        surf_front = pygame.Surface(CARD_SIZE)

        rounded.fill((0,0,0,0))
        rounded_front.fill((0,0,0,0))
        pygame.draw.rect(rounded, (255,255,255,255), pygame.Rect(0,0,CARD_SIZE[0],CARD_SIZE[1]), border_radius=7)
        pygame.draw.rect(rounded_front, (255,255,255,255), pygame.Rect(0,0,CARD_SIZE[0],CARD_SIZE[1]), border_radius=7)
        base.fill((50, 70, 123, 255))
        base_front.fill((246, 236, 205, 255))
        surf.fill((0, 255, 255, 255))
        surf_front.fill((0, 0, 0, 255))
        pygame.draw.rect(surf, (0, 0, 255, 255), pygame.Rect(5, 5, CARD_SIZE[0]-10, CARD_SIZE[1]-10))
        card_to_surf[c]=(base, rounded, surf, base_front, rounded_front, surf_front)
    return card_to_surf

game = None
masks = None
clock = None
def update():
    global screen
    global masks
    global clock
    global game
    screen.fill(0x6E355A)
    for i, p in enumerate(game.get_players()):
        screen.blit(draw_card_back(masks, (460, 240)), (460, 240))
        screen.blit(draw_card_back(masks, (465, 235)), (465, 235))
        screen.blit(draw_card_back(masks, (470, 230)), (470, 230))
        screen.blit(draw_card_front(game.get_discard(), masks, (430, 240)), (430, 240))
        draw_card_inventory(screen, masks, [(c, c.face_up) for c in p.get_cards()], None, i)
        pygame.display.flip()
        clock.tick(60)

def main():
    global screen
    global masks
    global clock
    global font
    global text_font
    global small_font
    global large_font
    global small_text_font
    global large_text_font
    global game
    pygame.init()
    running = True
    clock = pygame.Clock()
    WIDTH = 960
    HEIGHT = 720
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    masks = create_masks(screen.get_size())
    deck = Deck()
    deck.shuffle()
    cards = []
    screen.fill(0x6E355A)
    pygame.display.flip()
    

    players_count = int(input("How many players are playing the game? (2-4) "))
    game = Cambio(players_count)
    players_names = []
    for i in range(players_count):
        players_names += [input(f"Enter the name of player {i + 1}: ")]
    game.initialize_players(players_names)
    starter = input("Enter the name of the starting player: ")
    game.set_starting_player(starter)
    game.deal_starting_hands()

    

    card_to_surf = generate_card_surfaces(deck)

    f_name = "opensymbol" if "opensymbol" in pygame.font.get_fonts() else "timesnewroman"
    font = pygame.font.SysFont(f_name, 24)
    text_font = pygame.font.SysFont("timesnewroman", 24)
    small_font = pygame.font.SysFont(f_name, 12)
    small_text_font = pygame.font.SysFont("timesnewroman", 12)
    large_font = pygame.font.SysFont(f_name, 48)
    large_text_font = pygame.font.SysFont("timesnewroman", 48)

    game.start_game(update)
    while running:
        mx, my = pygame.mouse.get_pos()
        key_pressed = None
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        screen.fill(0x6E355A)

        for i, p in enumerate(game.get_players()):
            draw_card_inventory(screen, masks, [(c, c.face_up) for c in p.get_cards()], card_to_surf, i)
        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()
