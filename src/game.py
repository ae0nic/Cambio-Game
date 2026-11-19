"""Command-line entry point for starting a Cambio game."""

if __package__:
    from .cambio import Cambio, GameState
else:
    from cambio import Cambio, GameState


def main():
    """Run a complete text-based Cambio game."""
    while True:
        answer = input("Number of players (2-6): ").strip()
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
        name = input(f"Enter a name for player {len(player_names) + 1}: ").strip()
        if not name:
            print("Names cannot be empty.")
        elif name in player_names:
            print("Each player needs a unique name.")
        else:
            player_names.append(name)

    game = Cambio(player_count)
    game.initialize_players(player_names)

    while True:
        starting_name = input(
            f"Who starts? ({', '.join(player_names)}): "
        ).strip()
        try:
            game.set_starting_player(starting_name)
            break
        except ValueError:
            print("Enter one of the player names shown.")

    game.deal_starting_hands()
    print("\nStarting hands have been dealt. Each player may look at their two bottom cards.")
    for player_index, name in enumerate(player_names):
        input(f"{name}, press Enter when you are ready to view your cards.")
        print(f"{name}, remember these cards: {game.show_bottom_cards(player_index)}")
        input("Press Enter to pass the screen to the next player.")

    print(f"\nThe starting discard is {game.get_discard_top_card()}.")
    while game.get_game_state() != GameState.ENDED:
        current_player_index = game.get_current_player_index()
        game.turn_logic(current_player_index)
        if game.get_game_state() != GameState.ENDED:
            game.advance_turn()

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

if __name__ == "__main__":
    main()