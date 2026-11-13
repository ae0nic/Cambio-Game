class Player:
    """Represents a player in the game.

    Each player has a unique identifier, a display name, a running score, and a
    collection of cards currently held. The class also provides comparison
    operations based on the player's point total so players can be ordered in
    score-based game logic.
    """

    num_players:int = 0

    def __init__(self, name:str):
        """Initialize a player with a name and default empty game state.

        Args:
            name: The player's display name.
        """
        self.__name:str = name
        self.__cards:list[int] = []
        self.__points:int = 0
        self.__ID:int = Player.num_players
        Player.num_players += 1
    
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

    def set_cards(self, cards:list[int]):
        """Replace the player's card list with a new collection.

        Args:
            cards: A list of card values to assign to the player.
        """
        self.__cards = cards

    def add_card(self, card:int):
        """Add a single card to the player's hand if it is not already present.

        Args:
            card: The card value to add.

        Raises:
            ValueError: If the card is already in the player's hand.
        """
        if(card in self.__cards): raise ValueError(f"Cannot add duplicate card {card}: Player #{self.__ID} ({self.__name}) already has this card.")
        self.__cards.append(card)

    def add_cards(self, cards:list[int]):
        """Add multiple cards to the player's hand if none are duplicates.

        Args:
            cards: Card values to append to the player's collection.

        Raises:
            ValueError: If any card in the provided list is already present.
        """
        for card in cards:
            if(card in self.__cards): raise ValueError(f"Cannot add duplicate card {card}: Player #{self.__ID} ({self.__name}) already has this card.")
        self.__cards.extend(cards)

    def remove_card(self, card:int):
        """Remove a card from the player's hand.

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
