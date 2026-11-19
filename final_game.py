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
# Date:         11 18 2026

"""Standalone Cambio game with console input and a Pygame display."""


# --- cards.py ---


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


# --- player.py ---

"""Player state and hand-management operations for Cambio."""


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


# --- card_ability.py ---

"""Helpers for inspecting and exchanging cards during special-card abilities."""



def has_card_ability(card: Card) -> bool:
    """Return whether ``card`` has an implemented Cambio ability.

    Abilities are assigned to 7, 8, 9, 10, Jack, Queen, and the King of Clubs
    or Spades.
    """
    return card.rank in ("7", "8", "9", "10", "Jack", "Queen") or (
        card.rank == "King" and card.suit in ("Clubs", "Spades")
    )


def get_player_card(player: Player, position: int) -> Card:
    """Get one card from a player's hand using a zero-based position.

    Args:
        player: Player whose hand is inspected.
        position: Zero-based position of the card.

    Returns:
        The card at ``position``.

    Raises:
        IndexError: If ``position`` is outside the player's hand.
    """
    cards = player.get_cards()
    if position < 0 or position >= len(cards):
        raise IndexError("Invalid card position.")
    return cards[position]


def replace_player_card(player: Player, position: int, card: Card) -> Card:
    """Replace one card in a player's hand without changing other players.

    Args:
        player: Player whose hand is updated.
        position: Zero-based position of the card to replace.
        card: Card to place at that position.

    Returns:
        The card that was replaced.

    Raises:
        IndexError: If ``position`` is outside the player's hand.
    """
    cards = player.get_cards()
    if position < 0 or position >= len(cards):
        raise IndexError("Invalid card position.")
    replaced_card = cards[position]
    cards[position] = card
    player.set_cards(cards)
    return replaced_card


def card_ability(
    discarded_card: Card,
    current_player: Player,
    *,
    own_position: int | None = None,
    target_player: Player | None = None,
    target_position: int | None = None,
    swap: bool = False,
) -> Card | tuple[Card, Card] | None:
    """Apply a discarded card's ability using selections supplied by the UI.

    The positions are zero-based. A 7 or 8 reveals a card from the current
    player's hand; a 9 or 10 reveals a target player's card; a Jack or Queen
    exchanges one card from each hand; and a black King reveals one card from
    each hand and exchanges them when ``swap`` is true. This function performs
    no console input or output.

    Args:
        discarded_card: Card whose ability is being applied.
        current_player: Player who discarded the card.
        own_position: Selected position in the current player's hand.
        target_player: Other player selected for an opponent-targeting ability.
        target_position: Selected position in the target player's hand.
        swap: Whether a black King's selected cards should be exchanged.

    Returns:
        The revealed card, the pair of cards selected for an exchange, or
        ``None`` if the card has no implemented ability.

    Raises:
        ValueError: If a required selection is missing or the target is invalid.
        IndexError: If a selected card position is outside its player's hand.
    """
    if not has_card_ability(discarded_card):
        return None

    if discarded_card.rank in ("7", "8"):
        if own_position is None:
            raise ValueError("Select a card from the current player's hand.")
        return get_player_card(current_player, own_position)

    if discarded_card.rank in ("9", "10"):
        _validate_target(current_player, target_player)
        if target_position is None:
            raise ValueError("Select a card from the target player's hand.")
        return get_player_card(target_player, target_position)

    if discarded_card.rank in ("Jack", "Queen"):
        _validate_target(current_player, target_player)
        if own_position is None or target_position is None:
            raise ValueError("Select one card from each player's hand.")
        # Validate both selections before changing either hand.
        own_card = get_player_card(current_player, own_position)
        target_card = get_player_card(target_player, target_position)
        replace_player_card(current_player, own_position, target_card)
        replace_player_card(target_player, target_position, own_card)
        return own_card, target_card

    _validate_target(current_player, target_player)
    if own_position is None or target_position is None:
        raise ValueError("Select one card from each player's hand.")
    own_card = get_player_card(current_player, own_position)
    target_card = get_player_card(target_player, target_position)
    if swap:
        replace_player_card(current_player, own_position, target_card)
        replace_player_card(target_player, target_position, own_card)
    return own_card, target_card


def _validate_target(current_player: Player, target_player: Player | None) -> None:
    """Ensure an opponent-targeting ability names another player."""
    if target_player is None:
        raise ValueError("Select another player.")
    if target_player is current_player:
        raise ValueError("The target player must be someone else.")


# --- cambio.py ---


"""Core Cambio game state, turn actions, and scoring."""

from enum import Enum
from typing import Callable


class GameState(Enum):
    """Lifecycle states used to validate game actions."""

    NOT_STARTED = 1
    STARTING = 2
    IN_PROGRESS = 3
    DRAWING = 4
    CAMBIO_CALLED = 5
    ENDED = 6

