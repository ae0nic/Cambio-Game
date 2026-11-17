# By submitting this assignment, I agree to the following:
#   "Aggies do not lie, cheat, or steal, or tolerate those who do."
#   "I have not given or received any unauthorized aid on this assignment."
#
# Name:         YOUR NAME
# Section:      YOUR SECTION NUMBER
# Assignment:   THE ASSIGNMENT NUMBER (e.g. Lab 1b-2)
# Date:         12 11

import random

class Card:
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank

    def __repr__(self):
        return f"{self.rank} of {self.suit}"

class Deck:
    SUITS = ["Hearts", "Diamonds", "Clubs", "Spades"]
    RANKS = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "Jack", "Queen", "King", "Ace"]

    def __init__(self):
        self.cards = []
        self.build()

    def build(self):
        """Populates the deck with 52 unique Card objects."""
        self.cards = [Card(suit, rank) for suit in self.SUITS for rank in self.RANKS]

    def shuffle(self):
        """Randomizes the order of the cards in place."""
        random.shuffle(self.cards)

    def deal(self):
        """Removes and returns the top card from the deck."""
        if len(self.cards) > 0:
            return self.cards.pop()
        return None

    def __len__(self):
        return len(self.cards)

deck = Deck()
deck.shuffle()

print(f"Cards remaining: {len(deck)}") 
drawn_card = deck.deal()
print(f"Dealt: {drawn_card}")            
print(f"Cards remaining: {len(deck)}")  
