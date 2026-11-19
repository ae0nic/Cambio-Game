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

from symtable import Class
from cards import Card, Deck, DiscardPile
from player import Player
from enum import Enum

class GameState(Enum):
    NOT_STARTED = 1
    STARTING = 2
    IN_PROGRESS = 3
    DRAWING = 4
    CAMBIO_CALLED = 5
    ENDED = 6

class Cambio:
    def __init__(self, num_players:int):
        
        self.__CARD_POINTS = {
            "2": 2,
            "3": 3, 
            "4": 4,
            "5": 5, 
            "6": 6,
            "7": 7, 
            "8": 8,
            "9": 9, 
            "10": 10,
            "Jack": 10, 
            "Queen": 10,
            "King": 10, 
            "Ace": 1,
            "Joker": 0
        }
        self.__STARTING_HAND_SIZE:int = 4
        self.__NUM_PLAYERS:int = num_players

        self.__game_state:GameState = GameState.NOT_STARTED

        self.__deck:Deck = Deck()
        self.__discard_pile:DiscardPile = DiscardPile()

        self.__deck.shuffle()

        self.__players:list[Player] = []


        self.__current_player:int = 0

    def initialize_players(self, player_names:list[str]):
        if(self.__game_state != GameState.NOT_STARTED):
            raise Exception("Game has already started. Cannot initialize players.")
        if(len(player_names) != self.__NUM_PLAYERS):
            raise ValueError(f"Invalid number of players. Expected {self.__NUM_PLAYERS}.")
        [self.__players.append(Player(name)) for name in player_names]
        return len(self.__players) == self.__NUM_PLAYERS

    def set_starting_player(self, start_name:str):
        if(len(self.__players) != self.__NUM_PLAYERS):
            raise Exception("Players have not been initialized. Cannot set starting player.")
        if(self.__game_state != GameState.NOT_STARTED):
            raise Exception("Game has already started. Cannot set starting player.")
        if start_name not in [self.__players[i].get_name() for i in range(self.__NUM_PLAYERS)]:
            raise ValueError("Invalid name. Please enter a valid player name.")
        self.__current_player = [self.__players[i].get_name() for i in range(self.__NUM_PLAYERS)].index(start_name)
        return self.__current_player

    def deal_starting_hands(self):
        if(len(self.__players) != self.__NUM_PLAYERS):
            raise Exception("Players have not been initialized. Cannot deal starting hands.")
        for i in range(self.__NUM_PLAYERS):
            for j in range(self.__STARTING_HAND_SIZE):
                self.__players[i].add_card(self.__deck.deal())

    def advance_turn(self):
        self.__current_player = (self.__current_player + 1) % self.__NUM_PLAYERS

    def call_cambio(self):
        if self.__game_state == GameState.CAMBIO_CALLED:
            raise Exception("Cambio has already been called.")
        self.__game_state = GameState.CAMBIO_CALLED
        return self.__game_state

    def draw_card(self):
        if(self.__game_state != GameState.IN_PROGRESS):
            raise Exception("Game is not in progress. Cannot draw a card.")
        self.__game_state = GameState.DRAWING
        return self.__deck.deal()
    
    def keep_card(self, card:Card):
        if(self.__game_state != GameState.DRAWING):
            raise Exception("Not in the middle of drawing a card.")
        self.__game_state = GameState.IN_PROGRESS
        return card
    
    def swap_card(self, card:int, swap:Card):
        if(card < 0 or card > len(self.__players[self.__current_player].get_cards())):
            raise IndexError("Invalid card index. Please enter a valid index")
        current_player = self.__players[self.__current_player]
        temp_cards = current_player.get_cards()
        temp = temp_cards[card]
        current_player.remove_card(card)
        current_player.add_card(swap)
        
        return temp
        
    def discard_card(self, card:int):
        if(card < 0 or card > len(self.__players[self.__current_player].get_num_cards())):
            raise IndexError("Invalid card index. Please enter a valid index.")
        discarded_card = self.__players[self.__current_player].remove_card(card)
        self.__discard_pile.add_card(discarded_card)
        return discarded_card

    # def start_game(self):
    #     self.__is_game_running:bool = True

    #     for i in range(self.__NUM_PLAYERS):
    #         print(self.show_bottom_cards(i))         

    #     self.show_bottom_cards(self.__current_player)

    def count_points(self, turn: int):
        
        """"Calculates the amount of points a player has"""
        points = 0
        cards = self.__players[turn].get_cards()
        for card in cards:
            data = str(card).split(" ")
            try:
                points += int(data[0])
            except:
                if str(data[0]) != "King":
                    points += self.__CARD_POINTS[str(data[0])]
                else:
                    if "Spade" in str(data) or "Clubs" in str(data):
                        points += 10
                    else:
                        points -= 1
        return points
                        
    def turn_logic(self, turn):
        """Deals with all the possible decisions a player could make
        on their turn. Needs support from the function dealing with
        the cards with special abilities"""
        decision = input(f"{self.__players[turn].get_name()}, would you like to call Cambio? (yes, no): ").lower()
        if decision == "yes":
            return "cambio"
        card = self.__deck.deal()
        cards = self.__players[turn].get_cards()
        decision = input(f"{self.__players[turn].get_name()}, do you want to swap the {card} with one of your cards or discard? (swap, discard): ").lower()
        if decision == "swap":
            position = int(input("Which card would you like to swap? (1,2,3...) "))
            cards[position-1] = card
            self.__players[turn].set_cards(cards)
        if decision == "discard":
            a = "discard function"
            # discard function
        return turn

    def show_bottom_cards(self, turn):
        return tuple(self.__players[turn].get_cards()[-2:])
    def first_turn_logic(self, turn):
        pass