class Cambio:
    """Manage players, cards, turns, and abilities for one Cambio game.

    Card positions and player indexes are zero-based; console prompts may show
    one-based positions for players.
    """

    def __init__(
        self,
        num_players:int,
        input_fn:Callable[[str], str] = input,
    ):
        """Create and shuffle a deck for a game with ``num_players`` players.

        Args:
            num_players: Number of players expected in this game.
            input_fn: Function used to read console prompts.
        """
        
        self.__STARTING_HAND_SIZE:int = 4
        self.__NUM_PLAYERS:int = num_players
        self.__input_fn = input_fn

        self.__game_state:GameState = GameState.NOT_STARTED

        self.__deck:Deck = Deck()
        self.__discard_pile:DiscardPile = DiscardPile()
        # Identity checks keep unrelated cards from being used as the current draw.
        self.__drawn_card:Card | None = None
        # Set only by a direct draw discard; resolve it before the next draw.
        self.__pending_ability_card:Card | None = None

        self.__deck.shuffle()

        self.__players:list[Player] = []


        self.__current_player:int = 0
        self.__cambio_caller:int | None = None

    def get_game_state(self) -> GameState:
        """Return the game's current lifecycle state."""
        return self.__game_state

    def get_current_player_index(self) -> int:
        """Return the zero-based index of the current player."""
        return self.__current_player

    def get_current_player(self) -> Player:
        """Return the current player object."""
        return self.__players[self.__current_player]

    def get_players(self) -> list[Player]:
        """Return a copy of the game's player list."""
        return self.__players.copy()

    def get_discard_top_card(self) -> Card | None:
        """Return the top discard, or ``None`` if the pile is empty."""
        return self.__discard_pile.look_top_card()

    def get_discard_cards(self) -> list[Card]:
        """Return a copy of the face-up discard pile."""
        return self.__discard_pile.get_cards()

    def get_draw_pile_count(self) -> int:
        """Return the number of cards remaining in the draw pile."""
        return len(self.__deck)

    def get_drawn_card(self) -> Card | None:
        """Return the card currently awaiting the player's draw decision."""
        return self.__drawn_card

    def initialize_players(self, player_names:list[str]):
        """Create the game's players.

        Args:
            player_names: Names for all players, in turn order.

        Returns:
            ``True`` when the expected number of players has been created.

        Raises:
            Exception: If the game has already started.
            ValueError: If the number of names differs from ``num_players``.
        """
        if(self.__game_state != GameState.NOT_STARTED):
            raise Exception("Game has already started. Cannot initialize players.")
        if(len(player_names) != self.__NUM_PLAYERS):
            raise ValueError(f"Invalid number of players. Expected {self.__NUM_PLAYERS}.")
        [self.__players.append(Player(name)) for name in player_names]
        return len(self.__players) == self.__NUM_PLAYERS

    def set_starting_player(self, start_name:str):
        """Set the first player by name and return that player's index.

        Args:
            start_name: Name of the player who starts.

        Returns:
            The zero-based index of the selected starting player.

        Raises:
            Exception: If players are not initialized or the game has started.
            ValueError: If ``start_name`` is not one of the players.
        """
        if(len(self.__players) != self.__NUM_PLAYERS):
            raise Exception("Players have not been initialized. Cannot set starting player.")
        if(self.__game_state != GameState.NOT_STARTED):
            raise Exception("Game has already started. Cannot set starting player.")
        if start_name not in [self.__players[i].get_name() for i in range(self.__NUM_PLAYERS)]:
            raise ValueError("Invalid name. Please enter a valid player name.")
        self.__current_player = [self.__players[i].get_name() for i in range(self.__NUM_PLAYERS)].index(start_name)
        return self.__current_player

    def deal_starting_hands(self):
        """Deal the configured number of cards to every player.

        Raises:
            Exception: If players have not been initialized or hands are
                already dealt.
            RuntimeError: If the deck runs out while dealing.
        """
        if(len(self.__players) != self.__NUM_PLAYERS):
            raise Exception("Players have not been initialized. Cannot deal starting hands.")
        if self.__game_state != GameState.NOT_STARTED:
            raise Exception("Starting hands have already been dealt.")
        self.__game_state = GameState.STARTING
        for i in range(self.__NUM_PLAYERS):
            for j in range(self.__STARTING_HAND_SIZE):
                card = self.__deck.deal()
                if card is None:
                    raise RuntimeError("The deck ran out while dealing starting hands.")
                self.__players[i].add_card(card)
        opening_discard = self.__deck.deal()
        if opening_discard is None:
            raise RuntimeError("The deck ran out while starting the discard pile.")
        self.__discard_pile.add_card(opening_discard)
        self.__game_state = GameState.IN_PROGRESS

    def advance_turn(self):
        """Advance to the next player and finish the final round when appropriate.

        Returns:
            The current state after advancing.

        Raises:
            Exception: If a draw or card ability is unresolved, or turns cannot
                advance in the current state.
        """
        if self.__game_state not in (GameState.IN_PROGRESS, GameState.CAMBIO_CALLED):
            raise Exception("Cannot advance a turn in the current game state.")
        if self.__drawn_card is not None:
            raise Exception("Cannot advance while a drawn card is unresolved.")
        if self.__pending_ability_card is not None:
            raise Exception("Cannot advance while a card ability is unresolved.")
        self.__current_player = (self.__current_player + 1) % self.__NUM_PLAYERS
        if self.__cambio_caller is not None and self.__current_player == self.__cambio_caller:
            self.__game_state = GameState.ENDED
        return self.__game_state

    def call_cambio(self):
        """Start the final round, returning the ``CAMBIO_CALLED`` state.

        Every other player receives one turn. Reaching the caller again ends
        the game.

        Raises:
            Exception: If the game is not in progress or Cambio was already called.
        """
        if self.__game_state != GameState.IN_PROGRESS:
            raise Exception("Cambio can only be called during active play.")
        self.__cambio_caller = self.__current_player
        self.__game_state = GameState.CAMBIO_CALLED
        return self.__game_state

    def draw_card(self):
        """Draw a card for the current player and enter the drawing state.

        Returns:
            The card drawn from the deck.

        Raises:
            Exception: If the game is not in progress or the final round, or
                an earlier draw or ability is still unresolved.
            RuntimeError: If the deck is empty.
        """
        if self.__game_state not in (GameState.IN_PROGRESS, GameState.CAMBIO_CALLED):
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
        """Accept the current draw for a subsequent hand swap.

        This marks the draw as accepted but does not add it to the hand.
        ``swap_card`` updates the hand and its point total.

        Args:
            card: The exact card returned by ``draw_card``.

        Returns:
            The accepted card.

        Raises:
            Exception: If the game is not awaiting a draw decision.
            ValueError: If ``card`` is not the current draw.
        """
        if(self.__game_state != GameState.DRAWING):
            raise Exception("Not in the middle of drawing a card.")
        if card is not self.__drawn_card:
            raise ValueError("The card was not drawn on this turn.")
        self.__game_state = (
            GameState.CAMBIO_CALLED
            if self.__cambio_caller is not None
            else GameState.IN_PROGRESS
        )
        return card

    def keep_drawn_card(self, card:Card):
        """Add the current draw to the hand, used when a player has no cards.

        Args:
            card: The exact card returned by ``draw_card``.

        Returns:
            The card added to the current player's hand.
        """
        if self.__game_state != GameState.DRAWING:
            raise Exception("Not in the middle of drawing a card.")
        if card is not self.__drawn_card:
            raise ValueError("The card was not drawn on this turn.")
        self.__players[self.__current_player].add_card(card)
        self.__drawn_card = None
        self.__game_state = (
            GameState.CAMBIO_CALLED
            if self.__cambio_caller is not None
            else GameState.IN_PROGRESS
        )
        return card

    def discard_drawn_card(self, card:Card):
        """Discard the current draw and stage its ability for the UI.

        Abilities are not applied here because the UI must first supply the
        selected cards and target player. Hand-card discards use ``discard_card``
        and do not create a pending ability.

        Args:
            card: The exact card returned by ``draw_card``.

        Returns:
            The discarded card.

        Raises:
            Exception: If the game is not awaiting a draw decision.
            ValueError: If ``card`` is not the current draw.
        """
        if(self.__game_state != GameState.DRAWING):
            raise Exception("Not in the middle of drawing a card.")
        if card is not self.__drawn_card:
            raise ValueError("The card was not drawn on this turn.")
        self.__discard_pile.add_card(card)
        self.__drawn_card = None
        self.__game_state = (
            GameState.CAMBIO_CALLED
            if self.__cambio_caller is not None
            else GameState.IN_PROGRESS
        )
        if has_card_ability(card):
            # Only direct draw discards create this ability token.
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
        """Resolve the ability staged by ``discard_drawn_card``.

        Args:
            discarded_card: The exact card returned by ``discard_drawn_card``.
            own_position: Zero-based position in the current player's hand.
            target_player_index: Zero-based index of another player.
            target_position: Zero-based position in the target player's hand.
            swap: For a black King, whether to exchange the selected cards.

        Returns:
            The revealed card or cards, or ``None`` if the ability has no result.

        Raises:
            ValueError: If the card is not pending or a required selection is
                missing or invalid.
            IndexError: If a player or card index is out of range.
        """
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

    def skip_card_ability(self, discarded_card:Card) -> None:
        """Clear an ability when the game has no legal target for it.

        Args:
            discarded_card: The exact card with the pending ability.

        Raises:
            ValueError: If the card is not the pending ability.
        """
        if discarded_card is not self.__pending_ability_card:
            raise ValueError("The card does not have a pending ability.")
        self.__pending_ability_card = None

    def apply_stick_penalty(self) -> Card:
        """Draw a penalty card into the current player's hand.

        Returns:
            The card added to the current player's hand.

        Raises:
            RuntimeError: If the deck is empty.
        """
        card = self.__deck.deal()
        if card is None:
            raise RuntimeError("Cannot apply a stick penalty because the deck is empty.")
        self.__players[self.__current_player].add_card(card)
        return card

    def stick_card(
        self,
        *,
        own_position:int | None = None,
        target_player_index:int | None = None,
        target_position:int | None = None
    ) -> bool:
        """Attempt to stick a card matching the top discard's rank.

        With no target player, a matching card is removed from the current
        player's hand and placed on the discard pile. With a target player,
        a matching target card is exchanged for the selected card from the
        current player's hand. A wrong match draws a penalty card instead.

        All positions and the target player index are zero-based. The caller
        supplies selections directly; this method does not use console input.

        Args:
            own_position: Current player's selected card position. Required for
                a self-stick, and for a successful opponent stick.
            target_player_index: Another player to target, or ``None`` to stick
                a card from the current player's own hand.
            target_position: Selected card position in the target player's hand.

        Returns:
            ``True`` if the stick succeeds, or ``False`` if it draws a penalty.

        Raises:
            RuntimeError: If the discard pile is empty.
            ValueError: If a required selection is missing or the current
                player is selected as the target.
            IndexError: If a player or card position is out of range.
        """
        top_discard = self.__discard_pile.look_top_card()
        if top_discard is None:
            raise RuntimeError("Cannot stick a card because the discard pile is empty.")

        current_player = self.__players[self.__current_player]
        current_cards = current_player.get_cards()

        if target_player_index is None:
            if own_position is None:
                raise ValueError("Select a card from the current player's hand.")
            if own_position < 0 or own_position >= len(current_cards):
                raise IndexError("Invalid card position.")
            if current_cards[own_position].rank != top_discard.rank:
                self.apply_stick_penalty()
                return False
            stuck_card = current_player.remove_card_by_index(own_position)
            self.__discard_pile.add_card(stuck_card)
            return True

        if target_player_index < 0 or target_player_index >= len(self.__players):
            raise IndexError("Invalid target player index.")
        target_player = self.__players[target_player_index]
        if target_player is current_player:
            raise ValueError("The target player must be someone else.")
        if target_position is None:
            raise ValueError("Select a card from the target player's hand.")
        target_cards = target_player.get_cards()
        if target_position < 0 or target_position >= len(target_cards):
            raise IndexError("Invalid target card position.")
        if own_position is not None and (
            own_position < 0 or own_position >= len(current_cards)
        ):
            raise IndexError("Invalid card position.")
        if target_cards[target_position].rank != top_discard.rank:
            self.apply_stick_penalty()
            return False
        if own_position is None:
            raise ValueError("Select a card to give to the target player.")
        
        own_card = current_player.remove_card_by_index(own_position)
        stuck_card = target_player.remove_card_by_index(target_position)
        target_player.add_card(own_card)
        self.__discard_pile.add_card(stuck_card)
        return True
    
    def swap_card(self, card:int, swap:Card):
        """Replace one current-player card with the accepted draw.

        Args:
            card: Zero-based position in the current player's hand.
            swap: The exact card returned by ``draw_card`` and ``keep_card``.

        Returns:
            The card replaced in the hand; the caller can add it to the discard
            pile. The player's point total is recalculated with the new hand.

        Raises:
            Exception: If the game is not in progress.
            ValueError: If ``swap`` is not the current draw.
            IndexError: If ``card`` is outside the current hand.
        """
        if self.__game_state not in (GameState.IN_PROGRESS, GameState.CAMBIO_CALLED):
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

    def discard_replaced_card(self, card:Card) -> None:
        """Place a swapped-out hand card on the discard pile.

        Swapped-out cards do not trigger special-card abilities.

        Args:
            card: Card returned by ``swap_card``.
        """
        self.__discard_pile.add_card(card)
        
    def discard_card(self, card:int):
        """Remove a card from the current player's hand and discard it.

        This method handles a hand card, not the current draw, so it does not
        trigger a card ability.

        Args:
            card: Zero-based position in the current player's hand.

        Returns:
            The card moved to the discard pile.

        Raises:
            IndexError: If ``card`` is outside the current hand.
        """
        current_player = self.__players[self.__current_player]
        cards = current_player.get_cards()
        if(card < 0 or card >= len(cards)):
            raise IndexError("Invalid card index. Please enter a valid index.")
        discarded_card = current_player.remove_card_by_index(card)
        self.__discard_pile.add_card(discarded_card)
        return discarded_card


    def count_points(self, turn: int):
        """Calculate a player's hand score.

        Args:
            turn: Zero-based index of the player to score.

        Returns:
            The player's current hand total. Card additions, removals, and
            replacements keep this value synchronized.
        """
        return self.__players[turn].get_points()
                        
    def _prompt_choice(
        self, prompt:str, choices:tuple[str, ...]
    ) -> str:
        """Prompt until the user enters one of the allowed choices."""
        allowed = ", ".join(choices)
        while True:
            answer = self.__input_fn(f"{prompt} ({allowed}): ").strip().lower()
            if answer in choices:
                return answer
            print(f"Please enter one of: {allowed}.")

    def _prompt_position(self, prompt:str, count:int) -> int:
        """Prompt for a 1-based position and return its zero-based index."""
        while True:
            answer = self.__input_fn(f"{prompt} (1-{count}): ").strip()
            try:
                position = int(answer)
            except ValueError:
                print("Enter a number.")
                continue
            if 1 <= position <= count:
                return position - 1
            print(f"Enter a number from 1 to {count}.")

    def _prompt_hand_position(self, player:Player, prompt:str) -> int:
        """Show concealed hand positions and prompt for one."""
        cards = player.get_cards()
        for position in range(len(cards)):
            print(f"{position + 1}. [face down]")
        return self._prompt_position(prompt, len(cards))

    def _prompt_target_player(self) -> int | None:
        """Prompt for an opponent who currently has cards, if one exists."""
        options = [
            (index, player)
            for index, player in enumerate(self.__players)
            if index != self.__current_player and player.get_cards()
        ]
        if not options:
            return None
        print("Choose an opponent:")
        for option, (_, player) in enumerate(options, start=1):
            print(f"{option}. {player.get_name()}")
        choice = self._prompt_position("Opponent", len(options))
        return options[choice][0]

    def _resolve_drawn_ability(self, card:Card) -> None:
        """Prompt for and resolve the ability of a directly discarded draw."""
        current_player = self.__players[self.__current_player]
        rank = card.rank

        if rank in ("7", "8"):
            own_position = self._prompt_hand_position(
                current_player, "Which of your cards do you want to reveal?"
            )
            revealed = self.resolve_card_ability(
                card, own_position=own_position
            )
            print(f"Your selected card is {revealed}.")
            return

        target_player_index = self._prompt_target_player()
        if target_player_index is None:
            print("There are no opponents with cards to target; the ability has no effect.")
            self.skip_card_ability(card)
            return

        target_player = self.__players[target_player_index]
        if rank in ("9", "10"):
            target_position = self._prompt_hand_position(
                target_player, "Which opponent card do you want to reveal?"
            )
            revealed = self.resolve_card_ability(
                card,
                target_player_index=target_player_index,
                target_position=target_position,
            )
            print(f"{target_player.get_name()}'s selected card is {revealed}.")
            return

        own_position = self._prompt_hand_position(
            current_player, "Which of your cards do you want to select?"
        )
        target_position = self._prompt_hand_position(
            target_player, "Which opponent card do you want to select?"
        )
        if rank in ("Jack", "Queen"):
            self.resolve_card_ability(
                card,
                own_position=own_position,
                target_player_index=target_player_index,
                target_position=target_position,
            )
            print("The selected cards have been exchanged.")
            return

        own_card = current_player.get_cards()[own_position]
        target_card = target_player.get_cards()[target_position]
        print(f"Your selected card is {own_card}.")
        print(f"{target_player.get_name()}'s selected card is {target_card}.")
        swap = self._prompt_choice("Swap the selected cards?", ("yes", "no")) == "yes"
        self.resolve_card_ability(
            card,
            own_position=own_position,
            target_player_index=target_player_index,
            target_position=target_position,
            swap=swap,
        )
        if swap:
            print("The selected cards have been exchanged.")

    def _take_stick_action(
        self, on_update:Callable[[], None] | None = None
    ) -> None:
        """Let the current player attempt to stick a card to the discard top."""
        if not self.__players[self.__current_player].get_cards():
            print("You have no cards to stick.")
            return
        top_discard = self.get_discard_top_card()
        if top_discard is None:
            print("There is no card to stick to.")
            return

        mode = self._prompt_choice("Stick from your hand or target an opponent?", ("own", "opponent"))
        if mode == "own":
            own_position = self._prompt_hand_position(
                self.__players[self.__current_player], "Which card do you want to stick?"
            )
            success = self.stick_card(own_position=own_position)
        else:
            target_player_index = self._prompt_target_player()
            if target_player_index is None:
                print("There are no opponents with cards to target.")
                return
            target_player = self.__players[target_player_index]
            target_position = self._prompt_hand_position(
                target_player, "Which opponent card do you want to target?"
            )
            own_position = None
            target_card = target_player.get_cards()[target_position]
            if target_card.rank == top_discard.rank:
                own_position = self._prompt_hand_position(
                    self.__players[self.__current_player],
                    "Which of your cards do you want to give?",
                )
            success = self.stick_card(
                own_position=own_position,
                target_player_index=target_player_index,
                target_position=target_position,
            )
        if success:
            print("Stick succeeded.")
        else:
            print("Stick failed; you drew a penalty card.")
        if on_update is not None:
            on_update()

    def turn_logic(
        self,
        turn:int,
        on_update:Callable[[], None] | None = None,
    ) -> int | str:
        """Run one text-driven turn for the player at ``turn``.

        The caller advances the turn with ``advance_turn`` after this method
        returns. Card abilities are resolved only for directly discarded draws.

        Args:
            turn: Zero-based index of the player taking the turn.
            on_update: Optional callback to refresh a display after game changes.

        Returns:
            The player index, or ``"cambio"`` if Cambio was called.

        Raises:
            ValueError: If ``turn`` is not the current player.
            Exception: If a turn is requested in an invalid game state.
        """
        if turn != self.__current_player:
            raise ValueError("The requested player is not the current player.")
        if self.__game_state == GameState.IN_PROGRESS:
            player = self.__players[turn]
            decision = self._prompt_choice(
                f"{player.get_name()}, would you like to call Cambio?",
                ("yes", "no"),
            )
            if decision == "yes":
                self.call_cambio()
                print(f"{player.get_name()} called Cambio. One final round begins.")
                if on_update is not None:
                    on_update()
                return "cambio"
        elif self.__game_state != GameState.CAMBIO_CALLED:
            raise Exception("Cannot take a turn in the current game state.")

        player = self.__players[turn]
        print(f"\n{player.get_name()}'s turn.")
        top_discard = self.get_discard_top_card()
        print(f"Top discard: {top_discard}")

        actions = ("draw", "stick") if player.get_cards() else ("draw",)
        action = self._prompt_choice("Choose an action", actions)
        if action == "stick":
            self._take_stick_action(on_update)
            return turn

        drawn_card = self.draw_card()
        if on_update is not None:
            on_update()
        print(f"You drew {drawn_card}.")
        if not player.get_cards():
            print("Your hand is empty, so this card will be added to it.")
            self.keep_drawn_card(drawn_card)
            if on_update is not None:
                on_update()
            return turn

        decision = self._prompt_choice(
            "Keep the draw by swapping it with a hand card, or discard it?",
            ("swap", "discard"),
        )
        if decision == "swap":
            own_position = self._prompt_hand_position(
                player, "Which card do you want to replace?"
            )
            self.keep_card(drawn_card)
            replaced_card = self.swap_card(own_position, drawn_card)
            self.discard_replaced_card(replaced_card)
            print(f"{replaced_card} was discarded.")
            if on_update is not None:
                on_update()
        else:
            self.discard_drawn_card(drawn_card)
            print(f"{drawn_card} was discarded.")
            if on_update is not None:
                on_update()
            if has_card_ability(drawn_card):
                self._resolve_drawn_ability(drawn_card)
                if on_update is not None:
                    on_update()
        return turn

    def show_bottom_cards(self, turn):
        """Return the last two cards in a player's hand.

        Args:
            turn: Zero-based index of the player.

        Returns:
            A tuple containing up to the last two cards in that hand.
        """
        return tuple(self.__players[turn].get_cards()[-2:])


