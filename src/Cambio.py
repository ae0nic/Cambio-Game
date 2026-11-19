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

"""Core Cambio game state, turn actions, and scoring."""

from symtable import Class
from cards import Card, Deck, DiscardPile
from card_ability import card_ability, has_card_ability
from player import Player
from enum import Enum

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

    def __init__(self, num_players:int):
        """Create and shuffle a deck for a game with ``num_players`` players.

        Args:
            num_players: Number of players expected in this game.
        """
        
        self.__STARTING_HAND_SIZE:int = 4
        self.__NUM_PLAYERS:int = num_players

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
            Exception: If players have not been initialized.
        """
        if(len(self.__players) != self.__NUM_PLAYERS):
            raise Exception("Players have not been initialized. Cannot deal starting hands.")
        for i in range(self.__NUM_PLAYERS):
            for j in range(self.__STARTING_HAND_SIZE):
                self.__players[i].add_card(self.__deck.deal())

    def advance_turn(self):
        """Advance the current-player index, wrapping at the end of the player list."""
        self.__current_player = (self.__current_player + 1) % self.__NUM_PLAYERS

    def call_cambio(self):
        """Mark that Cambio has been called and return the resulting game state.

        Raises:
            Exception: If Cambio has already been called.
        """
        if self.__game_state == GameState.CAMBIO_CALLED:
            raise Exception("Cambio has already been called.")
        self.__game_state = GameState.CAMBIO_CALLED
        return self.__game_state

    def draw_card(self):
        """Draw a card for the current player and enter the drawing state.

        Returns:
            The card drawn from the deck.

        Raises:
            Exception: If the game is not in progress or an earlier draw or
                ability is still unresolved.
            RuntimeError: If the deck is empty.
        """
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
        self.__game_state = GameState.IN_PROGRESS
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
        self.__game_state = GameState.IN_PROGRESS
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

        own_card = current_cards[own_position]
        target_card = target_cards[target_position]
        current_cards[own_position] = target_card
        target_cards[target_position] = own_card
        current_player.set_cards(current_cards)
        target_player.set_cards(target_cards)
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
                        
    def turn_logic(self, turn):
        """Run one console-driven turn for the player at ``turn``.

        Args:
            turn: Zero-based index of the player taking the turn.

        Returns:
            The same player index, or the string ``"cambio"`` if Cambio was
            called.

        Raises:
            ValueError: If the player enters an action other than ``swap`` or
                ``discard``.
        """
        decision = input(f"{self.__players[turn].get_name()}, would you like to call Cambio? (yes, no): ").lower()
        if decision == "yes":
            return "cambio"
        card = self.draw_card()
        decision = input(f"{self.__players[turn].get_name()}, do you want to swap the {card} with one of your cards or discard? (swap, discard): ").lower()
        if decision == "swap":
            position = int(input("Which card would you like to swap? (1,2,3...) "))
            card_to_keep = self.keep_card(card)
            replaced_card = self.swap_card(position - 1, card_to_keep)
            # Discarding the replaced hand card does not trigger an ability.
            self.__discard_pile.add_card(replaced_card)
        elif decision == "discard":
            self.discard_drawn_card(card)
        else:
            raise ValueError("Invalid choice. Enter 'swap' or 'discard'.")
        return turn

    def show_bottom_cards(self, turn):
        """Return the last two cards in a player's hand.

        Args:
            turn: Zero-based index of the player.

        Returns:
            A tuple containing up to the last two cards in that hand.
        """
        return tuple(self.__players[turn].get_cards()[-2:])