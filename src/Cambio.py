# By submitting this assignment, I agree to the following:
#   "Aggies do not lie, cheat, or steal, or tolerate those who do."
#   "I have not given or received any unauthorized aid on this assignment."
#
# Names:        Benjamin Conley
#               Luke Petric
#               Lucas Allwein
#               Cristian Godinez
# Section:      215
# Assignment:   Lab 13 Team
# Date:         11 13 2026

import random
from src.deck import *
from src.player import Player

# dictionary helping calculate how much each card is worth in points
card_points = {"Jack": 10,
               "Queen": 10,
               "Joker": 0,
               "Ace": 1
               }

def count_points(player):
    """"Calculates the amount of points a player has"""
    points = 0
    cards = player.get_cards()
    for card in cards:
        data = str(card).split(" ")
        try:
            points += int(data[0])
        except:
            if str(data[0]) != "King":
                points += card_points[str(data[0])]
            else:
                if "Spade" in str(data) or "Clubs" in str(data):
                    points += 10
                else:
                    points -= 1
    return points

def turn_logic(player, turn):
    """Deals with all the possible decisions a player could make
       on their turn. Needs support from the function dealing with
       the cards with special abilities"""
    card = deck.deal()
    if turn == 1:
        cards = p1.get_cards()
        decision = input(f"{p1_name}, do you want to swap the {card} with one of your cards, discard, or call cambio? (swap, discard, Cambio): ").lower()
        if decision == "swap":
            position = int(input("Which card would you like to swap? (1,2,3...) "))
            cards[position-1] = card
            p1.set_cards(cards)
        turn += 1
        if decision == "cambio":
            return "cambio"
        else:
            return turn
    elif turn == 2:
        cards = p2.get_cards()
        decision = input(f"{p2_name}, do you want to swap the {card} with one of your cards, discard, or call cambio? (swap, discard, Cambio): ").lower()
        if decision == "swap":
            position = int(input("Which card would you like to swap? (1,2,3...) "))
            cards[position-1] = card
            p2.set_cards(cards)
        turn += 1
        if decision == "cambio":
            return "cambio"
        if turn-1 == amount_players:
            turn = 1
        else:
            return turn
    elif turn == 3:
        cards = p3.get_cards()
        decision = input(f"{p3_name}, do you want to swap the {card} with one of your cards, discard, or call cambio? (swap, discard, Cambio): ").lower()
        if decision == "swap":
            position = int(input("Which card would you like to swap? (1,2,3...) "))
            cards[position-1] = card
            p3.set_cards(cards)
        turn += 1 
        if decision == "cambio":
            return "cambio"
        if turn-1 == amount_players:
            turn = 1
        else:
            return turn
    elif turn == 4:
        cards = p4.get_cards()
        decision = input(f"{p4_name}, do you want to swap the {card} with one of your cards, discard, or call cambio? (swap, discard, Cambio): ").lower()
        if decision == "swap":
            position = int(input("Which card would you like to swap? (1,2,3...) "))
            cards[position-1] = card
            p4.set_cards(cards)
        turn += 1
        if decision == "cambio":
            return "cambio"
        if turn-1 == amount_players:
            turn = 1
        else:
            return turn
    elif turn == 5:
        cards = p5.get_cards()
        decision = input(f"{p5_name}, do you want to swap the {card} with one of your cards, discard, or call cambio? (swap, discard, Cambio): ").lower()
        if decision == "swap":
            position = int(input("Which card would you like to swap? (1,2,3...) "))
            cards[position-1] = card
            p5.set_cards(cards)
        turn += 1
        if decision == "cambio":
            return "cambio"
        if turn-1 == amount_players:
            turn = 1
        else:
            return turn
    elif turn == 6:
        cards = p6.get_cards()
        decision = input(f"{p6_name}, do you want to swap the {card} with one of your cards, discard, or call cambio? (swap, discard, Cambio): ").lower()
        if decision == "swap":
            position = int(input("Which card would you like to swap? (1,2,3...) "))
            cards[position-1] = card
            p6.set_cards(cards)
        turn += 1
        if decision == "cambio":
            return "cambio"
        if turn-1 == amount_players:
            turn = 1
        else:
            return turn