# --- display.py ---

"""Pygame table display for the console-driven Cambio game."""

import threading

import pygame
import math


class PygameDisplay:
    """Render game state while leaving all decisions to console prompts."""

    WIDTH = 1100
    HEIGHT = 760
    PANEL_WIDTH = 320
    PANEL_HEIGHT = 180
    CARD_WIDTH = 56
    CARD_HEIGHT = 78
    CARD_SIZE = (CARD_WIDTH, CARD_HEIGHT)

    FELT = (32, 91, 67)
    PANEL = (23, 68, 51)
    PANEL_ACTIVE = (211, 176, 92)
    CREAM = (248, 242, 222)
    INK = (34, 39, 37)
    RED = (176, 48, 48)
    MUTED = (190, 211, 197)
    MASK_COLORS = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0), (255, 0, 255), (0, 255, 255)]

    SUITS={"Hearts": "♥", "Diamonds": "♦", "Clubs": "♣", "Spades": "♠"}
    COLORS={"Hearts": (164, 40, 40, 255), "Diamonds": (163, 143, 21, 255), "Clubs": (24, 134, 34, 255), "Spades": (37, 21, 101, 255), "Joker": (0, 0, 0, 255)}
    PATTERNS = {"2":"020","3":"030","4":"202","5":"212","6":"303","7":"313","8":"323","9":"414","10":"424"}

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Cambio")
        self.clock = pygame.time.Clock()
        self.title_font = pygame.font.SysFont("arial", 32, bold=True)
        self.font = pygame.font.SysFont("arial", 20, bold=True)
        self.large_font = pygame.font.SysFont("timesnewroman", 48)
        symbols_font_name = "opensymbol" if "opensymbol" in pygame.font.get_fonts() else "timesnewroman"
        self.symbols_font = pygame.font.SysFont(symbols_font_name, 20)
        self.small_symbols_font = pygame.font.SysFont(symbols_font_name, 8)
        self.large_symbols_font = pygame.font.SysFont(symbols_font_name, 40)
        self.small_font = pygame.font.SysFont("arial", 15)
        self.tiny_font = pygame.font.SysFont("arial", 12, bold=True)
        self.game = None
        self.running = True
        self.revealed_player = None
        self.masks = self.create_masks(self.screen.size)

    def create_masks(self, size):
        masks = {}
        line_thickness = 2
        line_density = [35, 20, 13, 10, 4, 2]
        for i,c in enumerate(self.MASK_COLORS):
            m = pygame.Surface(size)
            m.fill((0,0,0))
            m.set_colorkey((0,0,0))
            for j in range(2 * math.ceil(size[0] / line_density[i])):
                pygame.draw.line(m, (255, 255, 255), (size[0] - j * line_density[i], 0), (size[0], j * line_density[i]), width=line_thickness)
                pygame.draw.line(m, (255, 255, 255), (size[0] - j * line_density[i], size[1]), (size[0], size[1] - j * line_density[i]), width=line_thickness)
            masks[c] = pygame.mask.from_surface(m)
        return masks

    def apply_masks(self, surface, masks, offset, line_color=(0,0,0,160)):
        mask_surface = pygame.Surface(surface.size, flags=pygame.SRCALPHA)
        mask_surface.fill((127,127,127,0))
        for i,c in enumerate(self.MASK_COLORS):
            m = pygame.mask.from_threshold(surface, c, threshold=(1,1,1,1))
            c_area = pygame.mask.from_surface(surface)
            c_area.fill()
            m2 = masks[c]
            overlap = m.overlap_mask(m2, offset=offset)
            c_surface = pygame.Surface(surface.size, flags=pygame.SRCALPHA)
            c_surface.blit(m2.overlap_mask(m, offset=offset).to_surface(unsetcolor=(0,0,0,0), setcolor=line_color), (-offset[0], -offset[1]))
            mask_surface.blit(c_surface)
        return mask_surface

    def bind(self, game) -> None:
        """Attach the game whose state is shown in the window."""
        self.game = game
        self.refresh()

    def show_initial_cards(self, player_index: int) -> None:
        """Reveal only the current player's two starting cards."""
        self.revealed_player = player_index
        self.refresh()

    def hide_initial_cards(self) -> None:
        """Conceal the starting cards before the next player looks."""
        self.revealed_player = None
        self.refresh()

    def refresh(self) -> None:
        """Draw the current table state and process pending window events."""
        if not self.running:
            return
        self._process_events()
        if not self.running:
            return
        self._draw()
        pygame.display.flip()

    def console_input(self, prompt: str = "") -> str:
        """Read console input while keeping the pygame window responsive."""
        if not self.running:
            return input(prompt)

        result = []
        errors = []
        finished = threading.Event()

        def read_console():
            try:
                result.append(input(prompt))
            except BaseException as error:
                errors.append(error)
            finally:
                finished.set()

        reader = threading.Thread(target=read_console, daemon=True)
        reader.start()
        while not finished.is_set() and self.running:
            self._process_events()
            if self.running:
                self._draw()
                pygame.display.flip()
                self.clock.tick(30)
        reader.join()
        if errors:
            raise errors[0]
        return result[0]

    def close(self) -> None:
        """Close the display and release pygame resources."""
        if self.running:
            self.running = False
            pygame.quit()

    def _process_events(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.close()
                return

    def _draw(self) -> None:
        self.screen.fill(self.FELT)
        title = self.title_font.render("CAMBIO", True, self.CREAM)
        self.screen.blit(title, title.get_rect(center=(self.WIDTH // 2, 30)))

        if self.game is None:
            hint = self.font.render(
                "Enter player details in the console to begin",
                True,
                self.MUTED,
            )
            self.screen.blit(hint, hint.get_rect(center=(self.WIDTH // 2, 100)))
            return

        players = self.game.get_players()
        current_index = self.game.get_current_player_index()
        status = self.game.get_game_state().name.replace("_", " ").title()
        current_name = players[current_index].get_name() if players else "-"
        status_text = self.small_font.render(
            f"{status}  |  Current turn: {current_name}",
            True,
            self.MUTED,
        )
        self.screen.blit(
            status_text,
            status_text.get_rect(center=(self.WIDTH // 2, 64)),
        )

        positions = (
            (30, 94),
            (390, 94),
            (750, 94),
            (30, 546),
            (390, 546),
            (750, 546),
        )
        for index, player in enumerate(players):
            self._draw_player(index, player, positions[index], index == current_index)

        self._draw_piles()

    def _draw_player(self, index: int, player, position, active: bool) -> None:
        x, y = position
        panel = pygame.Rect(x, y, self.PANEL_WIDTH, self.PANEL_HEIGHT)
        pygame.draw.rect(self.screen, self.PANEL, panel, border_radius=14)
        border = self.PANEL_ACTIVE if active else (74, 120, 94)
        pygame.draw.rect(self.screen, border, panel, width=3, border_radius=14)

        name = self.font.render(player.get_name(), True, self.CREAM)
        self.screen.blit(name, (x + 14, y + 10))
        hand = player.get_cards()
        count = self.small_font.render(f"{len(hand)} cards", True, self.MUTED)
        self.screen.blit(count, (x + self.PANEL_WIDTH - count.get_width() - 14, y + 15))

        count_in_hand = max(1, len(hand))
        gap = 6
        card_width = min(
            self.CARD_WIDTH,
            (self.PANEL_WIDTH - 28 - gap * (count_in_hand - 1)) // count_in_hand,
        )
        card_height = max(38, int(card_width * self.CARD_HEIGHT / self.CARD_WIDTH))
        total_width = count_in_hand * card_width + (count_in_hand - 1) * gap
        card_x = x + (self.PANEL_WIDTH - total_width) // 2
        card_y = y + 68
        for card_index, card in enumerate(hand):
            visible = (
                index == self.revealed_player
                and card_index >= max(0, len(hand) - 2)
            )
            self._draw_card(
                card,
                (card_x + card_index * (card_width + gap), card_y),
                (card_width, card_height),
                face_up=visible,
            )

    def _draw_piles(self) -> None:
        center_y = self.HEIGHT // 2
        draw_x = 360
        discard_x = 684
        drawn_x = 522
        card_size = (76, 106)

        draw_count = self.game.get_draw_pile_count()
        for layer in range(min(3, (draw_count + 9) // 10)):
            self.draw_card_back((draw_x + layer * 4, center_y - 40 - layer * 4))
        deck_count = self.small_font.render(f"MAIN PILE  ({draw_count})", True, self.CREAM)
        self.screen.blit(deck_count, deck_count.get_rect(center=(draw_x + 38, center_y + 84)))

        discard = self.game.get_discard_cards()
        if discard:
            for layer in range(min(3, len(discard)) - 1):
                self.draw_card_back(
                    (discard_x + layer * 4, center_y - 40 - layer * 4))
            self._draw_card(discard[-1], (discard_x, center_y - 40), card_size)
        else:
            self.draw_card_back((discard_x, center_y - 40))
        discard_count = self.small_font.render(
            f"DISCARD PILE  ({len(discard)})",
            True,
            self.CREAM,
        )
        self.screen.blit(
            discard_count,
            discard_count.get_rect(center=(discard_x + 38, center_y + 84)),
        )

        drawn_card = self.game.get_drawn_card()
        self._draw_card(
            drawn_card,
            (drawn_x, center_y - 40),
            card_size,
            face_up=drawn_card is not None,
        )
        drawn_label = self.small_font.render("DRAWN CARD", True, self.CREAM)
        self.screen.blit(
            drawn_label,
            drawn_label.get_rect(center=(drawn_x + 38, center_y + 84)),
        )

    def _draw_card(self, card, position, size, face_up=True) -> None:
        if face_up:
            self.draw_card_front(card, position)
        else:
            self.draw_card_back(position)

        
    def draw_card_front(self, card, offset, using = None, rot=0):
        card_round = None
        card_base = None
        card_surface = None
        masks = self.masks
        card_round = pygame.Surface(self.CARD_SIZE, flags=pygame.SRCALPHA)
        card_base = pygame.Surface(self.CARD_SIZE, flags=pygame.SRCALPHA)
        card_surface = pygame.Surface(self.CARD_SIZE, flags=pygame.SRCALPHA)
        card_base.fill((246, 236, 205, 255))
        card_round.fill((0,0,0,0))
        pygame.draw.rect(card_round, (255,255,255,255), pygame.Rect(0,0,self.CARD_SIZE[0],self.CARD_SIZE[1]), border_radius=7)

        if card.suit == "Joker":
            text = self.small_font.render("Joker!", False, (0, 255, 255, 255))
            card_surface.blit(text, (self.CARD_SIZE[0] / 2 - text.size[0] / 2, self.CARD_SIZE[1] / 2 - text.size[1] / 2))
        else:
            suit = self.SUITS[card.suit]
            rank = card.rank
            if rank in self.PATTERNS: # Non-face card
                pattern = self.PATTERNS[rank]
                left_spacing = int(pattern[0])
                mid_spacing = int(pattern[1])
                for i in range(left_spacing):
                    up = i < (left_spacing + 1) // 2
                    text = self.font.render(suit, False, (255,0,255,255))
                    up_adjustment = 0
                    if not up:
                        up_adjustment = 3
                        text = pygame.transform.flip(text, False, True)
                    diamonds_adjustment = 0 if card.suit == "Diamonds" else 0
                    card_surface.blit(text, (17 - text.size[0] / 2, -4 + i * ((self.CARD_SIZE[1] - 40) / (left_spacing - 1)) + text.size[1] / 2 + diamonds_adjustment + up_adjustment))
                    card_surface.blit(text, (self.CARD_SIZE[0] - 16 - text.size[0] / 2, -4 + i * ((self.CARD_SIZE[1] - 40) / (left_spacing - 1)) + text.size[1] / 2 + diamonds_adjustment + up_adjustment))
                    #pygame.draw.line(card_base, (0, 0, 255), (0, i * ((CARD_SIZE[1] - 40) / (left_spacing - 1)) + text.size[1] / 2 + diamonds_adjustment), (CARD_SIZE[0], i * ((CARD_SIZE[1] - 40) / (left_spacing - 1)) + text.size[1] / 2 + diamonds_adjustment), 2)
                for i in range(mid_spacing):
                    up = i < (mid_spacing + 1) // 2
                    text = self.font.render(suit, False, (255,0,255,255))
                    up_adjustment = 0
                    if not up:
                        up_adjustment = 3
                        text = pygame.transform.flip(text, False, True)
                    diamonds_adjustment = 0 if card.suit == "Diamonds" else 0
                    rows = 0
                    start_row = 0
                    row_step = 1
                    match int(rank):
                        case 2:
                            rows = 3
                            row_step = 2
                        case 3:
                            rows = 3
                        case 5 | 9:
                            rows = 3
                            start_row = 1
                        case 7 | 8:
                            rows = 5
                            start_row = 1
                            row_step = 2
                        case 10:
                            rows = 7
                            start_row = 1
                            row_step = 4
                    c_row = start_row + i * row_step
                    card_surface.blit(text, (self.CARD_SIZE[0] / 2 - text.size[0] / 2, -4 + c_row * ((self.CARD_SIZE[1] - 40) / (rows - 1)) + text.size[1] / 2 + diamonds_adjustment + up_adjustment))

            else: # Face card
                if rank == "Ace":
                    text = self.large_symbols_font.render(suit, False, (255, 0, 255, 255))
                    card_surface.blit(text, (self.CARD_SIZE[0] / 2 - text.size[0] / 2, self.CARD_SIZE[1] / 2 - text.size[1] / 2 + 10))
                elif rank == "Joker":
                    pass
                else:
                    letter = rank[0]
                    text = self.large_font.render(letter, False, (255, 0, 255, 255))
                    card_surface.blit(text, (self.CARD_SIZE[0] / 2 - text.size[0] / 2, self.CARD_SIZE[1] / 2 - text.size[1] / 2))

            self.tiny_font.set_bold(True)
            card_surface.blit(self.tiny_font.render(rank[0] if len(rank) > 2 else rank, False, (0, 255, 255)), (2, 3))
            card_surface.blit(self.small_symbols_font.render(suit, False, (0, 255, 255)), (3, 17))
            t = self.tiny_font.render(rank[0] if len(rank) > 2 else rank, False, (0, 255, 255))
            card_surface.blit(pygame.transform.rotate(t, 180), (self.CARD_SIZE[0] - t.size[0]/2-4, self.CARD_SIZE[1] - 15))
            card_surface.blit(pygame.transform.rotate(self.small_symbols_font.render(suit, False, (0, 255, 255)), 180), (self.CARD_SIZE[0] - 8, self.CARD_SIZE[1] - 24))
        
        card_base = pygame.transform.rotate(card_base, rot)
        card_surface = pygame.transform.rotate(card_surface, rot)
        card_round = pygame.transform.rotate(card_round, rot)
        self.tiny_font.set_bold(False)
        s = self.apply_masks(card_surface, masks, offset, line_color = self.COLORS[card.suit])
        card_base.blit(s)
        card_round.blit(card_base, special_flags=pygame.BLEND_RGBA_MULT)
        self.screen.blit(card_round, offset)
        return card_round

    def draw_card_back(self, offset, rot=0):
        card_round = None
        card_base = None
        card_surface = None
        masks = self.masks
        card_round = pygame.Surface(self.CARD_SIZE, flags=pygame.SRCALPHA)
        card_base = pygame.Surface(self.CARD_SIZE, flags=pygame.SRCALPHA)
        card_surface = pygame.Surface(self.CARD_SIZE, flags=pygame.SRCALPHA)
        card_base.fill((50, 70, 123, 255))
        card_round.fill((0,0,0,0))
        pygame.draw.rect(card_round, (255,255,255,255), pygame.Rect(0,0,self.CARD_SIZE[0],self.CARD_SIZE[1]), border_radius=7)
        card_surface.fill((0, 255, 255, 255))
        pygame.draw.rect(card_surface, (0, 0, 255, 255), pygame.Rect(5, 5, self.CARD_SIZE[0]-10, self.CARD_SIZE[1]-10))
        card_base = pygame.transform.rotate(card_base, rot)
        card_surface = pygame.transform.rotate(card_surface, rot)
        card_round = pygame.transform.rotate(card_round, rot)
        s = self.apply_masks(card_surface, masks, offset)
        card_base.blit(s)
        card_round.blit(card_base, special_flags=pygame.BLEND_RGBA_MULT)
        self.screen.blit(card_round, offset)

    def _draw_card_back(self, position, size, empty=False) -> None:
        x, y = position
        width, height = size
        rect = pygame.Rect(x, y, width, height)
        if empty:
            pygame.draw.rect(self.screen, (30, 77, 58), rect, border_radius=7)
            pygame.draw.rect(self.screen, (114, 157, 132), rect, width=2, border_radius=7)
        else:
            self._draw_card(None, position, size, face_up=False)


# --- instructions.py ---

def display_rules():
    output = "Cambio is a fast paced memory game where the goal of each round is to have the least amount of points in your hand."
    output += "\n The basic rules to Cambio are as follows:\n"
    output += "1: Each player starts with 4 cards in a 2x2 grid and are shown the bottom two cards in that grid\n"
    output += "2: At the start of each player's turn, they will be able to call Cambio\n"
    output += "3: Calling Cambio means every player other than the player who called Cambio gets one more turn before the game ends\n"
    output += "4: If the player does not call Cambio then they will draw a card from the deck\n"
    output += "5: The drawn card can be swapped with a card from the player's hand, or it can be discarded\n"
    output += "6: Some cards have special abilities that can be activated when they are discarded directly after being drawn\n"
    output += "7: Cards with this ability include 7s, 8s, 9s, 10s, Jacks, Queens, and Kings of Spades or Clubs\n"
    output += "8: The special effects for 7s and 8s allow the player to look at one of their own cards\n"
    output += "9: The special effects for 9s and 10s allow the player to look at one of their opponent's face down cards\n"
    output += "10: The special effects for Queens and Jacks allow the player to switch a card with one of their opponent's cards\n"
    output += "11: The special effects for Kings of Spades or Clubs allow the player to look at one of their opponent's cards then decide if they want to swap one of the cards from their hand with that card\n "
    output += "12: When a card is discarded regardless of when it was discarded, all players can choose if they want to stick a card to the discarded card\n"
    output += "13: If the stuck card is the same rank as the top card in the discard pile, then the stuck card is discarded\n"
    output += "14: If the stuck card is not the same rank as the top card in the discard pile, then the player who attempted to stick a card gets a card added to their hand\n"
    output += "15: Only one player can successfully stick a card, multiple can if the stuck card is invalid\n"
    output += "16: Each card has an assigned point value. Number cards are their number, Jokers are 0, Queens, Jacks, and Kings of Spades and Clubs are 10, Kings of Hearts and Diamonds are -1\n"
    output += "17: When the game is over, the player with the least amount of points at the end of each round wins!\n"
    output += display_instructions()
    with open("Rules_and_Instructions.txt", "w") as out_file:
        out_file.write(output)
def display_instructions():
    output = "\nInstructions for playing Cambio will be displayed on the screen\n"
    output += "All inputs will prompt the user for a text based response\n"
    output += "Inputs should be typed exactly as they are prompted in the console"
    return output
display_rules()


# --- game.py ---

"""Command-line entry point for starting a Cambio game."""




def _run_game(display):
    """Run a console-driven Cambio game with a live Pygame display."""
    while True:
        answer = display.console_input("Number of players (2-6): ").strip()
        try:
            player_count = int(answer)
        except ValueError:
            print("Enter a number.")
            continue
        if 2 <= player_count <= 6:
            break
        print("A Cambio game needs between 2 and 6 players.")

    player_names = []
    while len(player_names) < player_count:
        name = display.console_input(
            f"Enter a name for player {len(player_names) + 1}: "
        ).strip()
        if not name:
            print("Names cannot be empty.")
        elif name in player_names:
            print("Each player needs a unique name.")
        else:
            player_names.append(name)

    game = Cambio(player_count, input_fn=display.console_input)
    game.initialize_players(player_names)

    while True:
        starting_name = display.console_input(
            f"Who starts? ({', '.join(player_names)}): "
        ).strip()
        try:
            game.set_starting_player(starting_name)
            break
        except ValueError:
            print("Enter one of the player names shown.")

    display.bind(game)
    game.deal_starting_hands()
    display.refresh()
    print("\nStarting hands have been dealt. Each player may look at their two bottom cards.")
    for player_index, name in enumerate(player_names):
        display.console_input(f"{name}, press Enter when you are ready to view your cards.")
        display.show_initial_cards(player_index)
        print(f"{name}, remember these cards: {game.show_bottom_cards(player_index)}")
        display.console_input("Press Enter to pass the screen to the next player.")
        display.hide_initial_cards()

    print(f"\nThe starting discard is {game.get_discard_top_card()}.")
    while game.get_game_state() != GameState.ENDED:
        current_player_index = game.get_current_player_index()
        game.turn_logic(current_player_index, display.refresh)
        if game.get_game_state() != GameState.ENDED:
            game.advance_turn()
            display.refresh()

    players = game.get_players()
    lowest_score = min(game.count_points(index) for index in range(len(players)))
    winners = [
        player.get_name()
        for index, player in enumerate(players)
        if game.count_points(index) == lowest_score
    ]
    print("\nFinal scores:")
    for index, player in enumerate(players):
        print(
            f"{player.get_name()}: {game.count_points(index)} points "
            f"({player.get_cards()})"
        )
    print(f"Winner{'s' if len(winners) != 1 else ''}: {', '.join(winners)}")


def main():
    """Start the console-driven game and its Pygame display."""
    display = PygameDisplay()
    try:
        _run_game(display)
    finally:
        display.close()


if __name__ == "__main__":
    display_rules()
    main()
