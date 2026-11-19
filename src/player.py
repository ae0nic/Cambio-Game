"""Player state and hand-management operations for Cambio."""

if __package__:
    from .cards import Card
else:
    from cards import Card

class Player:
    """Represents a player in the game.

    Each player has a unique identifier, a display name, a hand, and a point
    total derived from the cards in that hand. The class also provides
    comparison operations based on that total.
    """

    __num_players:int = 0

    def __init__(self, name:str):
        """Initialize a player with a name and default empty game state.

        Args:
            name: The player's display name.
        """
        self.__name:str = name
        self.__cards:list[Card] = []
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
        """Return the total point value of the player's current hand."""
        return self.__points
    
    def change_points(self, amount:int):
        """Adjust the player's point total by a signed amount.

        Args:
            amount: Points to add to the total; may be positive or negative.
        """
        self.__points += amount

    def set_points(self, points:int):
        """Set the player's point total to an exact value.

        Args:
            points: The new total to assign.
        """
        self.__points = points

    def get_cards(self):
        """Return a copy of the player's cards to prevent external mutation."""
        return self.__cards.copy()

    def set_cards(self, cards:list[Card]):
        """Replace the player's card list with a new collection.

        Args:
            cards: A list of card values to assign to the player.

        The player's point total is recalculated from the new hand.
        """
        self.__cards = cards.copy()
        self.__recalculate_points()

    def add_card(self, card:Card):
        """Add a card to the hand and increase points by its value.

        Args:
            card: The card value to add.

        Raises:
            ValueError: If the card is already in the player's hand.
        """
        if(card in self.__cards): raise ValueError(f"Cannot add duplicate card {card}: Player #{self.__ID} ({self.__name}) already has this card.")
        card_points = card.get_points()
        self.__cards.append(card)
        self.__points += card_points

    def add_cards(self, cards:list[Card]):
        """Add multiple cards and increase points by their total value.

        Args:
            cards: Card values to append to the player's collection.

        Raises:
            ValueError: If any card in the provided list is already present.
        """
        for card in cards:
            if(card in self.__cards): raise ValueError(f"Cannot add duplicate card {card}: Player #{self.__ID} ({self.__name}) already has this card.")
        cards_points = sum(card.get_points() for card in cards)
        self.__cards.extend(cards)
        self.__points += cards_points

    def remove_card_by_value(self, card:Card):
        """Remove a card by value and subtract its points from the total.

        Args:
            card: The card value to remove.

        Raises:
            ValueError: If the card is not found in the player's hand.
        """
        self.__cards.remove(card)
        self.__points -= card.get_points()

    def remove_card_by_index(self, card:int):
        """Remove a card by index and subtract its points from the total.
        
        Args:
            card: The zero-based position of the card to remove.
        
        Returns:
            The removed card.

        Raises:
            IndexError: If the index is outside the player's hand.
        """
        removed_card = self.__cards.pop(card)
        self.__points -= removed_card.get_points()
        return removed_card

    def __recalculate_points(self):
        """Recompute the point total after replacing the entire hand."""
        self.__points = sum(card.get_points() for card in self.__cards)
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