def first_turn_logic(player, turn):
    """"Gives the player information about their bottom 2 cards """
    if turn == 1:
        print(f"{p1_name}, your two bottom cards are the {p1.get_cards()[2]} and the {p1.get_cards()[3]}")
    if turn == 2:
        print(f"{p2_name}, your two bottom cards are the {p1.get_cards()[2]} and the {p1.get_cards()[3]}")
    if turn == 3:
        print(f"{p3_name}, your two bottom cards are the {p1.get_cards()[2]} and the {p1.get_cards()[3]}")
    if turn == 4:
        print(f"{p4_name}, your two bottom cards are the {p1.get_cards()[2]} and the {p1.get_cards()[3]}")
    if turn == 5:
        print(f"{p5_name}, your two bottom cards are the {p1.get_cards()[2]} and the {p1.get_cards()[3]}")
    if turn == 6:
        print(f"{p6_name}, your two bottom cards are the {p1.get_cards()[2]} and the {p1.get_cards()[3]}")

# starts game set up by shuffling deck
deck = Deck()
deck.shuffle()

# gets input from player
amount_players = int(input("How many players are playing the game? (2-6): "))
turn = int(input("Which player starts? "))

# sets initial conditions for variables
running = True
hand_1 = []
hand_2 = []
hand_3 = []
hand_4 = []
hand_5 = []
hand_6 = []

final_turn_1 = False
final_turn_2 = False
final_turn_3 = False
final_turn_4 = False
final_turn_5 = False
final_turn_6 = False

# creates hands for each player in the game
if amount_players == 2:
    # get player names
    p1_name = input("What is player 1's name? ")
    p2_name = input("What is player 2's name? ")
    p1 = Player(p1_name)
    p2 = Player(p2_name)
    
    # draw cards for players
    for i in range(4):
        hand_1.append(deck.deal())
        hand_2.append(deck.deal())
    p1.add_cards(hand_1)
    p2.add_cards(hand_2)
    
    # more variables
    p1_first_turn = True
    p2_first_turn = True
elif amount_players == 3:
    # get player names
    p1_name = input("What is player 1's name? ")
    p2_name = input("What is player 2's name? ")
    p3_name = input("What is player 3's name? ")
    p1 = Player(p1_name)
    p2 = Player(p2_name)
    p3 = Player(p3_name)
    
    # draw cards for players
    for i in range(4):
        hand_1.append(deck.deal())
        hand_2.append(deck.deal())
        hand_3.append(deck.deal())
    p1.add_cards(hand_1)
    p2.add_cards(hand_2)
    p3.add_cards(hand_3)
    
    # more variables
    p1_first_turn = True
    p2_first_turn = True
    p3_first_turn = True

elif amount_players == 4:
    # get player names
    p1_name = input("What is player 1's name? ")
    p2_name = input("What is player 2's name? ")
    p3_name = input("What is player 3's name? ")
    p4_name = input("What is player 4's name? ")
    p1 = Player(p1_name)
    p2 = Player(p2_name)
    p3 = Player(p3_name)
    p4 = Player(p4_name)
    
    # draw cards for players
    for i in range(4):
        hand_1.append(deck.deal())
        hand_2.append(deck.deal())
        hand_3.append(deck.deal())
        hand_4.append(deck.deal())
    p1.add_cards(hand_1)
    p2.add_cards(hand_2)
    p3.add_cards(hand_3)
    p4.add_cards(hand_4)
    
    # more variables
    p1_first_turn = True
    p2_first_turn = True
    p3_first_turn = True
    p4_first_turn = True
    
elif amount_players == 5:
    # get player names
    p1_name = input("What is player 1's name? ")
    p2_name = input("What is player 2's name? ")
    p3_name = input("What is player 3's name? ")
    p4_name = input("What is player 4's name? ")
    p5_name = input("What is player 5's name? ")
    p1 = Player(p1_name)
    p2 = Player(p2_name)
    p3 = Player(p3_name)
    p4 = Player(p4_name)
    p5 = Player(p5_name)
    
    # draw cards for players
    for i in range(4):
        hand_1.append(deck.deal())
        hand_2.append(deck.deal())
        hand_3.append(deck.deal())
        hand_4.append(deck.deal())
        hand_5.append(deck.deal())
    p1.add_cards(hand_1)
    p2.add_cards(hand_2)
    p3.add_cards(hand_3)
    p4.add_cards(hand_4)
    p5.add_cards(hand_5)
    
    # more variables
    p1_first_turn = True
    p2_first_turn = True
    p3_first_turn = True
    p4_first_turn = True
    p5_first_turn = True

