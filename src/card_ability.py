"""Helpers for inspecting and exchanging cards during special-card abilities."""

if __package__:
    from .cards import Card
    from .player import Player
else:
    from cards import Card
    from player import Player


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
