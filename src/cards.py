# By submitting this assignment, I agree to the following:
#   "Aggies do not lie, cheat, or steal, or tolerate those who do."
#   "I have not given or received any unauthorized aid on this assignment."
#
# Name:         YOUR NAME
# Section:      YOUR SECTION NUMBER
# Assignment:   THE ASSIGNMENT NUMBER (e.g. Lab 1b-2)
# Date:         12 11 26

import random

class Card:
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank
    
    def __repr__(self):
        return f"{self.rank} of {self.suit}"

class Deck:
    SUITS = ["Hearts", "Diamonds", "Clubs", "Spades", "Joker"]
    RANKS = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "Jack", "Queen", "King", "Ace", "Joker"]

    def __init__(self):
        self.cards = []
        self.__build()


    def __build(self):
        """Populates the deck with 54 unique Card objects."""
        self.cards = [Card(suit, rank) for suit in self.SUITS for rank in self.RANKS]

    def shuffle(self):
        """Randomizes the order of the cards in place."""
        random.shuffle(self.cards)

    def deal(self):
        """Removes and returns the top card from the deck."""
        if len(self.cards) > 0:
            return self.cards.pop()
        return None
    
    def add_cards(self, cards:list[Card]):
        self.cards.extend(cards)

    def __len__(self):
        return len(self.cards)

class DiscardPile(Deck):
    def __init__(self):
        self.cards = []

    def add_card(self, card: Card):
        self.cards.append(card)

    def look_top_card(self):
        if len(self.cards) > 0:
            return self.cards[-1]
        return None
    def get_cards(self):
        return self.cards.copy()
    