elif amount_players == 6:
    # get player names
    p1_name = input("What is player 1's name? ")
    p2_name = input("What is player 2's name? ")
    p3_name = input("What is player 3's name? ")
    p4_name = input("What is player 4's name? ")
    p5_name = input("What is player 5's name? ")
    p6_name = input("What is player 6's name? ")
    p1 = Player(p1_name)
    p2 = Player(p2_name)
    p3 = Player(p3_name)
    p4 = Player(p4_name)
    p5 = Player(p5_name)
    p6 = Player(p6_name)
    
    # draw cards for players
    for i in range(4):
        hand_1.append(deck.deal())
        hand_2.append(deck.deal())
        hand_3.append(deck.deal())
        hand_4.append(deck.deal())
        hand_5.append(deck.deal())
        hand_6.append(deck.deal())
    p1.add_cards(hand_1)
    p2.add_cards(hand_2)
    p3.add_cards(hand_3)
    p4.add_cards(hand_4)
    p5.add_cards(hand_5)
    p6.add_cards(hand_6)
    
    # more variables
    p1_first_turn = True
    p2_first_turn = True
    p3_first_turn = True
    p4_first_turn = True
    p5_first_turn = True
    p6_first_turn = True



# loop while game is running
while running == True:
    # checks if the player called cambio on the previous turn
    if final_turn_1 == True:
        break
    if turn == 1:
        # checks if this is the first turn
        if p1_first_turn == True:
            first_turn_logic(p1, turn)
            p1_first_turn = False
        turn = turn_logic(p1, turn)
        if turn == "cambio":
            turn = 2
            final_turn_1 = True
        else:
            continue
    # checks if the player called cambio on the previous turn
    if final_turn_2 == True:
        break
    elif turn == 2:
        # checks if this is the first turn
        if p2_first_turn == True:
            first_turn_logic(p2, turn)
            p2_first_turn = False
        turn = turn_logic(p2, turn)
        if turn == "cambio":
            turn = 3
            final_turn_2 = True
            if turn == amount_players:
                turn = 1
        else:
            continue 
    # checks if the player called cambio on the previous turn
    if final_turn_3 == True:
        break
    elif turn == 3:
        # checks if this is the first turn
        if p3_first_turn == True:
            first_turn_logic(p3, turn)
            p3_first_turn = False
        turn = turn_logic(p3, turn)
        if turn == "cambio":
            turn = 4
            final_turn_3 = True
            if turn == amount_players:
                turn = 1
        else:
            continue
    # checks if the player called cambio on the previous turn
    if final_turn_4 == True:
        break
    elif turn == 4:
        # checks if this is the first turn
        if p4_first_turn == True:
            first_turn_logic(p4, turn)
            p4_first_turn = False
        turn = turn_logic(p4, turn)
        if turn == "cambio":
            turn = 5
            final_turn_4 = True
            if turn == amount_players:
                turn = 1
        else:
            continue
    # checks if the player called cambio on the previous turn
    if final_turn_5 == True:
        break
    elif turn == 5:
        # checks if this is the first turn
        if p5_first_turn == True:
            first_turn_logic(p5, turn)
            p5_first_turn = False
        turn = turn_logic(p5, turn)
        if turn == "cambio":
            turn = 6
            final_turn_5 = True
            if turn == amount_players:
                turn = 1
        else:
            continue
    # checks if the player called cambio on the previous turn
    if final_turn_6 == True:
        break
    elif turn == 6:
        # checks if this is the first turn
        if p6_first_turn == True:
            first_turn_logic(p6, turn)
            p6_first_turn = False
        turn = turn_logic(p6, turn)
        if turn == "cambio":
            turn = 1
            final_turn_6 = True
        else:
            continue

if amount_players == 2:
    p1.change_points(count_points(p1))
    p2.change_points(count_points(p2))
    print(f"Final game stats were: {p1} \n {p2}")
if amount_players == 3:
    p1.change_points(count_points(p1))
    p2.change_points(count_points(p2))
    p3.change_points(count_points(p3))
    print(f"Final game stats were: {p1} \n {p2} \n {p3}")
if amount_players == 4:
    p1.change_points(count_points(p1))
    p2.change_points(count_points(p2))
    p3.change_points(count_points(p3))
    p4.change_points(count_points(p4))
    print(f"Final game stats were: {p1} \n {p2} \n {p3} \n {p4}")
if amount_players == 5:
    p1.change_points(count_points(p1))
    p2.change_points(count_points(p2))
    p3.change_points(count_points(p3))
    p4.change_points(count_points(p4))
    p5.change_points(count_points(p5))
    print(f"Final game stats were: {p1} \n {p2} \n {p3} \n {p4} \n {p5}")
if amount_players == 6:
    p1.change_points(count_points(p1))
    p2.change_points(count_points(p2))
    p3.change_points(count_points(p3))
    p4.change_points(count_points(p4))
    p5.change_points(count_points(p5))
    p6.change_points(count_points(p6))
    print(f"Final game stats were: {p1} \n {p2} \n {p3} \n {p4} \n {p5} \n {p6}")
            
            