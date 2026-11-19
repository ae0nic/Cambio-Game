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
from card_ability import card_ability, has_card_ability
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
        self.screen_update = None

        self.__game_state:GameState = GameState.NOT_STARTED

        self.__deck:Deck = Deck()
        self.__discard_pile:DiscardPile = DiscardPile()
        self.__drawn_card:Card | None = None
        self.__pending_ability_card:Card | None = None

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
    
    def get_players(self):
        return self.__players

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
        if self.__drawn_card is not None:
            raise Exception("The previously drawn card has not been used.")
        if self.__pending_ability_card is not None:
            raise Exception("The previous card ability has not been resolved.")
        card = self.__deck.deal()
        if card is None:
            raise RuntimeError("Cannot draw a card because the deck is empty.")
        self.__drawn_card = card
        self.__game_state = GameState.DRAWING
        return card
    
    def keep_card(self, card:Card):
        if(self.__game_state != GameState.DRAWING):
            raise Exception("Not in the middle of drawing a card.")
        if card is not self.__drawn_card:
            raise ValueError("The card was not drawn on this turn.")
        self.__game_state = GameState.IN_PROGRESS
        return card

    def discard_drawn_card(self, card:Card):
        """Discard the current draw and make its ability available to the UI."""
        if(self.__game_state != GameState.DRAWING):
            raise Exception("Not in the middle of drawing a card.")
        if card is not self.__drawn_card:
            raise ValueError("The card was not drawn on this turn.")
        self.__discard_pile.add_card(card)
        self.__drawn_card = None
        self.__game_state = GameState.IN_PROGRESS
        if has_card_ability(card):
            self.__pending_ability_card = card
        return card

    def resolve_card_ability(
        self,
        discarded_card:Card,
        *,
        own_position:int | None = None,
        target_player_index:int | None = None,
        target_position:int | None = None,
        swap:bool = False
    ) -> Card | tuple[Card, Card] | None:
        """Resolve the pending ability using zero-based card and player indexes."""
        if discarded_card is not self.__pending_ability_card:
            raise ValueError("The card does not have a pending ability.")
        target_player = None
        if target_player_index is not None:
            if target_player_index < 0 or target_player_index >= len(self.__players):
                raise IndexError("Invalid target player index.")
            target_player = self.__players[target_player_index]
        result = card_ability(
            discarded_card,
            self.__players[self.__current_player],
            own_position=own_position,
            target_player=target_player,
            target_position=target_position,
            swap=swap,
        )
        self.__pending_ability_card = None
        return result
    
    def swap_card(self, card:int, swap:Card):
        if(self.__game_state != GameState.IN_PROGRESS):
            raise Exception("Game is not in progress. Cannot swap a card.")
        if self.__drawn_card is None or swap is not self.__drawn_card:
            raise ValueError("The swapped card was not drawn on this turn.")
        current_player = self.__players[self.__current_player]
        cards = current_player.get_cards()
        if(card < 0 or card >= len(cards)):
            raise IndexError("Invalid card index. Please enter a valid index")
        replaced_card = cards[card]
        cards[card] = swap
        current_player.set_cards(cards)
        self.__drawn_card = None
        return replaced_card
        
    def discard_card(self, card:int):
        current_player = self.__players[self.__current_player]
        cards = current_player.get_cards()
        if(card < 0 or card >= len(cards)):
            raise IndexError("Invalid card index. Please enter a valid index.")
        discarded_card = current_player.remove_card(card)
        self.__discard_pile.add_card(discarded_card)
        return discarded_card

    def start_game(self, screen_update):
        self.__is_game_running:bool = True
        self.screen_update = screen_update

        for i in range(self.__NUM_PLAYERS):
            print(f"Showing cards for player {i + 1}: ")
            print(self.show_bottom_cards(i))
            screen_update()
            input("Press enter when done.")
            self.hide_all(i)
            screen_update()

    def get_discard(self):
        return self.__discard_pile.look_top_card()

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
        self.screen_update()
        decision = input(f"{self.__players[turn].get_name()}, would you like to call Cambio? (yes, no): ").lower()
        if decision == "yes":
            return "cambio"
        card = self.draw_card()
        decision = input(f"{self.__players[turn].get_name()}, do you want to swap the {card} with one of your cards or discard? (swap, discard): ").lower()
        if decision == "swap":
            position = int(input("Which card would you like to swap? (1,2,3...) "))
            card_to_keep = self.keep_card(card)
            replaced_card = self.swap_card(position - 1, card_to_keep)
            self.__discard_pile.add_card(replaced_card)
        elif decision == "discard":
            self.discard_drawn_card(card)
        else:
            raise ValueError("Invalid choice. Enter 'swap' or 'discard'.")
        return turn

    def show_bottom_cards(self, turn):
        for c in self.__players[turn].get_cards()[::2]:
            c.show()
        return tuple(self.__players[turn].get_cards()[::2])
    def hide_all(self, turn):
        for c in self.__players[turn].get_cards()[::]:
            c.hide()
