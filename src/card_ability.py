from cards import Card
from player import Player


def has_card_ability(card: Card) -> bool:
    return card.rank in ("7", "8", "9", "10", "Jack", "Queen") or (
        card.rank == "King" and card.suit in ("Clubs", "Spades")
    )

def get_player_card(player: Player, position: int) -> Card:
    cards = player.get_cards()
    if position < 0 or position >= len(cards):
        raise IndexError("Invalid card position.")
    return cards[position]


def replace_player_card(player: Player, position: int, card: Card) -> Card:
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
    """Apply a discarded card's ability using zero-based positions selected by the UI."""
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
    if target_player is None:
        raise ValueError("Select another player.")
    if target_player is current_player:
        raise ValueError("The target player must be someone else.")
