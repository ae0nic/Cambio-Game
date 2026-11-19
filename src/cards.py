# By submitting this assignment, I agree to the following:
#   "Aggies do not lie, cheat, or steal, or tolerate those who do."
#   "I have not given or received any unauthorized aid on this assignment."
#
# Name:         YOUR NAME
# Section:      YOUR SECTION NUMBER
# Assignment:   THE ASSIGNMENT NUMBER (e.g. Lab 1b-2)
# Date:         12 11 26

"""Playing-card, deck, and discard-pile data structures."""

import random


class Card:
    """A playing card identified by its suit and rank."""

    POINTS = {
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
        "Joker": 0,
    }

    def __init__(self, suit, rank):
        """Create a card.

        Args:
            suit: The card's suit.
            rank: The card's rank.
        """
        self.suit = suit
        self.rank = rank
    
    def __repr__(self):
        """Return a readable representation such as ``'Ace of Spades'``."""
        return f"{self.rank} of {self.suit}"

    def get_points(self):
        """Return this card's point value using Cambio scoring rules.

        Black Kings are worth 10 points, while red Kings are worth -1 point.
        """
        if self.rank == "King" and self.suit not in ("Clubs", "Spades"):
            return -1
        return self.POINTS[self.rank]


class Deck:
    """A collection of cards that can be shuffled and dealt."""

    SUITS = ["Hearts", "Diamonds", "Clubs", "Spades"]
    RANKS = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "Jack", "Queen", "King", "Ace"]

    def __init__(self):
        """Build a deck from every configured suit and rank."""
        self.cards = []
        self.__build()


    def __build(self):
        """Populate the deck with each configured suit/rank combination."""
        self.cards = [Card(suit, rank) for suit in self.SUITS for rank in self.RANKS]
        for i in range(2):
            self.cards.append(Card("Joker", "Joker"))

    def shuffle(self):
        """Randomize the order of the cards in place."""
        random.shuffle(self.cards)

    def deal(self):
        """Remove and return the top card, or ``None`` if the deck is empty.

        Returns:
            The card at the end of the deck's list, or ``None`` when empty.
        """
        if len(self.cards) > 0:
            return self.cards.pop()
        return None
    
    def add_cards(self, cards:list[Card]):
        """Append cards to the deck.

        Args:
            cards: Cards to add to the end of the deck.
        """
        self.cards.extend(cards)

    def __len__(self):
        """Return the number of cards remaining."""
        return len(self.cards)


class DiscardPile(Deck):
    """A face-up pile of discarded cards, with access to its top card."""

    def __init__(self):
        """Create an empty discard pile."""
        self.cards = []

    def add_card(self, card: Card):
        """Place a card on top of the discard pile.

        Args:
            card: The card to add.
        """
        self.cards.append(card)

    def look_top_card(self):
        """Return the top discarded card, or ``None`` if the pile is empty."""
        if len(self.cards) > 0:
            return self.cards[-1]
        return None

    def get_cards(self):
        """Return a copy of the cards in discard order."""
        return self.cards.copy()
    