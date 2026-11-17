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

class Player:
    """Represents a player in the game.

    Each player has a unique identifier, a display name, a running score, and a
    collection of cards currently held. The class also provides comparison
    operations based on the player's point total so players can be ordered in
    score-based game logic.
    """

    __num_players:int = 0

    def __init__(self, name:str):
        """Initialize a player with a name and default empty game state.

        Args:
            name: The player's display name.
        """
        self.__name:str = name
        self.__cards:Card = []
        self.__points:int = 0
        self.__ID:int = Player.__num_players
        Player.__num_players += 1

    @classmethod
    def get_num_players(cls):
        """Return the total number of Player instances created."""
        return cls.__num_players

    def get_ID(self):
        """Return the player's unique identifier assigned at creation."""
        return self.__ID

    def get_name(self):
        """Return the player's current name."""
        return self.__name

    def set_name(self, name:str):
        """Update the player's display name.

        Args:
            name: The new name to assign to the player.
        """
        self.__name = name
    
    def get_points(self):
        """Return the player's current score."""
        return self.__points
    
    def change_points(self, amount:int):
        """Adjust the player's score by a signed amount.

        Args:
            amount: The number of points to add to the player's total. This may
                be positive or negative.
        """
        self.__points += amount

    def set_points(self, points:int):
        """Set the player's score to an exact value.

        Args:
            points: The new score to assign.
        """
        self.__points = points

    def get_cards(self):
        """Return a copy of the player's cards to prevent external mutation."""
        return self.__cards.copy()

    def set_cards(self, cards:Card):
        """Replace the player's card list with a new collection.

        Args:
            cards: A list of card values to assign to the player.
        """
        self.__cards = cards

    def add_card(self, card:Card):
        """Add a single card to the player's hand if it is not already present.

        Args:
            card: The card value to add.

        Raises:
            ValueError: If the card is already in the player's hand.
        """
        if(card in self.__cards): raise ValueError(f"Cannot add duplicate card {card}: Player #{self.__ID} ({self.__name}) already has this card.")
        self.__cards.append(card)

    def add_cards(self, cards:Card):
        """Add multiple cards to the player's hand if none are duplicates.

        Args:
            cards: Card values to append to the player's collection.

        Raises:
            ValueError: If any card in the provided list is already present.
        """
        for card in cards:
            if(card in self.__cards): raise ValueError(f"Cannot add duplicate card {card}: Player #{self.__ID} ({self.__name}) already has this card.")
        self.__cards.extend(cards)

    def remove_card(self, card:Card):
        """Remove a card from the player's hand by value.

        Args:
            card: The card value to remove.

        Raises:
            ValueError: If the card is not found in the player's hand.
        """
        self.__cards.remove(card)
    def __str__(self):
        """Return a readable summary of the player's identity, score, and cards."""
        return f"Player #{self.__ID}:\n\tName: {self.__name}\n\tPoints: {self.__points}\n\tCards: {self.__cards}"
    def __eq__(self, other):
        """Compare players by their unique identifier.

        Args:
            other: Another Player instance to compare against.

        Returns:
            True when both players refer to the same player instance.

        Raises:
            TypeError: If other is not a Player.
        """
        if not isinstance(other, Player):
            raise TypeError(f"Cannot compare Player with {type(other).__name__} using ==; expected another Player.")
        return self.__ID == other.__ID
    def __lt__(self, other):
        """Return whether this player has fewer points than another player.

        Args:
            other: Another Player instance to compare against.

        Returns:
            True when this player's score is lower than the other player's score.

        Raises:
            TypeError: If other is not a Player.
        """
        if not isinstance(other, Player):
            raise TypeError(f"Cannot compare Player with {type(other).__name__} using <; expected another Player.")
        return self.__points < other.__points
    def __gt__(self, other):
        """Return whether this player has more points than another player.

        Args:
            other: Another Player instance to compare against.

        Returns:
            True when this player's score is higher than the other player's score.

        Raises:
            TypeError: If other is not a Player.
        """
        if not isinstance(other, Player):
            raise TypeError(f"Cannot compare Player with {type(other).__name__} using >; expected another Player.")
        return self.__points > other.__points
    def __le__(self, other):
        """Return whether this player has at most the same number of points.

        Args:
            other: Another Player instance to compare against.

        Returns:
            True when this player's score is less than or equal to the other's.

        Raises:
            TypeError: If other is not a Player.
        """
        if not isinstance(other, Player):
            raise TypeError(f"Cannot compare Player with {type(other).__name__} using <=; expected another Player.")
        return self.__points <= other.__points
    def __ge__(self, other):
        """Return whether this player has at least the same number of points.

        Args:
            other: Another Player instance to compare against.

        Returns:
            True when this player's score is greater than or equal to the other's.

        Raises:
            TypeError: If other is not a Player.
        """
        if not isinstance(other, Player):
            raise TypeError(f"Cannot compare Player with {type(other).__name__} using >=; expected another Player.")
        return self.__points >= other.__points
    
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
    card = deck.deal()
    cards = players[turn].get_cards()
    decision = input(f"{players[turn].get_name()}, do you want to swap the {card} with one of your cards, discard, or call cambio? (swap, discard, Cambio): ").lower()
    if decision == "swap":
        position = int(input("Which card would you like to swap? (1,2,3...) "))
        cards[position-1] = card
        players[turn].set_cards(cards)
    if decision == "cambio":
        return "cambio"
    else:
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
for i in range(amount_players):
    players[i].add_card(deck.deal())
    players[i].add_card(deck.deal())
    players[i].add_card(deck.deal())
    players[i].add_card(deck.deal())
start_player = input("Which player starts? ")
for i in range(len(players)):
    if start_player == players[i].get_name():
        turn = i

running = True
final = None
while running == True:
    previous_turn = turn
    if final == turn:
        break
    print(turn)
    turn = turn_logic(players, turn)
    if turn == "cambio":
        final = previous_turn
        turn = previous_turn + 1
        print(final, turn)
    else:
        turn += 1
    if turn == amount_players:
        turn = 0
    
# After game ends count points
for i in range(amount_players):
    players[i].change_points(count_points(players, i))
    print(players[i])
