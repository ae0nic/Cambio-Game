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
from src.deck import Card, Deck
from src.player import Player
    
# dictionary helping calculate how much each card is worth in points
card_points = {"Jack": 10,
               "Queen": 10,
               "Joker": 0,
               "Ace": 1
               }

def count_points(players, turn):
    """"Calculates the amount of points a player has"""
    points = 0
    cards = players[turn].get_cards()
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
                    
def turn_logic(players, turn):
    """Deals with all the possible decisions a player could make
       on their turn. Needs support from the function dealing with
       the cards with special abilities"""
    decision = input(f"{players[turn].get_name()}, would you like to call Cambio? (yes, no): ").lower()
    if decision == "yes":
        return "cambio"
    card = deck.deal()
    cards = players[turn].get_cards()
    decision = input(f"{players[turn].get_name()}, do you want to swap the {card} with one of your cards or discard? (swap, discard): ").lower()
    if decision == "swap":
        position = int(input("Which card would you like to swap? (1,2,3...) "))
        cards[position-1] = card
        players[turn].set_cards(cards)
    if decision == "discard":
        a = "discard function"
        # discard function
    return turn
    
def first_turn_logic(players, turn):
    """"Gives the player information about their bottom 2 cards """
    print(f"{players[turn].get_name()}, your two bottom cards are the {players[turn].get_cards()[2]} and the {players[turn].get_cards()[3]}")
    
# starts game set up by shuffling deck
deck = Deck()
deck.shuffle()

# gets input from player
players = []
amount_players = int(input("How many players are playing the game? (2-6): "))
for i in range(amount_players):
    players.append(Player(input(f"What is player {i+1}'s name? ")))

# deals hands for each player
for i in range(amount_players):
    players[i].add_card(deck.deal())
    players[i].add_card(deck.deal())
    players[i].add_card(deck.deal())
    players[i].add_card(deck.deal())
    
# more user input
start_player = input("Which player starts? ")

# choose which player starts the game
for i in range(amount_players):
    if start_player == players[i].get_name():
        turn = i
        start_turn = turn

running = True
final = None
input("Press enter when you are ready to start the game")
for i in range(amount_players):
    first_turn_logic(players, turn)
    turn += 1
    input("Press enter when the next player is ready")
    if turn == amount_players:
        turn = 0
turn = start_turn
while running == True:
    
    # store turn as previous_turn so that it can be used later
    previous_turn = turn
    
    # chekc if the player called cambio on their previous turn
    if final == turn:
        break
    
    # do the players turn
    turn = turn_logic(players, turn)
    
    # handle if the player called cambio
    if turn == "cambio":
        final = previous_turn
        turn = previous_turn + 1
    else:
        turn += 1
    
    # loop back to player 1's turn
    if turn == amount_players:
        turn = 0
    input("Press enter when the next player is ready")
# After game ends count points
for i in range(amount_players):
    players[i].change_points(count_points(players, i))
    print(players[i])
